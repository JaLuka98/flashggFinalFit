#!/bin/bash

# Convert the 2024 PTH datacard to a workspace with the three-flavor
# light-quark shape-only physics model (kappa_u, kappa_d, kappa_s all free).
#
# Physics model: light_quarks.py::light_quarks_three_flavor_shape_only
# POIs:          kappa_s, kappa_u, kappa_d
# Shape-only:    one free global BR_hgg factor absorbs the overall
#                rate/BR uncertainty; PTH shape drives the constraint.
#
# Run this script ONCE before submitting any of the three scan scripts.
#
# Usage:
#   bash light_quarks/floating_all_scenario/t2w_three_flavor_shape_only.sh

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

PTH_OUTPUT=${FLASHGG_DIR}/outputs_run2_bins_20_04_2026/output_2024_PTH_htcondor_out_fiducial
DATACARD=${PTH_OUTPUT}/Combine/Datacard_PTH_2024.txt
SHAPE_ONLY_DATACARD=${PTH_OUTPUT}/Combine/Datacard_PTH_2024_three_flavor_shape_only.txt
OUTPUT=${PTH_OUTPUT}/Combine/LightQuarks_three_flavor_shape_only_Datacard_PTH_2024.root

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
echo " Three-flavor light-quark shape-only text2workspace"
echo "============================================================"
echo " Base datacard:    ${DATACARD}"
echo " Shape datacard:   ${SHAPE_ONLY_DATACARD}"
echo " Output workspace: ${OUTPUT}"
echo " Physics model:    light_quarks_three_flavor_shape_only"
echo " POIs:             kappa_s, kappa_u, kappa_d"
echo " Free nuisance:    BR_hgg (common signal-rate factor)"
echo "============================================================"

# Copy the base datacard and add BR_hgg as a flatParam if not already present
cp ${DATACARD} ${SHAPE_ONLY_DATACARD}
if ! grep -q "^BR_hgg[[:space:]]\+flatParam" ${SHAPE_ONLY_DATACARD}; then
    {
        echo ""
        echo "# Free common signal-rate factor for three-flavor shape-only scan"
        echo "BR_hgg flatParam"
    } >> ${SHAPE_ONLY_DATACARD}
    echo "Added BR_hgg flatParam to shape-only datacard."
else
    echo "BR_hgg flatParam already present in datacard."
fi

text2workspace.py ${SHAPE_ONLY_DATACARD} \
    -o ${OUTPUT} \
    -m 125.38 \
    --PO higgsMassRange=122,128 \
    -P light_quarks:light_quarks_three_flavor_shape_only

echo ""
echo "Done. Workspace saved to:"
echo "  ${OUTPUT}"
echo ""
echo "Next steps — submit the three scan scripts:"
echo "  bash light_quarks/floating_all_scenario/run_limits_kappas_condor.sh"
echo "  bash light_quarks/floating_all_scenario/run_limits_kappau_condor.sh"
echo "  bash light_quarks/floating_all_scenario/run_limits_kappad_condor.sh"
set +e
