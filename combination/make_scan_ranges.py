#!/usr/bin/env python3
"""Per-POI scan windows (best fit +- N sigma, as in HIG-26-007) from a first pass of the law scans.

For every fit folder <base>/<fit>, reads the total scans of the first pass (same files as summarize_scans.py)
and writes <base>/<fit>/Combine/scan_ranges.json, {"asimov"|"unblinded": {POI: [lo, hi]}, ...}, read by
Combine/law_combine.py (scan_window_ranges): the scanned POI is scanned in its window and the other POIs float
in theirs. Without the json all POIs keep the [0, 3] range of the combination model ([0, 2] for PTH), which
cuts the scans of the weakly constrained bins (and the observed ones near 0).

sigma up / down from the spline crossings of 2dNLL = 1 (summarize_scans.interval); a crossing outside the
first-pass range is taken from a parabola through the points with 2dNLL < 9. Windows are rounded outwards
to 0.05.

A scan is "cut" when it does not reach 2dNLL = 4 at both ends. With --supersede, the outputs of the cut POIs
(scan points, merged scans, scan plots and, for observed fits, the best-fit snapshots) are moved to
<run dir>/superseded_<date>/, so that the next law run redoes exactly these POIs in their new windows.
Repeat (ranges, law) until no scan is cut.

Example:
  python3 make_scan_ranges.py --base output_combination_NJ --obs NJ --fits h4l --kind asimov --supersede
"""
import argparse
import datetime
import glob
import json
import math
import os
import shutil

import summarize_scans as ss

LEVEL_CUT = 4.0


def parabola_sigma(points):
    """sigma of y = (x - x0)^2 / sigma^2 + c fitted to the points with y - min < 9."""
    ymin = min(y for _, y in points)
    sel = [(x, y - ymin) for x, y in points if y - ymin < 9]
    if len(sel) < 3:
        return None
    n = len(sel)
    sx = [sum(x ** k for x, _ in sel) for k in range(5)]
    sxy = [sum(y * x ** k for x, y in sel) for k in range(3)]
    # least squares y = a x^2 + b x + c
    m = [[sx[4], sx[3], sx[2]], [sx[3], sx[2], sx[1]], [sx[2], sx[1], n]]
    det = lambda a: (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                     + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    d = det(m)
    if d == 0:
        return None
    a = det([[sxy[2], sx[3], sx[2]], [sxy[1], sx[2], sx[1]], [sxy[0], sx[1], n]]) / d
    return 1 / math.sqrt(a) if a > 0 else None


def window(points, nsigma):
    iv = ss.interval(points)
    if iv is None:
        return None, None
    up, down = iv["up"], iv["down"]
    if up is None or down is None:
        sigma = parabola_sigma(points)
        if sigma is None:
            sigma = up or down
        if sigma is None:
            return None, iv
        up, down = up or sigma, down or sigma
    lo = math.floor((iv["bestfit"] - nsigma * down) * 20) / 20
    hi = math.ceil((iv["bestfit"] + nsigma * up) * 20) / 20
    return [round(lo, 2), round(hi, 2)], iv


def is_cut(points):
    ymin = min(y for _, y in points)
    return points[0][1] - ymin < LEVEL_CUT or points[-1][1] - ymin < LEVEL_CUT


def supersede(run_dir, kind_dir, poi, stamp, best_fits=True):
    dest = os.path.join(run_dir, f"superseded_{stamp}", kind_dir)
    patterns = [f"higgsCombine*PostFitScan*_{poi}.*", f"scans/scan_{poi}.*", f"scans/scan_{poi}_observed.*"]
    if kind_dir == "dataFit" and best_fits:
        patterns += [f"higgsCombineDataPostFitBestFit*_{poi}.*", f"multidimfitDataPostFitBestFit*_{poi}.root"]
    moved = 0
    for pattern in patterns:
        for f in glob.glob(os.path.join(run_dir, kind_dir, pattern)):
            target = os.path.join(dest, os.path.relpath(f, os.path.join(run_dir, kind_dir)))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.move(f, target)
            moved += 1
    return moved


def fit_sigmas(run_dir, kind_dir, poi, mass):
    """(best fit, sigma down, sigma up) of poi from the fits made before the scans, or None.

    observed: the --algo singles best fit (68% interval), with the fit_mdf error where an edge sits at the
    range boundary; Asimov: the first-step fit (best fit 1, fit_mdf error)."""
    import ROOT
    if kind_dir == "dataFit":
        mdf_path = os.path.join(run_dir, kind_dir, f"multidimfitDataPostFitBestFit_{poi}.root")
        singles = os.path.join(run_dir, kind_dir, f"higgsCombineDataPostFitBestFit_{poi}.MultiDimFit.mH{mass}.root")
    else:
        mdf_path = os.path.join(run_dir, kind_dir, f"multidimfitfirstStep_{poi}.root")
        singles = None
    if not os.path.exists(mdf_path):
        return None
    f = ROOT.TFile.Open(mdf_path)
    res = f.Get("fit_mdf") if f else None
    var = res.floatParsFinal().find(poi) if res else None
    if not var:
        return None
    best, err, vmin, vmax = var.getVal(), var.getError(), var.getMin(), var.getMax()
    at_edge = min(best - vmin, vmax - best) < 1e-3  # clipped by the model range: the fit is redone in the window
    down = up = err
    if singles and os.path.exists(singles):
        g = ROOT.TFile.Open(singles)
        rows = {round(e.quantileExpected, 2): getattr(e, poi) for e in g.Get("limit")} if g.Get("limit") else {}
        if -1.0 in rows and -0.32 in rows and 0.32 in rows:
            best = rows[-1.0]
            if rows[-0.32] > vmin + 1e-4:
                down = best - rows[-0.32]
            if rows[0.32] < vmax - 1e-4:
                up = rows[0.32] - best
    return best, down, up, at_edge


def windows_from_fits(opt, pois, run_name, key):
    """--from-fits: windows before the first scan pass (all observed POIs; the Asimov POIs whose [lo, hi] scan of
    the model range would not reach 2 sigma on both sides). Their scan points of an earlier pass are moved aside."""
    stamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
    for fit in opt.fits.split():
        run_dir = os.path.join(opt.base, fit, "Combine", run_name)
        json_path = os.path.join(opt.base, fit, "Combine", "scan_ranges.json")
        ranges = json.load(open(json_path)) if os.path.exists(json_path) else {}
        windows = ranges.get(key, {})
        print(f"== {fit} ({key}, from the fits)")
        for poi in pois:
            r = fit_sigmas(run_dir, opt.kind, poi, opt.mass)
            if r is None:
                print(f"  {poi:28s} no fit result, window unchanged {windows.get(poi)}")
                continue
            best, down, up, at_edge = r
            lo = round(math.floor((best - opt.nsigma * down) * 20) / 20, 2)
            hi = round(math.ceil((best + opt.nsigma * up) * 20) / 20, 2)
            model = ss.load_maps().OBS[opt.obs][4]
            if opt.kind == "asimov" and best - 2 * down >= model[0] and best + 2 * up <= model[1]:
                new, note = list(model), "model range reaches 2 sigma, kept"
            else:
                new, note = [lo, hi], ""
                redo_fit = at_edge and opt.kind == "dataFit"
                note = "best fit at the model range edge, redone in the window; " if redo_fit else ""
                if opt.supersede and not opt.dry_run:
                    note += f"{supersede(run_dir, opt.kind, poi, stamp, best_fits=redo_fit)} files moved aside"
            windows[poi] = new
            print(f"  {poi:28s} best fit {best:7.3f} -{down:.3f} +{up:.3f} -> window {new}  {note}")
        ranges[key] = windows
        ranges["nsigma"] = opt.nsigma
        ranges["source"] = "combination/make_scan_ranges.py --from-fits"
        if not opt.dry_run:
            with open(json_path, "w") as f:
                json.dump(ranges, f, indent=1)
            print(f"  wrote {json_path}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", required=True, help="output folder of run_combination.sh (contains <fit>/Combine)")
    p.add_argument("--obs", required=True)
    p.add_argument("--fits", default="hgg h4l comb")
    p.add_argument("--kind", choices=["asimov", "dataFit"], default="asimov")
    p.add_argument("--nsigma", type=float, default=3.0)
    p.add_argument("--mass", default="125.07")
    p.add_argument("--supersede", action="store_true", help="move the outputs of the cut scans aside")
    p.add_argument("--dry-run", action="store_true", help="only print (do not write the json while law still runs)")
    p.add_argument("--from-fits", action="store_true", help="windows from the best fits made before the scans "
                   "(singles / first step), to scan in the right range from the first pass")
    opt = p.parse_args()

    pois = list(ss.load_maps().patterns(opt.obs)[1])
    if opt.from_fits:
        windows_from_fits(opt, pois, "runFits_mu_fiducial" if opt.obs == "inclusive" else f"runFits_{opt.obs}",
                          "asimov" if opt.kind == "asimov" else "unblinded")
        return
    run_name = "runFits_mu_fiducial" if opt.obs == "inclusive" else f"runFits_{opt.obs}"
    key = "asimov" if opt.kind == "asimov" else "unblinded"
    stamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
    n_cut = 0
    for fit in opt.fits.split():
        run_dir = os.path.join(opt.base, fit, "Combine", run_name)
        json_path = os.path.join(opt.base, fit, "Combine", "scan_ranges.json")
        ranges = {}
        if os.path.exists(json_path):
            with open(json_path) as f:
                ranges = json.load(f)
        windows = ranges.get(key, {})
        print(f"== {fit} ({key})")
        for poi in pois:
            if opt.kind == "asimov":
                name = f"higgsCombineAsimovPostFitScanFit_{poi}.root"
            else:
                name = f"higgsCombineDataPostFitScanFit_{poi}.MultiDimFit.mH{opt.mass}.root"
            points = ss.read_scan(os.path.join(run_dir, opt.kind, name), poi)
            if not points:
                print(f"  {poi:28s} no scan, window unchanged {windows.get(poi)}")
                continue
            new, iv = window(points, opt.nsigma)
            cut = is_cut(points)
            if new is None:
                print(f"  {poi:28s} no minimum found in the scan, window unchanged {windows.get(poi)}")
                continue
            note = ""
            if cut:
                # a cut scan is redone in its new window, which must contain the first-pass range it was cut at
                old = [points[0][0], points[-1][0]]
                new = [min(new[0], old[0]) if points[0][1] - min(y for _, y in points) < LEVEL_CUT else new[0],
                       max(new[1], old[1]) if points[-1][1] - min(y for _, y in points) < LEVEL_CUT else new[1]]
                n_cut += 1
                note = "CUT"
                if opt.supersede and not opt.dry_run:
                    note += f", {supersede(run_dir, opt.kind, poi, stamp)} files moved aside"
            elif poi in windows:
                new = windows[poi]  # keep the window the scan was made in
            windows[poi] = new
            print(f"  {poi:28s} best fit {iv['bestfit']:7.3f}  +{ss.fmt(iv['up'])} -{ss.fmt(iv['down'])}  "
                  f"scanned [{points[0][0]:.3g}, {points[-1][0]:.3g}] -> window {new}  {note}")
        ranges[key] = windows
        ranges["nsigma"] = opt.nsigma
        ranges["source"] = "combination/make_scan_ranges.py from the first-pass total scans"
        if opt.dry_run:
            continue
        with open(json_path, "w") as f:
            json.dump(ranges, f, indent=1)
        print(f"  wrote {json_path}")
    print(f"{n_cut} cut scan(s)" + ("" if opt.supersede or not n_cut else "; rerun with --supersede to redo them"))


if __name__ == "__main__":
    main()
