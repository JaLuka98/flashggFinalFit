# Hgg acceptance (extrapolation) uncertainties

## Current prescription (2026-10-28)

The card writer now defaults to **AccBin**, not the historical **Acc** arrays
described below. `AccBin[b]` is the weighted fiducial yield in bin b divided by
the weighted generated yield in the same bin, with identical variations in both
sums. In/out factors are `AccBin_var / AccBin` and
`(1 - AccBin_var) / (1 - AccBin)`. Missing or nonphysical arrays fail explicitly.
Use `--acceptance-prefix Acc` only to reproduce historical cards.

Current inputs:
`/net/data_cms3a-2/nobackup/daumann/HIG-26-007/acceptance_inputs/2026_10_28_accbin/<variable>`.
These retain the legacy arrays for predictions and add seven `AccBin*` arrays.
They also swap the alphaS member labels relative to the older production.
The acceptance denominator correction does not require changing the prediction
arrays, and this update does not copy them into the plotting prediction modules.

See `combination/ACCBIN_VALIDATION.md` for checks, comparisons and unresolved
physics assumptions. Updated cards/workspaces are isolated in
`output_combination_accbin_<observable>`; historical fits are not updated results.

The rest of this document records the **historical** recipe and investigations;
its claim that the whole-sample denominator isolates acceptance is superseded.

The Hgg cards used in the Hgg+H4l combination (HIG-26-007) carry three lnN rows

    CMS_HIG25015_QCDscale_accMatrix
    CMS_HIG25015_pdf_accMatrix
    CMS_HIG25015_alphaS_accMatrix

They describe how a theory variation moves signal events across the fiducial
boundary. Each row is one nuisance shared by all Higgs processes, with one value
per (production mode, gen bin, in/out), identical for every era and category.
The names are shared with the H4l cards, so `combineCards.py` correlates them
between the two channels by name.

## Where things live

| What | Location |
|---|---|
| Acceptance calculation | HiggsDNA `higgs_dna/scripts/fiducial/fiducial_xsec_calculator.py` |
| Its outputs (`fidXS_<obs>_<proc>.py`) | `/net/data_cms3a-1/daumann/Hgg-PartialRun3-3A-ETH-Analysis/HiggsDNA/higgs_dna/scripts/fiducial/` |
| Cards with the rows already in (Hgg + H4l) | `/net/data_cms3a-2/nobackup/linuserdmann/H4l_datacards/prepared_cards/{hgg,h4l}_<obs>/` |
| Script that originally wrote the rows | unknown, not in any readable repository (likely Linus' preparation step) |
| Post-fit extrapolation to total XS | `/net/data_cms3a-1/daumann/ETH-Aachen-repo/Hgg-PartialRun3-3A-ETH-Analysis/fitting/tmp_extrapolation/extrapolate_total_xsec.py` |
| Tool to (re)write or validate the rows | `Datacard/addAcceptanceUncertainties.py` (this directory) |

## Definition

From the calculator, per gen bin b: `Acc[b] = sum w(fiducial and b) / sum w(all)`,
recomputed for each variation with the varied total in the denominator, so only
the acceptance effect remains. Scale = envelope over LHE weights 0,1,3,5,7,8;
PDF = nominal +- sqrt(sum over 100 replicas of (replica - nominal)^2);
alphaS = the two alphaS members. All interpolated to mH = 125.07 GeV.

The card entries ("down/up") are

    <prod>_<var>_<bin>_in  :  Acc_var[b] / Acc[b]
    <prod>_<var>_<bin>_out :  (1 - Acc_var[b]) / (1 - Acc[b])

## Usage

    python3 Datacard/addAcceptanceUncertainties.py --datacard <card> \
        --fidxs-dir <dir with fidXS files> --obs YH --validate
    python3 Datacard/addAcceptanceUncertainties.py --datacard <card> \
        --fidxs-dir <dir with fidXS files> --obs YH --output <new card>

Supported: YH, PTH, NJ, PTJ0, inclusive (`--obs PTH --fidxs-dir .../inclusive_output`,
single-bin files), MassJ0J1 (`--obs GenMassJ0J1 --card-var MassJ0J1`, 8-bin files
in `Plots/Spectra/fidXS`). Gen bins are matched by edge: interior edges must
agree exactly, outer under/overflow edges only produce a warning.

Candidate input sets on disk (all contain the same files, byte-identical diffs):
HiggsDNA `scripts/fiducial/` (+ `inclusive_output/`), and the copies in
`Plots/Spectra/fidXS` of this repo and of `../flashggFinalFit`. The run scripts
(`get_<obs>_xs.sh`) show they were made with `--year 2024 --era all` from the
particle-level production `2026_04_07` on EOS.

## Validation status (2026-10-20)

- Writing: only the three rows change; combine's DatacardParser reads the
  written card with the same bins, processes and nuisances as the original.
- Convention: confirmed (ggH rapidity PDF/alphaS agree to ~1e-4, inclusive ggH
  to 2.5e-4, several scale bins to ~2e-5).
- Numbers: **no input set on disk reproduces the cards.** Worst |diff| of the
  lnN factors per observable: inclusive 3e-3 (ttH), YH 3.5e-2 (ttH), PTH 3e-2,
  NJ 3e-2, PTJ0 5e-2 (ggH), MassJ0J1 1.2e-1 (ggH). The pattern (small for ggH
  inclusive, large for low-statistics modes/bins) points to a different sample
  set or year selection in the run that produced the cards, not a different formula.

## What Linus' preparation step does (verified 2026-10-20)

Source of the H4l inputs: `Hgg-H4l-combination-PartialRun3` (github maxwrabetz,
only zipped cards + README, no scripts); `mH125p07_datacards/` is byte-identical
to the H4l cards in `/net/data_cms3a-2/nobackup/linuserdmann/H4l_datacards/`.
Going from those to `prepared_cards/h4l_<obs>/` (same 8250 columns, all 52 shared
lnN rows value-identical, including the H4l `accMatrix`/`effMatrix`):

- removes `BR_hzz4e`, `BR_hzz4mu`, `BR_hzz2e2mu` (H4l-specific, ~1.5%),
- adds `HiggsDecayWidthTHU_{hbb,hcc,hgluglu,htautau,hww,hzz}`, `param_alphaS`, `param_mq`,
- merges the five `CMS_pileup_<era>` into one `CMS_pileup`.

On the Hgg side the same step adds the three `accMatrix` rows, the BR rows
(+ `HiggsDecayWidthTHU_hgg`) and renames `CMS_hgg_*` -> `CMS_HIG26007_*`.
The script doing this is still not available.

Reproduction of the deterministic parts (combine's YR4 tables
`HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/br/{BR4,WidthUncertainties_125GeV_YR4}.txt`
at mH = 125.07, per-decay propagation kappa_X = (1 + u_d [X=d]) / (1 + BR_d u_d)):

- `HiggsDecayWidthTHU_{hbb,hcc,hgluglu,htautau,hww,hzz}`: reproduced to 1e-5 in
  both channels, including the H4l own term hzz = 1.00487.
- `param_alphaS`: reproduced to 3e-4. `param_mq`: reproduced to 5e-4 when mB,
  mC, mt are combined in quadrature.
- `CMS_pileup` (H4l): exactly the union of the five disjoint per-era rows.
  Note this makes pileup fully correlated across eras and with the Hgg `CMS_pileup`.

Two problems found:

1. `HiggsDecayWidthTHU_hgg` = 1.0023 in the Hgg cards; the YR4 own-width
   uncertainty of 1.0% gives 1.00998. The card value equals 1 + BR_gg x 1%,
   i.e. the "other decay" term with the sign flipped. Underestimated by ~4x.
2. `param_mq` has opposite sign in the two channels: Hgg 0.9906/1.0097
   (theta=+1 raises the yield), H4l 0.9902 (theta=+1 lowers it). A quark-mass
   shift lowers BR(gg) and BR(ZZ) together, so the shared nuisance is
   anti-correlated where it should be correlated (the quadrature sum lost the sign).

## Run 2 reference (`FinalComb2.txt` in that repository)

Run 2 combined hgg, hzz, hww, htt, httboost. Hgg acceptance uncertainties were
`QCDscale_smH_ACCEPT`, `alphaS_smH_ACCEPT` and per-replica `pdf_Higgs_smH_<year>_<i>`,
on `smH` and `OutsideAcceptance`, **in hgg only**. hzz had no acceptance nuisance
shared with hgg, and the card has **no BR / partial-width nuisances at all**.
So the Run 3 scheme (acceptance correlated between Hgg and H4l, LHCHWG width
uncertainties added) is *different* from Run 2.

## Linus' actual script and the reruns (2026-10-20)

- The rows are written by `Combine/prepare_total_xsec_datacard.py` on
  `origin/hig19016-binning` of the FinalFits fork (names `CMS_acc_{scale,pdf,alphaS}`,
  later renamed by `law run NuisanceHandling --rename-parameters-file
  $CWS_BASE/cws/scripts/rename_hgg_parameters.txt`). Same formula as
  `addAcceptanceUncertainties.py`. It reads ONE file with per-process keys
  (`Acc_ggH`, `Acc_scale_up_ggH`, ...), i.e. a calculator run with
  `--process all --per-process-output`; only the inclusive one exists on disk.
- BR rows and pileup merge: `law run NuisanceHandling --nuisance-file
  $CWS_BASE/cws/scripts/add_nuisances.txt --remove-parameters ... --do-merge-pileup`.
- All on-disk fidXS files were made with `--year 2024`, i.e. 2024 samples only.
- Reruns of the calculator for rapidity on particleLevel/2026_04_07
  (scratch, not kept): 2022-only and all-years. Neither reproduces the card;
  ggH PDF agrees to 5e-5 but ggH QCD scale is off by ~1e-3 and ttH by ~1e-2.
  Since PDF matches for the same events while the scale envelope does not, the
  most likely remaining difference is the scale-weight set / indexing (e.g.
  the older 2022-only production `particleLevel/2025_12_08`) or the calculator
  version, not the event selection.

## PINNED: recipe of the acceptance rows in the cards (2026-10-20)

Reproduced exactly (all entries, all production modes, all three sources,
0 difference except one 1e-5 rounding) for the rapidity card:

    python3 fiducial_xsec_calculator.py \
        /net/data_cms3a-2/nobackup/group_JE_CMS/Hgg_PartialRun3/particleLevel/2026_04_07/ \
        --year 2022 2023 --era all --process <ggH|VBFH|VH|ttH> \
        --bin '|0.0|0.15|0.3|0.45|0.6|0.75|0.9|1.2|1.6|2.0|2.5|' --obs GenYH

i.e. production 2026_04_07, **2022 + 2023 samples only**, default geometric
fiducial flag, scale envelope {0,1,3,5,7,8}, interpolated to 125.07 GeV.
Found with a one-pass scan of 240 prescriptions (year sets, both productions,
geometric/classical flag, GenYH/TruthYH, four scale-weight sets, with/without
mass interpolation); the next best is off by ~5x, most by >100x.

Also reproduced exactly for the inclusive card (`--bin '|0|140000|' --obs GenPTH`).

**Decision: use 2022 + 2023 only.** 2024 is excluded on purpose (known problem
with the 2024 samples, reportedly VBF). Not visible in the rapidity acceptance
(VBF 2024 inclusive acceptance 0.5022 vs 0.5035 / 0.5029), but the 2024 ttH
QCD-scale envelope is larger (4.3% vs 2.4% / 2.8%).

- `Datacard/makeAcceptanceInputs.sh <outdir> [obs...]` regenerates all inputs
  with this recipe (inclusive, rapidity, PTH, NJ, PTJ0, MassJ0J1 in card binning).
- The theory predictions currently on disk (fidXS files used by the spectra
  plots) were made with `--year 2024`, i.e. exactly the excluded MC. They
  should be regenerated with 2022 + 2023 as well.

## Jet observables: one bin per card is wrong (2026-10-20)

With the pinned recipe, NJ is reproduced exactly. PTJ0 and MassJ0J1 are
reproduced exactly in every bin except one:

| card | broken bin | what the card contains |
|---|---|---|
| PTJ0 | 200p0_10000p0 (last) | underflow (no-jet events) + the bin |
| MassJ0J1 | 500p0_1000p0 (next-to-last) | underflow (<2 jets) + the bin |

Proof: summing the underflow and bin weights per weight (nominal, 9 scale,
100 PDF, 2 alphaS) before envelopes reproduces the card exactly for MassJ0J1
(all 4 production modes, all 3 sources) and for PTJ0 ggH; PTJ0 VBF/VH/ttH
within 6e-4 (my bin ends at 900 GeV, the card label at 10000 GeV).

Effect: those bins get an acceptance of ~0.3-0.45 instead of ~0.005, so their
`in` uncertainty is shrunk (ggH QCD scale MassJ0J1 500-1000: card +-1.9%,
correct +-14%; PTJ0 200+: card +-5%, correct +-8-9%) and their `out`
entries are inflated by ~10x. These are the same two bins that show the
normalisation problem in the total-XS spectra (the 500-1000 mjj bin carries
~the whole ggH cross section), so the per-bin acceptance inputs Linus used
are the common cause. The writing step itself is fine; the inputs are wrong.

## Open items

1. Get from Linus the fidXS files (or calculator command: years, eras, production
   date) used for the prepared cards; then rerun `--validate`.
2. The same unknown preparation step also injects the BR rows
   (`HiggsDecayWidthTHU_*`, `param_alphaS`, `param_mq`): 9 rows in the Hgg
   cards, 8 in the H4l cards, none written by this repo or HiggsDNA.
3. The `CMS_HIG25015_` prefix belongs to the H4l analysis; consider a neutral
   name, e.g. the `*_ACCEPT` convention of `systematics_master.yml`.
4. `extrapolate_total_xsec.py` applies the same `Acc_*` variations again when
   quoting the total cross section; check this is not double counted.
