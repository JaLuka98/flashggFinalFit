#!/usr/bin/env python3
"""
Rescale the signal of a datacard made with the YR4 cross sections to the LHCHWG Report 5 (R5) cross sections.

The signal normalisation in the workspace is XS * BR * eff * acc (Signal/tools/finalModel.py), with XS the constant
'factor' of the Run3FidXSAnalysis entries in commonTools/XSBRMap.py, and the datacard rate (the luminosity) multiplies
it. Multiplying the rate of every signal process by R5/YR4 of its production mode therefore gives the same yields as
remaking the datacard with the R5 XSBRMap, at every mH. The BR is the same in YR4 and R5.

Processes are matched by the production-mode prefix of their name (ggh_..., vbf_..., vh_..., tth_..., bbh_...,
wh_..., zh_...). Background and any other process (e.g. uuH) are left unchanged and listed.

Example:
    python3 Combine/scale_datacard_to_r5.py Datacard_PTH_2022_2023_2024.txt
    -> Datacard_PTH_2022_2023_2024_R5.txt next to the input; then run text2workspace.py on it as usual.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

# Cross sections in pb at 13.6 TeV, mH = 125.38 GeV.
# YR4: the values the old datacards were made with (ad-interim 13.6 TeV extrapolation of YR4, arXiv:2402.09955,
#      as in the previous commonTools/XSBRMap.py).
# R5:  LHCHWG Report 5, R5 v1.1.3 (https://gitlab.cern.ch/LHCHIGGSXS/LHCHXSWG1/crosssections, R5/), as in the current
#      commonTools/XSBRMap.py. VH = WH + ZH (ZH includes gg->ZH).
XS_YR4 = {"ggh": 51.96, "vbf": 4.067, "vh": 2.3781, "wh": 1.442, "zh": 0.9361, "tth": 0.5638, "bbh": 0.52218}
XS_R5 = {"ggh": 51.45, "vbf": 4.099837482, "vh": 2.39399, "wh": 1.45344, "zh": 0.94055, "tth": 0.5888, "bbh": 0.563}
RATIO = {mode: XS_R5[mode] / XS_YR4[mode] for mode in XS_YR4}

MARKER = "# Signal rates scaled from YR4 to LHCHWG Report 5 (R5 v1.1.3) cross sections by scale_datacard_to_r5.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scale the signal rates of a YR4 datacard to the R5 cross sections.")
    parser.add_argument("datacard", nargs="?", help="Input text datacard (made with the YR4 cross sections).")
    parser.add_argument("-o", "--output", help="Output datacard (default: <input>_R5.txt next to the input).")
    parser.add_argument("--dry-run", action="store_true", help="Only print what would be scaled.")
    parser.add_argument("--force", action="store_true", help="Scale even if the datacard was already scaled.")
    parser.add_argument("--print-ratios", action="store_true", help="Print the R5/YR4 ratios and exit.")
    return parser.parse_args()


def production_mode(process: str):
    prefix = process.split("_")[0].lower()
    return prefix if prefix in RATIO else None


def rewrite_tokens(line: str, new_tokens: list) -> str:
    """Replace the whitespace-separated tokens of a line, keeping each column's width where possible."""
    parts = list(re.finditer(r"(\S+)(\s*)", line))
    out = line[: parts[0].start()] if parts else ""
    for i, (m, tok) in enumerate(zip(parts, new_tokens)):
        width = len(m.group(1)) + len(m.group(2))
        if i == len(parts) - 1:
            out += tok + m.group(2)
        else:
            out += tok + " " * max(1, width - len(tok))
    return out


def main() -> int:
    args = parse_args()
    if args.print_ratios:
        for mode in RATIO:
            print(f"{mode:4s} YR4 {XS_YR4[mode]:<12g} R5 {XS_R5[mode]:<12g} R5/YR4 = {RATIO[mode]:.6f}")
        return 0
    if not args.datacard:
        sys.exit("give a datacard (or --print-ratios)")

    lines = open(args.datacard).read().split("\n")
    if any(l.startswith(MARKER) for l in lines) and not args.force:
        sys.exit(f"{args.datacard} was already scaled to R5 (use --force to scale it again)")

    # The process line with names is the first 'process' line after the observation; the rate line follows it.
    proc_idx = next(i for i, l in enumerate(lines) if l.split()[:1] == ["process"] and not l.split()[1].lstrip("-").isdigit())
    rate_idx = next(i for i, l in enumerate(lines) if l.split()[:1] == ["rate"])
    processes = lines[proc_idx].split()[1:]
    rates = lines[rate_idx].split()[1:]
    if len(processes) != len(rates):
        sys.exit(f"process ({len(processes)}) and rate ({len(rates)}) lines have different lengths")

    new_rates, scaled, untouched = [], {}, {}
    for proc, rate in zip(processes, rates):
        mode = production_mode(proc)
        if mode is None:
            untouched[proc.split("_")[0]] = untouched.get(proc.split("_")[0], 0) + 1
            new_rates.append(rate)
            continue
        if float(rate) < 0:
            sys.exit(f"rate {rate} of {proc}: the yield is taken from the workspace, cannot scale it here")
        new_rates.append(f"{float(rate) * RATIO[mode]:.10g}")
        scaled[mode] = scaled.get(mode, 0) + 1

    for mode, n in scaled.items():
        print(f"scaled   {mode:4s} x {RATIO[mode]:.6f}  ({n} columns)")
    for prefix, n in untouched.items():
        print(f"unchanged {prefix} ({n} columns)")
    if args.dry_run:
        return 0

    output = args.output or re.sub(r"(\.txt)?$", "_R5.txt", args.datacard, count=1)
    if os.path.abspath(output) == os.path.abspath(args.datacard):
        sys.exit("output would overwrite the input")
    lines[rate_idx] = rewrite_tokens(lines[rate_idx], ["rate"] + new_rates)

    # Relative shape paths are relative to the datacard: keep them pointing to the same files
    in_dir, out_dir = os.path.dirname(os.path.abspath(args.datacard)), os.path.dirname(os.path.abspath(output))
    if in_dir != out_dir:
        for i, l in enumerate(lines):
            tok = l.split()
            if tok[:1] == ["shapes"] and len(tok) > 3 and not os.path.isabs(tok[3]):
                tok[3] = os.path.relpath(os.path.join(in_dir, tok[3]), out_dir)
                lines[i] = rewrite_tokens(l, tok)

    summary = ", ".join(f"{mode} x{RATIO[mode]:.6f}" for mode in scaled)
    lines.insert(0, f"{MARKER}: {summary}")
    open(output, "w").write("\n".join(lines))
    print(f"written {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
