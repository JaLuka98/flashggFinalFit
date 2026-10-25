"""Health check of every combination fit run (obs x hgg/h4l/comb x asimov/dataFit).

Needs an inventory of the running processes of all nodes (lines "fit <host> <pid> <etimes> <rss> <stat> <cwd> <name>"
and "law <host> <pgid> <output_combination_obs/fit> <asimov-fits|unblinded-fits> <etimes>"), see the README.
Per run it reports: law process(es), first steps / best fits (valid, empty, fit status), scan points, merged scans,
locks without a running fit, empty result files without a running fit, crashes and failures in the law logs, and
whether scan windows (scan_ranges.json) are set.

usage: check_runs.py <inventory file> [obs ...]
"""
import collections
import glob
import json
import os
import re
import sys

import ROOT

ROOT.gErrorIgnoreLevel = ROOT.kError
here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(here, "combination"))
import summarize_scans as ss  # noqa: E402

inv = open(sys.argv[1]).read().splitlines()
obs_list = sys.argv[2:] or ["NJ", "PTJ0", "PTH", "rapidity", "MassJ0J1"]
running = collections.defaultdict(set)   # run dir -> names of running fits
laws = collections.defaultdict(list)     # (obs, fit, kind) -> hosts
for line in inv:
    t = line.split()
    if t and t[0] == "fit" and len(t) >= 8:
        running[t[6]].add(t[7])
    elif t and t[0] == "law" and len(t) >= 5:
        obs, fit = t[3].replace("output_combination_", "").split("/")
        laws[(obs, fit, "asimov" if t[4].startswith("asimov") else "dataFit")].append(t[1])


def fit_status(path, poi):
    f = ROOT.TFile.Open(path)
    r = f.Get("fit_mdf") if f else None
    if not r:
        return None
    v = r.floatParsFinal().find(poi)
    return r.status(), (v.getVal() if v else None), (v.getError() if v else None)


problems = []
for obs in obs_list:
    pois = list(ss.load_maps().patterns(obs)[1])
    for fit in ("h4l", "hgg", "comb"):
        for kind in ("asimov", "dataFit"):
            d = f"{here}/output_combination_{obs}/{fit}/Combine/runFits_{obs}/{kind}"
            if not os.path.isdir(f"{here}/output_combination_{obs}/{fit}/Combine"):
                continue
            files = set(os.listdir(d)) if os.path.isdir(d) else set()
            names_running = running.get(d, set())
            tag = "Asimov" if kind == "asimov" else "Data"
            issues = []
            # first steps / best fits
            if kind == "asimov":
                first = {p: f"higgsCombinefirstStep_{p}.MultiDimFit.mH125.07.root" for p in pois}
                mdf = {p: f"multidimfitfirstStep_{p}.root" for p in pois}
            else:
                first = {p: f"higgsCombineDataPostFitBestFit_{p}.MultiDimFit.mH125.07.root" for p in pois}
                mdf = {p: f"multidimfitDataPostFitBestFit_{p}.root" for p in pois}
            ok_first = empty_first = 0
            bad_status = []
            for p, fn in first.items():
                if fn not in files:
                    continue
                if os.path.getsize(f"{d}/{fn}") < 2000:
                    key = fn.replace("higgsCombine", "").replace(".MultiDimFit.mH125.07.root", "")
                    if key not in names_running:
                        empty_first += 1
                    continue
                ok_first += 1
                if mdf[p] in files:
                    st = fit_status(f"{d}/{mdf[p]}", p)
                    if st and (st[0] != 0 or not st[2]):
                        bad_status.append(f"{p.split('_', 2)[-1]}: status {st[0]}, r {st[1]:.3f} +- {st[2]:.3f}")
            # scan points, merged scans
            pts = [f for f in files if ".POINTS." in f and f.endswith(".root")]
            valid = sum(1 for f in pts if os.path.getsize(f"{d}/{f}") >= 2000)
            orphan_empty = [f for f in pts if os.path.getsize(f"{d}/{f}") < 2000
                            and f.replace("higgsCombine", "").replace(".MultiDimFit.mH125.07.root", "") not in names_running]
            merged = sum(1 for p in pois for k in ("Fit", "Stat")
                         if (f"higgsCombine{tag}PostFitScan{k}_{p}.root" if kind == "asimov"
                             else f"higgsCombine{tag}PostFitScan{k}_{p}.MultiDimFit.mH125.07.root") in files)
            locks = [f for f in files if f.endswith(".lock")]
            stale = [f for f in locks if f.replace(".lock", "").replace("higgsCombine", "").replace("multidimfit", "")
                     .replace(".MultiDimFit.mH125.07.root", "").replace(".root", "") not in names_running]
            # logs
            logs = glob.glob(f"{here}/output_combination_{obs}/logs/law_{'asimov' if kind == 'asimov' else 'unblind'}_{fit}*.log")
            seg = fails = 0
            errs = collections.Counter()
            for lg in logs:
                if "pass" in lg or "headtail" in lg:
                    continue
                txt = open(lg, errors="replace").read()
                seg += txt.count("died unexpectedly")
                fails += len(re.findall(r"failed    (Asimov|Unblinded)", txt))
                for m in re.findall(r"\n(\w+Error: [^\n]{0,70})", txt):
                    errs[re.sub(r"/\S+", "<path>", m)[:80]] += 1
            # windows
            jp = f"{here}/output_combination_{obs}/{fit}/Combine/scan_ranges.json"
            win = json.load(open(jp)).get("asimov" if kind == "asimov" else "unblinded", {}) if os.path.exists(jp) else {}
            n_win = sum(1 for p in pois if p in win)
            hosts = laws.get((obs, fit, kind), [])
            n = len(pois)
            done = merged == 2 * n
            if seg:
                issues.append(f"{seg} worker crashes")
            if stale:
                issues.append(f"{len(stale)} stale locks")
            if orphan_empty or empty_first:
                issues.append(f"{len(orphan_empty) + empty_first} empty results without a running fit")
            if bad_status:
                issues.append(f"{len(bad_status)} first steps with fit status != 0 / no error")
            if not hosts and not done:
                issues.append("no law process and not finished")
            if n_win < n and not done:
                issues.append(f"windows set for {n_win}/{n} POIs")
            line = (f"{obs:9s} {fit:4s} {kind:7s} law@{','.join(hosts) or '-':28s} first {ok_first:2d}/{n} "
                    f"points {valid:4d}/{n * 60} merged {merged:2d}/{2 * n} running {len(names_running):2d} "
                    f"fails {fails:4d}")
            print(line + ("   <- " + "; ".join(issues) if issues else ""))
            for e, c in errs.most_common(3):
                if "left to it" not in e:
                    print(f"{'':12s}{c:5d}x {e}")
            for b in bad_status[:3]:
                print(f"{'':12s}{b}")
            if issues:
                problems.append((obs, fit, kind, issues))
print(f"\n{len(problems)} runs with issues")
