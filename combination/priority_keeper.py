"""Keep this checkout's FinalFits condor jobs moving on every scheduler used by the law runs.

law submits to the schedd of the node it runs on (lxbatch01/03/05/...), so each node is queried over
ssh. Only jobs whose environment carries this checkout's ANALYSIS_PATH are touched (cluster numbers
are per schedd, and other productions share the schedds). Every 5 min, for idle jobs:
  JobPrio -> 10 (post-processing runs at 5);
  RequestMemory capped for the light signal-side tasks (measured 2026-10-21: <= 4 GB, configs request 16-50 GB).
The task of a cluster comes from the law job records in law/remote/<Task>/... .
Exits when no law run of the worktree is left on any node.
"""
import glob
import json
import subprocess
import time

import os

WT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this checkout
HOSTS = ["lxbatch01", "lxbatch02", "lxbatch03", "lxbatch04", "lxbatch05"]
MINE = f'regexp("{os.path.basename(WT)}", Environment)'  # only jobs of law runs from this checkout
CAP_MB = {"SignalFitCategoryProcess": (8192, 8192), "FTestCategory": (8192, 16384),
          "CalcPhotonSystCategory": (8192, 16384)}  # (2022/2023, 2024)
LAW_CHECK = ("for p in $(pgrep -u $USER -f 'law run FinalFits --years'); do "
             f"readlink /proc/$p/cwd 2>/dev/null | grep -q '^{WT}' && echo alive; done")


def log(msg):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), msg, flush=True)


def ssh(host, cmd, timeout=120):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host, cmd],
                          capture_output=True, text=True, timeout=timeout).stdout


def cluster_tasks():
    out = {}
    for f in glob.glob(f"{WT}/law/remote/*/*/*/htcondor_jobs_*.json"):
        task = f.split("/law/remote/")[1].split("/")[0]
        try:
            jobs = json.load(open(f))["jobs"].values()
        except (OSError, ValueError, KeyError):
            continue
        for j in jobs:
            c = str(j.get("job_id", "")).split(".")[0]
            if c.isdigit():
                out[c] = (task, "2024" in f)
    return out


while True:
    try:
        tasks = cluster_tasks()
        alive = False
        for host in HOSTS:
            try:
                if "alive" in ssh(host, LAW_CHECK, 60):
                    alive = True
                idle = ssh(host, f"condor_q -constraint 'JobStatus == 1 && {MINE}' -af ClusterId JobPrio RequestMemory")
            except subprocess.TimeoutExpired:
                alive = True
                continue
            prio, mem = set(), {}
            for line in idle.splitlines():
                p = line.split()
                if len(p) != 3:
                    continue
                if int(p[1]) < 10:
                    prio.add(p[0])
                task, is2024 = tasks.get(p[0], (None, False))
                if task in CAP_MB:
                    cap = CAP_MB[task][1 if is2024 else 0]
                    if int(p[2]) > cap:
                        mem[p[0]] = (task, cap)
            edits = [f"condor_qedit -constraint 'ClusterId == {c} && JobStatus == 1 && {MINE}' JobPrio 10"
                     for c in sorted(prio)]
            edits += [f"condor_qedit -constraint 'ClusterId == {c} && JobStatus == 1 && {MINE}' RequestMemory {cap}"
                      for c, (task, cap) in sorted(mem.items())]
            if edits:
                ssh(host, " ; ".join(edits) + " > /dev/null 2>&1", 300)
                log(f"{host}: priority 10 for {sorted(prio)}; memory caps {mem}")
        if not alive:
            log("no FinalFits law run of the worktree left on any node, exiting")
            break
    except Exception as exc:  # transient condor/NFS/ssh problems must not stop the keeper
        log(f"error: {exc!r}")
    time.sleep(300)
