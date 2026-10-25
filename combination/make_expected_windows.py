#!/usr/bin/env python3
"""Scan windows of the Hgg-only and Hgg+H4l fits before their first scan, from the expected uncertainties.

sigma_Hgg: the HIG-26-007 Hgg Asimov scans of the same observable (same binning required), x HGG_INFLATE for the
acceptance and BR uncertainties of the total cross section; sigma_H4l: our H4l Asimov scans;
sigma_comb = (1/sigma_Hgg^2 + 1/sigma_H4l^2)^-1/2 (per side). Windows:
  Asimov:   1 +- NSIG_ASIMOV sigma
  observed: centre +- NSIG_DATA sigma, centre = HIG-26-007 Hgg observed best fit (hgg) or the weighted mean of it
            and our H4l observed best fit (comb)
Written into <base>/<fit>/Combine/scan_ranges.json (keys asimov / unblinded) for the POIs without a window. The
scans read the windows when each point starts; the ranges step of the farm still redoes cut or coarse scans.

usage: make_expected_windows.py <obs> [--hig26007 <output prefix>] [--dry-run]
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import summarize_scans as ss  # noqa: E402

HGG_INFLATE, NSIG_ASIMOV, NSIG_DATA = 1.15, 3.0, 3.5


def interval(path, poi):
    if not os.path.exists(path):
        return None
    iv = ss.interval(ss.read_scan(path, poi))
    if not iv or iv["up"] is None or iv["down"] is None:
        return None
    return iv["bestfit"], iv["down"], iv["up"]


def comb_sigma(a, b):
    return (a ** -2 + b ** -2) ** -0.5


def rnd(lo, hi):
    return [round(math.floor(lo * 20) / 20, 2), round(math.ceil(hi * 20) / 20, 2)]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("obs")
    p.add_argument("--hig26007", default="/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/flashggFinalFit/output_2022_2023_2024")
    p.add_argument("--dry-run", action="store_true")
    opt = p.parse_args()
    repo = os.path.dirname(HERE)
    obs = opt.obs
    run = f"runFits_{obs}"
    pois = list(ss.load_maps().patterns(obs)[1])
    ref = f"{opt.hig26007}_{obs}/Combine/{run}"
    h4l = f"{repo}/output_combination_{obs}/h4l/Combine/{run}"
    for fit in ("hgg", "comb"):
        jp = f"{repo}/output_combination_{obs}/{fit}/Combine/scan_ranges.json"
        if not os.path.isdir(os.path.dirname(jp)):
            continue
        ranges = json.load(open(jp)) if os.path.exists(jp) else {}
        for key in ("asimov", "unblinded"):
            w = ranges.setdefault(key, {})
            for poi in pois:
                if poi in w:
                    continue
                g = interval(f"{ref}/asimov/higgsCombineAsimovPostFitScanFit_{poi}.root", poi)
                if g is None:
                    print(f"  {fit} {key} {poi}: no HIG-26-007 Hgg scan, left to the ranges step")
                    continue
                gd, gu = g[1] * HGG_INFLATE, g[2] * HGG_INFLATE
                z = interval(f"{h4l}/asimov/higgsCombineAsimovPostFitScanFit_{poi}.root", poi)
                # comb without an H4l scan yet: the Hgg sigma (conservative, the window is a bit wider than needed)
                sd, su = (gd, gu) if fit == "hgg" or z is None else (comb_sigma(gd, z[1]), comb_sigma(gu, z[2]))
                if key == "asimov":
                    w[poi] = rnd(1 - NSIG_ASIMOV * sd, 1 + NSIG_ASIMOV * su)
                else:
                    gobs = interval(f"{ref}/dataFit/higgsCombineDataPostFitScanFit_{poi}.MultiDimFit.mH125.07.root", poi)
                    if gobs is None:
                        print(f"  {fit} {key} {poi}: no HIG-26-007 Hgg observed scan, left to the ranges step")
                        continue
                    centre = gobs[0]
                    if fit == "comb":
                        zobs = interval(f"{h4l}/dataFit/higgsCombineDataPostFitScanFit_{poi}.MultiDimFit.mH125.07.root", poi)
                        if zobs is not None:
                            wg, wz = 1 / (0.5 * (gd + gu)) ** 2, 1 / (0.5 * (zobs[1] + zobs[2])) ** 2
                            centre = (wg * gobs[0] + wz * zobs[0]) / (wg + wz)
                    w[poi] = rnd(centre - NSIG_DATA * sd, centre + NSIG_DATA * su)
                print(f"  {fit} {key} {poi}: sigma -{sd:.3f} +{su:.3f} -> window {w[poi]}")
        ranges["source"] = ranges.get("source", "combination/make_expected_windows.py (expected uncertainties)")
        if not opt.dry_run:
            with open(jp, "w") as f:
                json.dump(ranges, f, indent=1)
            print(f"wrote {jp}")


if __name__ == "__main__":
    main()
