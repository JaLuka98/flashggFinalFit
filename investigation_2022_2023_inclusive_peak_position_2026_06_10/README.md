# 2022+2023 inclusive peak position dump

This directory contains a small helper for inspecting the post-fit workspace and
dumping peak-position information for the inclusive observed fit.

The script reads a post-fit `RooWorkspace`, loads the `MultiDimFit` snapshot,
loops over all signal pdfs of the form `hggpdfsmrel_*`, and for each one dumps:

- the fixed Higgs mass `MH`
- the component mean functions `mean_g*_*`
- a numerical estimate of the signal-pdf peak from a scan over `CMS_hgg_mass`

The output is written as a TSV file so we can inspect it in pandas, ROOT, or a
text editor.

Example:

```bash
cd /path/to/flashggFinalFit
cmsenv
python3 investigation_2022_2023_inclusive_peak_position_2026_06_10/dump_peak_positions.py \
  --inputWSFile output_2022_2023_inclusive/Combine/runFits_mu_fiducial/dataFit/higgsCombineDataPostFitBestFit_r.MultiDimFit.mH125.38.root \
  --output investigation_2022_2023_inclusive_peak_position_2026_06_10/peak_positions.tsv
```

If you want to inspect a different observed best-fit workspace, just point
`--inputWSFile` to that ROOT file.

There is also a small visual check plotter:

```bash
cd /path/to/flashggFinalFit
cmsenv
python3 investigation_2022_2023_inclusive_peak_position_2026_06_10/make_peak_check_plots.py \
  --inputWSFile output_2022_2023_inclusive/Combine/runFits_mu_fiducial/dataFit/higgsCombineDataPostFitBestFit_r.MultiDimFit.mH125.38.root
```

Recommended command for this repository layout:

```bash
export HOME=/tmp
export XDG_CACHE_HOME=/tmp/.cache
mkdir -p /tmp/.cache
source /cvmfs/cms.cern.ch/cmsset_default.sh >/dev/null 2>&1
cd /net/data_cms3a-1/spaeh/private/PhD/analyses/partial_Run3_differential/Hgg-PartialRun3-3A-ETH-Analysis/fitting/CMSSW_14_1_0_pre4/src
eval "$(scramv1 runtime -sh)" >/dev/null 2>&1
python3 /net/data_cms3a-1/spaeh/private/PhD/analyses/partial_Run3_differential/Hgg-PartialRun3-3A-ETH-Analysis/fitting/CMSSW_14_1_0_pre4/src/flashggFinalFit/investigation_2022_2023_inclusive_peak_position_2026_06_10/make_peak_check_plots.py \
  --inputWSFile /net/data_cms3a-1/spaeh/private/PhD/analyses/partial_Run3_differential/Hgg-PartialRun3-3A-ETH-Analysis/fitting/CMSSW_14_1_0_pre4/src/flashggFinalFit/output_2022_2023_inclusive/Combine/runFits_mu_fiducial/dataFit/higgsCombineDataPostFitBestFit_r.MultiDimFit.mH125.38.root \
  --outdir /tmp/peakcheck_all
```

By default it uses the workspace's native `CMS_hgg_mass` binning, which is
`320` bins over `100-180 GeV`, i.e. `0.25 GeV` per bin. The plot window is
restricted to `120-130 GeV` and the script writes one plot per channel plus a
`peak_summary.tsv` file in `./plots/` next to this README.
