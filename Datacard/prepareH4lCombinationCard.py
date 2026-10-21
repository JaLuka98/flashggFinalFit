#!/usr/bin/env python3
"""
Prepare an H4l datacard for the Hgg+H4l combination, i.e. the steps of
`law run NuisanceHandling --remove-parameters BR_hzz4e,BR_hzz2e2mu,BR_hzz4mu --do-merge-pileup`
plus the BR rows of add_nuisances.txt:

  1. remove BR_hzz4e, BR_hzz4mu, BR_hzz2e2mu
  2. merge the per-era CMS_pileup_<era> rows into one CMS_pileup row (they act on disjoint
     columns; this correlates pileup across eras and with the Hgg CMS_pileup)
  3. add HiggsDecayWidthTHU_* , param_alphaS, param_mq (addBranchingRatioUncertainties.py,
     channel hzz) on the smH_* and OutsideAcceptance processes
  4. keep kmax consistent

The output is written next to the input card, so relative shape paths stay valid.

Example:
  python3 prepareH4lCombinationCard.py --datacard hzz4l_all_13TeV_xs_pT4l_zzfloating_bin_v3.txt \
      --output hzz4l_all_13TeV_xs_pT4l_zzfloating_bin_v3_comb.txt
"""

import argparse
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REMOVE = ["BR_hzz4e", "BR_hzz4mu", "BR_hzz2e2mu"]
PILEUP = re.compile(r"^CMS_pileup_\w+$")
SIGNAL = re.compile(r"^(smH_.*|OutsideAcceptance)$")


def load_br_module():
    spec = importlib.util.spec_from_file_location("br", os.path.join(HERE, "addBranchingRatioUncertainties.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_options():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datacard", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--mass", type=float, default=125.07)
    p.add_argument("--br-dir", default=None, help="combine lhc-hxswg/sm/br directory (default: $CMSSW_BASE)")
    return p.parse_args()


def main():
    opt = get_options()
    br = load_br_module()
    with open(opt.datacard) as f:
        lines = f.readlines()
    split = [l.split() for l in lines]
    procs = next(t[1:] for t in split if t and t[0] == "process" and not re.match(r"^-?\d+$", t[1]))
    names = {t[0] for t in split if t}

    missing = [n for n in REMOVE if n not in names]
    if missing:
        sys.exit(f"[ERROR] expected rows not found: {missing}")
    if any(n.startswith(("HiggsDecayWidthTHU_", "param_")) for n in names):
        sys.exit("[ERROR] card already has BR rows; is it prepared already?")

    # merge pileup
    pileup_rows = [t for t in split if t and PILEUP.match(t[0]) and len(t) > 2 and t[1] == "lnN"]
    if not pileup_rows:
        sys.exit("[ERROR] no CMS_pileup_<era> rows")
    merged = ["-"] * len(procs)
    for t in pileup_rows:
        for i, v in enumerate(t[2:]):
            if v != "-":
                if merged[i] != "-":
                    sys.exit(f"[ERROR] pileup rows overlap in column {procs[i]}")
                merged[i] = v

    # BR rows
    br_tables = br.load_tables(opt.br_dir or br.DEFAULT_BR_DIR, opt.mass)
    rows = br.compute_rows(*br_tables, "hzz")
    is_sig = [bool(SIGNAL.match(p)) for p in procs]

    drop = set(REMOVE) | {t[0] for t in pileup_rows}
    kept = [l for l in lines if not (l.split() and l.split()[0] in drop)]
    new = [f"{'CMS_pileup':<50s}  lnN    {' '.join(merged)}\n"]
    new += [f"{n:<50s}  lnN    {' '.join(v if s else '-' for s in is_sig)}\n" for n, v in rows.items()]
    n_delta = len(new) - len(drop)
    for i, l in enumerate(kept):
        t = l.split()
        if len(t) > 1 and t[0] == "kmax" and t[1].isdigit():
            kept[i] = l.replace(t[1], str(int(t[1]) + n_delta), 1)
            break
    last = max(i for i, l in enumerate(kept) if len(l.split()) > 1 and l.split()[1] == "lnN")
    with open(opt.output, "w") as f:
        f.writelines(kept[: last + 1] + new + kept[last + 1:])
    print(f"{os.path.basename(opt.output)}: removed {sorted(drop)}, merged {len(pileup_rows)} pileup rows, "
          f"added {len(rows)} BR rows on {sum(is_sig)}/{len(procs)} columns, kmax {n_delta:+d}")


if __name__ == "__main__":
    main()
