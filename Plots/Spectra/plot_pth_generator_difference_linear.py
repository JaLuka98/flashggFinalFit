"""Plot the POWHEG–MG5 generator difference divided by combined PTH fit errors.

The numerator is the full absolute bin-wise difference between the two ggH
predictions, expressed relative to the nominal total cross section. It is a
model-comparison estimate; the fit and spectrum theory band do not contain it.
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


FIT_DIR = Path(__file__).resolve().parents[2] / "output_asimov_PTH_HggH4l/comb/Combine/runFits_PTH"
SOURCE = FIT_DIR / "pth_generator_difference_vs_uncertainty.csv"
Y_MAX = 1.1
OUTPUT = FIT_DIR / "pth_mg5_powheg_uncertainty_ratios_0to1p1"
SUMMARY = FIT_DIR / "pth_mg5_powheg_uncertainty_ratios.csv"


def main():
    with SOURCE.open(newline="") as handle:
        rows = [row for row in csv.DictReader(handle)
                if row["channel"] == "comb" and row["alternative"] == "POWHEG"]
    if len(rows) != 19:
        raise ValueError(f"Expected 19 combined PTH bins, found {len(rows)} in {SOURCE}")

    labels = [f"{float(row['bin_low_GeV']):g}–{float(row['bin_high_GeV']):g}"
              for row in rows[:-1]] + [f">{float(rows[-1]['bin_low_GeV']):g}"]
    shift = np.array([float(row["generator_shift_fraction"]) for row in rows])
    total = np.array([float(row["total_fit_uncertainty_fraction"]) for row in rows])
    systematic = np.array([float(row["systematic_fit_uncertainty_fraction"]) for row in rows])
    if np.any(shift < 0) or np.any(total <= 0) or np.any(systematic <= 0):
        raise ValueError("Generator differences must be nonnegative and fit errors positive")

    ratios = (shift / total, shift / systematic)
    x = np.arange(len(labels))
    fig, axes = plt.subplots(2, 1, figsize=(14.5, 8.5), sharex=True)
    for ax, values, denominator in zip(axes, ratios, ("total", "systematic")):
        visible = values <= Y_MAX
        ax.plot(x, np.where(visible, values, np.nan), "o-", color="#ad3a35",
                markersize=5.5, linewidth=1.8)
        for i in np.flatnonzero(~visible):
            ax.scatter(i, Y_MAX - 0.015, marker="^", s=70, color="#ad3a35", zorder=4)
        ax.axhline(1, color="#333333", linestyle="--", linewidth=1.2)
        ax.set_ylim(0, Y_MAX)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.1])
        ax.set_xlim(-0.5, len(labels) - 0.5)
        ax.set_ylabel(r"$\delta_{\rm gen}/\delta_{\rm " + denominator + r"}$", fontsize=14)
        ax.grid(axis="y", color="#d7dbe1", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", labelbottom=True)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=55, ha="right", fontsize=9)
        ax.set_title(f"Generator-model estimate / {denominator} fit uncertainty", fontsize=12)

    axes[-1].set_xlabel(r"$p_T^H$ bin (GeV)")
    fig.suptitle("PTH combination: POWHEG–MG5 difference relative to fit uncertainties",
                 fontsize=15, y=0.99)
    fig.text(0.5, 0.012,
             r"$\delta_{\rm gen}=|\sigma_{\rm POWHEG}-\sigma_{\rm MG5}|/\sigma_{\rm nominal}$. "
             f"Dashed line = equal size. Triangles mark values above {Y_MAX:g}; exact ratios are in the CSV.",
             ha="center", fontsize=10)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.91, bottom=0.16, hspace=0.46)
    for extension in ("pdf", "png"):
        fig.savefig(OUTPUT.with_suffix(f".{extension}"), dpi=200)
    plt.close(fig)

    with SUMMARY.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("pth_bin_GeV", "generator_difference_percent_of_nominal",
                         "total_fit_uncertainty_percent", "systematic_fit_uncertainty_percent",
                         "generator_over_total", "generator_over_systematic"))
        for label, difference, total_error, systematic_error, total_ratio, systematic_ratio in zip(
                labels, shift, total, systematic, *ratios):
            writer.writerow((label, 100 * difference, 100 * total_error, 100 * systematic_error,
                             total_ratio, systematic_ratio))
    print(f"Wrote {OUTPUT}.pdf/.png and {SUMMARY}")


if __name__ == "__main__":
    main()
