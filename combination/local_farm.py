#!/usr/bin/env python3
"""Run the combination fits on the free cores of the lxbatch login nodes instead of HTCondor, and watch them.

Each run "obs:fit:kind" (kind asimov or dataFit) is one law FinalFitsYear process with local workflows
(run_combination.sh with EXECUTION=local: the fits run in WORKERS law workers, nice 10, idle I/O class),
started over ssh on the login node with the most free cores. Never on the condor worker nodes.

Every minute the farm checks every node and protects the other users and the file server:
  - load above the core count (someone else needs the cores): the youngest fits of the farm are stopped
    (SIGSTOP) and continued (SIGCONT) once the load is back below cores - 4;
  - MemAvailable below MEM_STOP GB: the youngest fit is stopped, below MEM_KILL GB it is killed (law
    redoes it in the next pass);
  - NFS: create + fsync + remove of a file in the output folder slower than NFS_SLOW s twice in a row: all
    fits of the farm are stopped until it is fast again; no new run starts meanwhile.
New runs start only on nodes with >= 3 free cores and > MEM_START GB available, with at most MAX_WORKERS
fits in total.

When a run's law process has ended, the ranges step of run_combination.sh is applied (per-POI windows,
cut scans moved aside). The run is restarted while scans were cut or law reported failed tasks, at most
MAX_PASSES times.

Usage (from the checkout, on any login node; log in logs/local_farm.log, state in logs/local_farm_state.json):
  python3 combination/local_farm.py PTH:h4l:asimov PTH:h4l:dataFit NJ:hgg:asimov ...
Running law processes of a listed run (e.g. after a restart of the farm) are adopted, not restarted.
"""
import glob
import json
import os
import re
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# run folders <REPO>/<OUT_PREFIX><obs>, the default OUT of run_combination.sh (AccBin cards since 2026-10-28)
OUT_PREFIX = os.environ.get("COMB_OUT_PREFIX", "output_combination_accbin_")
# FARM_NODES=lxbatch01,lxbatch03 restricts the farm to these nodes (e.g. one full of other jobs of this user,
# which node_guard.py does not count but answers by killing the fits of this checkout)
NODES = os.environ.get("FARM_NODES", "lxbatch01,lxbatch02,lxbatch03,lxbatch04,lxbatch05").split(",")
MAX_WORKERS = int(os.environ.get("FARM_MAX_WORKERS", 48))  # fits of the farm on all nodes together (file server)
NODE_WORKERS = int(os.environ.get("FARM_NODE_WORKERS", 8))  # per law process
HEADROOM = 4            # cores left free on every node
MEM_START, MEM_STOP, MEM_KILL = 20, 10, 5   # GB MemAvailable
GB_PER_WORKER = float(os.environ.get("FARM_GB_PER_WORKER", 3.5))  # fit + its law worker; the H4l PTH fits take ~2 GB
CAP_FRAC = 0.60  # memory budget of the checkout per node, the same as the cap of node_guard.py
NFS_SLOW, NFS_OK = 5.0, 2.0                 # s for create + fsync + remove
MAX_PASSES = 5
LOG = os.path.join(REPO, "logs", "local_farm.log")
STATE = os.path.join(REPO, "logs", "local_farm_state.json")
LOCK = os.path.join(REPO, "logs", "local_farm.lock")  # "<host> <pid>", touched every cycle
# optional time windows per node, read every cycle: {"lxbatch16": [["2026-10-26 17:00", "2026-10-26 20:00", 12], ...]}
# (start, end, max workers of the farm on the node); a node listed there gets no new runs outside its windows
NODE_CAPS = os.path.join(REPO, "logs", "farm_node_caps.json")


def node_cap(host):
    try:
        windows = json.load(open(NODE_CAPS)).get(host)
    except (OSError, ValueError):
        return None
    if windows is None:
        return None
    now = time.strftime("%Y-%m-%d %H:%M")
    return next((n for start, end, n in windows if start <= now < end), 0)

# per node: cores, load, MemAvailable, the law processes of the combination fits, the fits (combine) of the farm
PROBE = r"""
echo "cores $(nproc) load $(cut -d' ' -f1 /proc/loadavg) mem $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)"
cd @REPO@ && python3 -c "import sys; sys.path.insert(0, 'combination'); import node_guard as g; print('usage', sum(p[2] for p in g.checkout_processes()) // 1048576, g.meminfo()[0] // 1048576)"
# the memory guard of this node (it exits at once when one is running already)
cd @REPO@ && setsid -f python3 combination/node_guard.py < /dev/null > /dev/null 2>&1
for p in $(pgrep -u $USER -x python3; pgrep -u $USER -f '^/cvmfs/.*/python3 .*law run FinalFitsYear'); do
  a=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
  case "$a" in *"law run FinalFitsYear"*output_combination_*) echo "law $p $(ps -o pgid= -p $p | tr -d ' ') $a";; esac
done | sort -u
for p in $(pgrep -u $USER -x combine); do
  case "$(readlink /proc/$p/cwd 2>/dev/null)" in */output_combination_*)
    echo "fit $p $(awk '{print $3, $22}' /proc/$p/stat)";; esac
done
"""


PROBE = PROBE.replace("@REPO@", REPO)


def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def agent_ok(sock):
    try:
        return subprocess.run(["ssh-add", "-l"], env=dict(os.environ, SSH_AUTH_SOCK=sock), capture_output=True,
                              timeout=5).returncode == 0
    except subprocess.TimeoutExpired:
        return False


def find_agent():
    """A working ssh-agent: the key has a passphrase, and the agent forwarded by VS Code dies with each
    reconnect. Keep the current one while it works, else take the newest live VS Code socket."""
    sock = os.environ.get("SSH_AUTH_SOCK", "")
    if sock and agent_ok(sock):
        return
    uid = os.getuid()
    # a long-lived agent of the user on the farm node first (survives the VS Code disconnects), see README
    stable = glob.glob(f"/tmp/farm-agent-{os.environ.get('USER', uid)}/agent.sock")
    for cand in stable + sorted(glob.glob(f"/run/user/{uid}/vscode-ssh-auth-sock-*") + glob.glob(f"/run/user/{uid}/claude-agent.sock"),
                                key=lambda f: os.lstat(f).st_mtime, reverse=True):
        if agent_ok(cand):
            os.environ["SSH_AUTH_SOCK"] = cand
            log(f"ssh agent: {cand}")
            return
    log("no working ssh agent: nodes cannot be reached, their runs are left alone")


def sh(host, cmd, timeout=60):
    try:
        return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host, cmd],
                              capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return None


def probe(host):
    out = sh(host, PROBE)
    if out is None:
        return None
    node = {"law": [], "fits": []}
    for line in out.splitlines():
        p = line.split()
        if p and p[0] == "cores":
            node.update(cores=int(p[1]), load=float(p[3]), mem=int(p[5]))
        elif p and p[0] == "usage" and len(p) == 3:
            node.update(usage=int(p[1]), total=int(p[2]))
        elif p and p[0] == "law" and len(p) > 2 and p[2].isdigit():
            m = re.search(r"--output-dir (\S+)", line)
            kind = "asimov" if "--asimov-fits" in line else "dataFit"
            if m:
                node["law"].append((int(p[1]), m.group(1), kind))
                w = re.search(r"--workers (\d+)", line)
                if p[1] == p[2] and w:  # the law main process (its workers share the command line)
                    node["booked"] = node.get("booked", 0) + int(w.group(1))
        elif p and p[0] == "fit" and len(p) == 4:
            node["fits"].append({"pid": int(p[1]), "state": p[2], "start": int(p[3])})
    return node if "cores" in node else None


def nfs_latency():
    path = os.path.join(REPO, "logs", f".nfs_probe_{os.getpid()}")
    t0 = time.time()
    try:
        with open(path, "w") as f:
            f.write("x")
            f.flush()
            os.fsync(f.fileno())
        os.remove(path)
    except OSError:
        return 99.0
    return time.time() - t0


def run_dir(run):
    obs, fit, _ = run.split(":")
    return os.path.join(REPO, f"{OUT_PREFIX}{obs}", fit)


def law_log(run):
    obs, fit, kind = run.split(":")
    return os.path.join(REPO, f"{OUT_PREFIX}{obs}", "logs", f"law_{'asimov' if kind == 'asimov' else 'unblind'}_{fit}.log")


def launch(run, host, workers):
    obs, fit, kind = run.split(":")
    step = "law" if kind == "asimov" else "unblind"
    out = sh(host, f"cd {REPO} && EXECUTION=local WORKERS={workers} FITS={fit} combination/run_combination.sh {obs} {step}", 300)
    log(f"{run}: started on {host} with {workers} workers: {(out or '').strip().splitlines()[-1:]}")


def finish(run, st):
    """ranges step after the law process ended; True when the run has to be redone."""
    obs, fit, kind = run.split(":")
    if not os.path.exists(law_log(run)):
        log(f"{run}: no law log, the start failed; starting again")
        return True
    text = open(law_log(run)).read()
    # luigi prints the summary between two marker lines: take the last summary, not the (empty) text after it;
    # no summary at all = the law process was killed
    summaries = text.split("===== Luigi Execution Summary =====")
    last = summaries[-2] if len(summaries) >= 3 else ""
    failed = not last or re.search(r"^\* \d+ failed", last, re.M) is not None
    missing = missing_scans(run)
    out = subprocess.run(f"cd {REPO} && FITS={fit} KIND={kind} combination/run_combination.sh {obs} ranges",
                         shell=True, capture_output=True, text=True).stdout
    m = re.search(r"^(\d+) cut scan", out, re.M)
    ncut = int(m.group(1)) if m else -1
    for line in out.splitlines():
        if "CUT" in line:
            log(f"{run}:   {line.strip()}")
    log(f"{run}: pass {st['pass']} done, law {'with failed tasks / no summary' if failed else 'ok'}, "
        f"{missing} merged scan(s) missing, {ncut} cut scan(s)")
    if (ncut > 0 or failed or missing) and st["pass"] < MAX_PASSES:
        os.rename(law_log(run), law_log(run).replace(".log", f"_pass{st['pass']}.log"))
        st["pass"] += 1
        return True
    if missing:
        log(f"{run}: INCOMPLETE after {st['pass']} passes ({missing} merged scans missing), needs a look")
    st["done"] = True
    return False


def missing_scans(run):
    """merged Fit + Stat scans of every POI that do not exist yet: a run is finished only with all of them"""
    import importlib.util
    obs, fit, kind = run.split(":")
    spec = importlib.util.spec_from_file_location("maps", os.path.join(REPO, "Combine", "makeCombinationMaps.py"))
    maps = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(maps)
    runfits = "runFits_mu_fiducial" if obs == "inclusive" else f"runFits_{obs}"  # the inclusive fits (variable '')
    d = os.path.join(REPO, f"{OUT_PREFIX}{obs}", fit, "Combine", runfits, kind)
    n = 0
    for poi in maps.patterns(obs)[1]:
        for k in ("Fit", "Stat"):
            name = (f"higgsCombineAsimovPostFitScan{k}_{poi}.root" if kind == "asimov"
                    else f"higgsCombineDataPostFitScan{k}_{poi}.MultiDimFit.mH125.07.root")
            n += not os.path.exists(os.path.join(d, name))
    return n


def signal(host, pids, sig):
    if pids:
        sh(host, f"kill -{sig} {' '.join(map(str, pids))}")


def take_lock():
    """One farm at a time: a second one would not see the runs of the first as its own and start them again."""
    if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 300:
        sys.exit(f"another farm is running ({open(LOCK).read().strip()}, {LOCK} touched "
                 f"{time.time() - os.path.getmtime(LOCK):.0f} s ago); stop it first")
    with open(LOCK, "w") as f:
        f.write(f"{os.uname().nodename} {os.getpid()}\n")


def main():
    runs = sys.argv[1:]
    take_lock()
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    for r in runs:
        state.setdefault(r, {"pass": 1, "done": False, "host": None, "workers": 0})
    nfs_slow = 0
    paused_nfs = False
    log(f"farm started for {runs}")
    while not all(state[r]["done"] for r in runs):
        find_agent()
        nodes = {h: probe(h) for h in NODES}
        lat = nfs_latency()
        nfs_slow = nfs_slow + 1 if lat > NFS_SLOW else 0
        if nfs_slow >= 2 and not paused_nfs:
            paused_nfs = True
            log(f"NFS slow ({lat:.1f} s): stopping all farm fits")
            for h, n in nodes.items():
                if n:
                    signal(h, [f["pid"] for f in n["fits"] if f["state"] != "T"], "STOP")
        elif paused_nfs and lat < NFS_OK:
            paused_nfs = False
            log(f"NFS ok again ({lat:.1f} s): continuing")
            for h, n in nodes.items():
                if n:
                    signal(h, [f["pid"] for f in n["fits"] if f["state"] == "T"], "CONT")

        # which runs have a law process, where
        alive = {}
        for h, n in nodes.items():
            for pid, outdir, kind in (n or {}).get("law", []):
                for r in runs:
                    if os.path.normpath(run_dir(r)) == os.path.normpath(outdir) and r.split(":")[2] == kind:
                        alive[r] = h
        n_fits = sum(state[r]["workers"] for r in runs if state[r]["host"] and not state[r]["done"])

        # protect the nodes
        for h, n in nodes.items():
            if not n or paused_nfs:
                continue
            running = sorted((f for f in n["fits"] if f["state"] != "T"), key=lambda f: -f["start"])
            stopped = sorted((f for f in n["fits"] if f["state"] == "T"), key=lambda f: f["start"])
            if n["mem"] < MEM_KILL and running:
                log(f"{h}: MemAvailable {n['mem']} GB, killing fit {running[0]['pid']}")
                signal(h, [running[0]["pid"]], "TERM")
            elif n["mem"] < MEM_STOP and running:
                log(f"{h}: MemAvailable {n['mem']} GB, stopping fit {running[0]['pid']}")
                signal(h, [running[0]["pid"]], "STOP")
            elif n["load"] > n["cores"] and running:
                k = min(len(running), int(n["load"] - n["cores"]) + 1)
                log(f"{h}: load {n['load']} on {n['cores']} cores, stopping {k} fit(s)")
                signal(h, [f["pid"] for f in running[:k]], "STOP")
            elif stopped and n["load"] < n["cores"] - HEADROOM and n["mem"] > MEM_STOP + 4:
                k = min(len(stopped), int(n["cores"] - HEADROOM - n["load"]))
                if k > 0:
                    log(f"{h}: load {n['load']}, MemAvailable {n['mem']} GB, continuing {k} fit(s)")
                    signal(h, [f["pid"] for f in stopped[:k]], "CONT")

        # ended runs, new runs
        for r in runs:
            st = state[r]
            if st["done"]:
                continue
            if st["host"] and nodes.get(st["host"]) is None:
                continue  # its node did not answer: unknown, never "ended"
            if r in alive:
                st["host"] = alive[r]
                st["workers"] = st.get("workers") or NODE_WORKERS  # adopted run: assume the maximum
                continue
            if st["host"] is not None:  # it was running and its law process has ended
                st["host"], st["workers"] = None, 0
                if not finish(r, st):
                    log(f"{r}: finished after {st['pass']} pass(es)")
                    continue
            if paused_nfs or n_fits >= MAX_WORKERS:
                continue
            # workers that fit the free cores and the memory budget of the checkout on the node (node_guard.py
            # kills fits above CAP_FRAC of the RAM, so a run must never be sized beyond it)
            slots = {}
            for h, n in nodes.items():
                if not n or "total" not in n or n["mem"] <= MEM_START:
                    continue
                # fits just started are still small: count every run of the farm on this node at its full size
                # every law run on the node at its declared workers (also the ones started by hand), and the farm's
                # runs started in this cycle (not visible to the probe yet)
                booked = max(n.get("booked", 0),
                             sum(state[q]["workers"] for q in runs if state[q]["host"] == h and not state[q]["done"]))
                budget = CAP_FRAC * n["total"] - max(n["usage"], booked * GB_PER_WORKER) - 2
                slots[h] = int(min(n["cores"] - n["load"] - HEADROOM, budget / GB_PER_WORKER))
                cap = node_cap(h)
                if cap is not None:
                    slots[h] = min(slots[h], cap - booked)
            slots = {h: k for h, k in slots.items() if k >= 2}
            if not slots:
                continue
            h = max(slots, key=slots.get)
            n = nodes[h]
            workers = int(max(2, min(slots[h], NODE_WORKERS, MAX_WORKERS - n_fits)))
            launch(r, h, workers)
            st["host"], st["workers"] = h, workers
            n["load"] += workers  # until the next probe sees the fits
            n["usage"] += int(workers * GB_PER_WORKER)
            n["booked"] = n.get("booked", 0) + workers
            n_fits += workers
        json.dump(state, open(STATE, "w"), indent=1)
        down = [h for h, n in nodes.items() if n is None]
        if down:
            log(f"no answer from {down}: their runs are left alone this cycle")
        os.utime(LOCK)
        time.sleep(60)
    log("all runs done")
    os.remove(LOCK)


if __name__ == "__main__":
    main()
