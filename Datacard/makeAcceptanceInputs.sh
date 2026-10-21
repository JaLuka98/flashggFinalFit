#!/bin/bash
# Produce the HiggsDNA acceptance inputs (fidXS_<obs>_<proc>.py) used by
# addAcceptanceUncertainties.py, with the recipe that reproduces the HIG-26-007
# cards exactly (see ACCEPTANCE_UNCERTAINTIES.md):
#   particleLevel/2026_04_07, 2022 + 2023 only (2024 excluded), geometric
#   fiducial flag, scale envelope {0,1,3,5,7,8}, interpolated to 125.07 GeV.
#
# Usage: makeAcceptanceInputs.sh <output dir> [observable ...]
#   observables: inclusive rapidity PTH NJ PTJ0 MassJ0J1 (default: all)

set -euo pipefail

HIGGSDNA=${HIGGSDNA:-/net/data_cms3a-1/daumann/Hgg-PartialRun3-3A-ETH-Analysis/HiggsDNA}
PARTICLE_LEVEL=${PARTICLE_LEVEL:-/net/data_cms3a-2/nobackup/group_JE_CMS/Hgg_PartialRun3/particleLevel/2026_04_07/}
YEARS=${YEARS:-"2022 2023"}
WORKERS=${WORKERS:-4}
CALC=$HIGGSDNA/higgs_dna/scripts/fiducial/fiducial_xsec_calculator.py

OUTDIR=$(realpath -m "${1:?usage: $0 <output dir> [observable ...]}")
shift
OBSERVABLES=${*:-"inclusive rapidity PTH NJ PTJ0 MassJ0J1"}

# observable -> "<HiggsDNA observable> <bins>"; bins follow the card binning
declare -A SPEC=(
  [inclusive]="GenPTH |0|140000|"
  [rapidity]="GenYH |0.0|0.15|0.3|0.45|0.6|0.75|0.9|1.2|1.6|2.0|2.5|"
  [PTH]="GenPTH |0.0|5.0|10.0|15.0|20.0|25.0|30.0|35.0|45.0|60.0|80.0|100.0|120.0|140.0|170.0|200.0|250.0|350.0|450.0|14000.0|"
  [NJ]="GenNJ |0.0|1.0|2.0|3.0|4.0|100.0|"
  [PTJ0]="GenPTJ0 |-1000.0|30.0|40.0|55.0|75.0|95.0|120.0|150.0|200.0|900.0|"
  [MassJ0J1]="GenMassJ0J1 |-1000.0|0.0|75.0|120.0|180.0|300.0|500.0|1000.0|9900.0|"
)

for obs in $OBSERVABLES; do
  read -r var bins <<< "${SPEC[$obs]:?unknown observable $obs}"
  mkdir -p "$OUTDIR/$obs"
  for proc in ggH VBFH VH ttH; do
    echo "[$obs] $proc ($var, years $YEARS)"
    (cd "$OUTDIR/$obs" && PYTHONPATH=$HIGGSDNA python3 "$CALC" "$PARTICLE_LEVEL" \
        --year $YEARS --era all --process $proc --bin "$bins" --obs "$var" \
        --workers "$WORKERS" > "log_$proc.txt" 2>&1) &
  done
  wait
done
echo "Outputs in $OUTDIR/<observable>/fidXS_<obs>_<proc>.py"
