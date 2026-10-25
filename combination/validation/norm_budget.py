"""Signal normalisation budget of a per-bin-out Hgg card vs the HIG-26-007 card of the same production.

Sums the signal normalisations at MH=125.07 of the Models_* folders next to each card, separately for the
in- and out-processes, per production mode. The per-bin-out card splits the single out process of
HIG-26-007 into one out per gen bin; the pieces below the pruning threshold are dropped (SignalPruneList),
so the out yield of the new card is smaller. This prints how much, as a fraction of the total signal.

usage: norm_budget.py <new card> <HIG-26-007 card>
"""
import collections
import glob
import os
import re
import sys

import ROOT

ROOT.gErrorIgnoreLevel = ROOT.kError
NORM = re.compile(r"^hggpdfsmrel_(?P<proc>.+?)_(?P<cat>RECO_.+?_cat\w+?)_13TeV_norm$")


def norms(card):
    out = {}
    for f in glob.glob(os.path.dirname(os.path.abspath(card)) + "/Models_*/signal/*.root"):
        tf = ROOT.TFile.Open(f)
        w = tf.Get("wsig_13TeV")
        w.var("MH").setVal(125.07)
        for o in w.allFunctions():
            m = NORM.match(o.GetName())
            if m:
                out[(m["proc"], m["cat"])] = o.getVal()
        tf.Close()
    return out


def budget(n):
    s = collections.Counter()
    for (proc, _), v in n.items():
        prod = proc.split("_")[0]
        kind = "out" if "_out_" in proc else "in"
        s[kind] += v
        s[(prod, kind)] += v
    return s


new, ref = budget(norms(sys.argv[1])), budget(norms(sys.argv[2]))
total = ref["in"] + ref["out"]
print(f"{'':10s} {'in':>10s} {'out':>10s}   out/total")
for tag, s in (("new", new), ("HIG-26-007", ref)):
    print(f"{tag:10s} {s['in']:10.4g} {s['out']:10.4g}   {100 * s['out'] / (s['in'] + s['out']):.2f}%")
print(f"out missing in the new card: {100 * (ref['out'] - new['out']) / total:+.2f}% of the total signal "
      f"(in differs by {100 * (ref['in'] - new['in']) / total:+.3f}%)")
for prod in sorted({k[0] for k in ref if isinstance(k, tuple)}):
    r, n = ref[(prod, "out")], new[(prod, "out")]
    print(f"    {prod:4s} out: new {n:.4g} vs {r:.4g} ({100 * (n - r) / max(r, 1e-12):+.1f}%)")
