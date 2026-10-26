"""H4l models and data in every reco bin of an observable, summed over the 15 channels (4e, 4mu, 2e2mu x 5 periods).

Per reco bin, the m4l distribution of ZZ, Z+jets, the Higgs signal of the same gen bin, the signal from the other
gen bins (migrations, out of acceptance, non-resonant) and the data: before the fit (all r = 1, nominal
nuisances and ZZ yields) and, with a best-fit file, at the observed best fit (snapshot MultiDimFit), where a
negative signal is drawn hatched. Plus an overview of the observed and expected events per reco bin.

Yields: n_exp_final_bin<channel>_proc_<proc> (n_exp_bin where there is no n_exp_final), the yield of the
likelihood; the pdf of the process gives only the shape in the fit range.

usage: plot_h4l_bins.py <workspace> <best-fit file | none> <output folder> <title>
"""
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import ROOT  # noqa: E402

ROOT.gErrorIgnoreLevel = ROOT.kError
ws_path, bestfit_path, out_dir, title = sys.argv[1:5]
WIDTH, SUB = 2.5, 4  # GeV per bin, shape evaluations per bin
COLORS = (("ZZ", "#7fb8e6"), ("Z+jets", "#5aa05a"), ("H other gen bins", "#f2c14e"), ("H same gen bin", "#d9534f"))
CHANNEL = re.compile(r"^n_exp(_final)?_bin(h4l_hzz_\w+?_zzfloating_(\w+?)_cat\w+?)_proc_(.+)$")


def lower_edge(label):
    if label.startswith("GT"):
        return float(label[2:]) + 0.5
    return float(label.split("_")[0].replace("m", "-").replace("p", "."))


def yields(w):
    """{reco bin: {channel: {process: yield function}}}, n_exp_final where it exists"""
    out = {}
    for o in w.allFunctions():
        m = CHANNEL.match(o.GetName())
        if not m:
            continue
        procs = out.setdefault(m.group(3), {}).setdefault(m.group(2), {})
        if m.group(1) or m.group(4) not in procs:
            procs[m.group(4)] = o
    return out


def expected(w, table, rb, edges):
    x = w.var("ZZMass")
    nset = ROOT.RooArgSet(x)
    nb = len(edges) - 1
    sub = np.linspace(edges[0], edges[-1], SUB * nb + 1)
    centers = 0.5 * (sub[1:] + sub[:-1])
    parts = {k: np.zeros(nb) for k, _ in COLORS}
    for ch, procs in table[rb].items():
        for proc, nfun in procs.items():
            n = nfun.getVal()
            if abs(n) < 1e-5:
                continue
            pdf = next((w.pdf(p) for p in (f"shapeSig_{proc}_{ch}_morph", f"shapeSig_{proc}_{ch}",
                                            f"shapeBkg_{proc}_{ch}_morph", f"shapeBkg_{proc}_{ch}") if w.pdf(p)), None)
            if pdf is None:
                raise RuntimeError(f"no pdf for {proc} in {ch}")
            dens = []
            for c in centers:
                x.setVal(c)
                dens.append(pdf.getVal(nset))
            dens = np.array(dens)
            if dens.sum() <= 0:
                continue
            per_bin = dens.reshape(nb, SUB).sum(axis=1) / dens.sum() * n
            if proc in ("bkg_qqzz", "bkg_ggzz"):
                parts["ZZ"] += per_bin
            elif proc == "bkg_zjets":
                parts["Z+jets"] += per_bin
            elif proc.endswith(f"_zzfloating_{rb}"):
                parts["H same gen bin"] += per_bin
            else:
                parts["H other gen bins"] += per_bin
    return parts


def observed(w, edges):
    d = w.data("data_obs")
    vals = {}
    for i in range(d.numEntries()):
        a = d.get(i)
        m = re.search(r"_zzfloating_(\w+?)_cat", a.getCatLabel("CMS_channel"))
        if m and d.weight() > 0:
            vals.setdefault(m.group(1), []).extend([a.getRealValue("ZZMass")] * int(round(d.weight())))
    return vals


def draw(ax, parts, obs, edges, panel_title):
    c = 0.5 * (edges[1:] + edges[:-1])
    bottom = np.zeros(len(c))
    for k, col in COLORS:
        v = parts[k]
        pos = np.clip(v, 0, None)
        ax.bar(c, pos, WIDTH, bottom=bottom, color=col, label=f"{k}  ({v.sum():.2f})", lw=0)
        bottom += pos
        if (v < 0).any():
            ax.bar(c, np.clip(v, None, 0), WIDTH, color=col, hatch="///", edgecolor="k", alpha=0.6, lw=0.3,
                   label=f"{k} < 0")
    tot = sum(parts.values())
    ax.step(edges, np.append(tot, tot[-1]), where="post", color="k", lw=1.5, label=f"total  ({tot.sum():.2f})")
    ok = obs > 0
    ax.errorbar(c[ok], obs[ok], yerr=np.sqrt(obs[ok]), fmt="o", color="k", ms=5, label=f"data  ({obs.sum()})")
    ax.axhline(0, color="k", lw=0.7)
    ax.axvline(125.07, color="gray", ls=":", lw=1)
    ax.set_title(panel_title, fontsize=10)
    ax.set_xlabel(r"$m_{4\ell}$ (GeV)")
    ax.set_ylabel(f"events / {WIDTH:g} GeV")
    ax.legend(fontsize=8, loc="upper right")


os.makedirs(out_dir, exist_ok=True)
f = ROOT.TFile.Open(ws_path)
w = f.Get("w")
x = w.var("ZZMass")
edges = np.arange(x.getMin(), x.getMax() + 1e-6, WIDTH)
table = yields(w)
bins = sorted(table, key=lower_edge)
data = observed(w, edges)

wb = post_table = None
if bestfit_path != "none":
    fb = ROOT.TFile.Open(bestfit_path)
    wb = fb.Get("w")
    wb.loadSnapshot("MultiDimFit")
    post_table = yields(wb)
    # POI of each reco bin: the same position in the bin order (the labels differ, e.g. 4p0_20p0 / r_NJ_4p0_100p0)
    poi_vals = {v.GetName(): v.getVal() for v in wb.allVars() if re.match(r"^r_\w+_m?\d+p\d+_\d+p\d+$", v.GetName())}
    ordered = sorted(poi_vals, key=lambda p: float(re.search(r"_(m?\d+p\d+)_\d+p\d+$", p).group(1).replace("m", "-").replace("p", ".")))
    poi_of = dict(zip(bins, ordered)) if len(ordered) == len(bins) else {}

summary = []
for rb in bins:
    obs = np.histogram(data.get(rb, []), bins=edges)[0]
    pre = expected(w, table, rb, edges)
    panels = [(pre, f"before the fit (r = 1, nominal ZZ)")]
    post = None
    if wb is not None:
        post = expected(wb, post_table, rb, edges)
        poi = poi_of.get(rb) or ("r" if wb.var("r") else None)
        label = f"{poi} = {wb.var(poi).getVal():.2f}" if poi else ""
        panels.append((post, f"at the observed best fit  {label}"))
    fig, axes = plt.subplots(1, len(panels), figsize=(7.5 * len(panels), 5.6), squeeze=False)
    for ax, (p, t) in zip(axes[0], panels):
        draw(ax, p, obs, edges, t)
    lo = min(a.get_ylim()[0] for a in axes[0])
    hi = max(a.get_ylim()[1] for a in axes[0])
    for a in axes[0]:
        a.set_ylim(min(lo, -0.05 * hi), hi)
    fig.suptitle(f"{title}, reco bin {rb}: H4l, all 15 channels summed", fontsize=12)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(out_dir, f"bin_{rb}.{ext}"), dpi=100)
    plt.close(fig)
    summary.append((rb, obs.sum(), sum(pre.values()).sum(), sum(post.values()).sum() if post is not None else None,
                    pre["H same gen bin"].sum() + pre["H other gen bins"].sum()))
    print(f"{rb:22s} obs {obs.sum():5d}  exp before fit {summary[-1][2]:8.2f}"
          + (f"  at best fit {summary[-1][3]:8.2f}" if post is not None else ""), flush=True)

fig, ax = plt.subplots(figsize=(max(8, 0.7 * len(bins) + 3), 5))
xs = np.arange(len(bins))
ax.bar(xs - 0.2, [s[2] for s in summary], 0.4, color="#9ecae1", label="expected before the fit")
if wb is not None:
    ax.bar(xs + 0.2, [s[3] for s in summary], 0.4, color="#fdae6b", label="expected at the observed best fit")
ax.errorbar(xs, [s[1] for s in summary], yerr=np.sqrt([s[1] for s in summary]), fmt="o", color="k", label="data")
ax.set_xticks(xs)
ax.set_xticklabels(bins, rotation=45, ha="right", fontsize=8)
ax.set_ylabel("events (105-160 GeV)")
ax.set_yscale("symlog", linthresh=1)
ax.set_title(f"{title}: H4l observed and expected events per reco bin", fontsize=11)
ax.legend(fontsize=9)
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(out_dir, f"overview.{ext}"), dpi=100)
print("wrote", out_dir)
