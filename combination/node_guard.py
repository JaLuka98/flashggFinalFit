#!/usr/bin/env python3
"""Memory guard for the local fits of this checkout, running on the node itself (no ssh, no ROOT).

The farm (local_farm.py) watches the nodes over ssh, which stops working exactly when a node runs out of
memory (2026-10-24: lxbatch03 at 0 GB for hours, ssh timing out). This guard runs on every login node used by
the farm and acts within seconds, on this user's processes of this checkout only:

  - MemAvailable < FLOOR_FRAC of RAM, or
  - the summed PSS of this checkout's processes > CAP_FRAC of RAM
  -> SIGKILL the youngest fit of the checkout (>= 0.5 GB: combine / fit scripts; never a law process, the
     farm or a guard), one per cycle, until both conditions are fine again. law marks that branch as
     failed and the farm redoes it in its next pass.

A paused (SIGSTOP) process is killed as well (SIGKILL needs no SIGCONT). One guard per node: a second one
exits. The guard exits after IDLE_EXIT s without any process of the checkout. Actions are logged to
logs/node_guard_<host>.log (only on action, plus an hourly heartbeat).

Usage (on the node): setsid nohup python3 combination/node_guard.py > /dev/null 2>&1 &
"""
import os
import signal
import socket
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOOR_FRAC = float(os.environ.get("GUARD_FLOOR_FRAC", 0.15))  # keep at least this fraction of RAM available
CAP_FRAC = float(os.environ.get("GUARD_CAP_FRAC", 0.35))      # this checkout may use at most this fraction
INTERVAL = 5
IDLE_EXIT = 3600
HOST = socket.gethostname().split(".")[0]
LOG = os.path.join(REPO, "logs", f"node_guard_{HOST}.log")
UID = os.getuid()
PROTECTED = ("law run", "local_farm.py", "node_guard.py", "priority_keeper.py")


def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def meminfo():
    vals = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, rest = line.split(":", 1)
            vals[key] = int(rest.split()[0])  # kB
    return vals["MemTotal"], vals["MemAvailable"]


def checkout_processes():
    """(pid, start ticks, rss kB, cmdline, killable) of this user's processes working in this checkout."""
    out = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) == os.getpid():
            continue
        try:
            if os.stat(f"/proc/{pid}").st_uid != UID:
                continue
            cwd = os.readlink(f"/proc/{pid}/cwd")
            if not cwd.startswith(REPO):
                continue
            cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode(errors="replace")
            stat = open(f"/proc/{pid}/stat").read()
            fields = stat[stat.rindex(")") + 2:].split()
            start = int(fields[19])
            # PSS, not RSS: law forks its workers, and RSS counts the shared pages of every fork in full
            rss = 0
            for line in open(f"/proc/{pid}/smaps_rollup"):
                if line.startswith("Pss:"):
                    rss = int(line.split()[1])
            killable = not any(p in cmd for p in PROTECTED) and not cmd.startswith(("-bash", "bash", "/bin/bash", "sh ", "ssh"))
            out.append((int(pid), start, rss, cmd, killable))
        except (OSError, ValueError, IndexError):
            continue
    return out


def other_guard_running():
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) == os.getpid():
            continue
        try:
            if os.stat(f"/proc/{pid}").st_uid != UID:
                continue
            cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode(errors="replace")
            if "node_guard.py" in cmd and "python" in cmd.split()[0] and os.readlink(f"/proc/{pid}/cwd").startswith(REPO):
                return True
        except OSError:
            continue
    return False


def main():
    if other_guard_running():
        sys.exit(0)
    os.chdir(REPO)
    total, _ = meminfo()
    floor, cap = FLOOR_FRAC * total, CAP_FRAC * total
    log(f"guard started: RAM {total / 1048576:.0f} GB, floor {floor / 1048576:.0f} GB available, "
        f"cap {cap / 1048576:.0f} GB for this checkout")
    last_seen = last_beat = time.time()
    while True:
        _, avail = meminfo()
        procs = checkout_processes()
        used = sum(p[2] for p in procs)
        if procs:
            last_seen = time.time()
        elif time.time() - last_seen > IDLE_EXIT:
            log("no process of the checkout for 1 h, exiting")
            return
        if avail < floor or used > cap:
            # the youngest real fit (>= 0.5 GB; killing small helpers frees nothing), else the largest killable
            killable = [p for p in procs if p[4]]
            victims = sorted((p for p in killable if p[2] >= 524288), key=lambda p: -p[1]) or \
                sorted(killable, key=lambda p: -p[2])
            if victims:
                pid, _, rss, cmd, _ = victims[0]
                try:
                    os.kill(pid, signal.SIGKILL)
                    log(f"MemAvailable {avail / 1048576:.1f} GB, checkout uses {used / 1048576:.1f} GB: killed {pid} "
                        f"({rss / 1048576:.1f} GB) {cmd[:150]}")
                except OSError:
                    pass
            else:
                log(f"MemAvailable {avail / 1048576:.1f} GB, checkout uses {used / 1048576:.1f} GB: nothing killable")
                time.sleep(60)
        if time.time() - last_beat > 3600:
            log(f"heartbeat: MemAvailable {avail / 1048576:.1f} GB, checkout uses {used / 1048576:.1f} GB "
                f"in {len(procs)} processes")
            last_beat = time.time()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
