# Hgg+H4l combination, 2022+2023+2024 (HIG-26-007)

Total-XS extrapolation: every gen bin has an `_in` and an `_out` Hgg process (and `smH` + `OutsideAcceptance`
in H4l), all scaled by the POI of that bin. The chain uses three code bases:

| step | repository / branch |
|---|---|
| 1. trees with per-bin out ids | `Hgg-PartialRun3-3A-ETH-Analysis`, branch `Hzz_Hyy_222324_combination` (`postprocessing/`) |
| 2. raw Hgg cards | `flashggFinalFit`, branch `Hzz_Hyy_222324_combination_perbinout` |
| 3. acceptance inputs | HiggsDNA `fiducial_xsec_calculator.py`, recipe `Datacard/makeAcceptanceInputs.sh` (this branch) |
| 4. card treatment, combination, fits | `flashggFinalFit`, branch `Hzz_Hyy_222324_combination` (this folder) |

Shared inputs and outputs: `/net/data_cms3a-2/nobackup/group_JE_CMS/Hyy_Hzz_combination` (`$STAGE`).

## 1. Post-processing (MC with per-bin out ids)

Data and the inclusive measurement use the October smoothed sigma_m/m production
(`outputs_postprocessing_smoothed_decorr_smeared_mass100to180_2026_10_01`). The MC is rerun with one out id
per gen bin, "9" + in id, as in `differentialProcTable_` of step 2 (NJ 930-934, PTJ0 940-948, PTH 910-9118,
YH 920-929, MassJ0J1 970-977), `configs/gen_binning_perbinout_2026_10_21.json`:

```bash
cd postprocessing
python3 submit_smoothed_decorr_smeared_perbinout.py --obs NJ PTJ0 PTH rapidity MassJ0J1
# after the jobs: samples -> root/mc, 2024 WH/ZH -> VH (as for the October outputs)
outputs_postprocessing_smoothed_decorr_smeared_mass100to180_2026_10_01_perbinout_2026_10_20/watch/prepare_mc.sh NJ PTJ0 ...
```

PTH 2022/2023 use merged categories (`mc_merged_cats`), with the merge decided by the October data:
`merge_empty_categories.py --base-dir <out>/<year>/PTH/root --data-subdir data_october` (`data_october` -> the
October `root/data`). `watch/pipeline_perbinout.py` does prepare -> merge -> validation -> FinalFits launch
unattended.

Why the out ids have to be in the trees: the systematics trees carry no `Gen*` branches, so Trees2WS cannot
bin them with the gen variables (this is what broke the per-bin systematics in the first combination cards).

## 2. Raw Hgg cards (FinalFits, branch `Hzz_Hyy_222324_combination_perbinout`)

```bash
cd flashggFinalFit_hig19016_perbinout          # checkout of the perbinout branch
(source /cvmfs/cms.cern.ch/cmsset_default.sh; cd ..; cmsenv; cd -; cd Background; make)   # once per checkout
source law/htcondor_setup.sh; cd law
law run FinalFits --years 2022,2023,2024 --variable <obs> --batch-system htcondor --batch-flavor htcondor
```

`config/<year>_<obs>.yml` sets the inputs, `diffSplitByCode: True` (split by the per-bin out ids) and the
output folders; the card is `output_2022_2023_2024_<obs>/Combine/Datacard_<obs>_2022_2023_2024.txt`.
The inclusive Hgg card comes from the HIG-26-007 production (no per-bin out needed):
`$STAGE/Hyy_datacards_smoothed_decorrelation/raw/inclusive/Datacard_2022_2023_2024.txt`.
Do not use `Combine/prepare_total_xsec_datacard.py` of that branch for the combination (BR rows, see below).

## 3. Acceptance inputs

`Datacard/makeAcceptanceInputs.sh <out dir> [obs ...]` runs the HiggsDNA fiducial calculator with the pinned
recipe (2022+2023, card binning, GenNJ, 8-bin MassJ0J1); details and validation in
`Datacard/ACCEPTANCE_UNCERTAINTIES.md`. The inputs used: `$STAGE/fiducial_samples/acceptance_2022_2023/<obs>`.

## 4. Card treatment, combination and fits

```bash
combination/run_combination.sh <obs> hgg-card h4l-card cards t2w prepare   # cards and workspaces
combination/run_combination.sh <obs> law                                   # expected (Asimov) fits
combination/run_combination.sh <obs> unblind                               # observed fits
combination/run_combination.sh <obs> summary                               # tables + plots (KIND=dataFit for observed)
```

| step | what |
|---|---|
| `hgg-card` | `Datacard/addAcceptanceUncertainties.py` (`CMS_HIG25015_{QCDscale,pdf,alphaS}_accMatrix`) and `Datacard/addBranchingRatioUncertainties.py --channel hgg` (`HiggsDecayWidthTHU_*`, `param_alphaS`, `param_mq`) -> `<raw card>_total.txt` |
| `h4l-card` | `Datacard/prepareH4lCombinationCard.py`: remove `BR_hzz*`, merge per-era `CMS_pileup`, BR rows -> `..._zzfloating_bin_v3_comb.txt` |
| `cards` | `combineCards.py hgg= h4l=`; Hgg-only / H4l-only cards cut out with `--ic` and `clean_card.py`, so all three fits share the inputs |
| `t2w` | `Combine/makeCombinationMaps.py` builds the multiSignalModel map on the combined card and checks that every signal is mapped exactly once and no background; no `higgsMassRange` (MH stays fixed) |
| `law`, `unblind` | `law run FinalFitsYear --year 2022_2023_2024 [--variable <obs>] --{asimov,unblinded}-fits` per fit |
| `summary` | `summarize_scans.py` (spline crossings, syst = sqrt(total^2 - stat^2)) and `plot1DScan.py` comparisons |

An existing `_total` / `_comb` card is never overwritten: the step regenerates it and stops if it differs.
Checked on 2026-10-21: the inclusive Hgg card and all six H4l cards are reproduced byte for byte, and the
combined / single-channel inclusive cards are identical up to the (unordered) `group` lines of combineCards.

BR rows w.r.t. the first combination cards (and `prepare_total_xsec_datacard.py`): own-channel term
`HiggsDecayWidthTHU_hgg` 1.00998 (was 1.0023), `param_mq` with the physical sign, correlated with H4l.

## Validation (`combination/validation/`)

| script | checks |
|---|---|
| `check_inputs.py <obs> <year> <sample>` | per-bin-out trees vs the October trees event by event (in codes unchanged, out events split), codes vs the gen-variable definition of `differentialProcTable_`; env `WT OCT PBO [MCSUB]` |
| `check_trees2ws.py <obs> <ws dir> <tree file> <prod> <mass>` | Trees2WS per-bin nominal and systematic datasets vs an uproot count of the trees |
| `check_cards.py <new card> <HIG-26-007 card>` | in-processes: jet lnN, photon constants, normalisations equal; sum of per-bin outs == single out; capped photon constants vs the reference |

## Pitfalls seen

- a new FinalFits checkout needs `make` in `Background/` (fTest), otherwise every background job fails (exit 127)
- PTJ0 first bin is `m10000p0_30p0` (cards, maps and `combineVariableDict` override in `commonObjects.py`)
- law runs started with `setsid`; stop them with `kill -- -<pgid>`, otherwise the luigi workers keep submitting
