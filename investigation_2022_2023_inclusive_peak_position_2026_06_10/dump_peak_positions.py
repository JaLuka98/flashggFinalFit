#!/usr/bin/env python3

"""Dump fitted peak-position information from a post-fit H->yy workspace.

The script loads a Combine/flashgg post-fit workspace, restores the
MultiDimFit snapshot, and for each signal pdf matching ``hggpdfsmrel_*``
it records:

- the fixed Higgs mass value (``MH``)
- all component mean functions (``mean_g*_*``)
- a numerical estimate of the pdf peak from a scan over ``CMS_hgg_mass``

The output is a TSV table. This is intentionally lightweight so we can
iterate on the interpretation after the first inspection.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple


def load_root():
    try:
        import ROOT  # type: ignore
    except Exception as exc:  # pragma: no cover - runtime environment issue
        raise RuntimeError(
            "Failed to import ROOT. Please run this inside the CMSSW environment "
            "(for example after sourcing cmsenv)."
        ) from exc

    return ROOT


@dataclass
class PeakResult:
    pdf_name: str
    pdf_class: str
    mh: float
    peak_mass: float
    peak_value: float
    mean_names: List[str]
    mean_values: List[float]

    @property
    def best_mean_name(self) -> str:
        if not self.mean_names:
            return ""
        # Use the component mean closest to the numerical pdf peak.
        idx = min(
            range(len(self.mean_values)),
            key=lambda i: abs(self.mean_values[i] - self.peak_mass),
        )
        return self.mean_names[idx]

    @property
    def best_mean_value(self) -> float:
        if not self.mean_values:
            return float("nan")
        idx = min(
            range(len(self.mean_values)),
            key=lambda i: abs(self.mean_values[i] - self.peak_mass),
        )
        return self.mean_values[idx]


def iter_roo_collection(collection) -> Iterable[object]:
    it = collection.createIterator()
    obj = it.Next()
    while obj:
        yield obj
        obj = it.Next()


def scan_pdf_peak(ROOT, pdf, xvar, scan_min: float, scan_max: float) -> Tuple[float, float]:
    """Return (peak_mass, pdf_value) from a coarse+fine scan."""

    argset = ROOT.RooArgSet(xvar)

    def eval_at(value: float) -> float:
        xvar.setVal(value)
        return float(pdf.getVal(argset))

    # Coarse scan
    best_mass = scan_min
    best_value = -1.0
    n_coarse = 600
    for i in range(n_coarse):
        mass = scan_min + (scan_max - scan_min) * i / max(1, n_coarse - 1)
        value = eval_at(mass)
        if value > best_value:
            best_mass = mass
            best_value = value

    # Fine scan around the best coarse point
    window = 0.5
    lo = max(scan_min, best_mass - window)
    hi = min(scan_max, best_mass + window)
    n_fine = 1000
    for i in range(n_fine):
        mass = lo + (hi - lo) * i / max(1, n_fine - 1)
        value = eval_at(mass)
        if value > best_value:
            best_mass = mass
            best_value = value

    return best_mass, best_value


def find_component_means(w, rest_name: str) -> Tuple[List[str], List[float]]:
    names: List[str] = []
    values: List[float] = []

    # The signal model uses names like mean_g0_<rest>, mean_g1_<rest>, ...
    pattern = re.compile(rf"^mean_g\d+_{re.escape(rest_name)}$")
    for obj in iter_roo_collection(w.allFunctions()):
        name = obj.GetName()
        if not pattern.match(name):
            continue
        try:
            values.append(float(obj.getVal()))
            names.append(name)
        except Exception:
            continue

    return names, values


def extract_peak_info(ROOT, w, pdf_name: str) -> Optional[PeakResult]:
    pdf = w.pdf(pdf_name)
    if not pdf:
        return None

    mh_var = w.var("MH")
    xvar = w.var("CMS_hgg_mass")
    if not mh_var or not xvar:
        raise RuntimeError("Workspace does not contain MH and/or CMS_hgg_mass.")

    # Determine the matching mean functions by stripping the common prefix.
    rest_name = pdf_name[len("hggpdfsmrel_") :]
    mean_names, mean_values = find_component_means(w, rest_name)

    scan_min = float(xvar.getMin()) if xvar.hasMin() else 100.0
    scan_max = float(xvar.getMax()) if xvar.hasMax() else 180.0
    peak_mass, peak_value = scan_pdf_peak(ROOT, pdf, xvar, scan_min, scan_max)

    return PeakResult(
        pdf_name=pdf_name,
        pdf_class=pdf.ClassName(),
        mh=float(mh_var.getVal()),
        peak_mass=float(peak_mass),
        peak_value=float(peak_value),
        mean_names=mean_names,
        mean_values=mean_values,
    )


def write_tsv(results: Sequence[PeakResult], output_path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            [
                "pdf_name",
                "pdf_class",
                "mh",
                "peak_mass",
                "peak_value",
                "delta_peak_minus_mh",
                "best_mean_name",
                "best_mean_value",
                "delta_best_mean_minus_mh",
                "mean_names",
                "mean_values",
            ]
        )
        for row in results:
            writer.writerow(
                [
                    row.pdf_name,
                    row.pdf_class,
                    f"{row.mh:.6f}",
                    f"{row.peak_mass:.6f}",
                    f"{row.peak_value:.12g}",
                    f"{row.peak_mass - row.mh:.6f}",
                    row.best_mean_name,
                    f"{row.best_mean_value:.6f}" if not math.isnan(row.best_mean_value) else "",
                    f"{row.best_mean_value - row.mh:.6f}" if not math.isnan(row.best_mean_value) else "",
                    ";".join(row.mean_names),
                    ";".join(f"{v:.6f}" for v in row.mean_values),
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dump peak-position information from a post-fit H->yy workspace."
    )
    parser.add_argument(
        "--inputWSFile",
        required=True,
        help="Path to the post-fit ROOT workspace file (Combine MultiDimFit output).",
    )
    parser.add_argument(
        "--snapshotName",
        default="MultiDimFit",
        help="Snapshot to load from the workspace (default: MultiDimFit).",
    )
    parser.add_argument(
        "--pattern",
        default=r"^hggpdfsmrel_.*",
        help="Regex used to select signal pdf names (default: ^hggpdfsmrel_.*).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output TSV file.",
    )
    args = parser.parse_args()

    ROOT = load_root()
    ROOT.gROOT.SetBatch(True)
    ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

    f = ROOT.TFile.Open(args.inputWSFile)
    if not f or f.IsZombie():
        raise RuntimeError(f"Failed to open input file: {args.inputWSFile}")

    w = f.Get("w")
    if not w:
        raise RuntimeError("Could not find RooWorkspace 'w' in the input file.")

    if not w.loadSnapshot(args.snapshotName):
        raise RuntimeError(
            f"Could not load snapshot '{args.snapshotName}'. "
            "Check the workspace and snapshot name."
        )

    pdf_pattern = re.compile(args.pattern)
    results: List[PeakResult] = []
    for obj in iter_roo_collection(w.allPdfs()):
        pdf_name = obj.GetName()
        if not pdf_pattern.match(pdf_name):
            continue
        result = extract_peak_info(ROOT, w, pdf_name)
        if result is not None:
            results.append(result)

    results.sort(key=lambda r: r.pdf_name)
    write_tsv(results, args.output)

    print(f"Wrote {len(results)} rows to {args.output}")
    for row in results[:10]:
        print(
            f"{row.pdf_name}: peak={row.peak_mass:.3f} GeV, "
            f"MH={row.mh:.3f} GeV, best_mean={row.best_mean_value:.3f} GeV"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
