#!/usr/bin/env python3
"""Best fit and 68% CL intervals from the law likelihood scans of the Hgg / H4l / Hgg+H4l fits.

Reads, per fit and POI, the scans written by law (CreateAsimovFit / CreateUnblindedFit):
  <base>/<fit>/Combine/<runFits>/asimov/higgsCombineAsimovPostFitScan{Fit,Stat}_<poi>.root
  <base>/<fit>/Combine/<runFits>/dataFit/higgsCombineDataPostFitScan{Fit,Stat}_<poi>.MultiDimFit.mH<mass>.root
(<runFits> = runFits_mu_fiducial for the inclusive fit, runFits_<obs> otherwise), and writes
<base>/results/<kind>_<obs>_results.{json,md}.

total: scan with all nuisances profiled; stat: scan with the constrained nuisances frozen;
syst = sqrt(total^2 - stat^2), separately up and down. Crossings of 2dNLL = 1 from a cubic spline
through the points, as plot1DScan.py: linear interpolation is biased on the coarse law grids
(spacing ~0.07 for sigma ~0.06 gives crossings ~10% too close to the minimum).

Example:
  python3 summarize_scans.py --base output_combination_NJ --obs NJ --kind asimov
"""
import argparse
import importlib.util
import json
import math
import os
from array import array

import ROOT

ROOT.gROOT.SetBatch(True)
HERE = os.path.dirname(os.path.abspath(__file__))


def load_maps():
    spec = importlib.util.spec_from_file_location("maps", os.path.join(HERE, "..", "Combine", "makeCombinationMaps.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_scan(path, poi):
    if not os.path.exists(path):
        return None
    f = ROOT.TFile.Open(path)
    t = f.Get("limit")
    if not t:
        return None
    pts = {}
    for e in t:
        if e.quantileExpected < -1.5:
            continue
        x = round(getattr(e, poi), 8)
        pts[x] = min(2 * e.deltaNLL, pts.get(x, float("inf")))
    return sorted(pts.items())


def interval(points):
    if not points or len(points) < 3:
        return None
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    spline = ROOT.TSpline3("scan", array("d", xs), array("d", ys), len(xs))
    i = ys.index(min(ys))
    lo_x, hi_x = xs[max(i - 1, 0)], xs[min(i + 1, len(xs) - 1)]
    best = min((lo_x + (hi_x - lo_x) * n / 2000 for n in range(2001)), key=spline.Eval)
    ymin = spline.Eval(best)

    def crossing(direction):
        rng = range(i, len(xs) - 1) if direction > 0 else range(i, 0, -1)
        for j in rng:
            a, b = xs[j], xs[j + direction]
            if (spline.Eval(a) - ymin - 1) * (spline.Eval(b) - ymin - 1) <= 0:
                if (direction > 0 and a < best) or (direction < 0 and a > best):
                    a = best
                for _ in range(60):
                    m = 0.5 * (a + b)
                    if (spline.Eval(a) - ymin - 1) * (spline.Eval(m) - ymin - 1) <= 0:
                        b = m
                    else:
                        a = m
                return 0.5 * (a + b)
        return None

    hi, lo = crossing(+1), crossing(-1)
    return {"bestfit": best, "up": (hi - best) if hi is not None else None,
            "down": (best - lo) if lo is not None else None, "n_points": len(xs),
            "scan_min": xs[0], "scan_max": xs[-1]}


def quad_sub(tot, stat):
    if tot is None or stat is None:
        return None
    return math.sqrt(max(tot * tot - stat * stat, 0.0))


def fmt(v):
    return "n/a" if v is None else "%.3f" % v


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", required=True, help="output folder of run_combination.sh (contains <fit>/Combine)")
    p.add_argument("--obs", required=True, help="inclusive, PTH, rapidity, NJ, PTJ0 or MassJ0J1")
    p.add_argument("--kind", choices=["asimov", "dataFit"], default="asimov")
    p.add_argument("--fits", default="hgg h4l comb")
    p.add_argument("--mass", default="125.07")
    opt = p.parse_args()

    maps = load_maps()
    pois = list(maps.patterns(opt.obs)[1])
    fits = opt.fits.split()
    run_dir = "runFits_mu_fiducial" if opt.obs == "inclusive" else f"runFits_{opt.obs}"
    results = {}
    for fit in fits:
        results[fit] = {}
        for poi in pois:
            entry = {}
            for kind, law_name in (("total", "Fit"), ("stat", "Stat")):
                if opt.kind == "asimov":
                    name = f"higgsCombineAsimovPostFitScan{law_name}_{poi}.root"
                else:
                    name = f"higgsCombineDataPostFitScan{law_name}_{poi}.MultiDimFit.mH{opt.mass}.root"
                entry[kind] = interval(read_scan(os.path.join(opt.base, fit, "Combine", run_dir, opt.kind, name), poi))
            t, s = entry["total"], entry["stat"]
            if t and s:
                entry["syst"] = {"up": quad_sub(t["up"], s["up"]), "down": quad_sub(t["down"], s["down"])}
            results[fit][poi] = entry

    out = os.path.join(opt.base, "results")
    os.makedirs(out, exist_ok=True)
    stem = os.path.join(out, f"{opt.kind}_{opt.obs}_results")
    with open(stem + ".json", "w") as f:
        json.dump(results, f, indent=1)

    title = "Expected (Asimov)" if opt.kind == "asimov" else "Observed"
    lines = [f"# {title} results, {opt.obs} (MH fixed at {opt.mass})\n",
             "total: all nuisances profiled; stat: constrained nuisances frozen; syst = sqrt(total^2 - stat^2). "
             "Crossings from a spline through the scan points. `n/a` = crossing outside the scan range.\n"]
    for fit in fits:
        lines.append(f"\n## {fit}\n\n| POI | best fit | total (+/-) | stat (+/-) | syst (+/-) |\n|---|---|---|---|---|")
        for poi in pois:
            e = results[fit][poi]
            t, s, y = e.get("total"), e.get("stat"), e.get("syst")
            if not t:
                lines.append(f"| {poi} | missing | | | |")
                continue
            lines.append("| %s | %s | +%s / -%s | +%s / -%s | +%s / -%s |" % (
                poi, fmt(t["bestfit"]), fmt(t["up"]), fmt(t["down"]),
                fmt(s["up"] if s else None), fmt(s["down"] if s else None),
                fmt(y["up"] if y else None), fmt(y["down"] if y else None)))
    lines.append("\n## Total uncertainty (symmetrised)\n\n| POI | " + " | ".join(fits) + " |\n|---|" + "---|" * len(fits))
    for poi in pois:
        row = []
        for fit in fits:
            t = results[fit][poi].get("total")
            ok = t and t["up"] is not None and t["down"] is not None
            row.append("%.3f" % (0.5 * (t["up"] + t["down"])) if ok else "n/a")
        lines.append(f"| {poi} | {' | '.join(row)} |")
    with open(stem + ".md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
