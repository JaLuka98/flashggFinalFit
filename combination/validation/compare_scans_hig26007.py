"""Hgg-only Asimov intervals of the combination workspace vs the HIG-26-007 fits of the same observable.

The stat-only intervals must agree (same signal models, background and in-processes; the per-bin outs
change the out yield by < 0.2%), the total ones are slightly larger (acceptance and BR uncertainties of the
total cross section).

usage: compare_scans_hig26007.py <obs> [<HIG-26-007 output prefix>]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import summarize_scans as ss  # noqa: E402

obs = sys.argv[1]
ref = sys.argv[2] if len(sys.argv) > 2 else \
    "/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/flashggFinalFit/output_2022_2023_2024"
here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"{'POI':26s} {'stat ours':>14s} {'stat 007':>14s} {'total ours':>14s} {'total 007':>14s}")
for poi in ss.load_maps().patterns(obs)[1]:
    row = []
    for kind in ("Stat", "Fit"):
        for base in (f"{here}/output_combination_{obs}/hgg/Combine/runFits_{obs}/asimov",
                     f"{ref}_{obs}/Combine/runFits_{obs}/asimov"):
            p = f"{base}/higgsCombineAsimovPostFitScan{kind}_{poi}.root"
            iv = ss.interval(ss.read_scan(p, poi)) if os.path.exists(p) else None
            row.append("missing" if not iv else f"+{ss.fmt(iv['up'])}/-{ss.fmt(iv['down'])}")
    print(f"{poi:26s} " + " ".join(f"{x:>14s}" for x in row))
