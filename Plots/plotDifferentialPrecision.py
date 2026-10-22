#!/usr/bin/env python3
"""Compare expected differential precision in Hgg, H4l, and their combination.

The script reads the stat-only and stat+syst one-dimensional MultiDimFit scans,
determines the 68% CL intervals from the crossings of -2 Delta ln L = 1, and
creates a CMS-style forest plot.  The three input paths may point to the top-level
output directory, the ``Combine/runFits_<variable>`` directory, or directly to
``asimov``.

Example
-------
python Plots/plotDifferentialPrecision.py NJ \
    output_2022_2023_2024_NJ \
    /path/to/output_h4l_NJ \
    output_hgg_h4l_2022_2023_2024_NJ \
    -o differential_precision_NJ
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import ROOT
from matplotlib.legend_handler import HandlerBase
from matplotlib.lines import Line2D
from matplotlib.ticker import NullLocator


ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
hep.style.use("CMS")


VARIABLES = {
    "PTH": {
        "aliases": ("PTH",),
        "title": r"$p_{\mathrm{T}}^{\mathrm{H}}$",
        "bin_title": r"$p_{\mathrm{T}}^{\mathrm{H}}$ bin (GeV)",
        "underflow": None,
        "overflow": 10000.0,
    },
    "NJ": {
        "aliases": ("NJ", "NJETS"),
        "title": r"$N_{\mathrm{jets}}$",
        "bin_title": r"$N_{\mathrm{jets}}$ bin",
        "underflow": None,
        "overflow": 100.0,
    },
    "RAPIDITY": {
        "aliases": ("YH", "RAPIDITY"),
        "title": r"$|y^{\mathrm{H}}|$",
        "bin_title": r"$|y^{\mathrm{H}}|$ bin",
        "underflow": None,
        "overflow": None,
    },
    "PTJ0": {
        "aliases": ("PTJ0",),
        "title": r"$p_{\mathrm{T}}^{j_1}$",
        "bin_title": r"$p_{\mathrm{T}}^{j_1}$ bin (GeV)",
        "underflow": -10000.0,
        "underflow_label": r"$0j$",
        "overflow": 10000.0,
    },
    "MASSJ0J1": {
        "aliases": ("MASSJ0J1", "MJJ"),
        "title": r"$m_{jj}$",
        "bin_title": r"$m_{jj}$ bin (GeV)",
        "underflow": -10000.0,
        "underflow_label": r"$<2j$",
        "overflow": 10000.0,
    },
}


@dataclass(frozen=True)
class Interval:
    poi: str
    source: Path
    bestfit: float
    low: float
    high: float

    @property
    def precision(self) -> float:
        """Effective symmetric precision from the full 68% CL width."""
        return 0.5 * (self.high - self.low)


@dataclass(frozen=True)
class ChannelLegendHandle:
    label: str
    color: str
    marker: str

    def get_label(self) -> str:
        return self.label


class HandlerChannelErrorbar(HandlerBase):
    """Draw a horizontal errorbar with two caps and a central marker."""

    def create_artists(
        self, legend, handle, xdescent, ydescent, width, height, fontsize, transform
    ):
        xleft = xdescent + 0.05 * width
        xright = xdescent + 0.95 * width
        xcenter = 0.5 * (xleft + xright)
        ycenter = ydescent + 0.5 * height
        cap_half_height = 0.32 * height
        common = {"color": handle.color, "linewidth": 1.8, "transform": transform}
        artists = [
            Line2D([xleft, xright], [ycenter, ycenter], **common),
            Line2D(
                [xleft, xleft],
                [ycenter - cap_half_height, ycenter + cap_half_height],
                **common,
            ),
            Line2D(
                [xright, xright],
                [ycenter - cap_half_height, ycenter + cap_half_height],
                **common,
            ),
            Line2D(
                [xcenter],
                [ycenter],
                color=handle.color,
                marker=handle.marker,
                linestyle="none",
                markerfacecolor=handle.color,
                markeredgecolor=handle.color,
                markersize=6.5,
                transform=transform,
            ),
        ]
        return artists


def canonical_variable(value: str) -> str:
    value = value.upper()
    if value in VARIABLES:
        return value
    for canonical, settings in VARIABLES.items():
        if value in settings["aliases"]:
            return canonical
    raise argparse.ArgumentTypeError(
        f"unknown variable '{value}'; choose PTH, NJ, rapidity/YH, PTJ0, "
        "or MassJ0J1/mjj"
    )


def decode_number(token: str) -> float:
    """Decode Combine's filename representation, e.g. 0p15 or m0p5."""
    sign = -1.0 if token.startswith("m") else 1.0
    if token.startswith("m"):
        token = token[1:]
    if not re.fullmatch(r"\d+(?:p\d+)?", token):
        raise ValueError(f"not a Combine-style number: {token}")
    return sign * float(token.replace("p", "."))


def bin_from_poi(poi: str, variable: str) -> Tuple[float, float]:
    aliases = VARIABLES[variable]["aliases"]
    for alias in aliases:
        match = re.search(
            rf"(?:^|_){re.escape(alias)}_(m?\d+(?:p\d+)?)_(m?\d+(?:p\d+)?)(?:_|$)",
            poi,
            flags=re.IGNORECASE,
        )
        if match:
            return decode_number(match.group(1)), decode_number(match.group(2))
    raise ValueError(f"cannot determine a {variable} bin from POI '{poi}'")


def matching_poi_branches(tree: ROOT.TTree, variable: str) -> List[str]:
    aliases = tuple(alias.upper() for alias in VARIABLES[variable]["aliases"])
    matches = []
    for branch in tree.GetListOfBranches():
        name = branch.GetName()
        upper = name.upper()
        if not upper.startswith("R_"):
            continue
        if any(re.search(rf"(?:^|_){re.escape(alias)}_", upper) for alias in aliases):
            try:
                bin_from_poi(name, variable)
            except ValueError:
                continue
            matches.append(name)
    return matches


def candidate_files(directory: Path, uncertainty: str) -> List[Path]:
    if not directory.is_dir():
        raise FileNotFoundError(f"input directory does not exist: {directory}")

    candidates = []
    for path in directory.rglob("*.root"):
        lower = path.name.lower()
        # Split/POINTS files are deliberately not combined here; the production
        # step should merge them first.
        if ".points." in lower or "_split_" in lower:
            continue
        is_stat = "scanstat" in lower or "statonly" in lower or "stat_only" in lower
        is_total = "postfitscanfit" in lower or "withsyst" in lower
        if (uncertainty == "stat" and is_stat) or (uncertainty == "total" and is_total):
            candidates.append(path)
    return sorted(candidates)


def discover_scans(
    directory: Path, variable: str, uncertainty: str
) -> Dict[Tuple[float, float], Path]:
    if uncertainty not in ("stat", "total"):
        raise ValueError(f"unknown uncertainty type: {uncertainty}")
    found: Dict[Tuple[float, float], List[Path]] = {}
    for path in candidate_files(directory, uncertainty):
        root_file = ROOT.TFile.Open(str(path), "READ")
        if not root_file or root_file.IsZombie():
            print(f"warning: skipping unreadable ROOT file: {path}", file=sys.stderr)
            continue
        tree = root_file.Get("limit")
        if not tree or tree.GetEntries() < 2:
            root_file.Close()
            continue
        pois = matching_poi_branches(tree, variable)
        root_file.Close()
        if len(pois) != 1:
            continue
        key = bin_from_poi(pois[0], variable)
        found.setdefault(key, []).append(path)

    if not found:
        expected = "PostFitScanStat/statOnly" if uncertainty == "stat" else "PostFitScanFit/withSyst"
        raise RuntimeError(
            f"no final {uncertainty} {variable} scans found below {directory}. "
            f"Expected filenames containing '{expected}'."
        )

    selected = {}
    preferred_fit_dirs = {f"runfits_{alias.lower()}" for alias in VARIABLES[variable]["aliases"]}
    preferred_fit_dirs.add(f"runfits_{variable.lower()}")

    def rank(path: Path) -> Tuple[bool, bool, int, str]:
        relative = path.relative_to(directory)
        has_exact_fit_dir = any(part.lower() in preferred_fit_dirs for part in relative.parts)
        standard_token = "postfitscanstat" if uncertainty == "stat" else "postfitscanfit"
        return (
            standard_token not in path.name.lower(),
            not has_exact_fit_dir,
            len(relative.parts),
            str(path),
        )

    for key, paths in found.items():
        # Prefer the standard flashggFinalFit output name, then the shallowest
        # match. Raise on a remaining ambiguity instead of silently mixing fits.
        ranked = sorted(paths, key=rank)
        best_rank = rank(ranked[0])[:-1]
        tied = [p for p in ranked if rank(p)[:-1] == best_rank]
        if len(tied) > 1:
            listing = "\n  ".join(str(p) for p in tied)
            raise RuntimeError(f"ambiguous scans for bin {key} below {directory}:\n  {listing}")
        selected[key] = ranked[0]
    return selected


def linear_crossing(x0: float, y0: float, x1: float, y1: float, level: float) -> float:
    if y1 == y0:
        return 0.5 * (x0 + x1)
    return x0 + (level - y0) * (x1 - x0) / (y1 - y0)


def interval_from_scan(path: Path, variable: str, level: float = 1.0) -> Interval:
    root_file = ROOT.TFile.Open(str(path), "READ")
    if not root_file or root_file.IsZombie():
        raise RuntimeError(f"cannot open ROOT file: {path}")
    tree = root_file.Get("limit")
    pois = matching_poi_branches(tree, variable)
    if len(pois) != 1:
        root_file.Close()
        raise RuntimeError(f"expected one scanned {variable} POI in {path}, found {pois}")
    poi = pois[0]
    poi_leaf = tree.GetLeaf(poi)
    nll_leaf = tree.GetLeaf("deltaNLL")
    if not poi_leaf or not nll_leaf:
        root_file.Close()
        raise RuntimeError(f"missing '{poi}' or 'deltaNLL' branch in {path}")

    raw: List[Tuple[float, float]] = []
    for entry in range(tree.GetEntries()):
        tree.GetEntry(entry)
        x = float(poi_leaf.GetValue())
        y = 2.0 * float(nll_leaf.GetValue())
        if math.isfinite(x) and math.isfinite(y) and y > -1.0e-5:
            raw.append((x, max(0.0, y)))
    root_file.Close()
    if len(raw) < 3:
        raise RuntimeError(f"too few valid scan points in {path}")

    # Merged Combine outputs can repeat the best-fit row before every grid
    # point. At a duplicate x, retain the smallest NLL.
    unique: Dict[float, float] = {}
    for x, y in raw:
        unique[x] = min(y, unique.get(x, math.inf))
    xvals = np.array(sorted(unique), dtype=float)
    yvals = np.array([unique[x] for x in xvals], dtype=float)
    imin = int(np.argmin(yvals))
    bestfit = float(xvals[imin])

    low = None
    for i in range(imin - 1, -1, -1):
        if yvals[i] >= level and yvals[i + 1] <= level:
            low = linear_crossing(xvals[i], yvals[i], xvals[i + 1], yvals[i + 1], level)
            break
    high = None
    for i in range(imin, len(xvals) - 1):
        if yvals[i] <= level and yvals[i + 1] >= level:
            high = linear_crossing(xvals[i], yvals[i], xvals[i + 1], yvals[i + 1], level)
            break
    if low is None or high is None:
        raise RuntimeError(
            f"scan in {path} does not bracket both -2 Delta ln L = {level:g} crossings "
            f"around the best fit {bestfit:.5g}"
        )
    return Interval(poi, path, bestfit, float(low), float(high))


def number_label(value: float) -> str:
    return f"{value:g}"


def bin_label(key: Tuple[float, float], variable: str) -> str:
    low, high = key
    underflow = VARIABLES[variable]["underflow"]
    overflow = VARIABLES[variable]["overflow"]
    if underflow is not None and low <= underflow:
        if "underflow_label" in VARIABLES[variable]:
            return VARIABLES[variable]["underflow_label"]
        return rf"$< {number_label(high)}$"
    if variable == "NJ":
        if overflow is not None and high >= overflow:
            return rf"$\geq {low:g}$"
        if math.isclose(high, low + 1.0):
            return rf"${low:g}$"
    if overflow is not None and high >= overflow:
        return rf"$\geq {number_label(low)}$"
    return rf"${number_label(low)}\mathrm{{-}}{number_label(high)}$"


def gain(channel: Interval, combination: Interval) -> float:
    return 100.0 * (1.0 - combination.precision / channel.precision)


def systematic_bounds(total: Interval, stat: Interval) -> Tuple[float, float]:
    """Return asymmetric systematic bounds from quadrature subtraction."""
    total_down = total.bestfit - total.low
    total_up = total.high - total.bestfit
    stat_down = stat.bestfit - stat.low
    stat_up = stat.high - stat.bestfit

    def subtract(total_error: float, stat_error: float, side: str) -> float:
        difference = total_error**2 - stat_error**2
        if difference < -1.0e-8:
            print(
                f"warning: stat-only {side} uncertainty exceeds stat+syst for "
                f"{total.poi}; setting the systematic component to zero",
                file=sys.stderr,
            )
        return math.sqrt(max(0.0, difference))

    syst_down = subtract(total_down, stat_down, "downward")
    syst_up = subtract(total_up, stat_up, "upward")
    return total.bestfit - syst_down, total.bestfit + syst_up


def write_csv(
    path: Path,
    bins: Sequence[Tuple[float, float]],
    results: Dict[str, Dict[Tuple[float, float], Interval]],
    stat_results: Dict[str, Dict[Tuple[float, float], Interval]],
) -> None:
    fields = ["bin_low", "bin_high"]
    for channel in ("hgg", "h4l", "combination"):
        fields.extend(
            [
                f"{channel}_bestfit",
                f"{channel}_low68",
                f"{channel}_high68",
                f"{channel}_precision",
                f"{channel}_source",
                f"{channel}_stat_bestfit",
                f"{channel}_stat_low68",
                f"{channel}_stat_high68",
                f"{channel}_stat_precision",
                f"{channel}_stat_source",
                f"{channel}_syst_low68",
                f"{channel}_syst_high68",
            ]
        )
    with path.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for key in bins:
            row = {"bin_low": key[0], "bin_high": key[1]}
            for channel in ("hgg", "h4l", "combination"):
                item = results[channel][key]
                stat_item = stat_results[channel][key]
                syst_low, syst_high = systematic_bounds(item, stat_item)
                row.update(
                    {
                        f"{channel}_bestfit": item.bestfit,
                        f"{channel}_low68": item.low,
                        f"{channel}_high68": item.high,
                        f"{channel}_precision": item.precision,
                        f"{channel}_source": str(item.source),
                        f"{channel}_stat_bestfit": stat_item.bestfit,
                        f"{channel}_stat_low68": stat_item.low,
                        f"{channel}_stat_high68": stat_item.high,
                        f"{channel}_stat_precision": stat_item.precision,
                        f"{channel}_stat_source": str(stat_item.source),
                        f"{channel}_syst_low68": syst_low,
                        f"{channel}_syst_high68": syst_high,
                    }
                )
            writer.writerow(row)


def make_plot(
    bins: Sequence[Tuple[float, float]],
    results: Dict[str, Dict[Tuple[float, float], Interval]],
    stat_results: Dict[str, Dict[Tuple[float, float], Interval]],
    variable: str,
    output_base: Path,
    cms_label: str,
    lumi: float,
    energy: float,
    xlim: Tuple[float, float] | None,
) -> None:
    height = max(6.0, 0.52 * len(bins) + 3.4)
    fig, ax = plt.subplots(figsize=(9.0, height))
    y = np.arange(len(bins), dtype=float)
    styles = {
        "hgg": (r"$\mathrm{H}\to\gamma\gamma$", "#3f90da", "o", 0.22),
        "h4l": (r"$\mathrm{H}\to\mathrm{ZZ}\to4\ell$", "#ffa90e", "s", 0.0),
        "combination": ("Combination", "black", "D", -0.22),
    }

    for channel, (label, color, marker, offset) in styles.items():
        intervals = [results[channel][key] for key in bins]
        stat_intervals = [stat_results[channel][key] for key in bins]
        centers = np.array([item.bestfit for item in intervals])
        errors = np.array(
            [
                [item.bestfit - item.low for item in intervals],
                [item.high - item.bestfit for item in intervals],
            ]
        )
        ax.errorbar(
            centers,
            y + offset,
            xerr=errors,
            fmt="none",
            color=color,
            ecolor=color,
            elinewidth=2.2 if channel == "combination" else 1.8,
            capsize=3.5,
            capthick=1.8,
            zorder=3,
        )
        for key, ypos, item, stat_item in zip(
            bins, y + offset, intervals, stat_intervals
        ):
            # The systematic component is not shown for H4l in the final bin.
            # Keep the total interval and central marker unchanged.
            if channel == "h4l" and key == bins[-1] and variable == "PTH":
                continue
            syst_low, syst_high = systematic_bounds(item, stat_item)
            ax.plot(
                [syst_low, syst_high],
                [ypos, ypos],
                color=color,
                linewidth=8.0,
                alpha=0.38,
                solid_capstyle="butt",
                zorder=2,
            )
        ax.plot(
            centers,
            y + offset,
            linestyle="none",
            marker=marker,
            color=color,
            markersize=6.5,
            markerfacecolor=color,
            markeredgecolor=color,
            zorder=4,
        )

    # Leave the legend area clear of the SM reference line.
    if variable == "PTH":
        sm_line_top = 0.91
    elif variable == "MASSJ0J1":
        sm_line_top = 0.84
    else:
        sm_line_top = 0.80
    ax.axvline(
        1.0, color="#d62728", linestyle="--", linewidth=1.7, ymax=sm_line_top, zorder=1
    )
    ax.set_yticks(y)
    ax.set_yticklabels([bin_label(key, variable) for key in bins])
    # Reserve enough space between the two-row legend and the first result.
    ax.set_ylim(-2.6, len(bins) - 0.35)
    ax.invert_yaxis()
    ax.set_xlabel(r"POI $r_{\mathrm{bin}}$", fontsize=18)
    ax.set_ylabel(VARIABLES[variable]["bin_title"], fontsize=18)
    ax.yaxis.set_minor_locator(NullLocator())
    ax.tick_params(axis="x", which="major", labelsize=16)
    ax.tick_params(
        axis="y", which="major", left=True, right=False, length=5, labelsize=16
    )
    ax.tick_params(axis="y", which="minor", left=False, right=False)
    if xlim is not None:
        radius = max(abs(xlim[0] - 1.0), abs(xlim[1] - 1.0))
    else:
        all_limits = [
            value
            for channel in results.values()
            for key in bins
            for value in (channel[key].low, channel[key].high)
        ]
        radius = 1.06 * max(abs(value - 1.0) for value in all_limits)
    radius = max(radius, 0.1)
    reference_ticks = np.arange(0.0, 2.01, 0.25)
    if variable == "PTH":
        # Keep the automatically determined right edge, but do not waste space
        # on negative POI values in the PTH precision comparison.  Integer ticks
        # remain readable even when the weakly constrained high-PTH bins extend
        # the range well beyond the ranges used for the other observables.
        xmin, xmax = 0.0, 2 # 1.0 + radius
        ax.set_xlim(xmin, xmax)
        ax.set_xticks(reference_ticks)
        # The SM reference at r = 1 is already drawn in red above.  The other
        # interior tick positions get neutral dashed guide lines.
        for tick in reference_ticks[1:-1]:
            if not math.isclose(tick, 1.0):
                ax.axvline(
                    tick,
                    color="0.70",
                    linestyle="--",
                    linewidth=1.0,
                    zorder=0,
                )

    else:
        xmin, xmax = 1.0 - radius, 1.0 + radius
        ax.set_xlim(xmin, xmax)
        visible_ticks = [tick for tick in reference_ticks if xmin <= tick <= xmax]
        ax.set_xticks(visible_ticks)
        for tick in visible_ticks:
            if not math.isclose(tick, 1.0):
                ax.axvline(
                    tick,
                    color="0.70",
                    linestyle="--",
                    linewidth=1.0,
                    zorder=0,
                )

    channel_handles = [
        ChannelLegendHandle(*styles[channel][:3])
        for channel in ("combination", "h4l", "hgg")
    ]
    uncertainty_handles = [
        Line2D(
            [0], [0], color="0.35", linewidth=8, alpha=0.38,
            label="Exp. systematic uncertainty",
        ),
        Line2D([0], [0], color="#d62728", linewidth=1.7, linestyle="--", label="SM"),
    ]
    ax.legend(
        handles=channel_handles + uncertainty_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.98),
        ncol=3,
        frameon=False,
        fontsize=14,
        handler_map={ChannelLegendHandle: HandlerChannelErrorbar()},
    )
    hep.cms.label(cms_label, exp="", data=True, lumi=lumi, com=energy, ax=ax, fontsize=16)
    fig.tight_layout()

    output_base.parent.mkdir(parents=True, exist_ok=True)
    for extension in ("pdf", "png"):
        fig.savefig(output_base.with_suffix(f".{extension}"), bbox_inches="tight", dpi=200)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a CMS-style differential precision comparison from stat-only and stat+syst scans."
    )
    parser.add_argument(
        "variable",
        type=canonical_variable,
        help="PTH, NJ, rapidity (or YH), PTJ0, or MassJ0J1 (mjj)",
    )
    parser.add_argument("hgg_dir", type=Path, help="directory containing the Hgg scans")
    parser.add_argument("h4l_dir", type=Path, help="directory containing the H4l scans")
    parser.add_argument("combination_dir", type=Path, help="directory containing the combined scans")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output path without extension (default: differential_precision_<variable>)",
    )
    parser.add_argument("--cms-label", default="Private work (CMS data/simulation)")
    parser.add_argument("--lumi", type=float, default=171.4, help="integrated luminosity in fb^-1")
    parser.add_argument("--energy", type=float, default=13.6, help="centre-of-mass energy in TeV")
    parser.add_argument("--xlim", nargs=2, type=float, metavar=("MIN", "MAX"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    variable = args.variable
    directories = {
        "hgg": args.hgg_dir.resolve(),
        "h4l": args.h4l_dir.resolve(),
        "combination": args.combination_dir.resolve(),
    }
    scans = {
        uncertainty: {
            name: discover_scans(path, variable, uncertainty)
            for name, path in directories.items()
        }
        for uncertainty in ("total", "stat")
    }
    bin_sets = {
        f"{name} ({uncertainty})": set(items)
        for uncertainty, channel_scans in scans.items()
        for name, items in channel_scans.items()
    }
    if len({frozenset(items) for items in bin_sets.values()}) != 1:
        union = set().union(*bin_sets.values())
        details = []
        for name, items in bin_sets.items():
            missing = sorted(union - items)
            if missing:
                details.append(f"{name} is missing: {missing}")
        raise RuntimeError("the three inputs do not contain identical bins; " + "; ".join(details))
    bins = sorted(next(iter(bin_sets.values())))
    results = {
        name: {key: interval_from_scan(paths[key], variable) for key in bins}
        for name, paths in scans["total"].items()
    }
    stat_results = {
        name: {key: interval_from_scan(paths[key], variable) for key in bins}
        for name, paths in scans["stat"].items()
    }

    output_base = args.output or Path(f"differential_precision_{variable}")
    output_base = output_base.with_suffix("")
    output_base.parent.mkdir(parents=True, exist_ok=True)
    write_csv(output_base.with_suffix(".csv"), bins, results, stat_results)
    make_plot(
        bins,
        results,
        stat_results,
        variable,
        output_base,
        args.cms_label,
        args.lumi,
        args.energy,
        tuple(args.xlim) if args.xlim else None,
    )

    print(f"Wrote {output_base.with_suffix('.pdf')}")
    print(f"Wrote {output_base.with_suffix('.png')}")
    print(f"Wrote {output_base.with_suffix('.csv')}")
    print("\nBin                 gain vs Hgg    gain vs H4l")
    for key in bins:
        print(
            f"{bin_label(key, variable):<20} "
            f"{gain(results['hgg'][key], results['combination'][key]):>+9.2f}% "
            f"{gain(results['h4l'][key], results['combination'][key]):>+13.2f}%"
        )


if __name__ == "__main__":
    main()
