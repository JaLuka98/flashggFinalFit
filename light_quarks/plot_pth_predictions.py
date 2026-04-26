#!/usr/bin/env python3
"""
Plot the SM and light-quark (uuH, ddH, ssH) PTH predictions used to build
the light-quark model ratios.

BSM CSV inputs are in pb/GeV and are converted to fb/GeV.
The SM input is stored as fiducial cross section per bin in fb and is divided
by the bin width to obtain fb/GeV.
The final BSM bin is rescaled by SSH_LAST_BIN_SCALE to match the analysis
overflow bin.

Usage:
    python3 light_quarks/plot_pth_predictions.py
    python3 light_quarks/plot_pth_predictions.py --output-dir /some/path
"""

import argparse
import csv
import json
import os

import numpy as np

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-light-quarks")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SM_JSON  = os.path.join(SCRIPT_DIR, "run3_with_HIG_19_016_Binning.json")
DEFAULT_SSH_CSV  = os.path.join(SCRIPT_DIR, "ssH_13p6TeV_PTH_HIG19016-aafidR3.csv")
DEFAULT_DDH_CSV  = os.path.join(SCRIPT_DIR, "ddH_13p6TeV_PTH_HIG19016-aafidR3.csv")
DEFAULT_UUH_CSV  = os.path.join(SCRIPT_DIR, "uuH_13p6TeV_PTH_HIG19016-aafidR3.csv")
BSM_LAST_BIN_SCALE = 100.0

QUARKS = [
    ("uuH", "up",     "#2ca02c"),
    ("ddH", "down",   "#ff7f0e"),
    ("ssH", "strange","#1f77b4"),
]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sm-json",  default=DEFAULT_SM_JSON)
    parser.add_argument("--ssh-csv",  default=DEFAULT_SSH_CSV)
    parser.add_argument("--ddh-csv",  default=DEFAULT_DDH_CSV)
    parser.add_argument("--uuh-csv",  default=DEFAULT_UUH_CSV)
    parser.add_argument("--output-dir",  default=SCRIPT_DIR)
    parser.add_argument("--output-name", default="pth_sm_vs_lightquarks")
    return parser.parse_args()


def load_sm(sm_json):
    with open(sm_json) as fin:
        payload = json.load(fin)["total"]
    edges   = np.array(payload["bins"],  dtype=float)
    fid_xs  = np.array(payload["fidXS"], dtype=float)
    widths  = edges[1:] - edges[:-1]
    return edges, fid_xs / widths


def load_bsm(bsm_csv):
    rows = []
    with open(bsm_csv) as fin:
        reader = csv.DictReader(
            (line for line in fin if not line.startswith("#")),
            fieldnames=["bin_lo", "bin_hi", "value", "error"],
        )
        for row in reader:
            rows.append(row)

    xs  = np.array([float(r["value"]) for r in rows]) * 1e3   # pb→fb
    err = np.array([float(r["error"]) for r in rows]) * 1e3
    xs[-1]  *= BSM_LAST_BIN_SCALE
    err[-1] *= BSM_LAST_BIN_SCALE
    return xs, err


def main():
    args = parse_args()

    sm_edges, sm_vals = load_sm(args.sm_json)
    centers = 0.5 * (sm_edges[1:] + sm_edges[:-1])
    widths  = sm_edges[1:] - sm_edges[:-1]

    bsm_data = {
        "uuH": load_bsm(args.uuh_csv),
        "ddH": load_bsm(args.ddh_csv),
        "ssH": load_bsm(args.ssh_csv),
    }

    # Sanity check
    for key, (xs, _) in bsm_data.items():
        if len(xs) != len(sm_vals):
            raise RuntimeError(
                "%s has %d bins but SM has %d" % (key, len(xs), len(sm_vals))
            )

    plt.rcParams.update({
        "font.family":       "sans-serif",
        "font.sans-serif":   ["DejaVu Sans"],
        "font.size":         13,
        "axes.linewidth":    1.2,
        "xtick.direction":   "in",
        "ytick.direction":   "in",
        "xtick.top":         True,
        "ytick.right":       True,
    })

    fig, (ax, rax) = plt.subplots(
        2, 1,
        figsize=(8, 7),
        sharex=True,
        gridspec_kw={"height_ratios": [3.0, 1.5], "hspace": 0.04},
    )
    fig.subplots_adjust(left=0.14, right=0.96, bottom=0.12, top=0.90)

    # --- top panel: absolute predictions ---
    ax.stairs(sm_vals, sm_edges, color="black", linewidth=2.2, label="SM (ggH)", zorder=5)

    for key, flavor, color in QUARKS:
        xs, err = bsm_data[key]
        label = "%s (%s quark)" % (key, flavor)
        ax.stairs(xs, sm_edges, color=color, linewidth=2.0, label=label)
        ax.errorbar(
            centers, xs,
            yerr=err, xerr=widths / 2.0,
            fmt="none", ecolor=color, elinewidth=1.0, capsize=0, alpha=0.7,
        )

    ax.set_yscale("log")
    ax.set_ylabel(r"$d\sigma/dp_{T}^{H}$ [fb/GeV]", fontsize=15)
    ax.legend(frameon=False, loc="upper right", fontsize=12)
    ax.text(0.00,  1.015, "CMS",      transform=ax.transAxes,
            ha="left",  va="bottom", fontsize=22, fontweight="bold")
    ax.text(0.125, 1.017, "Internal", transform=ax.transAxes,
            ha="left",  va="bottom", fontsize=17, style="italic")
    ax.text(0.98,  1.015, "13.6 TeV", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=14)

    # --- bottom panel: BSM/SM ratios ---
    rax.axhline(1.0, color="0.45", linestyle="--", linewidth=1.0)

    for key, flavor, color in QUARKS:
        xs, _ = bsm_data[key]
        ratio = xs / sm_vals
        rax.stairs(ratio, sm_edges, color=color, linewidth=2.0, label=key)
        rax.plot(centers, ratio, "o", color=color, markersize=4)

    rax.set_yscale("log")
    rax.set_ylabel("BSM / SM", fontsize=14)
    rax.set_xlabel(r"$p_{T}^{H}$ [GeV]", fontsize=15)
    rax.set_xlim(sm_edges[0], sm_edges[-1])
    rax.legend(frameon=False, loc="upper left", fontsize=11, ncol=3)

    for axis in (ax, rax):
        axis.minorticks_on()
        axis.tick_params(axis="both", which="major", labelsize=12, length=7)
        axis.tick_params(axis="both", which="minor", length=4)

    os.makedirs(args.output_dir, exist_ok=True)
    out_base = os.path.join(args.output_dir, args.output_name)
    fig.savefig(out_base + ".pdf")
    fig.savefig(out_base + ".png")

    print("Saved: %s.pdf" % out_base)
    print("Saved: %s.png" % out_base)
    print("")

    # Print derived BSM/SM ratios for all quarks
    for key, flavor, _ in QUARKS:
        xs, _ = bsm_data[key]
        ratio = xs / sm_vals
        print("--- %s (%s quark) BSM/SM ratios ---" % (key, flavor))
        for lo, hi, sm, bsm, rat in zip(
            sm_edges[:-1], sm_edges[1:], sm_vals, xs, ratio
        ):
            print("  %7.1f-%-7.1f  SM=%12.6g fb/GeV  BSM=%12.6g fb/GeV  ratio=%12.6g"
                  % (lo, hi, sm, bsm, rat))
        print("")


if __name__ == "__main__":
    main()
