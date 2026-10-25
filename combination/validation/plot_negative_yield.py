"""Why the H4l likelihood stops at negative signal strength: the expected m4l distribution per category.

For the reco categories of one H4l bin, the expected events per m4l bin from the workspace
(model at its nominal values): background (ZZ, Z+jets, non-resonant H), the signal of the scanned gen bin
(scaled by r) and the signal migrating from the other gen bins (r = 1). The total is drawn for several r:
where it drops below zero (at the peak, where the signal dominates), the likelihood is not defined.

usage: plot_negative_yield.py <workspace> <reco bin label, e.g. YH_zzfloating_2p0_2p5> <gen bin, e.g. 2p0_2p5> <out.png>
"""
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import ROOT  # noqa: E402

ROOT.gErrorIgnoreLevel = ROOT.kError
ws_path, reco, gen, out = sys.argv[1:5]
R_VALUES = (1.0, 0.0, -0.2, -0.5)

f = ROOT.TFile.Open(ws_path)
w = f.Get("w")
x = w.var("ZZMass")
nb, lo, hi = x.getBins(), x.getMin(), x.getMax()
edges = np.linspace(lo, hi, nb + 1)
centers = 0.5 * (edges[1:] + edges[:-1])

cats = sorted({m.group(1) for o in w.allFunctions()
               for m in [re.match(rf"^n_exp_binh4l_hzz_{reco}_(cat\w+?)_proc_", o.GetName())] if m})


def expected(cat):
    """per m4l bin: background, signal of the scanned gen bin, signal of the other gen bins"""
    b = f"h4l_hzz_{reco}_{cat}"
    parts = {"bkg": np.zeros(nb), "sig": np.zeros(nb), "other": np.zeros(nb)}
    for o in w.allFunctions():
        m = re.match(rf"^n_exp_(?:final_)?bin{re.escape(b)}_proc_(.+)$", o.GetName())
        if not m:
            continue
        proc = m.group(1)
        pdf = None
        for name in (f"shapeSig_{proc}_{b}_morph", f"shapeSig_{proc}_{b}", f"shapeBkg_{proc}_{b}_morph",
                     f"shapeBkg_{proc}_{b}", f"shape_{proc}_{b}"):
            pdf = w.pdf(name)
            if pdf:
                break
        if not pdf:
            raise RuntimeError(f"no pdf for {proc} in {b}")
        norm = o.getVal()  # card rate; parametric shapes carry their own normalisation (<pdf>__norm)
        shape_norm = w.function(f"{pdf.GetName()}__norm")
        if shape_norm:
            norm *= shape_norm.getVal()
        nset = ROOT.RooArgSet(x)
        dens = []
        for c in centers:
            x.setVal(c)
            dens.append(pdf.getVal(nset))
        dens = np.array(dens) * (hi - lo) / nb * norm
        if proc.startswith("bkg_") or proc == "nonResH":
            parts["bkg"] += dens
        elif proc == "OutsideAcceptance" or proc.endswith(f"_{gen}"):
            parts["sig"] += dens
        else:
            parts["other"] += dens
    return parts


data = {c: expected(c) for c in cats}
# the categories with the largest signal / background at the peak (where the total turns negative first)
def peak_ratio(p):
    i = int(np.argmax(p["sig"]))
    return p["sig"][i] / max(p["bkg"][i] + p["other"][i], 1e-9)


shown = sorted(cats, key=lambda c: -peak_ratio(data[c]))[:5]
total = {k: sum(data[c][k] for c in cats) for k in ("bkg", "sig", "other")}

fig, axes = plt.subplots(2, 3, figsize=(16, 9.5), sharex=True)
colors = {1.0: "black", 0.0: "tab:blue", -0.2: "tab:orange", -0.5: "tab:red"}
for ax, (title, p) in zip(axes.flat, [(f"all {len(cats)} categories summed", total)] + [(c, data[c]) for c in shown]):
    ax.fill_between(centers, 0, p["bkg"], step="mid", color="lightgray", label="background (ZZ, Z+jets, non-res. H)")
    ax.fill_between(centers, p["bkg"], p["bkg"] + p["other"], step="mid", color="khaki", label="signal from other gen bins (r = 1)")
    for r in R_VALUES:
        tot = p["bkg"] + p["other"] + r * p["sig"]
        ax.step(centers, tot, where="mid", color=colors[r], lw=1.6, label=f"total, r = {r:g}")
        neg = tot < 0
        if neg.any():
            ax.fill_between(centers, tot, 0, where=neg, step="mid", color=colors[r], alpha=0.35)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title(title.replace("cat", "", 1) if title.startswith("cat") else title + f"   S/B at peak {peak_ratio(p):.1f}, negative below r = {-1 / max(peak_ratio(p), 1e-9):.2f}", fontsize=10)
    ax.set_xlim(110, 140)
    ax.set_ylabel("expected events / bin")
for ax in axes[-1]:
    ax.set_xlabel(r"$m_{4\ell}$ (GeV)")
axes.flat[0].legend(fontsize=8.5, loc="upper left")
fig.suptitle(f"H4l reco bin {reco.replace('_zzfloating', '')}: expected events for the scanned r of gen bin {gen} "
             f"(shaded: negative prediction, likelihood undefined)", fontsize=12)
fig.tight_layout()
fig.savefig(out, dpi=110)
print("wrote", out)
for c in cats:
    p = data[c]
    tot0 = p["bkg"] + p["other"]
    i = int(np.argmax(p["sig"]))
    wall = -tot0[i] / p["sig"][i] if p["sig"][i] > 0 else float("-inf")
    print(f"  {c:16s} peak bin: bkg+other {tot0[i]:.4f}, signal {p['sig'][i]:.4f} -> negative below r = {wall:.2f}")
