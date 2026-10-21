"""Layers 3 and 4: new per-bin-out Hgg card vs the HIG-26-007 card of the same production.

Layer 3, in-processes (same trees, reco categories and in-bins): per (category, process) the jet lnN
entries (CMS_scale_j_*, CMS_res_j_*) and the photon scale/smearing constants of the signal model must agree.
Layer 4, closure: per (category, production mode, era) the signal normalisation at MH=125.07 summed over
the per-bin outs must equal the single out process of the HIG-26-007 card, and the in-processes must agree.

usage: check_cards.py <new card> <HIG-26-007 card>   (Models_* folders next to the cards)
"""
import collections
import glob
import os
import re
import sys

import ROOT

ROOT.gErrorIgnoreLevel = ROOT.kError
new_card, ref_card = sys.argv[1:3]


def parse(card):
    L = [l.split() for l in open(card)]
    procs = next(t[1:] for t in L if t and t[0] == "process" and not re.match(r"^-?\d+$", t[1]))
    bins = next(t[1:] for t in L if t and t[0] == "bin" and len(t) - 1 == len(procs))
    jets = {}
    for t in L:
        if len(t) > 2 and t[1] == "lnN" and re.match(r"CMS_(scale|res)_j_", t[0]):
            for b, p, v in zip(bins, procs, t[2:]):
                if p.endswith("_hgg"):
                    jets[(t[0], re.sub(r"^.*?(RECO_)", r"\1", b), p)] = v
    shapes = [t for t in L if t and t[0] == "shapes"]
    return jets, shapes


CONST = re.compile(r"^const_(?P<proc>.+?)_(?P<cat>RECO_.+?_cat\w+?)_13TeV_(?P<par>mean|sigma|rate)_(?P<syst>.+)$")
NORM = re.compile(r"^hggpdfsmrel_(?P<proc>.+?)_(?P<cat>RECO_.+?_cat\w+?)_13TeV_norm$")


def models(card):
    consts, norms = {}, {}
    base = os.path.dirname(os.path.abspath(card))
    for f in glob.glob(f"{base}/Models_*/signal/*.root"):
        tf = ROOT.TFile.Open(f)
        w = tf.Get("wsig_13TeV")
        w.var("MH").setVal(125.07)
        for coll in (w.allVars(), w.allFunctions(), w.components()):  # photon constants are RooConstVars
            for o in coll:
                n = o.GetName()
                m = CONST.match(n)
                if m:
                    consts[(m["proc"], m["cat"], m["par"], m["syst"])] = o.getVal()
                m = NORM.match(n)
                if m:
                    norms[(m["proc"], m["cat"])] = o.getVal()
        tf.Close()
    return consts, norms


def close(a, b, rel=1e-4):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-12)


nj, _ = parse(new_card)
rj, _ = parse(ref_card)
nc, nn = models(new_card)
rc, rn = models(ref_card)

# layer 3: jet lnN entries of in-processes
common = [k for k in rj if "_in_" in k[2] and k in nj]
missing = [k for k in rj if "_in_" in k[2] and k not in nj]
diff = [k for k in common if nj[k] != rj[k]]
print(f"jet lnN (in-processes): {len(common)} common entries, {len(diff)} differ, {len(missing)} only in HIG-26-007 card")
for k in diff[:5]:
    print(f"    {k}: new {nj[k]} vs HIG-26-007 {rj[k]}")
present_new = sum(v != "-" for k, v in nj.items()) / max(1, len(nj))
present_ref = sum(v != "-" for k, v in rj.items()) / max(1, len(rj))
print(f"    (jet row, signal column) pairs with an entry, all eras: new {present_new:.0%}, HIG-26-007 {present_ref:.0%}")

# layer 3: photon constants of in-processes
ckeys = [k for k in rc if "_in_" in k[0] and k in nc]
cdiff = [k for k in ckeys if not close(nc[k], rc[k])]
if not rc:
    sys.exit("[ERROR] no photon constants found in the HIG-26-007 models")
print(f"photon constants (in-processes): {len(ckeys)} common, {len(cdiff)} differ, "
      f"{sum(1 for k in rc if '_in_' in k[0] and k not in nc)} only in HIG-26-007 models")
for k in cdiff[:5]:
    print(f"    {k}: new {nc[k]:.5g} vs HIG-26-007 {rc[k]:.5g}")
def capped_frac(consts, kind):
    sel = [(k, v) for k, v in consts.items() if f"_{kind}_" in k[0] and k[2] in ("mean", "sigma")]
    n = sum(1 for k, v in sel if (k[2] == "mean" and abs(v) >= 0.05) or (k[2] == "sigma" and abs(v) >= 0.5))
    return n / max(1, len(sel)), n, len(sel)


# The caps (0.05 mean / 0.5 sigma) are what empty systematic datasets produce; a few low-statistics
# processes reach them also in a correct production, so compare the capped fractions with HIG-26-007.
caps = {}
for kind in ("in", "out"):
    caps[kind] = (capped_frac(nc, kind), capped_frac(rc, kind))
    (fn, nn_, tn), (fr, nr, tr) = caps[kind]
    print(f"    {kind}-processes at the caps: new {nn_}/{tn} ({fn:.1%}), HIG-26-007 {nr}/{tr} ({fr:.1%})")
capped = caps["out"][0][0] > 2 * caps["out"][1][0] + 0.01 or caps["in"][0][0] > caps["in"][1][0] + 1e-9

# layer 4: normalisations, in-processes equal and sum of per-bin outs == single out
ikeys = [k for k in rn if "_in_" in k[0] and k in nn]
idiff = [k for k in ikeys if not close(nn[k], rn[k])]
print(f"in-process normalisations: {len(ikeys)} common, {len(idiff)} differ")
for k in idiff[:5]:
    print(f"    {k}: new {nn[k]:.6g} vs HIG-26-007 {rn[k]:.6g}")


def group(norms):
    g = collections.defaultdict(float)
    for (proc, cat), v in norms.items():
        m = re.match(r"^(?P<prod>[a-z]+)_\w+?_out_(?P<era>\w+?)$", proc)
        if m:
            g[(m["prod"], m["era"], cat)] += v
    return g


go, gr = group(nn), group(rn)
okeys = sorted(set(go) | set(gr))
odiff = [k for k in okeys if not close(go.get(k, 0.0), gr.get(k, 0.0), 1e-3)]
nouts = len({k[0] for k in nn if "_out_" in k[0]})
print(f"out closure: {len(okeys)} (prod, era, category) groups, sum of {nouts} per-bin out processes vs single out -> "
      f"{len(odiff)} differ by >0.1%")
for k in odiff[:5]:
    print(f"    {k}: per-bin sum {go.get(k, 0):.6g} vs single out {gr.get(k, 0):.6g}")
ok = not (diff or missing or cdiff or idiff or odiff or capped)
print("RESULT:", "ALL OK" if ok else "CHECK THE DIFFERENCES ABOVE")
