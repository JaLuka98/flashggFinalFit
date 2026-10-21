#!/usr/bin/env python3
"""
Add the Higgs branching-ratio uncertainties (LHC HXSWG YR4 partial widths) to a datacard,
with the names used in the HIG-26-007 combination:

    HiggsDecayWidthTHU_<decay>   one lnN per partial-width theory uncertainty
    param_alphaS, param_mq       parametric uncertainties (alpha_s; quark masses mb, mc, mt)

The effect on the measured channel X (hgg or hzz) is propagated through the total width:

    BR_X = Gamma_X / Gamma_tot  ->  kappa = (1 + delta_X) / (1 + sum_d BR_d delta_d)

using combine's tables HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/br/{BR4,
WidthUncertainties_125GeV_YR4}.txt at the given mH. These reproduce the rows in the
prepared cards of 2026-08 except for two fixes:
  - own-channel term: (1 + u_X)/(1 + BR_X u_X), e.g. hgg 1.00998 (cards had 1 + BR_X u_X = 1.0023)
  - param_mq: mb, mc, mt shifts added in quadrature with their physical sign (heavier quarks
    lower BR(gg) and BR(ZZ) alike), so the nuisance is correlated between the channels.

Example:
  python3 addBranchingRatioUncertainties.py --datacard card.txt --channel hgg --output new.txt
"""

import argparse
import os
import re
import sys

import numpy as np

DEFAULT_BR_DIR = os.path.join(os.environ.get("CMSSW_BASE", ""), "src/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/br")
# decays with a THU nuisance in the combination (name suffix -> YR4 table key)
THU_DECAYS = {"hbb": "hbb", "hcc": "hcc", "hgluglu": "hgluglu", "htautau": "htt", "hww": "hww", "hzz": "hzz", "hgg": "hgg"}
# HiggsDecayWidthTHU_hgg is only written for the hgg channel, like in the existing cards
CHANNEL_EXTRA = {"hgg": ["hgg"], "hzz": []}
DEFAULT_SIGNAL = {"hgg": r"^(ggh|vbf|vh|tth)_.*_hgg$", "hzz": r"^(smH_.*|OutsideAcceptance|nonResH)$"}


def get_options():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datacard", required=True)
    p.add_argument("--channel", required=True, choices=["hgg", "hzz"])
    p.add_argument("--mass", type=float, default=125.07)
    p.add_argument("--br-dir", default=DEFAULT_BR_DIR)
    p.add_argument("--signal-regex", default=None, help="processes that get the rows (default per channel)")
    p.add_argument("--output", default=None, help="write the card here (otherwise only print the values)")
    return p.parse_args()


def load_tables(br_dir, mass):
    path = os.path.join(br_dir, "BR4.txt")
    with open(path) as f:
        cols = f.readline().split()[1:]
        rows = np.array([[float(x) for x in l.split()[: len(cols) + 1]] for l in f if l.strip()])
    br = {c: float(np.interp(mass, rows[:, 0], rows[:, i + 1])) for i, c in enumerate(cols) if c != "Total_Width_GeV"}
    unc = {}
    with open(os.path.join(br_dir, "WidthUncertainties_125GeV_YR4.txt")) as f:
        keys = f.readline().split()[1:]
        for l in f:
            t = l.split()
            if t:
                unc[t[0]] = {k: 0.01 * float(v) for k, v in zip(keys, t[1:])}
    return br, unc


def kappa(br, channel, deltas):
    return (1 + deltas.get(channel, 0.0)) / (1 + sum(br[d] * x for d, x in deltas.items()))


def compute_rows(br, unc, channel):
    rows = {}
    for name, d in THU_DECAYS.items():
        if name == "hgg" and "hgg" not in CHANNEL_EXTRA[channel]:
            continue  # BR(gg) x 1% is negligible for H->ZZ, and the H4l cards have no such row
        rows[f"HiggsDecayWidthTHU_{name}"] = f"{kappa(br, channel, {d: unc[d]['thu']}):.5f}"
    up = kappa(br, channel, {d: u["alphaS"] for d, u in unc.items()})
    dn = kappa(br, channel, {d: -u["alphaS"] for d, u in unc.items()})
    rows["param_alphaS"] = f"{dn:.4f}/{up:.4f}"
    # independent quark-mass parameters: quadrature sum, keeping the common physical sign
    q = {}
    for direction, sgn in (("up", 1), ("dn", -1)):
        s = np.array([kappa(br, channel, {d: sgn * u[k] for d, u in unc.items()}) - 1 for k in ("mB", "mC", "mt")])
        q[direction] = 1 + np.sign(s.sum()) * np.sqrt(np.sum(s ** 2))
    rows["param_mq"] = f"{q['dn']:.4f}/{q['up']:.4f}"
    return rows


def main():
    opt = get_options()
    br, unc = load_tables(opt.br_dir, opt.mass)
    rows = compute_rows(br, unc, opt.channel)
    print(f"{opt.channel} at mH = {opt.mass} (BR_{opt.channel} = {br[opt.channel]:.5f}):")
    for n, v in rows.items():
        print(f"  {n:28s} {v}")
    if not opt.output:
        return
    with open(opt.datacard) as f:
        lines = f.readlines()
    procs = next(l.split()[1:] for l in lines if l.split() and l.split()[0] == "process" and not re.match(r"^-?\d+$", l.split()[1]))
    rx = re.compile(opt.signal_regex or DEFAULT_SIGNAL[opt.channel])
    is_sig = [bool(rx.match(p)) for p in procs]
    if not any(is_sig):
        sys.exit(f"[ERROR] no signal processes match {rx.pattern}")
    n_added = len(set(rows) - {l.split()[0] for l in lines if l.split()})
    kept = [l for l in lines if not (l.split() and l.split()[0] in rows)]
    for i, l in enumerate(kept):  # keep a numeric kmax consistent with the added rows
        t = l.split()
        if len(t) > 1 and t[0] == "kmax" and t[1].isdigit():
            kept[i] = l.replace(t[1], str(int(t[1]) + n_added), 1)
            break
    last = max(i for i, l in enumerate(kept) if len(l.split()) > 1 and l.split()[1] == "lnN")
    new = [f"{n:<50s}  lnN    {' '.join(v if s else '-' for s in is_sig)}\n" for n, v in rows.items()]
    with open(opt.output, "w") as f:
        f.writelines(kept[: last + 1] + new + kept[last + 1:])
    print(f"Wrote {opt.output}: {len(new)} rows on {sum(is_sig)} of {len(procs)} columns")


if __name__ == "__main__":
    main()
