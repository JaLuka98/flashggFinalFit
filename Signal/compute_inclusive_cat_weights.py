#!/usr/bin/env python3
"""
Compute S/(S+B) weights per analysis category (cat0/cat1/cat2), evaluated in
the mH +/- sigma_eff signal window of an inclusive datacard.

Reuses the S/B computation from Plots/pth_sb_yields.py. Output feeds
RunPlotter.py's --cats wall --loadCatWeights <this file> (S/(S+B)-weighted
combination of categories for the mass-resolution plots).

Run:
  python3 Signal/compute_inclusive_cat_weights.py \\
    --datacard-incl output_2022_2023_2024_inclusive/Combine/Datacard_2022_2023_2024.txt \\
    --output Signal/outdir_inclusive_mass_resolution_2022_2023_2024/catWeights.json
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Plots"))
import pth_sb_yields as sb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datacard-incl", required=True, help="Inclusive datacard path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    datacard_dir = os.path.dirname(os.path.abspath(args.datacard_incl))
    _, sig_procs = sb.assemble(args.datacard_incl, datacard_dir, sb.INCL_CONFIG)
    df_sigma = sb.assemble_sigma_window(
        args.datacard_incl, datacard_dir, sb.INCL_CONFIG, sig_procs,
        include_all_categories=False)

    weights = {row["cat"]: float(row["S"] / (row["S"] + row["B"])) for _, row in df_sigma.iterrows()}

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(weights, f, indent=2)
    print(f"saved {args.output}")
    print(json.dumps(weights, indent=2))


if __name__ == "__main__":
    main()
