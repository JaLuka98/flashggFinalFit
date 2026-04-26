#!/bin/bash

# Run the kappa_q expected NLL scan for the 2024 PTH differential shape-only
# workspace. The model profiles BR_hgg as one free common signal-rate factor
# and scans the PTH-shape distortion from kappa_q.
#
# Build the workspace first with:
#   bash light_quarks/light_quarks_t2w_differential_shape_only.sh
#
# Usage: bash light_quarks/light_quarks_run_limits_differential_shape_only.sh

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

PTH_OUTPUT=${FLASHGG_DIR}/outputs_run2_bins_20_04_2026/output_2024_PTH_htcondor_out_fiducial
WORKSPACE=${PTH_OUTPUT}/Combine/LightQuarks_kappaq_shape_only_Datacard_PTH_2024.root
OUTPUT_DIR=${PTH_OUTPUT}/LightQuarks_limits_kappaq_PTH_shape_only
SCAN_RANGE="kappa_q=-3,3:BR_hgg=0,10"
SCAN_POINTS=21
MASS=125.38
COMBINE_NAME=LightQuarks_2024_PTH_shape_only_expected

if [ ! -f "${WORKSPACE}" ]; then
    echo "ERROR: workspace not found:"
    echo "  ${WORKSPACE}"
    echo "Build it first with:"
    echo "  bash light_quarks/light_quarks_t2w_differential_shape_only.sh"
    exit 1
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

mkdir -p ${OUTPUT_DIR}
cd ${OUTPUT_DIR}

echo "Using workspace: ${WORKSPACE}"
echo "Output dir:      ${OUTPUT_DIR}"
echo "Scan range:      ${SCAN_RANGE}"
echo "Scan points:     ${SCAN_POINTS}"
echo "Shape-only:      profiled BR_hgg common signal rate"

echo ""
echo "=== Expected shape-only NLL scan (Asimov) ==="
combine -M MultiDimFit \
    --algo grid \
    --points ${SCAN_POINTS} \
    --alignEdges 1 \
    --setParameterRanges ${SCAN_RANGE} \
    --setParameters kappa_q=0,BR_hgg=1 \
    --redefineSignalPOIs kappa_q \
    -t -1 \
    -m ${MASS} \
    --saveNLL \
    --trackParameters BR_hgg \
    --cminDefaultMinimizerStrategy 0 \
    --cminApproxPreFitTolerance 0.01 \
    --name ${COMBINE_NAME} \
    ${WORKSPACE}

echo ""
echo "=== Done. Output in: ${OUTPUT_DIR} ==="
echo "Plot with:"
echo "  python3 ${FLASHGG_DIR}/light_quarks/plot_kappaq_scan.py --input ${OUTPUT_DIR}/higgsCombine${COMBINE_NAME}.MultiDimFit.mH${MASS}.root --output-dir ${OUTPUT_DIR}"
set +e
