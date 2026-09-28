#!/usr/bin/env python3
"""Plot total differential Higgs-boson cross sections by production mode.

The theory inputs and plotting conventions are taken from the same YAML files
that are used by ``law_spectra.py``.  By default, plots for PTH and rapidity are
written as both PDF and PNG files.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
from types import ModuleType

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import mplhep as hep
import numpy as np
import yaml


# plt.style.use(hep.style.CMS)
hep.style.use("CMS")

SCRIPT_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = Path(os.environ.get("ANALYSIS_PATH", SCRIPT_DIR.parents[1])).resolve()
THEORY_DIR = SCRIPT_DIR / "fidXS"

PRODUCTION_MODES = {
    "ggh": ("ggH", "#5790fc"),
    "vbf": ("VBF", "#f89c20"),
    "vh": ("VH", "#e42536"),
    "tth": (r"$t\bar{t}H$", "#964a8b"),
}

GENERATED_PROCESS_NAMES = {
    "ggh": "ggH",
    "vbf": "VBFH",
    "vh": "VH",
    "tth": "ttH",
}

FB_TO_PB = 1.0e-3
RAPIDITY_X_LIM = (0.0, 4.0)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot total differential cross sections for PTH and rapidity.",
    )
    parser.add_argument(
        "--year",
        default="2022_2023_2024",
        help="Year tag used for the analysis and plotting YAML files.",
    )
    parser.add_argument(
        "--variables",
        nargs="+",
        choices=("PTH", "rapidity"),
        default=("PTH", "rapidity"),
        help="Variables to plot (default: PTH rapidity).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SCRIPT_DIR / "total_differential_xsec",
        help="Directory in which PDF and PNG files are written.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file does not exist: {path}")
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_theory_file(module_path: Path) -> ModuleType:
    """Load a Python theory-input file directly from its path."""
    if not module_path.is_file():
        raise FileNotFoundError(f"Theory input does not exist: {module_path}")

    module_name = f"theory_input_{module_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import theory input: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_theory_module(module_name: str) -> ModuleType:
    """Load a conventional theory input from Plots/Spectra/fidXS."""
    return load_theory_file(THEORY_DIR / f"{module_name}.py")


def cms_label(spectra_config: dict, plotting_config: dict) -> None:
    hep.cms.label(
        "Private work (CMS simulation)",
        exp="",
        data=True,
        # lumi=plotting_config.get("lumi"),
        com=13.6,
        fontsize=20,
    )


def validate_inputs(
    modules: dict[str, ModuleType],
    attributes: dict[str, str] | None = None,
) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    reference_edges = np.asarray(modules["ggh"].Boundaries, dtype=float)
    cross_sections = {}
    attributes = attributes or {mode: "totXS" for mode in modules}

    if reference_edges.ndim != 1 or len(reference_edges) < 2:
        raise ValueError("Theory bin boundaries must be a one-dimensional array.")

    for mode, module in modules.items():
        edges = np.asarray(module.Boundaries, dtype=float)
        attribute = attributes[mode]
        if not hasattr(module, attribute):
            raise AttributeError(f"{module.__name__} does not define {attribute}.")
        values = np.asarray(getattr(module, attribute), dtype=float)
        if not np.array_equal(edges, reference_edges):
            raise ValueError(f"The bin boundaries for {mode} differ from those for ggH.")
        if values.shape != (len(reference_edges) - 1,):
            raise ValueError(
                f"{attribute} in {module.__name__} has {len(values)} values, "
                f"but {len(reference_edges) - 1} are required."
            )
        if not np.all(np.isfinite(values)) or np.any(values < 0):
            raise ValueError(f"{attribute} in {module.__name__} contains invalid values.")
        cross_sections[mode] = values

    return reference_edges, cross_sections


def make_plot(variable: str, year: str, output_dir: Path) -> None:
    analysis_config = load_yaml(ANALYSIS_DIR / "config" / f"{year}_{variable}.yml")
    plotting_config = load_yaml(SCRIPT_DIR / "config" / f"{year}_{variable}.yml")
    spectra_config = dict(analysis_config["spectra"])
    spectra_config.update(spectra_config.get("total", {}))

    generated_observable = "PTH" if variable == "PTH" else "YH"
    generated_input = output_dir / f"fidXS_{generated_observable}_all_spectra.py"
    if generated_input.is_file():
        generated_module = load_theory_file(generated_input)
        modules = {mode: generated_module for mode in PRODUCTION_MODES}
        attributes = {
            mode: f"totXS_{GENERATED_PROCESS_NAMES[mode]}"
            for mode in PRODUCTION_MODES
        }
        print(f"Using generated theory input {generated_input}")
    else:
        modules = {
            mode: load_theory_module(spectra_config[f"{mode}_xs"])
            for mode in PRODUCTION_MODES
        }
        attributes = None
    physical_edges, cross_sections = validate_inputs(modules, attributes)

    # Match law_spectra.py: the final open PTH bin is displayed up to the
    # configured overflow edge and normalized by that displayed width.
    plot_edges = physical_edges.copy()
    if "overflow" in spectra_config:
        plot_edges[-1] = float(spectra_config["overflow"])
    bin_widths = np.diff(plot_edges)
    if variable == "PTH":
        # Zero cannot be drawn on a logarithmic x-axis.  Clip only the visible
        # edge; bin_widths above still contains the physical first-bin width.
        plot_edges[0] = 1.0
    differential_xs = {
        mode: FB_TO_PB * values / bin_widths
        for mode, values in cross_sections.items()
    }
    differential_xs["sum"] = np.sum(list(differential_xs.values()), axis=0)

    fig, ax = plt.subplots(figsize=(10, 8), dpi=120)
    cms_label(spectra_config, plotting_config)

    # Draw the inclusive prediction first so that the production-mode curves
    # remain visible wherever they run close to All.
    ax.stairs(
        differential_xs["sum"],
        plot_edges,
        baseline=None,
        label="All",
        color="black",
        linewidth=3.0,
        zorder=1,
    )
    for mode, (label, color) in PRODUCTION_MODES.items():
        ax.stairs(
            differential_xs[mode],
            plot_edges,
            baseline=None,
            label=label,
            color=color,
            linewidth=2.2,
            zorder=2,
        )

    use_log_scale = spectra_config.get("plot_log", False) or variable == "rapidity"
    if use_log_scale:
        ax.set_yscale("log")

    if variable == "PTH":
        ax.set_xscale("log")
        ax.set_xlim(1, spectra_config["x_lim"][1])
    else:
        ax.set_xlim(RAPIDITY_X_LIM)
    # The spectrum-task y range also has to accommodate fitted data and its
    # uncertainties.  For this prediction-only plot, derive a tighter range
    # directly from the five curves.
    maximum = float(np.max(differential_xs["sum"]))
    if variable == "rapidity":
        headroom_factor = 30.0
    else:
        headroom_factor = 30.0 if use_log_scale else 1.35
    ax.set_ylim(top=maximum * headroom_factor)

    x_unit = spectra_config.get("x_unit", "")
    y_unit = "(pb/GeV)" if variable == "PTH" else "(pb)"
    ax.set_xlabel(r"$" + spectra_config["variable"] + r"$ " + x_unit, fontsize=20)
    ax.set_ylabel(
        r"$\Delta\sigma_{\mathrm{tot}} / \Delta "
        + spectra_config["variable"]
        + r"$ "
        + y_unit,
        fontsize=20,
    )
    ax.tick_params(axis="both", labelsize=18)
    handles, labels = ax.get_legend_handles_labels()
    handles_by_label = dict(zip(labels, handles))
    blank_handle = Line2D([], [], linestyle="none", label="")
    legend_handles = [
        handles_by_label["All"],
        blank_handle,
        handles_by_label["ggH"],
        handles_by_label["VH"],
        handles_by_label["VBF"],
        handles_by_label[r"$t\bar{t}H$"],
    ]
    legend_labels = ["All", "", "ggH", "VH", "VBF", r"$t\bar{t}H$"]
    ax.legend(
        legend_handles,
        legend_labels,
        ncol=3,
        fontsize=19,
        handlelength=2.4,
        labelspacing=0.45,
        columnspacing=1.2,
        loc=spectra_config.get("legend_location", "upper right"),
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_stem = output_dir / f"total_differential_xsec_{variable}"
    for extension in ("pdf", "png"):
        fig.savefig(output_stem.with_suffix(f".{extension}"), bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"Wrote {output_stem}.pdf and {output_stem}.png")


def main() -> None:
    args = parse_arguments()
    for variable in args.variables:
        make_plot(variable, args.year, args.output_dir.resolve())


if __name__ == "__main__":
    main()
