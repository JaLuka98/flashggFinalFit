"""
Compute S, B, S/B and S/sqrt(B) per analysis bin and per category,
for the PTH differential case and/or the inclusive case.

  S = hggpdfsmrel_..._normThisLumi from the signal workspaces
      (= XS × BR × eff × acc × lumi evaluated at MH=125.07 GeV)
  B(full window) = total data events from the background workspace RooDataHist
                   in m_gg = [100, 180] GeV
  B(sigma_eff)  = background model integral in m_H +/- sigma_eff, normalized
                  to the data yield in [100, 180] GeV

Requires the CMSSW environment (source setup_caio.sh), which provides
  libHiggsAnalysisCombinedLimit.so  (for RooSpline1D in signal ws)
  libBackgroundProfileFitting.so    (for RooBernsteinFast in bkg ws)

Run:
  python3 Plots/pth_sb_yields.py \\
    --datacard-pth  /path/to/input/PTH/Datacard_PTH_2022_2023_2024.txt \\
    --datacard-incl /path/to/input/inclusive/Datacard_2022_2023_2024.txt \\
    --outdir Plots/pth_yields

Outputs include the default full-window S/B plots and a second
S_over_B_sigmaEff.pdf plot where S and B are integrated only in the
m_H +/- sigma_eff window of the combined signal model per bin/category.
"""

import os, re, argparse
from collections import namedtuple
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)

# ── load custom libraries (must be in CMSSW environment) ─────────────────────
_cmssw = os.environ.get("CMSSW_BASE", "")
_arch  = os.environ.get("SCRAM_ARCH", "el9_amd64_gcc12")
_combine_loaded = False
if _cmssw:
    _combine_lib = os.path.join(_cmssw, "lib", _arch, "libHiggsAnalysisCombinedLimit.so")
    if os.path.exists(_combine_lib):
        _combine_loaded = ROOT.gSystem.Load(_combine_lib) >= 0
if not _combine_loaded:
    _combine_loaded = ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so") >= 0
if not _combine_loaded:
    raise RuntimeError(
        "Could not load libHiggsAnalysisCombinedLimit.so. "
        "Run this from a working CMSSW/Combine environment, e.g. after setup_caio.sh."
    )

_fgf_root = os.environ.get("ANALYSIS_PATH",
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_bkg_lib = os.path.join(_fgf_root, "Background/lib/libBackgroundProfileFitting.so")
if ROOT.gSystem.Load(_bkg_lib) < 0:
    raise RuntimeError(f"Could not load background fitting library: {_bkg_lib}")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from plottingTools import getEffSigma

# ── constants ─────────────────────────────────────────────────────────────────
PTH_BINS = [
    "0p0_5p0", "5p0_10p0", "10p0_15p0", "15p0_20p0", "20p0_25p0", "25p0_30p0",
    "30p0_35p0", "35p0_45p0", "45p0_60p0", "60p0_80p0", "80p0_100p0",
    "100p0_120p0", "120p0_140p0", "140p0_170p0", "170p0_200p0", "200p0_250p0",
    "250p0_350p0", "350p0_450p0", "450p0_10000p0",
]
CATS     = ["cat0", "cat1", "cat2"]
CAT_ORDER = ["cat0", "cat1", "cat2", "catMerged"]
YEARS    = ["2022", "2023", "2024"]
YEAR_TAG = {"2022": "Y22", "2023": "Y23", "2024": "Y24"}
PROCS_SIG = ["ggh", "vbf", "vh", "tth"]
MH_VAL    = 125.07  # GeV
SIGMA_WINDOW_LABEL = r"$m_H \pm \sigma_{\mathrm{eff}}$"
_BKG_MODEL_CACHE = {}
_SIGNAL_MODEL_CACHE = {}


# ── analysis config ───────────────────────────────────────────────────────────
Config = namedtuple("Config", [
    "name",           # human label
    "var_bins",       # ordered list of variable bins (PTH_BINS or ["inclusive"])
    "bin_re",         # compiled regex; groups: (ytag, [vbin,] cat)
    "ws_dir",         # year -> subdirectory name relative to datacard_dir
    "bkg_ws_file",    # (vbin, cat) -> background workspace filename
    "data_hist",      # (vbin, cat) -> RooDataHist name inside workspace
    "sig_ws_file",    # (vbin, cat) -> signal workspace filename
    "sig_pdf",        # (proc_no_hgg, vbin, cat) -> PDF stem name
])

PTH_CONFIG = Config(
    name       = "PTH",
    var_bins   = PTH_BINS,
    bin_re     = re.compile(r"^(Y\d+)_RECO_PTH_(.+)_(cat(?:\d+|Merged))$"),
    ws_dir     = lambda year: f"Models_PTH_{year}",
    bkg_ws_file= lambda vbin, cat: f"CMS-HGG_multipdf_RECO_PTH_{vbin}_{cat}.root",
    data_hist  = lambda vbin, cat: f"roohist_data_mass_RECO_PTH_{vbin}_{cat}",
    sig_ws_file= lambda vbin, cat: f"CMS-HGG_sigfit_packaged_RECO_PTH_{vbin}_{cat}.root",
    sig_pdf    = lambda proc, vbin, cat:
                 f"hggpdfsmrel_{proc}_RECO_PTH_{vbin}_{cat}_13TeV",
)

INCL_CONFIG = Config(
    name       = "inclusive",
    var_bins   = ["inclusive"],
    bin_re     = re.compile(r"^(Y\d+)_(cat(?:\d+|Merged))$"),
    ws_dir     = lambda year: f"Models_{year}",
    bkg_ws_file= lambda vbin, cat: f"CMS-HGG_multipdf_{cat}.root",
    data_hist  = lambda vbin, cat: f"roohist_data_mass_{cat}",
    sig_ws_file= lambda vbin, cat: f"CMS-HGG_sigfit_packaged_{cat}.root",
    sig_pdf    = lambda proc, vbin, cat: f"hggpdfsmrel_{proc}_{cat}_13TeV",
)


def bin_label(b):
    if b == "inclusive":
        return "Inclusive"
    lo, hi = b.replace("p0", "").split("_")
    hi = hi.replace("10000", "∞")
    return f"[{lo},{hi})"


def _ordered_cats(cats):
    present = set(cats)
    ordered = [cat for cat in CAT_ORDER if cat in present]
    ordered += sorted(present - set(ordered))
    return ordered


def _cats_in_df(df):
    return _ordered_cats(df["cat"].dropna().unique())


def _cat_color(cat):
    return CAT_COLORS.get(cat, "#999999")


def _cat_label(cat):
    return CAT_LABELS.get(cat, cat)


def _cat_offsets(cats):
    ncat = max(1, len(cats))
    width = min(0.8 / ncat, 0.27)
    offsets = [(i - (ncat - 1) / 2.0) * width for i in range(ncat)]
    return width, offsets


def _model_dir(datacard_dir, cfg, year):
    """
    Locate the year-specific model directory. This accepts either a datacard
    in Combine/ or the mirrored copy in Datacards/.
    """
    rel = cfg.ws_dir(year)
    datacard_dir = os.path.abspath(datacard_dir)
    parent = os.path.dirname(datacard_dir)

    candidates = [
        os.path.join(datacard_dir, rel),
        os.path.join(parent, "Combine", rel),
    ]
    if os.path.basename(datacard_dir) == "Combine":
        candidates.append(os.path.join(datacard_dir, rel))
    elif os.path.basename(datacard_dir) == "Datacards":
        candidates.append(os.path.join(parent, "Combine", rel))

    seen = []
    for path in candidates:
        if path not in seen:
            seen.append(path)
        if os.path.isdir(path):
            return path
    raise FileNotFoundError(
        f"Could not find model directory for {cfg.name} {year}. Tried: {seen}"
    )


def _parse_card_bins(datacard_path, cfg):
    """Return all datacard analysis bins as (vbin, cat, ytag)."""
    bins = set()
    with open(datacard_path) as fh:
        for line in fh:
            stripped = line.strip()
            if not re.match(r"^bin\s", stripped):
                continue
            for token in stripped.split()[1:]:
                m = cfg.bin_re.match(token)
                if not m:
                    continue
                groups = m.groups()
                if len(groups) == 3:
                    ytag, vbin, cat = groups
                else:
                    ytag, cat = groups
                    vbin = "inclusive"
                bins.add((vbin, cat, ytag))
    return bins


# ── 1. Parse datacard: in-bin signal processes + rates per (vbin, cat, ytag) ──
def parse_signal_procs(datacard_path, cfg):
    """
    Returns {(vbin, cat, ytag): [(proc_no_hgg, rate_pb), ...]}
    rate_pb is the datacard rate, which equals the era luminosity in pb^-1.
    normThisLumi in the workspace is normalised to intLumi=1 pb^-1, so
    actual expected events = normThisLumi * rate_pb.
    For inclusive cfg, vbin is always "inclusive".
    """
    result = {}
    with open(datacard_path) as fh:
        lines = fh.readlines()

    bin_idx = proc_name_idx = rate_idx = None
    for i, l in enumerate(lines):
        s = l.strip()
        if re.match(r"^bin\s", s):
            bin_idx = i
        elif re.match(r"^process\s", s) and proc_name_idx is None:
            proc_name_idx = i
        elif re.match(r"^rate\s", s):
            rate_idx = i
            break

    if bin_idx is None or proc_name_idx is None or rate_idx is None:
        raise RuntimeError("Could not parse datacard header rows (bin/process/rate)")

    bins      = lines[bin_idx].split()[1:]
    procs     = lines[proc_name_idx].split()[1:]
    rate_vals = lines[rate_idx].split()[1:]
    if not (len(bins) == len(procs) == len(rate_vals)):
        raise RuntimeError(
            "Datacard bin/process/rate rows have different lengths: "
            f"{len(bins)} / {len(procs)} / {len(rate_vals)}"
        )

    for b, proc, rate_str in zip(bins, procs, rate_vals):
        m = cfg.bin_re.match(b)
        if not m:
            continue
        groups = m.groups()
        if len(groups) == 3:
            ytag, vbin, cat = groups
        else:  # inclusive: 2 groups
            ytag, cat = groups
            vbin = "inclusive"

        if not (any(proc.startswith(p + "_") for p in PROCS_SIG)
                and "_in_" in proc and proc.endswith("_hgg")):
            continue
        proc_no_hgg = proc[:-4]  # strip "_hgg"
        rate = float(rate_str)
        key = (vbin, cat, ytag)
        existing = [p for p, _ in result.setdefault(key, [])]
        if proc_no_hgg not in existing:
            result[key].append((proc_no_hgg, rate))
    return result


# ── 2. Signal yield from signal workspace ─────────────────────────────────────
def read_signal_events(datacard_dir, vbin, cat, year, procs_with_rates, cfg):
    """
    procs_with_rates: [(proc_no_hgg, rate_pb), ...]
    normThisLumi in the workspace is XS*BR*effAcc*1 pb^-1 (intLumi=1 reference).
    Actual events = normThisLumi * rate_pb (era luminosity in pb^-1).
    """
    if not procs_with_rates:
        return 0.0

    ws_path = os.path.join(
        _model_dir(datacard_dir, cfg, year), "signal", cfg.sig_ws_file(vbin, cat))
    if not os.path.exists(ws_path):
        raise FileNotFoundError(f"Missing signal workspace: {ws_path}")

    f = ROOT.TFile.Open(ws_path)
    if not f or f.IsZombie():
        raise OSError(f"Could not open signal workspace: {ws_path}")
    ws = f.Get("wsig_13TeV")
    if not ws:
        f.Close()
        raise KeyError(f"Missing wsig_13TeV in {ws_path}")

    mh = ws.var("MH")
    if mh:
        mh.setVal(MH_VAL)

    total = 0.0
    missing = []
    for p, rate_pb in procs_with_rates:
        fn_name = cfg.sig_pdf(p, vbin, cat) + "_normThisLumi"
        fn = ws.function(fn_name)
        if fn:
            # normThisLumi ~ XS*BR*effAcc at intLumi=1 pb^-1; scale to actual lumi
            total += max(0.0, fn.getVal()) * rate_pb
        else:
            missing.append(fn_name)
    f.Close()
    if missing:
        raise KeyError(f"Missing signal normalisation(s) in {ws_path}: {missing}")
    return total


# ── 3. Background: data events from background workspace ──────────────────────
def read_data_events(datacard_dir, vbin, cat, year, cfg):
    ws_path = os.path.join(
        _model_dir(datacard_dir, cfg, year), "background", cfg.bkg_ws_file(vbin, cat))
    if not os.path.exists(ws_path):
        raise FileNotFoundError(f"Missing background workspace: {ws_path}")

    f = ROOT.TFile.Open(ws_path)
    if not f or f.IsZombie():
        raise OSError(f"Could not open background workspace: {ws_path}")
    ws = f.Get("multipdf")
    if not ws:
        f.Close()
        raise KeyError(f"Missing multipdf workspace in {ws_path}")

    mobs = ws.var("CMS_hgg_mass")
    data = ws.data(cfg.data_hist(vbin, cat))
    if not mobs:
        f.Close()
        raise KeyError(f"Missing CMS_hgg_mass in {ws_path}")
    if not data:
        f.Close()
        raise KeyError(f"Missing {cfg.data_hist(vbin, cat)} in {ws_path}")
    th1 = data.createHistogram(_hname(), mobs,
                               ROOT.RooFit.Binning(NBINS_DATA, MASS_MIN, MASS_MAX))
    n = sum(th1.GetBinContent(ib) for ib in range(1, NBINS_DATA + 1))
    th1.Delete()
    f.Close()
    return max(0.0, n)


# ── 4. Assemble table ──────────────────────────────────────────────────────────
def assemble(datacard_path, datacard_dir, cfg):
    print(f"  [{cfg.name}] parsing signal processes ...")
    sig_procs = parse_signal_procs(datacard_path, cfg)
    card_bins = _parse_card_bins(datacard_path, cfg)
    if not card_bins:
        raise RuntimeError(
            f"No {cfg.name} bins parsed from {datacard_path}. "
            "For combined cards, bins should be prefixed like Y22_, Y23_, Y24_."
        )
    if not sig_procs:
        raise RuntimeError(
            f"No signal processes parsed from {datacard_path}. "
            "Expected names like ggh_*_in_*_hgg, vbf_*_in_*_hgg, vh_*_in_*_hgg, "
            "or tth_*_in_*_hgg."
        )

    active_pairs = [
        (vbin, cat)
        for vbin in cfg.var_bins
        for cat in _ordered_cats(c for _, c, _ in card_bins)
        if any((vbin, cat, YEAR_TAG[year]) in card_bins for year in YEARS)
    ]
    if not active_pairs:
        raise RuntimeError(f"No active {cfg.name} bin/category pairs found in {datacard_path}")
    total = sum(
        1 for vbin, cat in active_pairs for year in YEARS
        if (vbin, cat, YEAR_TAG[year]) in card_bins
    )
    done  = 0
    rows  = []
    for vbin, cat in active_pairs:
        S = B = 0.0
        for year in YEARS:
            ytag = YEAR_TAG[year]
            if (vbin, cat, ytag) not in card_bins:
                continue
            procs_with_rates = sig_procs.get((vbin, cat, ytag), [])
            S += read_signal_events(datacard_dir, vbin, cat, year, procs_with_rates, cfg)
            B += read_data_events(datacard_dir, vbin, cat, year, cfg)
            done += 1
            if done % 20 == 0:
                print(f"    {done}/{total} ...")
        SoB   = S / B if B > 0 else float("nan")
        SoSqB = S / np.sqrt(B) if B > 0 else float("nan")
        rows.append(dict(vbin=vbin, cat=cat, S=S, B=B, SoB=SoB, SoSqB=SoSqB))
    return pd.DataFrame(rows), sig_procs


# ── 5. Plotting helpers ────────────────────────────────────────────────────────
CAT_COLORS = {
    "cat0": "#e6194b",
    "cat1": "#3cb44b",
    "cat2": "#4363d8",
    "catMerged": "#8c6bb1",
}
CAT_LABELS = {
    "cat0": "cat0 (best)",
    "cat1": "cat1 (medium)",
    "cat2": "cat2 (worst)",
    "catMerged": "catMerged",
}
SIG_COLOR  = "#ff7f0e"


def _cms_label(fig):
    fig.text(0.02, 0.985, "CMS", fontsize=12, va="top", fontweight="bold")
    fig.text(0.09, 0.985, "Preliminary", fontsize=11, va="top", fontstyle="italic")
    fig.text(0.98, 0.985, r"172 fb$^{-1}$ (13.6 TeV)",
             fontsize=11, va="top", ha="right")


def _save(fig, path):
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  saved {path}")


# ── 6. Metric plots (S, B, S/B, S/√B) ────────────────────────────────────────
def make_metric_plots(df, cfg, outdir):
    os.makedirs(outdir, exist_ok=True)
    vbins   = cfg.var_bins
    xlabels = [bin_label(b) for b in vbins]
    x       = np.arange(len(vbins))
    cats    = _cats_in_df(df)
    w, offsets = _cat_offsets(cats)

    # choose figure width: narrow for inclusive (1 var-bin), wide for PTH
    fw = max(8, 0.9 * len(vbins) + 2)

    for metric, ylabel, fname, logy in [
        ("S",     "Signal events (µ=1)",  "signal_events.pdf",  False),
        ("B",     "Data events",           "data_events.pdf",    True),
        ("SoB",   "S / B",                 "S_over_B.pdf",       True),
        ("SoSqB", r"S / $\sqrt{B}$",       "S_over_sqrtB.pdf",   False),
    ]:
        fig, ax = plt.subplots(figsize=(fw, 5))
        for i, cat in enumerate(cats):
            sub  = df[df.cat == cat].set_index("vbin").reindex(vbins)
            vals = sub[metric].fillna(0).values
            ax.bar(x + offsets[i], vals, w,
                   color=_cat_color(cat), label=_cat_label(cat), alpha=0.85)
        ax.set_xticks(x)
        ax.set_xticklabels(xlabels,
                           rotation=45 if len(vbins) > 3 else 0,
                           ha="right" if len(vbins) > 3 else "center", fontsize=8)
        xlabel = r"$p_T(H)$ bin [GeV]" if cfg.name == "PTH" else "Category"
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(f"{cfg.name} — {ylabel} (2022+2023+2024)", fontsize=12)
        ax.legend(fontsize=10)
        if logy:
            ax.set_yscale("log")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        _cms_label(fig)
        _save(fig, os.path.join(outdir, fname))

    # combined S/B + S/√B panel
    fig, axes = plt.subplots(1, 2, figsize=(2 * fw, 5))
    for ax, (metric, ylabel) in zip(axes,
            [("SoB", "S / B"), ("SoSqB", r"S / $\sqrt{B}$")]):
        for i, cat in enumerate(cats):
            sub  = df[df.cat == cat].set_index("vbin").reindex(vbins)
            vals = sub[metric].fillna(0).values
            ax.bar(x + offsets[i], vals, w,
                   color=_cat_color(cat), label=_cat_label(cat), alpha=0.85)
        ax.set_xticks(x)
        ax.set_xticklabels(xlabels,
                           rotation=45 if len(vbins) > 3 else 0,
                           ha="right" if len(vbins) > 3 else "center", fontsize=8)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        if metric == "SoB":
            ax.set_yscale("log")
    axes[0].set_title("S / B", fontsize=12)
    axes[1].set_title(r"S / $\sqrt{B}$", fontsize=12)
    fig.suptitle(f"{cfg.name} — 2022+2023+2024", fontsize=12, y=0.945)
    _save(fig, os.path.join(outdir, "SB_summary.pdf"))


def make_sigma_window_plots(df, cfg, outdir):
    os.makedirs(outdir, exist_ok=True)
    vbins   = cfg.var_bins
    xlabels = [bin_label(b) for b in vbins]
    x       = np.arange(len(vbins))
    cats    = _cats_in_df(df)
    w, offsets = _cat_offsets(cats)
    fw = max(8, 0.9 * len(vbins) + 2)

    fig, ax = plt.subplots(figsize=(fw, 5))
    for i, cat in enumerate(cats):
        sub  = df[df.cat == cat].set_index("vbin").reindex(vbins)
        vals = sub["SoB"].fillna(0).values
        ax.bar(x + offsets[i], vals, w,
               color=_cat_color(cat), label=_cat_label(cat), alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels,
                       rotation=45 if len(vbins) > 3 else 0,
                       ha="right" if len(vbins) > 3 else "center", fontsize=8)
    xlabel = r"$p_T(H)$ bin [GeV]" if cfg.name == "PTH" else "Category"
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(r"S / B in $m_H \pm \sigma_{\mathrm{eff}}$", fontsize=11)
    ax.set_title(
        f"{cfg.name} — S / B in {SIGMA_WINDOW_LABEL} (2022+2023+2024)",
        fontsize=12,
    )
    ax.set_yscale("log")
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _cms_label(fig)
    _save(fig, os.path.join(outdir, "S_over_B_sigmaEff.pdf"))

    fig, ax = plt.subplots(figsize=(fw, 5))
    for i, cat in enumerate(cats):
        sub  = df[df.cat == cat].set_index("vbin").reindex(vbins)
        vals = sub["sigma_eff"].fillna(0).values
        ax.bar(x + offsets[i], vals, w,
               color=_cat_color(cat), label=_cat_label(cat), alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels,
                       rotation=45 if len(vbins) > 3 else 0,
                       ha="right" if len(vbins) > 3 else "center", fontsize=8)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(r"$\sigma_{\mathrm{eff}}$ [GeV]", fontsize=11)
    ax.set_title(f"{cfg.name} — signal effective mass resolution", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _cms_label(fig)
    _save(fig, os.path.join(outdir, "sigma_eff.pdf"))


# ── 7. S+B stacked plots (subfolder sb_plots/) ────────────────────────────────
def make_sb_plots(df, cfg, outdir):
    sb_dir = os.path.join(outdir, "sb_plots")
    os.makedirs(sb_dir, exist_ok=True)
    vbins   = cfg.var_bins
    xlabels = [bin_label(b) for b in vbins]
    x       = np.arange(len(vbins))
    cats    = _cats_in_df(df)
    w, offsets = _cat_offsets(cats)
    fw      = max(8, 0.9 * len(vbins) + 2)

    # ── individual per-category ───────────────────────────────────────────────
    for cat in cats:
        sub   = df[df.cat == cat].set_index("vbin").reindex(vbins)
        S_arr = sub["S"].fillna(0).values
        B_arr = sub["B"].fillna(0).values

        fig, ax = plt.subplots(figsize=(fw, 5))
        ax.bar(x, B_arr, color=_cat_color(cat), alpha=0.75,
               label=f"B = {B_arr.sum():.0f} events")
        ax.bar(x, S_arr, bottom=B_arr, color=SIG_COLOR, alpha=0.90,
               label=f"S = {S_arr.sum():.2f} events (µ=1)")
        ax.set_xticks(x)
        ax.set_xticklabels(xlabels,
                           rotation=45 if len(vbins) > 3 else 0,
                           ha="right" if len(vbins) > 3 else "center", fontsize=8)
        xlabel = r"$p_T(H)$ bin [GeV]" if cfg.name == "PTH" else "Category"
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel("Events", fontsize=11)
        ax.set_title(f"{cfg.name} — S + B — {_cat_label(cat)} (2022+2023+2024)",
                     fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        _cms_label(fig)
        _save(fig, os.path.join(sb_dir, f"SB_{cat}.pdf"))

    # ── all categories side by side ───────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(fw + 2, 6))
    for i, cat in enumerate(cats):
        sub   = df[df.cat == cat].set_index("vbin").reindex(vbins)
        S_arr = sub["S"].fillna(0).values
        B_arr = sub["B"].fillna(0).values
        xpos  = x + offsets[i]
        ax.bar(xpos, B_arr, w, color=_cat_color(cat), alpha=0.75,
               label=f"{_cat_label(cat)}  S={S_arr.sum():.2f}  B={B_arr.sum():.0f}")
        ax.bar(xpos, S_arr, w, bottom=B_arr, color=SIG_COLOR, alpha=0.90)

    handles, labels = ax.get_legend_handles_labels()
    handles.append(Patch(facecolor=SIG_COLOR, alpha=0.90))
    labels.append("Signal (S) stacked on top")
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels,
                       rotation=45 if len(vbins) > 3 else 0,
                       ha="right" if len(vbins) > 3 else "center", fontsize=8)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel("Events", fontsize=11)
    ax.set_title(f"{cfg.name} — S + B — all categories (2022+2023+2024)",
                 fontsize=12)
    ax.legend(handles=handles, labels=labels, fontsize=9, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _cms_label(fig)
    _save(fig, os.path.join(sb_dir, "SB_allcats.pdf"))

    # ── all categories summed per bin ─────────────────────────────────────────
    S_total = np.zeros(len(vbins))
    B_total = np.zeros(len(vbins))
    for cat in cats:
        sub = df[df.cat == cat].set_index("vbin").reindex(vbins)
        S_total += sub["S"].fillna(0).values
        B_total += sub["B"].fillna(0).values

    fig, ax = plt.subplots(figsize=(fw, 5))
    ax.bar(x, B_total, color="#6baed6", alpha=0.80,
           label=f"B = {B_total.sum():.0f} events (all cats)")
    ax.bar(x, S_total, bottom=B_total, color=SIG_COLOR, alpha=0.90,
           label=f"S = {S_total.sum():.2f} events (all cats, µ=1)")
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels,
                       rotation=45 if len(vbins) > 3 else 0,
                       ha="right" if len(vbins) > 3 else "center", fontsize=8)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel("Events (cat0 + cat1 + cat2)", fontsize=11)
    ax.set_title(f"{cfg.name} — S + B — all categories combined (2022+2023+2024)",
                 fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _cms_label(fig)
    _save(fig, os.path.join(sb_dir, "SB_combined.pdf"))


# ── 8. m_γγ mass distribution plots (subfolder mass/) ────────────────────────
_hcnt = [0]

def _hname():
    _hcnt[0] += 1
    return f"_h{_hcnt[0]}"


MASS_MIN, MASS_MAX = 100, 180
NBINS_DATA  = 80    # 1 GeV/bin — for data error bars
NBINS_MODEL = 800   # 0.1 GeV/bin — for smooth parametric model curves
BW_DATA     = (MASS_MAX - MASS_MIN) / NBINS_DATA    # 1 GeV
BW_MODEL    = (MASS_MAX - MASS_MIN) / NBINS_MODEL   # 0.1 GeV
MASS_CTR_DATA  = np.linspace(MASS_MIN + BW_DATA  / 2, MASS_MAX - BW_DATA  / 2, NBINS_DATA)
MASS_CTR_MODEL = np.linspace(MASS_MIN + BW_MODEL / 2, MASS_MAX - BW_MODEL / 2, NBINS_MODEL)
BLIND_LO, BLIND_HI = 115, 135   # signal region: blinded in data
BLIND_MASK = (MASS_CTR_DATA >= BLIND_LO) & (MASS_CTR_DATA <= BLIND_HI)


def _get_data_arr(datacard_dir, vbin, cat, year, cfg):
    """Data histogram: events per 1-GeV bin (NBINS_DATA bins)."""
    ws_path = os.path.join(
        _model_dir(datacard_dir, cfg, year), "background", cfg.bkg_ws_file(vbin, cat))
    arr = np.zeros(NBINS_DATA)
    if not os.path.exists(ws_path):
        return arr
    f = ROOT.TFile.Open(ws_path)
    if not f or f.IsZombie():
        return arr
    ws = f.Get("multipdf")
    if ws:
        mobs = ws.var("CMS_hgg_mass")
        dat  = ws.data(cfg.data_hist(vbin, cat))
        if mobs and dat:
            th1 = dat.createHistogram(_hname(), mobs,
                                      ROOT.RooFit.Binning(NBINS_DATA, MASS_MIN, MASS_MAX))
            for ib in range(1, NBINS_DATA + 1):
                arr[ib - 1] = th1.GetBinContent(ib)
            th1.Delete()
    f.Close()
    return arr


def _get_bkg_model(datacard_dir, vbin, cat, year, cfg):
    """
    Fine-binned background parametric model (NBINS_MODEL bins).
    Evaluates the RooMultiPdf (or first PDF found) from the background workspace
    and normalises it to the data event count for this era/category.
    Returns (arr, n_data) where arr.sum() == n_data.
    """
    ws_path = os.path.join(
        _model_dir(datacard_dir, cfg, year), "background", cfg.bkg_ws_file(vbin, cat))
    arr    = np.zeros(NBINS_MODEL)
    n_data = 0.0
    if not os.path.exists(ws_path):
        return arr, n_data
    f = ROOT.TFile.Open(ws_path)
    if not f or f.IsZombie():
        return arr, n_data
    ws = f.Get("multipdf")
    if not ws:
        f.Close()
        return arr, n_data

    mobs = ws.var("CMS_hgg_mass")
    dat  = ws.data(cfg.data_hist(vbin, cat))
    if mobs is None or dat is None:
        f.Close()
        return arr, n_data

    th1 = dat.createHistogram(_hname(), mobs,
                              ROOT.RooFit.Binning(NBINS_DATA, MASS_MIN, MASS_MAX))
    n_data = sum(th1.GetBinContent(ib) for ib in range(1, NBINS_DATA + 1))
    th1.Delete()

    # The RooWorkspace is named "multipdf"; it typically contains a RooMultiPdf
    # also named "multipdf" (CMS HGG convention). PyROOT can return a null proxy
    # (not None) for missing objects — validate with GetName() before using.
    bkg_pdf = None
    for candidate in [ws.pdf("multipdf")]:
        try:
            candidate.GetName()   # raises if null proxy
            bkg_pdf = candidate
        except Exception:
            pass
    if bkg_pdf is None:
        try:
            it = ws.allPdfs().createIterator()
            obj = it.Next()
            while obj:
                try:
                    obj.GetName()
                    bkg_pdf = obj
                    break
                except Exception:
                    pass
                obj = it.Next()
        except Exception:
            pass

    if bkg_pdf is not None:
        # Use point-by-point getVal instead of createHistogram — more robust for
        # RooMultiPdf (custom flashggFinalFit class with non-standard dispatch).
        try:
            norm_set = ROOT.RooArgSet(mobs)
            vals = np.empty(NBINS_MODEL)
            for i in range(NBINS_MODEL):
                mobs.setVal(MASS_MIN + (i + 0.5) * BW_MODEL)
                vals[i] = max(0.0, float(bkg_pdf.getVal(norm_set)))
            total = vals.sum()
            if total > 0:
                arr = vals * (n_data / total)
        except Exception as exc:
            print(f"    Warning: bkg PDF eval failed ({exc}); background curve will be empty")

    f.Close()
    return arr, n_data


def _get_bkg_pdf(ws):
    # The RooWorkspace is named "multipdf"; it typically contains a RooMultiPdf
    # also named "multipdf" (CMS HGG convention). PyROOT can return a null proxy
    # for missing objects, so validate with GetName() before using.
    for candidate in [ws.pdf("multipdf")]:
        try:
            candidate.GetName()
            return candidate
        except Exception:
            pass
    try:
        it = ws.allPdfs().createIterator()
        obj = it.Next()
        while obj:
            try:
                obj.GetName()
                return obj
            except Exception:
                pass
            obj = it.Next()
    except Exception:
        pass
    return None


def _data_events_in_window(data, mobs, lo, hi):
    th1 = data.createHistogram(_hname(), mobs,
                               ROOT.RooFit.Binning(NBINS_DATA, MASS_MIN, MASS_MAX))
    n = 0.0
    for ib in range(1, NBINS_DATA + 1):
        x = th1.GetBinCenter(ib)
        if lo <= x <= hi:
            n += th1.GetBinContent(ib)
    th1.Delete()
    return max(0.0, n)


def _get_bkg_peak_events(datacard_dir, vbin, cat, year, cfg, lo, hi):
    """
    Background events in [lo, hi] from the fitted background PDF, normalized
    to the data yield in [100, 180] GeV. Falls back to the data histogram only
    if RooFit cannot integrate the selected PDF.
    """
    cache_key = (os.path.abspath(datacard_dir), cfg.name, vbin, cat, year)
    if cache_key not in _BKG_MODEL_CACHE:
        _BKG_MODEL_CACHE[cache_key] = _get_bkg_model(datacard_dir, vbin, cat, year, cfg)
    bkg_arr, _ = _BKG_MODEL_CACHE[cache_key]
    if np.asarray(bkg_arr).sum() > 0:
        return _integral_in_window(bkg_arr, lo, hi)

    ws_path = os.path.join(
        _model_dir(datacard_dir, cfg, year), "background", cfg.bkg_ws_file(vbin, cat))
    if not os.path.exists(ws_path):
        return 0.0
    f = ROOT.TFile.Open(ws_path)
    if not f or f.IsZombie():
        return 0.0
    ws = f.Get("multipdf")
    if not ws:
        f.Close()
        return 0.0

    mobs = ws.var("CMS_hgg_mass")
    dat  = ws.data(cfg.data_hist(vbin, cat))
    if mobs is None or dat is None:
        f.Close()
        return 0.0

    n_data = _data_events_in_window(dat, mobs, MASS_MIN, MASS_MAX)
    bkg_pdf = _get_bkg_pdf(ws)
    if bkg_pdf is None:
        fallback = _data_events_in_window(dat, mobs, lo, hi)
        f.Close()
        return fallback

    try:
        norm_set = ROOT.RooArgSet(mobs)
        full_range = f"full_{_hname()}"
        peak_range = f"peak_{_hname()}"
        mobs.setRange(full_range, MASS_MIN, MASS_MAX)
        mobs.setRange(peak_range, lo, hi)
        full_int = bkg_pdf.createIntegral(
            norm_set, ROOT.RooFit.NormSet(norm_set), ROOT.RooFit.Range(full_range)).getVal()
        peak_int = bkg_pdf.createIntegral(
            norm_set, ROOT.RooFit.NormSet(norm_set), ROOT.RooFit.Range(peak_range)).getVal()
        if full_int > 0:
            out = max(0.0, n_data * peak_int / full_int)
            f.Close()
            return out
    except Exception as exc:
        print(f"    Warning: bkg PDF integral failed ({exc}); using data histogram in peak window")

    fallback = _data_events_in_window(dat, mobs, lo, hi)
    f.Close()
    return fallback


def _array_to_th1(arr, name):
    hist = ROOT.TH1F(name, name, NBINS_MODEL, MASS_MIN, MASS_MAX)
    for ib, val in enumerate(arr, start=1):
        hist.SetBinContent(ib, float(val))
    return hist


def _integral_in_window(arr, lo, hi):
    mask = (MASS_CTR_MODEL >= lo) & (MASS_CTR_MODEL <= hi)
    return float(np.asarray(arr)[mask].sum())


def _get_signal_model(datacard_dir, vbin, cat, year, procs_with_rates, cfg):
    """
    Fine-binned signal model for all requested processes in one year/category.
    The returned array is in events per 0.1 GeV bin, normalized to the datacard
    rate and normThisLumi values.
    """
    if not procs_with_rates:
        return np.zeros(NBINS_MODEL)
    cache_key = (
        os.path.abspath(datacard_dir), cfg.name, vbin, cat, year,
        tuple(procs_with_rates),
    )
    if cache_key in _SIGNAL_MODEL_CACHE:
        return _SIGNAL_MODEL_CACHE[cache_key]

    ws_path = os.path.join(
        _model_dir(datacard_dir, cfg, year), "signal", cfg.sig_ws_file(vbin, cat))
    if not os.path.exists(ws_path):
        raise FileNotFoundError(f"Missing signal workspace: {ws_path}")

    f = ROOT.TFile.Open(ws_path)
    if not f or f.IsZombie():
        raise OSError(f"Could not open signal workspace: {ws_path}")
    ws = f.Get("wsig_13TeV")
    if not ws:
        f.Close()
        raise KeyError(f"Missing wsig_13TeV in {ws_path}")

    mh = ws.var("MH")
    if mh:
        mh.setVal(MH_VAL)
    mobs = ws.var("CMS_hgg_mass")
    if not mobs:
        f.Close()
        raise KeyError(f"Missing CMS_hgg_mass in {ws_path}")

    arr = np.zeros(NBINS_MODEL)
    missing = []
    for p, rate_pb in procs_with_rates:
        pdf_name = cfg.sig_pdf(p, vbin, cat)
        fn_name = pdf_name + "_normThisLumi"
        pdf = ws.pdf(pdf_name)
        fn = ws.function(fn_name)
        if not pdf or not fn:
            missing.append(pdf_name if not pdf else fn_name)
            continue

        th1 = pdf.createHistogram(
            _hname(), mobs, ROOT.RooFit.Binning(NBINS_MODEL, MASS_MIN, MASS_MAX))
        integral = sum(th1.GetBinContent(ib) for ib in range(1, NBINS_MODEL + 1))
        if integral > 0:
            yield_events = max(0.0, fn.getVal()) * rate_pb
            for ib in range(1, NBINS_MODEL + 1):
                arr[ib - 1] += yield_events * th1.GetBinContent(ib) / integral
        th1.Delete()

    f.Close()
    if missing:
        raise KeyError(f"Missing signal shape/normalisation(s) in {ws_path}: {missing}")
    _SIGNAL_MODEL_CACHE[cache_key] = arr
    return arr


def _compute_sigma_window_row(datacard_dir, vbin, cats, cfg, sig_procs, card_bins):
    sig_arr = np.zeros(NBINS_MODEL)
    for cat in cats:
        for year in YEARS:
            ytag = YEAR_TAG[year]
            if (vbin, cat, ytag) not in card_bins:
                continue
            procs_with_rates = sig_procs.get((vbin, cat, ytag), [])
            sig_arr += _get_signal_model(datacard_dir, vbin, cat, year, procs_with_rates, cfg)

    if sig_arr.sum() <= 0:
        raise RuntimeError(f"Zero signal model for {cfg.name} {vbin} {','.join(cats)}")

    sig_hist = _array_to_th1(sig_arr, _hname())
    sigma_eff = float(getEffSigma(sig_hist))
    sig_hist.Delete()
    if sigma_eff <= 0:
        raise RuntimeError(
            f"Invalid sigma_eff={sigma_eff} for {cfg.name} {vbin} {','.join(cats)}"
        )

    lo = max(MASS_MIN, MH_VAL - sigma_eff)
    hi = min(MASS_MAX, MH_VAL + sigma_eff)
    S = _integral_in_window(sig_arr, lo, hi)
    B = 0.0
    for cat in cats:
        for year in YEARS:
            ytag = YEAR_TAG[year]
            if (vbin, cat, ytag) not in card_bins:
                continue
            B += _get_bkg_peak_events(datacard_dir, vbin, cat, year, cfg, lo, hi)
    if B <= 0:
        raise RuntimeError(f"Zero background in peak window for {cfg.name} {vbin} {','.join(cats)}")
    SoB = S / B if B > 0 else float("nan")
    SoSqB = S / np.sqrt(B) if B > 0 else float("nan")
    return dict(
        vbin=vbin, sigma_eff=sigma_eff,
        mass_lo=lo, mass_hi=hi, S=S, B=B, SoB=SoB, SoSqB=SoSqB,
    )


def assemble_sigma_window(datacard_path, datacard_dir, cfg, sig_procs,
                          include_all_categories=False):
    """
    Compute S/B in a narrow mass window defined per (bin, category) as
    MH +/- sigma_eff of the combined signal model.
    """
    card_bins = _parse_card_bins(datacard_path, cfg)
    active_pairs = [
        (vbin, cat)
        for vbin in cfg.var_bins
        for cat in _ordered_cats(c for _, c, _ in card_bins)
        if any((vbin, cat, YEAR_TAG[year]) in card_bins for year in YEARS)
    ]

    rows = []
    total_rows = len(active_pairs) + (len(cfg.var_bins) if include_all_categories else 0)
    done_rows = 0
    for vbin, cat in active_pairs:
        row = _compute_sigma_window_row(datacard_dir, vbin, [cat], cfg, sig_procs, card_bins)
        row["cat"] = cat
        rows.append(row)
        done_rows += 1
        print(f"    peak-window rows: {done_rows}/{total_rows} ({vbin}, {cat})", flush=True)

    if include_all_categories:
        for vbin in cfg.var_bins:
            cats = _ordered_cats(
                cat for vbin_i, cat, _ in card_bins
                if vbin_i == vbin
            )
            if not cats:
                continue
            row = _compute_sigma_window_row(datacard_dir, vbin, cats, cfg, sig_procs, card_bins)
            row["cat"] = "all_categories"
            rows.append(row)
            done_rows += 1
            print(f"    peak-window rows: {done_rows}/{total_rows} ({vbin}, all_categories)", flush=True)

    return pd.DataFrame(rows)


def add_full_range_totals(df, cfg):
    rows = [row.to_dict() for _, row in df.iterrows()]
    for vbin in cfg.var_bins:
        sub = df[df["vbin"] == vbin]
        if sub.empty:
            continue
        S = float(sub["S"].sum())
        B = float(sub["B"].sum())
        rows.append(dict(
            vbin=vbin,
            cat="all_categories",
            S=S,
            B=B,
            SoB=S / B if B > 0 else float("nan"),
            SoSqB=S / np.sqrt(B) if B > 0 else float("nan"),
        ))
    return pd.DataFrame(rows)


def make_readable_yield_table(df_full, df_peak, cfg):
    full = add_full_range_totals(df_full, cfg).rename(columns={
        "S": "signal_full_100_180",
        "B": "background_full_100_180",
        "SoB": "S_over_B_full_100_180",
        "SoSqB": "S_over_sqrtB_full_100_180",
    })
    peak = df_peak.rename(columns={
        "S": "signal_peak_pm_sigma_eff",
        "B": "background_peak_pm_sigma_eff",
        "SoB": "S_over_B_peak_pm_sigma_eff",
        "SoSqB": "S_over_sqrtB_peak_pm_sigma_eff",
        "mass_lo": "peak_mass_low_GeV",
        "mass_hi": "peak_mass_high_GeV",
        "sigma_eff": "sigma_eff_GeV",
    })
    table = full.merge(
        peak,
        on=["vbin", "cat"],
        how="outer",
        validate="one_to_one",
    )
    table.insert(0, "mode", cfg.name)
    table.insert(2, "bin_label", table["vbin"].map(bin_label))
    table.insert(4, "category_label", table["cat"].map(
        lambda cat: "all categories summed" if cat == "all_categories" else _cat_label(cat)
    ))

    ordered_cols = [
        "mode", "vbin", "bin_label", "cat", "category_label",
        "signal_full_100_180", "background_full_100_180",
        "S_over_B_full_100_180", "S_over_sqrtB_full_100_180",
        "sigma_eff_GeV", "peak_mass_low_GeV", "peak_mass_high_GeV",
        "signal_peak_pm_sigma_eff", "background_peak_pm_sigma_eff",
        "S_over_B_peak_pm_sigma_eff", "S_over_sqrtB_peak_pm_sigma_eff",
    ]
    table = table[ordered_cols]
    cat_rank = {cat: i for i, cat in enumerate(CAT_ORDER + ["all_categories"])}
    bin_rank = {vbin: i for i, vbin in enumerate(cfg.var_bins)}
    table["_bin_rank"] = table["vbin"].map(bin_rank)
    table["_cat_rank"] = table["cat"].map(lambda cat: cat_rank.get(cat, 999))
    table = table.sort_values(["_bin_rank", "_cat_rank"]).drop(columns=["_bin_rank", "_cat_rank"])
    return table


def _get_sig_shape(datacard_dir, vbin, cat, sig_procs, cfg):
    """
    Fine-binned signal shape (NBINS_MODEL bins), normalised so arr.sum() == 1.
    Uses the first year/process for which a valid signal PDF exists.
    """
    arr = np.zeros(NBINS_MODEL)
    for year in YEARS:
        ytag             = YEAR_TAG[year]
        procs_with_rates = sig_procs.get((vbin, cat, ytag), [])
        if not procs_with_rates:
            continue
        ws_path = os.path.join(
            _model_dir(datacard_dir, cfg, year), "signal", cfg.sig_ws_file(vbin, cat))
        if not os.path.exists(ws_path):
            continue
        f = ROOT.TFile.Open(ws_path)
        if not f or f.IsZombie():
            continue
        ws = f.Get("wsig_13TeV")
        if ws:
            mh = ws.var("MH")
            if mh:
                mh.setVal(MH_VAL)
            mobs = ws.var("CMS_hgg_mass")
            if mobs:
                for p, _ in procs_with_rates:
                    pdf = ws.pdf(cfg.sig_pdf(p, vbin, cat))
                    if pdf:
                        th1 = pdf.createHistogram(
                            _hname(), mobs,
                            ROOT.RooFit.Binning(NBINS_MODEL, MASS_MIN, MASS_MAX))
                        integral = sum(th1.GetBinContent(ib)
                                       for ib in range(1, NBINS_MODEL + 1))
                        if integral > 0:
                            for ib in range(1, NBINS_MODEL + 1):
                                arr[ib - 1] = th1.GetBinContent(ib) / integral
                            th1.Delete()
                            f.Close()
                            return arr
                        th1.Delete()
        f.Close()
    return arr


def make_mass_dist_plots(df, sig_procs, datacard_dir, cfg, outdir):
    """
    For each variable bin, produce m_γγ distribution plots in outdir/mass/{vbin}/:
      mass_cat0/1/2.pdf  — data (1 GeV error bars) + background model +
                           signal model + B+S model curves
      mass_weighted.pdf  — S/(S+B)-weighted combination of all categories
    All quantities are in Events / GeV for a consistent y-axis.
    """
    mass_root = os.path.join(outdir, "mass")
    os.makedirs(mass_root, exist_ok=True)
    cats = _cats_in_df(df)

    for vbin in cfg.var_bins:
        lbl      = bin_label(vbin)
        vbin_dir = os.path.join(mass_root, vbin)
        os.makedirs(vbin_dir, exist_ok=True)

        data_per_cat = {}   # cat → NBINS_DATA-bin array (events/bin)
        bkg_per_cat  = {}   # cat → NBINS_MODEL-bin array (events/bin)
        sig_per_cat  = {}   # cat → NBINS_MODEL-bin array (events/bin)

        for cat in cats:
            row = df[(df["vbin"] == vbin) & (df["cat"] == cat)]
            if row.empty:
                continue
            S_cat = float(row.iloc[0]["S"])

            # Data (1 GeV bins)
            data_arr = np.zeros(NBINS_DATA)
            for year in YEARS:
                data_arr += _get_data_arr(datacard_dir, vbin, cat, year, cfg)
            data_per_cat[cat] = data_arr

            # Background parametric model (fine)
            bkg_arr = np.zeros(NBINS_MODEL)
            for year in YEARS:
                bkg_y, _ = _get_bkg_model(datacard_dir, vbin, cat, year, cfg)
                bkg_arr += bkg_y
            bkg_per_cat[cat] = bkg_arr

            # Signal parametric model (fine), scaled to expected yield
            sig_shape = _get_sig_shape(datacard_dir, vbin, cat, sig_procs, cfg)
            sig_per_cat[cat] = S_cat * sig_shape

        # ── per-category plots ────────────────────────────────────────────────
        for cat in cats:
            if cat not in data_per_cat:
                continue
            d = data_per_cat[cat]                              # events/bin (1 GeV)
            b = bkg_per_cat.get(cat, np.zeros(NBINS_MODEL))   # events/bin (0.1 GeV)
            s = sig_per_cat.get(cat, np.zeros(NBINS_MODEL))   # events/bin (0.1 GeV)

            B_tot = d.sum()
            S_tot = s.sum()

            # Convert to events/GeV
            d_gev  = d / BW_DATA
            b_gev  = b / BW_MODEL
            s_gev  = s / BW_MODEL
            bs_gev = b_gev + s_gev

            fig, ax = plt.subplots(figsize=(10, 5))

            # Blind [115,135] GeV: replace those bins with NaN for plotting
            d_plot   = np.where(BLIND_MASK, np.nan, d_gev)
            err_plot = np.where(BLIND_MASK, np.nan,
                               np.sqrt(np.maximum(d, 1)) / BW_DATA)
            ax.errorbar(MASS_CTR_DATA, d_plot, yerr=err_plot,
                        fmt="ko", ms=3, elinewidth=1, capsize=2,
                        label=f"Data  ({B_tot:.0f} events, blinded in [115,135] GeV)",
                        zorder=5)
            ax.axvspan(BLIND_LO, BLIND_HI, color="gray", alpha=0.15,
                       label="Blinded region")
            ax.plot(MASS_CTR_MODEL, b_gev, color="#4878d0", lw=2,
                    label=f"Background model  (B = {B_tot:.0f} events)")
            ax.plot(MASS_CTR_MODEL, s_gev, color=SIG_COLOR, lw=2,
                    label=f"Signal model  (S = {S_tot:.2f} events, µ=1)")
            ax.plot(MASS_CTR_MODEL, bs_gev, color="#6a3d9a", lw=2, ls="--",
                    label="B + S model")

            ax.set_xlim(MASS_MIN, MASS_MAX)
            ax.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]", fontsize=12)
            ax.set_ylabel("Events / GeV", fontsize=12)
            ax.set_title(
                f"{cfg.name}  {lbl} — {_cat_label(cat)} (2022+2023+2024)",
                fontsize=12)
            ax.legend(fontsize=10)
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            _cms_label(fig)
            _save(fig, os.path.join(vbin_dir, f"mass_{cat}.pdf"))

        # ── S/(S+B)-weighted combination ──────────────────────────────────────
        w_data  = np.zeros(NBINS_DATA)
        w_bkg   = np.zeros(NBINS_MODEL)
        w_sig   = np.zeros(NBINS_MODEL)
        w2_data = np.zeros(NBINS_DATA)
        tot_S   = tot_B = 0.0

        for cat in cats:
            if cat not in data_per_cat:
                continue
            d  = data_per_cat[cat]
            b  = bkg_per_cat.get(cat, np.zeros(NBINS_MODEL))
            s  = sig_per_cat.get(cat, np.zeros(NBINS_MODEL))
            Sc = s.sum()
            Bc = d.sum()
            tot_S += Sc
            tot_B += Bc
            wc = Sc / (Sc + Bc) if (Sc + Bc) > 0 else 0.0
            w_data  += wc * d
            w_bkg   += wc * b
            w_sig   += wc * s
            w2_data += wc ** 2 * np.maximum(d, 1)

        wd_gev  = w_data / BW_DATA
        wb_gev  = w_bkg  / BW_MODEL
        ws_gev  = w_sig  / BW_MODEL
        wbs_gev = wb_gev + ws_gev
        werr    = np.sqrt(w2_data) / BW_DATA

        fig, ax = plt.subplots(figsize=(10, 5))
        # Blind [115,135] GeV
        wd_plot  = np.where(BLIND_MASK, np.nan, wd_gev)
        werr_plot = np.where(BLIND_MASK, np.nan, werr)
        ax.errorbar(MASS_CTR_DATA, wd_plot, yerr=werr_plot,
                    fmt="ko", ms=3, elinewidth=1, capsize=2,
                    label=r"Data  ($S/(S+B)$ weighted, blinded in [115,135] GeV)",
                    zorder=5)
        ax.axvspan(BLIND_LO, BLIND_HI, color="gray", alpha=0.15,
                   label="Blinded region")
        ax.plot(MASS_CTR_MODEL, wb_gev, color="#4878d0", lw=2,
                label=f"Background model  (B = {tot_B:.0f} events)")
        ax.plot(MASS_CTR_MODEL, ws_gev, color=SIG_COLOR, lw=2,
                label=f"Signal model  (S = {tot_S:.2f} events, µ=1)")
        ax.plot(MASS_CTR_MODEL, wbs_gev, color="#6a3d9a", lw=2, ls="--",
                label="B + S model")
        ax.set_xlim(MASS_MIN, MASS_MAX)
        ax.set_xlabel(r"$m_{\gamma\gamma}$ [GeV]", fontsize=12)
        ax.set_ylabel(r"$S/(S+B)$-weighted Events / GeV", fontsize=12)
        ax.set_title(
            f"{cfg.name}  {lbl} — S/(S+B) weighted, all cats (2022+2023+2024)",
            fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        _cms_label(fig)
        _save(fig, os.path.join(vbin_dir, "mass_weighted.pdf"))

        print(f"  [{cfg.name}] {vbin} done")


# ── 9. Run one complete analysis mode ─────────────────────────────────────────
def run_mode(datacard_path, cfg, outdir, skip_plots=False):
    datacard_dir = os.path.dirname(os.path.abspath(datacard_path))
    mode_dir     = os.path.join(outdir, cfg.name)
    os.makedirs(mode_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Running: {cfg.name}")
    print(f"{'='*60}")

    df, sig_procs = assemble(datacard_path, datacard_dir, cfg)

    csv_path = os.path.join(mode_dir, f"{cfg.name}_SB_yields.csv")
    df.to_csv(csv_path, index=False, float_format="%.4f")
    print(f"  saved {csv_path}")
    print(df.to_string(index=False))

    print(f"  [{cfg.name}] computing {SIGMA_WINDOW_LABEL} S/B ...")
    df_sigma = assemble_sigma_window(
        datacard_path, datacard_dir, cfg, sig_procs, include_all_categories=True)
    sigma_csv_path = os.path.join(mode_dir, f"{cfg.name}_SB_yields_sigmaEff.csv")
    df_sigma.to_csv(sigma_csv_path, index=False, float_format="%.4f")
    print(f"  saved {sigma_csv_path}")
    print(df_sigma.to_string(index=False))

    summary_df = make_readable_yield_table(df, df_sigma, cfg)
    summary_csv_path = os.path.join(mode_dir, f"{cfg.name}_SB_yields_summary.csv")
    summary_df.to_csv(summary_csv_path, index=False, float_format="%.6g")
    print(f"  saved {summary_csv_path}")
    print(summary_df.to_string(index=False))

    if skip_plots:
        return summary_df

    print(f"  [{cfg.name}] making metric plots ...")
    make_metric_plots(df, cfg, mode_dir)

    print(f"  [{cfg.name}] making {SIGMA_WINDOW_LABEL} S/B plots ...")
    make_sigma_window_plots(df_sigma[df_sigma["cat"] != "all_categories"], cfg, mode_dir)

    print(f"  [{cfg.name}] making S+B stacked plots ...")
    make_sb_plots(df, cfg, mode_dir)

    print(f"  [{cfg.name}] making m_γγ mass distribution plots ...")
    make_mass_dist_plots(df, sig_procs, datacard_dir, cfg, mode_dir)
    return summary_df


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Compute S, B, S/B, S/√B and mass distributions "
                    "for the PTH differential and/or inclusive analyses.")
    parser.add_argument("--datacard-pth", metavar="PATH",
                        help="Datacard_PTH_2022_2023_2024.txt")
    parser.add_argument("--datacard-incl", metavar="PATH",
                        help="Datacard_2022_2023_2024.txt (inclusive)")
    parser.add_argument("--outdir", default="pth_yields",
                        help="Top-level output directory")
    parser.add_argument("--skip-plots", action="store_true",
                        help="Only write the CSV tables; do not remake plots")
    args = parser.parse_args()

    if not args.datacard_pth and not args.datacard_incl:
        parser.error("Provide at least one of --datacard-pth or --datacard-incl")

    summary_tables = []
    if args.datacard_pth:
        summary_tables.append(
            run_mode(args.datacard_pth, PTH_CONFIG, args.outdir, args.skip_plots))

    if args.datacard_incl:
        summary_tables.append(
            run_mode(args.datacard_incl, INCL_CONFIG, args.outdir, args.skip_plots))

    summary_tables = [df for df in summary_tables if df is not None]
    if summary_tables:
        combined = pd.concat(summary_tables, ignore_index=True)
        combined_path = os.path.join(args.outdir, "SB_yields_summary.csv")
        combined.to_csv(combined_path, index=False, float_format="%.6g")
        print(f"  saved {combined_path}")

    print("\nAll done.")


if __name__ == "__main__":
    main()
