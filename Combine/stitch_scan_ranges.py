#!/usr/bin/env python3
"""Stitch consecutive MultiDimFit grid scans into one likelihood curve.

Each scan range is normalized by Combine to the best fit inside that range.
This script restores a common normalization by matching consecutive segments
at their shared boundary, drops unreadable point files, and writes the minimal
``limit`` tree understood by ``plot1DScan.py``.
"""

import argparse
from array import array
from pathlib import Path

import ROOT


ROOT.gROOT.SetBatch(True)


def read_segment(paths, poi):
    points = {}
    best_fits = []
    invalid = []

    for path in paths:
        root_file = ROOT.TFile.Open(str(path))
        tree = None if not root_file or root_file.IsZombie() else root_file.Get("limit")
        if not tree or not tree.GetLeaf(poi) or not tree.GetLeaf("deltaNLL"):
            invalid.append(str(path))
            if root_file:
                root_file.Close()
            continue

        quantile_leaf = tree.GetLeaf("quantileExpected")
        for entry in range(tree.GetEntries()):
            tree.GetEntry(entry)
            x_value = float(tree.GetLeaf(poi).GetValue())
            twice_delta_nll = 2.0 * float(tree.GetLeaf("deltaNLL").GetValue())
            quantile = float(quantile_leaf.GetValue()) if quantile_leaf else 1.0
            if quantile > -0.5:
                points.setdefault(round(x_value, 8), []).append(twice_delta_nll)
            else:
                best_fits.append((x_value, twice_delta_nll))
        root_file.Close()

    averaged = sorted((x, sum(values) / len(values)) for x, values in points.items())
    if len(averaged) < 2:
        raise RuntimeError("scan segment contains fewer than two valid grid points")
    return averaged, best_fits, invalid


def interpolate(points, x_value):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= x_value <= x1:
            if x1 == x0:
                return 0.5 * (y0 + y1)
            fraction = (x_value - x0) / (x1 - x0)
            return y0 + fraction * (y1 - y0)
    raise RuntimeError(
        f"cannot interpolate at boundary {x_value:g}; available range is "
        f"[{points[0][0]:g}, {points[-1][0]:g}]"
    )


def stitch(segments):
    stitched = list(segments[0])
    offsets = [0.0]
    for segment in segments[1:]:
        boundary = segment[0][0]
        offset = interpolate(stitched, boundary) - segment[0][1]
        shifted = [(x, y + offset) for x, y in segment]
        stitched.extend((x, y) for x, y in shifted if x > boundary + 1.0e-7)
        stitched.sort()
        offsets.append(offset)
    return stitched, offsets


def crossings(points, level=1.0):
    result = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if y0 == y1 or (y0 - level) * (y1 - level) > 0.0:
            continue
        result.append(x0 + (level - y0) * (x1 - x0) / (y1 - y0))
    return result


def write_tree(output, poi, points, best_fit):
    output.parent.mkdir(parents=True, exist_ok=True)
    root_file = ROOT.TFile(str(output), "RECREATE")
    tree = ROOT.TTree("limit", "limit")

    poi_value = array("f", [0.0])
    delta_nll = array("f", [0.0])
    quantile = array("f", [0.0])
    limit = array("d", [0.0])
    tree.Branch(poi, poi_value, f"{poi}/F")
    tree.Branch("deltaNLL", delta_nll, "deltaNLL/F")
    tree.Branch("quantileExpected", quantile, "quantileExpected/F")
    tree.Branch("limit", limit, "limit/D")

    poi_value[0] = best_fit[0]
    delta_nll[0] = 0.0
    quantile[0] = -1.0
    tree.Fill()

    for x_value, twice_delta_nll in points:
        poi_value[0] = x_value
        delta_nll[0] = 0.5 * twice_delta_nll
        quantile[0] = 1.0
        tree.Fill()

    tree.Write()
    root_file.Close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--poi", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--segment",
        action="append",
        nargs="+",
        type=Path,
        required=True,
        help="ordered list of ROOT files for one scan range; repeat per range",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    segments = []
    first_best_fits = []
    invalid = []
    for index, paths in enumerate(args.segment):
        points, best_fits, bad_paths = read_segment(paths, args.poi)
        segments.append(points)
        if index == 0:
            first_best_fits = best_fits
        invalid.extend(bad_paths)

    stitched, offsets = stitch(segments)
    best_fit = min(first_best_fits, key=lambda item: item[1]) if first_best_fits else min(
        stitched, key=lambda item: item[1]
    )
    write_tree(args.output, args.poi, stitched, best_fit)

    print(f"wrote {args.output} with {len(stitched)} grid points")
    print("segment offsets in -2DeltaLnL:", ", ".join(f"{value:.8g}" for value in offsets))
    print("1 sigma crossings:", ", ".join(f"{value:.8g}" for value in crossings(stitched)))
    if invalid:
        print(f"skipped {len(invalid)} invalid input files")
        for path in invalid:
            print(f"  {path}")


if __name__ == "__main__":
    main()
