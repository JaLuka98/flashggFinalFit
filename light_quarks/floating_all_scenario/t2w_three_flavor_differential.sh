#!/bin/bash

# Convert the 2024 PTH datacard to a workspace with the three-flavor
# differential (full rate + BR) physics model.
#
# Physics model: light_quarks.py::light_quarks_three_flavor_differential
# POIs:          kappa_s, kappa_u, kappa_d
# Formula per bin:
#   mu_i = (1 + A_ssH_i*ks^2 + A_uuH_i*ku^2 + A_ddH_i*kd^2)
#          / (1 + B_width*(ks^2 + ku^2 + kd^2))
#
# Unlike the shape-only version, this model is sensitive to both the PTH
# shape AND the overall rate/BR via the denominator.
#
# Run this script ONCE before submitting the three scan scripts.
#
# Usage:
#   bash light_quarks/floating_all_scenario/t2w_three_flavor_differential.sh

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

PTH_OUTPUT=${FLASHGG_DIR}/outputs_run2_bins_20_04_2026/output_2024_PTH_htcondor_out_fiducial
DATACARD=${PTH_OUTPUT}/Combine/Datacard_PTH_2024.txt
OUTPUT=${PTH_OUTPUT}/Combine/LightQuarks_three_flavor_Datacard_PTH_2024.root

if [ ! -f "${DATACARD}" ]; then
    echo "ERROR: base datacard not found:"
    echo "  ${DATACARD}"
    exit 1
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

export PYTHONPATH=${FLASHGG_DIR}/light_quarks:${PYTHONPATH}
export PYTHON3PATH=${FLASHGG_DIR}/light_quarks:${PYTHON3PATH}

echo "============================================================"
echo " Three-flavor differential (rate+BR) text2workspace"
echo "============================================================"
echo " Datacard:         ${DATACARD}"
echo " Output workspace: ${OUTPUT}"
echo " Physics model:    light_quarks_three_flavor_differential"
echo " POIs:             kappa_s, kappa_u, kappa_d"
echo " Denominator:      1 + B_width*(ks^2 + ku^2 + kd^2)"
echo "============================================================"

text2workspace.py ${DATACARD} \
    -o ${OUTPUT} \
    -m 125.38 \
    higgsMassRange=122,128 \
    -P light_quarks:light_quarks_three_flavor_differential

echo ""
echo "Done. Workspace saved to:"
echo "  ${OUTPUT}"
echo ""
echo "Next steps — submit the three scan scripts:"
echo "  bash light_quarks/floating_all_scenario/run_limits_kappas_differential_condor.sh"
echo "  bash light_quarks/floating_all_scenario/run_limits_kappau_differential_condor.sh"
echo "  bash light_quarks/floating_all_scenario/run_limits_kappad_differential_condor.sh"
set +e
