"""Observed and expected m4l distribution of one H4l reco bin, summed over its categories (flavours, years).

Panels: the expected events before the fit (model at its nominal values) with the data, the same at the
observed best fit (snapshot of a best-fit file, where the signal can be negative) and, for comparison,
a second reco bin before the fit. Yields: n_exp_final_bin<channel>_proc_<proc> (card rate x rateParams x
systematics), the pdf only for the shape in the fit range; n_exp_bin only where no n_exp_final exists (summing both
counts the process twice).

usage: plot_bin_data.py <workspace> <best-fit file with snapshot MultiDimFit> <reco bin, e.g. 2p0_2p5>
                        <comparison reco bin> <gen bin label of the scanned POI> <out.png>
"""
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import ROOT  # noqa: E402

ROOT.gErrorIgnoreLevel = ROOT.kError
ws_path, bestfit_path, reco, reco_cmp, poi, out = sys.argv[1:7]
WIDTH = 2.5  # GeV per bin


def yield_functions(w):
    """{channel: {process: n_exp function}}, one pass over the workspace (n_exp_final where it exists)"""
    out = {}
    for o in w.allFunctions():
        m = re.match(r"^n_exp(_final)?_bin(h4l_hzz_\w+?_cat\w+?)_proc_(.+)$", o.GetName())
        if m and (m.group(1) or m.group(3) not in out.get(m.group(2), {})):
            out.setdefault(m.group(2), {})[m.group(3)] = o
    return out


def expected(w, rb, edges):
    """expected events per m4l bin, summed over the channels of reco bin rb: ZZ, Z+jets, H (gen bin = rb), other H"""
    x = w.var("ZZMass")
    nset = ROOT.RooArgSet(x)
    fine = np.linspace(edges[0], edges[-1], 10 * (len(edges) - 1) + 1)
    fc = 0.5 * (fine[1:] + fine[:-1])
    parts = {k: np.zeros(len(edges) - 1) for k in ("ZZ", "Z+jets", "H", "H other")}
    if not hasattr(w, "_yields"):
        w._yields = yield_functions(w)
    for ch, norms in w._yields.items():
        if not re.search(rf"YH_zzfloating_{rb}_cat", ch):
            continue
        for proc, nfun in norms.items():
            pdf = next((w.pdf(n) for n in (f"shapeSig_{proc}_{ch}_morph", f"shapeSig_{proc}_{ch}",
                                            f"shapeBkg_{proc}_{ch}_morph", f"shapeBkg_{proc}_{ch}") if w.pdf(n)), None)
            if pdf is None:
                raise RuntimeError(f"no pdf for {proc} in {ch}")
            # the pdf gives only the shape in the fit range; the yield is the one of the likelihood (n_exp_final)
            n = nfun.getVal()
            dens = []
            for c in fc:
                x.setVal(c)
                dens.append(pdf.getVal(nset))
            dens = np.array(dens)
            per_bin = dens.reshape(len(edges) - 1, 10).sum(axis=1) / dens.sum() * n if dens.sum() > 0 else 0 * dens[:len(edges) - 1]
            if proc in ("bkg_qqzz", "bkg_ggzz"):
                parts["ZZ"] += per_bin
            elif proc == "bkg_zjets":
                parts["Z+jets"] += per_bin
            elif proc.endswith(f"_{rb}") or proc == "OutsideAcceptance":
                parts["H"] += per_bin
            else:
                parts["H other"] += per_bin
    return parts


def observed(w, rb, edges):
    d = w.data("data_obs")
    vals = []
    for i in range(d.numEntries()):
        a = d.get(i)
        if re.search(rf"YH_zzfloating_{rb}_cat", a.getCatLabel("CMS_channel")):
            vals += [a.getRealValue("ZZMass")] * int(round(d.weight()))
    return np.histogram(vals, bins=edges)[0], vals


def draw(ax, parts, obs, edges, title, total_label="total expected"):
    c = 0.5 * (edges[1:] + edges[:-1])
    bottom = np.zeros(len(c))
    for k, col in (("ZZ", "#7fb8e6"), ("Z+jets", "#5aa05a"), ("H other", "#f2c14e"), ("H", "#d9534f")):
        v = parts[k]
        pos = np.clip(v, 0, None)
        ax.bar(c, pos, WIDTH, bottom=bottom, color=col, label=f"{k}  ({v.sum():.2f})", align="center", lw=0)
        bottom = bottom + pos
        neg = np.clip(v, None, 0)
        if (neg < 0).any():
            ax.bar(c, neg, WIDTH, bottom=0, color=col, hatch="///", edgecolor="k", alpha=0.6, align="center", lw=0.3,
                   label=f"{k} < 0")
    tot = sum(parts.values())
    ax.step(edges, np.append(tot, tot[-1]), where="post", color="k", lw=1.6, label=f"{total_label}  ({tot.sum():.2f})")
    err = np.sqrt(obs)
    ax.errorbar(c[obs > 0], obs[obs > 0], yerr=err[obs > 0], fmt="o", color="k", ms=6, label=f"data  ({obs.sum()})")
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(125.07, color="gray", ls=":", lw=1)
    ax.set_title(title, fontsize=10.5)
    ax.set_xlabel(r"$m_{4\ell}$ (GeV)")
    ax.set_ylabel(f"events / {WIDTH:g} GeV")
    ax.legend(fontsize=8.5, loc="upper right")


f = ROOT.TFile.Open(ws_path)
w = f.Get("w")
x = w.var("ZZMass")
edges = np.arange(x.getMin(), x.getMax() + 1e-6, WIDTH)

pre = expected(w, reco, edges)
obs, vals = observed(w, reco, edges)
pre_cmp = expected(w, reco_cmp, edges)
obs_cmp, _ = observed(w, reco_cmp, edges)

fb = ROOT.TFile.Open(bestfit_path)
wb = fb.Get("w")
wb.loadSnapshot("MultiDimFit")
r_best = wb.var(poi).getVal()
zz = [v.GetName() + f" = {v.getVal():.2f}" for v in wb.allVars() if v.GetName().startswith("zz_norm_9")]
post = expected(wb, reco, edges)

fig, axes = plt.subplots(1, 3, figsize=(19, 6))
draw(axes[0], pre, obs, edges, f"reco |y| {reco.replace('p', '.').replace('_', '-')}: before the fit (r = 1, ZZ nominal)")
draw(axes[1], post, obs, edges, f"reco |y| {reco.replace('p', '.').replace('_', '-')}: at the observed best fit\n"
     f"{poi} = {r_best:.2f}, {', '.join(zz)}", total_label="total at best fit")
draw(axes[2], pre_cmp, obs_cmp, edges, f"for comparison, reco |y| {reco_cmp.replace('p', '.').replace('_', '-')}: before the fit")
lim = max(axes[0].get_ylim()[1], axes[1].get_ylim()[1])
axes[0].set_ylim(min(axes[1].get_ylim()[0], -0.2), lim)
axes[1].set_ylim(min(axes[1].get_ylim()[0], -0.2), lim)
fig.suptitle("H4l, all years and flavours summed (" + ", ".join(f"{v:.1f}" for v in sorted(vals))
             + " GeV are the observed events in |y| " + reco.replace("p", ".").replace("_", "-") + ")", fontsize=12)
fig.tight_layout()
fig.savefig(out, dpi=110)
print("wrote", out)
for name, p, o in (("prefit " + reco, pre, obs), ("best fit " + reco, post, obs), ("prefit " + reco_cmp, pre_cmp, obs_cmp)):
    peak = (edges[:-1] >= 120) & (edges[1:] <= 130)
    print(f"  {name:22s} " + "  ".join(f"{k} {v.sum():6.2f}" for k, v in p.items())
          + f"  total {sum(p.values()).sum():6.2f}  obs {o.sum()}  | 120-130 GeV: exp {sum(p.values())[peak].sum():.2f} obs {o[peak].sum()}")
