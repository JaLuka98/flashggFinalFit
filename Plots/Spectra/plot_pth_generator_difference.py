"""Compare the combined PTH fit with the POWHEG versus MG5 prediction shift.

Run with ``python3 Plots/Spectra/plot_pth_generator_difference.py``.
The generator difference is a model comparison, not a nuisance added to the fit.
"""

import csv
import json
import runpy
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


REPO = Path(__file__).resolve().parents[2]
FIT_DIR = REPO / "output_asimov_PTH_HggH4l/comb/Combine/runFits_PTH"
SOURCE_DIR = REPO / "Plots/Spectra/fidXS"


def fiducial_xs(name, boundaries):
    source = SOURCE_DIR / f"fidXS_PTH_{name}.py"
    values = runpy.run_path(str(source))
    if not np.allclose(values["Boundaries"], boundaries):
        raise ValueError(f"Generator binning differs: {source}")
    result = np.asarray(values["fidXS"], dtype=float)
    if result.shape != (len(boundaries) - 1,):
        raise ValueError(f"Unexpected number of prediction bins: {source}")
    return result


def save_figure(fig, stem):
    for extension in ("pdf", "png"):
        fig.savefig(FIT_DIR / f"{stem}.{extension}", dpi=200, bbox_inches="tight")
    plt.close(fig)


def bin_labels(boundaries):
    labels = [f"{low:g}–{high:g}" for low, high in zip(boundaries[:-2], boundaries[1:-1])]
    labels.append(f"≥{boundaries[-2]:g}")
    return labels


def plot_signed_comparison(labels, signed_shift, total, systematic):
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(11.8, 10.8))
    for i in y:
        ax.axhspan(i - 0.5, i + 0.5, color="#f5f6f8" if i % 2 == 0 else "white", zorder=0)
    ax.hlines(y, -100 * total, 100 * total, color="#c8ced8", linewidth=13,
              capstyle="round", zorder=1)
    ax.hlines(y, -100 * systematic, 100 * systematic, color="#457b9d",
              linewidth=7, capstyle="round", zorder=2)
    ax.scatter(100 * signed_shift, y, s=70, facecolor="#d04b36",
               edgecolor="white", linewidth=1.0, zorder=3)
    ax.axvline(0, color="#333333", linewidth=0.8, zorder=1)
    ax.set(yticks=y, yticklabels=labels, xlabel="Relative change in bin cross section (%)",
           title="POWHEG − MG5_aMC@NLO (NNLOPS): PTH combination")
    ax.invert_yaxis()
    ax.set_xlim(-58, 58)
    ax.set_ylim(len(labels) - 0.5, -0.5)
    ax.xaxis.grid(True, color="#e0e3e8", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.legend(handles=[
        Line2D([0], [0], color="#c8ced8", linewidth=10, label="Combined fit: ±total uncertainty"),
        Line2D([0], [0], color="#457b9d", linewidth=6, label="Combined fit: ±systematic uncertainty"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#d04b36",
               markeredgecolor="white", markersize=9, label="POWHEG prediction shift"),
    ], loc="lower center", bbox_to_anchor=(0.5, -0.16), ncol=1, frameon=False)
    fig.text(0.5, 0.012,
             "Shift is (POWHEG − MG5) / nominal total prediction; only ggH changes. "
             "Fit errors are averages of the up/down values.",
             ha="center", fontsize=9)
    fig.subplots_adjust(left=0.16, right=0.98, top=0.94, bottom=0.19)
    save_figure(fig, "pth_mg5_powheg_vs_fit_uncertainty")


def plot_uncertainty_fractions(labels, absolute_shift, total, systematic):
    y = np.arange(len(labels))
    percentages = (100 * absolute_shift / total, 100 * absolute_shift / systematic)
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 10.8), sharey=True,
                             gridspec_kw={"width_ratios": [1, 1.45], "wspace": 0.08})
    for ax, values, name in zip(axes, percentages, ("Total fit uncertainty", "Systematic fit uncertainty")):
        colors = np.where(values > 100, "#d04b36", "#457b9d")
        ax.barh(y, values, height=0.64, color=colors, zorder=2)
        ax.axvline(100, color="#333333", linestyle="--", linewidth=1.2, zorder=3)
        ax.set_xlim(0, max(110, np.ceil(values.max() / 25) * 25 + 18))
        ax.set_xlabel("POWHEG–MG5 difference / fit uncertainty (%)")
        ax.set_title(name)
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, color="#e0e3e8", linewidth=0.8)
        ax.tick_params(axis="y", length=0, pad=8)
        for pos, value in zip(y, values):
            ax.text(value + 2, pos, f"{value:.0f}%", va="center", fontsize=9)
    axes[0].set(yticks=y, yticklabels=labels)
    axes[0].invert_yaxis()
    axes[1].tick_params(axis="y", labelleft=False)
    fig.suptitle("How large is the POWHEG–MG5 difference in each PTH bin?", fontsize=16, y=0.975)
    fig.text(0.5, 0.045,
             "Dashed line = 100% (same size as fit uncertainty). Red bars exceed it. "
             "This model difference is not added to the fit uncertainty.",
             ha="center", fontsize=10)
    fig.subplots_adjust(left=0.13, right=0.98, top=0.91, bottom=0.12)
    save_figure(fig, "pth_mg5_powheg_fraction_of_fit_uncertainty")


def main():
    with (FIT_DIR / "combined_spectra_blinded.json").open() as handle:
        spectra = json.load(handle)
    bins = np.asarray(spectra["bins"], dtype=float)
    if len(spectra["pois"]) != len(bins) - 1:
        raise ValueError("The PTH scans and prediction have different bin counts")

    nominal_gg_h = fiducial_xs("ggH", bins)
    other_h = sum(fiducial_xs(name, bins) for name in ("VBFH", "VH", "ttH"))
    nominal = nominal_gg_h + other_h
    if np.any(nominal <= 0):
        raise ValueError("Nonpositive nominal cross section")
    signed_shift = (fiducial_xs("ggH_powheg", bins) - nominal_gg_h) / nominal
    fit = spectra["fits"]["comb"]
    total = (np.asarray(fit["tot_up"]) + np.asarray(fit["tot_dn"])) / 2
    systematic = (np.asarray(fit["syst_up"]) + np.asarray(fit["syst_dn"])) / 2
    if np.any(total <= 0) or np.any(systematic <= 0):
        raise ValueError("Nonpositive fit uncertainty")

    labels = bin_labels(bins)
    plot_signed_comparison(labels, signed_shift, total, systematic)
    plot_uncertainty_fractions(labels, np.abs(signed_shift), total, systematic)

    rows = []
    for i, poi in enumerate(spectra["pois"]):
        rows.append({
            "poi": poi, "pth_bin_GeV": labels[i],
            "powheg_minus_mg5_percent": 100 * signed_shift[i],
            "total_fit_uncertainty_percent": 100 * total[i],
            "systematic_fit_uncertainty_percent": 100 * systematic[i],
            "difference_over_total_percent": 100 * abs(signed_shift[i]) / total[i],
            "difference_over_systematic_percent": 100 * abs(signed_shift[i]) / systematic[i],
        })
    with (FIT_DIR / "pth_mg5_powheg_bin_summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote two plots and {len(rows)} bin summaries to {FIT_DIR}")


if __name__ == "__main__":
    main()
