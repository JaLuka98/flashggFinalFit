#!/usr/bin/env python3
"""Safety net for law runs shared by several processes (_shared_fit locks), every INTERVAL s until a given time:

  - lock keeper: touches the lock of every running fit of this checkout, so that a fit longer than the stale age of
    _shared_fit (3 h) is never taken for a dead one (law processes started before the lock heartbeat existed);
  - duplicates: when the same fit (folder + combine -n name) runs more than once, the copies whose open output file is
    no longer the file at that path (another copy recreated it, so their result is lost) are killed.

usage: dup_guard.py "<YYYY-mm-dd HH:MM>" host [host ...]   (run detached on a node with the farm agent)
"""
import collections
import os
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(REPO, "logs", "dup_guard.log")
INTERVAL = 600
# per fit: folder, name, pid, whether its open output file is the file at that path
PROBE = r'''for p in $(pgrep -u $USER -x combine); do c=$(readlink /proc/$p/cwd 2>/dev/null); case "$c" in *output_combination_*) ;; *) continue;; esac
n=$(tr "\0" " " < /proc/$p/cmdline | grep -oE "\-n [^ ]+" | cut -c4-); o=none
for fd in /proc/$p/fd/*; do t=$(readlink $fd); case "$t" in *higgsCombine*) a=$(stat -L -c %i $fd); b=$(stat -c %i "${t% (deleted)}" 2>/dev/null || echo x); [ "$a" = "$b" ] && o=owns || o=lost; break;; esac; done
echo "$c $n $p $o"; done'''


def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def ssh(host, cmd, timeout=120):
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", host, cmd],
                       capture_output=True, text=True, timeout=timeout)
    return r.stdout


def main():
    until, hosts = sys.argv[1], sys.argv[2:]
    os.environ["SSH_AUTH_SOCK"] = f"/tmp/farm-agent-{os.environ['USER']}/agent.sock"
    log(f"started for {hosts} until {until}")
    while time.strftime("%Y-%m-%d %H:%M") < until:
        fits = collections.defaultdict(list)
        for h in hosts:
            try:
                out = ssh(h, PROBE)
            except subprocess.TimeoutExpired:
                continue
            for line in out.splitlines():
                t = line.split()
                if len(t) == 4:
                    fits[(t[0], t[1])].append((h, t[2], t[3]))
        touched = 0
        for (folder, name) in fits:
            for lock in (f"{folder}/higgsCombine{name}.MultiDimFit.mH125.07.root.lock",
                         f"{folder}/multidimfit{name}.root.lock"):
                if os.path.isdir(lock):
                    os.utime(lock)
                    touched += 1
        killed = 0
        for (folder, name), copies in fits.items():
            if len(copies) < 2:
                continue
            for h, pid, state in copies:
                if state == "lost":
                    ssh(h, f"grep -qF -- '{name}' /proc/{pid}/cmdline && kill -9 {pid}")
                    log(f"duplicate {folder.split('output_combination_')[-1]} {name}: killed the copy on {h} "
                        f"(pid {pid}), whose output was recreated by another copy")
                    killed += 1
        log(f"{sum(len(c) for c in fits.values())} fits, {touched} locks refreshed, {killed} lost duplicates killed")
        time.sleep(INTERVAL)
    log("stopped")


if __name__ == "__main__":
    main()
