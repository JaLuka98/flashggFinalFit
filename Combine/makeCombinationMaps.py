#!/usr/bin/env python3
"""
Build and verify the multiSignalModel POI maps for the Hgg+H4l combination (total-XS
extrapolation) from a combined card made with `combineCards.py hgg=<card> h4l=<card>`.

Per POI (gen bin) three anchored patterns, matched on "<bin>/<process>" like multiSignalModel:
  hgg_<bin>/(ggh|vbf|vh|tth)_<VAR>_<label>_(in|out)_<era>_hgg     in and per-bin out processes
  h4l_<bin>/smH_<prod>_<H4L VAR>[_zzfloating]_<h4l label>          H4l signal
  h4l_hzz_<H4L VAR>[_zzfloating]_<h4l label>_cat.../OutsideAcceptance
H4l labels are translated to the Hgg POI labels (e.g. GT450 -> 450p0_10000p0).

Verification: every signal (bin, process) is matched by exactly one pattern and no background
by any. Signal processes that cannot be mapped (e.g. a single full-range Hgg out process of a
fiducial-style card) make the script fail instead of silently staying at SM.

Example:
  python3 makeCombinationMaps.py --card Datacard_hgg_h4l_PTJ0.txt --obs PTJ0 \
      --output t2w_PTJ0.sh --workspace workspace_hgg_h4l_PTJ0.root
"""

import argparse
import re
import shlex
import sys

# obs -> (Hgg variable label, H4l variable label, Hgg bins, H4l -> Hgg label translation, POI range)
OBS = {
    "inclusive": (None, "mass4l", None, {}, (0, 3)),
    "PTH": ("PTH", "PTH", ["0p0_5p0", "5p0_10p0", "10p0_15p0", "15p0_20p0", "20p0_25p0", "25p0_30p0", "30p0_35p0",
                           "35p0_45p0", "45p0_60p0", "60p0_80p0", "80p0_100p0", "100p0_120p0", "120p0_140p0",
                           "140p0_170p0", "170p0_200p0", "200p0_250p0", "250p0_350p0", "350p0_450p0", "450p0_10000p0"],
            {"GT450": "450p0_10000p0"}, (0, 2)),
    "rapidity": ("YH", "YH", ["0p0_0p15", "0p15_0p3", "0p3_0p45", "0p45_0p6", "0p6_0p75", "0p75_0p9", "0p9_1p2",
                              "1p2_1p6", "1p6_2p0", "2p0_2p5"], {}, (0, 3)),
    "NJ": ("NJ", "Nj_2p5", ["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_4p0", "4p0_100p0"], {"4p0_20p0": "4p0_100p0"}, (0, 3)),
    "PTJ0": ("PTJ0", "pTj1_2p5", ["m10000p0_30p0", "30p0_40p0", "40p0_55p0", "55p0_75p0", "75p0_95p0", "95p0_120p0",
                                  "120p0_150p0", "150p0_200p0", "200p0_10000p0"],
             {"m100p0_30p0": "m10000p0_30p0", "GT200": "200p0_10000p0"}, (0, 3)),
    "MassJ0J1": ("MassJ0J1", "mjj_4p7", ["m10000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0",
                                         "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"],
                 {"m100p0_0p0": "m10000p0_0p0", "GT1000": "1000p0_10000p0"}, (0, 3)),
}
BACKGROUND = re.compile(r"^(bkg_.*|nonResH)$")


def get_options():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--card", required=True, help="combined card (channels named hgg and h4l), or a single-channel card with --channels")
    p.add_argument("--obs", required=True, choices=OBS)
    p.add_argument("--output", default=None, help="write the text2workspace command here")
    p.add_argument("--workspace", default=None, help="output workspace name in the command")
    p.add_argument("--mass", default="125.07")
    p.add_argument("--channels", default="hgg,h4l", help="channels the card must contain (e.g. h4l for an H4l-only card)")
    return p.parse_args()


def columns(card):
    """(bin, process) per column: the 'bin' line with one entry per process column."""
    with open(card) as f:
        split = [l.split() for l in f if l.split()]
    procs = next(t[1:] for t in split if t[0] == "process" and not re.match(r"^-?\d+$", t[1]))
    bins = next(t[1:] for t in split if t[0] == "bin" and len(t) - 1 == len(procs))
    return list(zip(bins, procs))


def patterns(obs):
    hvar, zvar, hbins, trans, (lo, hi) = OBS[obs]
    zfl = "(_zzfloating)?"
    maps = []  # (poi, pattern)
    if obs == "inclusive":
        maps += [("r", r"^hgg_.*/(ggh|vbf|vh|tth)_(in|out)_.*_hgg$"),
                 ("r", rf"^h4l_.*/smH_[A-Za-z]+_{zvar}{zfl}_105p0_160p0$"),
                 ("r", r"^h4l_.*/OutsideAcceptance$")]
        return maps, {"r": (lo, hi)}
    inverse = {}
    for h4l_label, hgg_label in trans.items():
        inverse.setdefault(hgg_label, []).append(h4l_label)
    for b in hbins:
        poi = f"r_{hvar}_{b}"
        zlabels = "|".join(re.escape(x) for x in inverse.get(b, [b]))
        maps += [(poi, rf"^hgg_.*/(ggh|vbf|vh|tth)_{hvar}_{re.escape(b)}_(in|out)_.*_hgg$"),
                 (poi, rf"^h4l_.*/smH_[A-Za-z]+_{zvar}{zfl}_({zlabels})$"),
                 (poi, rf"^h4l_hzz_{zvar}{zfl}_({zlabels})_cat.*/OutsideAcceptance$")]
    return maps, {f"r_{hvar}_{b}": (lo, hi) for b in hbins}


def is_signal(bin_, proc):
    if BACKGROUND.match(proc):
        return False
    if bin_.startswith("hgg_"):
        return proc.endswith("_hgg") and not proc.startswith("bkg")
    return proc.startswith("smH_") or proc == "OutsideAcceptance"


def main():
    opt = get_options()
    cols = columns(opt.card)
    maps, ranges = patterns(opt.obs)
    compiled = [(poi, pat, re.compile(pat)) for poi, pat in maps]
    unique = sorted(set(cols))
    problems, counts = [], {}
    for b, p in unique:
        hits = [poi for poi, _, rx in compiled if rx.match(f"{b}/{p}")]
        if is_signal(b, p):
            if len(hits) != 1:
                problems.append(f"signal {b}/{p}: matched {len(hits)} times {hits}")
            else:
                key = (hits[0], "hgg" if b.startswith("hgg_") else ("h4l OA" if p == "OutsideAcceptance" else "h4l smH"))
                counts[key] = counts.get(key, 0) + 1
        elif hits:
            problems.append(f"background {b}/{p} matched by {hits}")
    channels = opt.channels.split(",")
    kinds = (["hgg"] if "hgg" in channels else []) + (["h4l smH", "h4l OA"] if "h4l" in channels else [])
    for poi in ranges:
        for kind in kinds:
            if (poi, kind) not in counts:
                problems.append(f"POI {poi}: no {kind} entries mapped")
    print(f"{opt.card}: {len(unique)} (bin, process) pairs, {len(ranges)} POIs")
    for poi in ranges:
        print(f"  {poi:26s} hgg {counts.get((poi, 'hgg'), 0):4d}   h4l smH {counts.get((poi, 'h4l smH'), 0):4d}   h4l OutsideAcceptance {counts.get((poi, 'h4l OA'), 0):3d}")
    if problems:
        print(f"[ERROR] {len(problems)} mapping problems, e.g.:\n  " + "\n  ".join(problems[:15]))
        sys.exit(1)
    print("MAPPING OK: every signal process mapped exactly once, no background mapped")

    if opt.output:
        declared, pos = set(), []
        for poi, pat in maps:
            spec = poi if poi in declared else f"{poi}[1,{ranges[poi][0]},{ranges[poi][1]}]"
            declared.add(poi)
            pos.append(f"--PO {shlex.quote(f'map={pat}:{spec}')}")
        ws = opt.workspace or re.sub(r"\.txt$", ".root", opt.card)
        # No higgsMassRange: MH stays a fixed parameter at -m instead of a second POI. With MH as
        # the first POI, combine applies --rMin/--rMax (used by the FinalFits unblinded fits) to MH,
        # which pushes MH far off the BR(gg) spline and makes every Hgg signal yield NaN.
        cmd = (f"text2workspace.py {shlex.quote(opt.card)} -o {shlex.quote(ws)} -m {opt.mass} \\\n"
               f"  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \\\n  "
               + " \\\n  ".join(pos) + "\n")
        with open(opt.output, "w") as f:
            f.write("#!/bin/bash\n# generated by makeCombinationMaps.py\n" + cmd)
        print(f"wrote {opt.output}")


if __name__ == "__main__":
    main()
