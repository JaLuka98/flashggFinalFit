"""Quality of every finished likelihood scan of the combination fits.

Per scan: failed points (2dNLL > 1000, combine could not fit; for H4l mostly where an expected yield turns
negative), whether the curve reaches 2dNLL = 4 on both sides, and how many points lie inside 2 sigma.

usage: survey_scans.py [obs ...]
"""
import os
import sys

import ROOT

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import summarize_scans as ss  # noqa: E402

ROOT.gErrorIgnoreLevel = ROOT.kError
here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for obs in sys.argv[1:] or ["NJ", "PTJ0", "PTH", "rapidity", "MassJ0J1"]:
    for fit in ("h4l", "hgg", "comb"):
        for kind, tag in (("asimov", "Asimov"), ("dataFit", "Data")):
            d = f"{here}/output_combination_{obs}/{fit}/Combine/runFits_{obs}/{kind}"
            if not os.path.isdir(d):
                continue
            n = good = 0
            bad = []
            for poi in ss.load_maps().patterns(obs)[1]:
                for k in ("Fit", "Stat"):
                    p = f"{d}/higgsCombine{tag}PostFitScan{k}_{poi}" + (".root" if kind == "asimov" else ".MultiDimFit.mH125.07.root")
                    if not os.path.exists(p):
                        continue
                    f = ROOT.TFile.Open(p)
                    t = f.Get("limit")
                    pts = sorted((getattr(e, poi), 2 * e.deltaNLL) for e in t
                                 if e.quantileExpected > -1.5 and abs(e.quantileExpected + 1) > 1e-6)
                    f.Close()
                    n += 1
                    failed = [x for x, y in pts if y > 1000]
                    ok_pts = [(x, y) for x, y in pts if y <= 1000]
                    if not ok_pts:
                        bad.append(f"{poi} {k}: no valid point"); continue
                    ymin = min(y for _, y in ok_pts)
                    i = min(range(len(ok_pts)), key=lambda j: ok_pts[j][1])
                    left = max(y for _, y in ok_pts[:i + 1]) - ymin
                    right = max(y for _, y in ok_pts[i:]) - ymin
                    inside = sum(1 for _, y in ok_pts if y - ymin < 4)
                    issues = []
                    if failed:
                        issues.append(f"{len(failed)} failed at r {min(failed):.2f}..{max(failed):.2f}")
                    if left < 4 or right < 4:
                        issues.append(f"ends 2dNLL {left:.1f} / {right:.1f}")
                    if inside < 15:
                        issues.append(f"{inside} points inside 2 sigma")
                    if issues:
                        bad.append(f"{poi} {k}: " + ", ".join(issues))
                    else:
                        good += 1
            if n:
                print(f"== {obs:9s} {fit:4s} {kind:7s}: {good}/{n} scans clean")
                for b in bad:
                    print("     ", b)
