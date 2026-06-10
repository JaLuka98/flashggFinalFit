#!/usr/bin/env python3

"""Make minimal post-fit peak-check plots for the inclusive observed workspace.

The goal is to visually inspect whether the fitted signal peak position is
really shifted in a given channel, by overlaying:

- the observed data
- the S+B model
- the background component
- the background-subtracted data
- the signal-only model

The script uses the post-fit ``MultiDimFit`` snapshot and draws each channel in
the requested mass window. It also writes a TSV summary with the extracted peak
positions.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
from typing import Iterable, List, Optional, Sequence, Tuple

import ROOT
import scipy.stats


def iter_roo_collection(collection) -> Iterable[object]:
    iterator = collection.createIterator()
    obj = iterator.Next()
    while obj:
        yield obj
        obj = iterator.Next()


def load_root():
    try:
        return ROOT
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("ROOT is not available in this environment.") from exc


def poisson_graph_from_hist(
    hist,
    name: str,
    error_hist=None,
) -> ROOT.TGraphAsymmErrors:
    """Build a TGraphAsymmErrors with gamma-based Poisson intervals.

    When ``error_hist`` is given, the y-values come from ``hist`` but the
    interval widths are computed from ``error_hist``. This is useful for
    background-subtracted residual plots, where the central value can be
    negative but the uncertainty should still track the underlying data.
    """

    graph = ROOT.TGraphAsymmErrors()
    graph.SetName(name)

    for ibin in range(1, hist.GetNbinsX() + 1):
        y = hist.GetBinContent(ibin)
        y_for_error = error_hist.GetBinContent(ibin) if error_hist is not None else y
        x = hist.GetBinCenter(ibin)

        lower = scipy.stats.gamma.interval(0.68, max(y_for_error, 0.0))[0]
        upper = scipy.stats.gamma.interval(0.68, max(y_for_error, 0.0) + 1.0)[1]
        if lower != lower:
            lower = 0.0
        if upper != upper:
            upper = y_for_error

        graph.SetPoint(ibin - 1, x, y)
        graph.SetPointError(
            ibin - 1,
            0.0,
            0.0,
            abs(y_for_error - lower),
            abs(upper - y_for_error),
        )

    return graph


def peak_from_hist(hist) -> Tuple[float, float]:
    """Return the peak position and value from a histogram.

    We use a simple bin-maximum estimate. The bin width is already 0.25 GeV in
    this workspace, so this is sufficient for a visual/manual cross-check.
    """

    ibin = hist.GetMaximumBin()
    return hist.GetBinCenter(ibin), hist.GetBinContent(ibin)


def make_hist(
    pdf,
    xvar,
    name: str,
    nbins: int,
    xmin: float,
    xmax: float,
    scale: float = 1.0,
):
    hist = pdf.createHistogram(
        name,
        xvar,
        ROOT.RooFit.Binning(nbins, xmin, xmax),
    )
    if scale != 1.0:
        hist.Scale(scale)
    hist.SetDirectory(0)
    return hist


def max_abs_content(*hists) -> float:
    values = []
    for hist in hists:
        for ibin in range(1, hist.GetNbinsX() + 1):
            values.append(abs(hist.GetBinContent(ibin)))
    return max(values) if values else 1.0


def draw_channel_plot(
    *,
    out_base: str,
    channel: str,
    mh: float,
    plot_min: float,
    plot_max: float,
    bin_width: float,
    data_hist,
    data_sub_hist,
    sb_hist,
    b_hist,
    sig_hist,
    peak_mass: float,
    peak_value: float,
):
    ROOT.gStyle.SetOptStat(0)
    ROOT.TGaxis.SetMaxDigits(4)

    canvas = ROOT.TCanvas(f"c_{channel}", f"c_{channel}", 700, 700)
    pad_top = ROOT.TPad(f"pad_top_{channel}", "", 0.0, 0.30, 1.0, 1.0)
    pad_bot = ROOT.TPad(f"pad_bot_{channel}", "", 0.0, 0.0, 1.0, 0.34)
    for pad in (pad_top, pad_bot):
        pad.SetTickx()
        pad.SetTicky()
        pad.Draw()

    # Top pad: data, S+B, and B
    pad_top.cd()
    top_axes = data_hist.Clone(f"top_axes_{channel}")
    top_axes.Reset()
    top_axes.SetTitle("")
    top_axes.GetXaxis().SetLabelSize(0.0)
    top_axes.GetXaxis().SetTitle("")
    top_axes.GetYaxis().SetTitle(f"Events / {bin_width:.2f} GeV")
    top_axes.GetYaxis().SetTitleOffset(1.10)
    top_axes.GetYaxis().SetTitleSize(0.050)
    top_axes.GetYaxis().SetLabelSize(0.035)
    top_axes.SetMinimum(0.0)
    top_axes.SetMaximum(1.35 * max(data_hist.GetMaximum(), sb_hist.GetMaximum(), 1.0))
    top_axes.Draw("AXIS")

    g_data = poisson_graph_from_hist(data_hist, f"g_data_{channel}")
    g_data.SetMarkerStyle(20)
    g_data.SetMarkerSize(0.9)
    g_data.SetMarkerColor(ROOT.kBlack)
    g_data.SetLineColor(ROOT.kBlack)
    g_data.Draw("P SAME")

    sb_hist.SetLineColor(ROOT.kRed + 1)
    sb_hist.SetLineWidth(3)
    sb_hist.Draw("HIST SAME")

    b_hist.SetLineColor(ROOT.kRed + 1)
    b_hist.SetLineStyle(2)
    b_hist.SetLineWidth(3)
    b_hist.Draw("HIST SAME")

    legend = ROOT.TLegend(0.56, 0.53, 0.86, 0.78)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.043)
    legend.AddEntry(g_data, "Data", "pe")
    legend.AddEntry(sb_hist, "S+B fit", "l")
    legend.AddEntry(b_hist, "B component", "l")
    legend.Draw()

    label = ROOT.TLatex()
    label.SetNDC()
    label.SetTextFont(42)
    label.SetTextSize(0.055)
    label.DrawLatex(0.12, 0.92, "#bf{CMS} #it{Preliminary}")
    label.SetTextSize(0.040)
    label.DrawLatex(0.58, 0.92, "27.8 fb^{-1} (13.6 TeV)")
    label.DrawLatex(0.15, 0.84, "H #rightarrow #gamma#gamma")
    label.DrawLatex(0.15, 0.78, f"#it{{{channel}}}")
    label.DrawLatex(0.15, 0.72, f"m_{{H}} = {mh:.2f} GeV")

    # Bottom pad: background-subtracted data and signal model
    pad_bot.cd()
    bot_axes = data_sub_hist.Clone(f"bot_axes_{channel}")
    bot_axes.Reset()
    bot_axes.SetTitle("")
    bot_axes.GetXaxis().SetTitle("m_{#gamma#gamma} (GeV)")
    bot_axes.GetXaxis().SetTitleSize(0.10)
    bot_axes.GetXaxis().SetLabelSize(0.08)
    bot_axes.GetXaxis().SetTitleOffset(1.0)
    bot_axes.GetYaxis().SetTitle(f"Data - B / {bin_width:.2f} GeV")
    bot_axes.GetYaxis().SetTitleSize(0.085)
    bot_axes.GetYaxis().SetTitleOffset(0.72)
    bot_axes.GetYaxis().SetLabelSize(0.075)

    max_abs = max_abs_content(data_sub_hist, sig_hist)
    bot_axes.SetMinimum(-1.35 * max_abs)
    bot_axes.SetMaximum(1.35 * max_abs)
    bot_axes.Draw("AXIS")

    g_sub = poisson_graph_from_hist(
        data_sub_hist,
        f"g_sub_{channel}",
        error_hist=data_hist,
    )
    g_sub.SetMarkerStyle(20)
    g_sub.SetMarkerSize(0.9)
    g_sub.SetMarkerColor(ROOT.kBlack)
    g_sub.SetLineColor(ROOT.kBlack)
    g_sub.Draw("P SAME")

    sig_hist.SetLineColor(ROOT.kBlue + 1)
    sig_hist.SetLineWidth(3)
    sig_hist.Draw("HIST SAME")

    zero_line = ROOT.TLine(plot_min, 0.0, plot_max, 0.0)
    zero_line.SetLineColor(ROOT.kGray + 2)
    zero_line.SetLineStyle(2)
    zero_line.Draw("SAME")

    mh_line = ROOT.TLine(mh, bot_axes.GetMinimum(), mh, bot_axes.GetMaximum())
    mh_line.SetLineColor(ROOT.kGray + 2)
    mh_line.SetLineStyle(2)
    mh_line.SetLineWidth(2)
    mh_line.Draw("SAME")

    peak_line = ROOT.TLine(peak_mass, bot_axes.GetMinimum(), peak_mass, bot_axes.GetMaximum())
    peak_line.SetLineColor(ROOT.kBlue + 1)
    peak_line.SetLineStyle(1)
    peak_line.SetLineWidth(2)
    peak_line.Draw("SAME")

    bot_text = ROOT.TLatex()
    bot_text.SetNDC()
    bot_text.SetTextFont(42)
    bot_text.SetTextSize(0.060)
    bot_text.DrawLatex(0.58, 0.82, f"peak = {peak_mass:.3f} GeV")
    bot_text.DrawLatex(0.58, 0.72, f"MH = {mh:.2f} GeV")

    canvas.SaveAs(f"{out_base}.pdf")
    canvas.SaveAs(f"{out_base}.png")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Make minimal post-fit peak-check plots for each channel."
    )
    parser.add_argument(
        "--inputWSFile",
        required=True,
        help="Post-fit Combine ROOT file containing the workspace 'w'.",
    )
    parser.add_argument(
        "--loadSnapshot",
        default="MultiDimFit",
        help="Snapshot name to load from the workspace.",
    )
    parser.add_argument(
        "--cats",
        default="all",
        help="Comma-separated list of categories to process, or 'all'.",
    )
    parser.add_argument(
        "--plotMin",
        type=float,
        default=120.0,
        help="Lower edge of the plot window in GeV.",
    )
    parser.add_argument(
        "--plotMax",
        type=float,
        default=130.0,
        help="Upper edge of the plot window in GeV.",
    )
    parser.add_argument(
        "--binWidth",
        type=float,
        default=None,
        help="Data bin width in GeV. Defaults to the workspace bin width.",
    )
    parser.add_argument(
        "--outdir",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots"),
        help="Directory to write plots and the TSV summary.",
    )
    parser.add_argument(
        "--summary",
        default=None,
        help="Output TSV summary path. Defaults to <outdir>/peak_summary.tsv.",
    )
    args = parser.parse_args()

    ROOT = load_root()
    ROOT.gROOT.SetBatch(True)
    ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

    os.makedirs(args.outdir, exist_ok=True)
    summary_path = args.summary or os.path.join(args.outdir, "peak_summary.tsv")

    f = ROOT.TFile.Open(args.inputWSFile)
    if not f or f.IsZombie():
        raise RuntimeError(f"Could not open input file: {args.inputWSFile}")

    w = f.Get("w")
    if not w:
        raise RuntimeError("Could not find workspace 'w' in the input file.")

    if not w.loadSnapshot(args.loadSnapshot):
        raise RuntimeError(f"Could not load snapshot '{args.loadSnapshot}'.")

    xvar = w.var("CMS_hgg_mass")
    if not xvar:
        raise RuntimeError("Workspace does not contain CMS_hgg_mass.")

    mh_var = w.var("MH")
    if not mh_var:
        raise RuntimeError("Workspace does not contain MH.")

    # The workspace already stores CMS_hgg_mass with 320 bins over 100-180,
    # i.e. 0.25 GeV bins. Use that unless the user explicitly overrides it.
    workspace_bin_width = (xvar.getMax() - xvar.getMin()) / float(xvar.getBins())
    bin_width = args.binWidth if args.binWidth is not None else workspace_bin_width
    data_bins = int(round((args.plotMax - args.plotMin) / bin_width))
    if data_bins <= 0:
        raise RuntimeError("Requested plot range/bin width gives zero bins.")
    pdf_bins = max(10 * data_bins, 200)

    print(
        f"Workspace CMS_hgg_mass binning: {xvar.getBins()} bins over "
        f"{xvar.getMin():.1f}-{xvar.getMax():.1f} GeV "
        f"({workspace_bin_width:.3f} GeV/bin)"
    )
    print(
        f"Using plot window {args.plotMin:.1f}-{args.plotMax:.1f} GeV with "
        f"{data_bins} data bins of width {bin_width:.3f} GeV and "
        f"{pdf_bins} pdf bins."
    )

    chan = w.cat("CMS_channel")
    if not chan:
        raise RuntimeError("Workspace does not contain CMS_channel.")

    cat_filter = None if args.cats == "all" else set(args.cats.split(","))
    data_obs = w.data("data_obs")
    if not data_obs:
        raise RuntimeError("Workspace does not contain data_obs.")

    sb_model = w.pdf("model_s")
    b_model = w.pdf("model_b")
    if not sb_model or not b_model:
        raise RuntimeError("Workspace does not contain model_s and/or model_b.")

    rows: List[dict] = []

    for cidx in range(chan.numTypes()):
        chan.setIndex(cidx)
        channel = chan.getLabel()
        if cat_filter is not None and channel not in cat_filter:
            continue

        d_cat = data_obs.reduce(f"CMS_channel=={cidx}")
        if not d_cat:
            print(f"Skipping {channel}: no data after category reduction")
            continue

        xarg = ROOT.RooArgList(xvar)

        data_hist = xvar.createHistogram(
            f"h_data_{channel}",
            ROOT.RooFit.Binning(data_bins, args.plotMin, args.plotMax),
        )
        data_hist.SetDirectory(0)
        data_hist.SetBinErrorOption(ROOT.TH1.kPoisson)
        d_cat.fillHistogram(data_hist, xarg)

        sb_pdf = sb_model.getPdf(channel)
        b_pdf = b_model.getPdf(channel)
        if not sb_pdf or not b_pdf:
            print(f"Skipping {channel}: missing signal/background pdf")
            continue

        # RooFit returns the pdf histograms in density-like units. Multiply by
        # the plot bin width so the curves are in the same "events per bin"
        # convention as the data histogram.
        sb_hist_coarse = make_hist(
            sb_pdf,
            xvar,
            f"h_sb_coarse_{channel}",
            data_bins,
            args.plotMin,
            args.plotMax,
            scale=bin_width,
        )
        b_hist_coarse = make_hist(
            b_pdf,
            xvar,
            f"h_b_coarse_{channel}",
            data_bins,
            args.plotMin,
            args.plotMax,
            scale=bin_width,
        )

        sb_hist = make_hist(
            sb_pdf,
            xvar,
            f"h_sb_fine_{channel}",
            pdf_bins,
            args.plotMin,
            args.plotMax,
            scale=bin_width,
        )
        b_hist = make_hist(
            b_pdf,
            xvar,
            f"h_b_fine_{channel}",
            pdf_bins,
            args.plotMin,
            args.plotMax,
            scale=bin_width,
        )

        sig_hist = sb_hist.Clone(f"h_sig_{channel}")
        sig_hist.SetDirectory(0)
        sig_hist.Add(b_hist, -1.0)

        # Background-subtracted observed data.
        data_sub_hist = data_hist.Clone(f"h_data_sub_{channel}")
        data_sub_hist.SetDirectory(0)
        data_sub_hist.Add(b_hist_coarse, -1.0)
        for ibin in range(1, data_sub_hist.GetNbinsX() + 1):
            data_sub_hist.SetBinError(ibin, data_hist.GetBinError(ibin))

        peak_mass, peak_value = peak_from_hist(sig_hist)
        data_peak_mass, data_peak_value = peak_from_hist(data_sub_hist)

        sb_yield = float(sb_pdf.expectedEvents(ROOT.RooArgSet(xvar)))
        b_yield = float(b_pdf.expectedEvents(ROOT.RooArgSet(xvar)))
        s_yield = sb_yield - b_yield

        print(
            f"{channel}: MH={mh_var.getVal():.3f} GeV, "
            f"signal peak={peak_mass:.3f} GeV, "
            f"data-bkg peak={data_peak_mass:.3f} GeV, "
            f"S={s_yield:.2f}, B={b_yield:.2f}"
        )

        out_base = os.path.join(args.outdir, f"peakcheck_{channel}")
        draw_channel_plot(
            out_base=out_base,
            channel=channel,
            mh=float(mh_var.getVal()),
            plot_min=args.plotMin,
            plot_max=args.plotMax,
            bin_width=bin_width,
            data_hist=data_hist,
            data_sub_hist=data_sub_hist,
            sb_hist=sb_hist,
            b_hist=b_hist,
            sig_hist=sig_hist,
            peak_mass=peak_mass,
            peak_value=peak_value,
        )

        rows.append(
            {
                "channel": channel,
                "mh": f"{float(mh_var.getVal()):.6f}",
                "workspace_bin_width": f"{workspace_bin_width:.6f}",
                "plot_bin_width": f"{bin_width:.6f}",
                "data_bins": str(data_bins),
                "pdf_bins": str(pdf_bins),
                "signal_peak_mass": f"{peak_mass:.6f}",
                "signal_peak_value": f"{peak_value:.12g}",
                "signal_peak_minus_mh": f"{peak_mass - float(mh_var.getVal()):.6f}",
                "data_sub_peak_mass": f"{data_peak_mass:.6f}",
                "data_sub_peak_value": f"{data_peak_value:.12g}",
                "data_sub_peak_minus_mh": f"{data_peak_mass - float(mh_var.getVal()):.6f}",
                "signal_yield": f"{s_yield:.6f}",
                "background_yield": f"{b_yield:.6f}",
            }
        )

    with open(summary_path, "w", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)

    print(f"Wrote summary TSV: {summary_path}")
    print(f"Wrote plots to: {args.outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
