#!/bin/bash

# Run the kappa_q expected NLL scan for the 2024 PTH differential workspace.
#
# Build the workspace first with:
#   bash light_quarks/light_quarks_t2w_differential.sh
#
# The 95% CL limit is where 2*delta_NLL > 3.84.
# Usage: bash light_quarks/light_quarks_run_limits_differential.sh

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

PTH_OUTPUT=${FLASHGG_DIR}/outputs_run2_bins_20_04_2026/output_2024_PTH_htcondor_out_fiducial
WORKSPACE=${PTH_OUTPUT}/Combine/LightQuarks_kappaq_Datacard_PTH_2024.root
OUTPUT_DIR=${PTH_OUTPUT}/LightQuarks_limits_kappaq_PTH
SCAN_RANGE="kappa_q=-3,3"
SCAN_POINTS=21
MASS=125.38

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

mkdir -p ${OUTPUT_DIR}
cd ${OUTPUT_DIR}

echo "Using workspace: ${WORKSPACE}"
echo "Scan range: ${SCAN_RANGE}  Points: ${SCAN_POINTS}"

echo ""
echo "=== Expected NLL scan (Asimov) ==="
combine -M MultiDimFit \
    --algo grid \
    --points ${SCAN_POINTS} \
    --setParameterRanges ${SCAN_RANGE} \
    --setParameters kappa_q=0 \
    --redefineSignalPOIs kappa_q \
    -t -1 \
    -m ${MASS} \
    --saveNLL \
    --cminDefaultMinimizerStrategy 0 \
    --cminApproxPreFitTolerance 0.01 \
    --name LightQuarks_2024_PTH_expected \
    ${WORKSPACE}

echo ""
echo "=== Done. Output in: ${OUTPUT_DIR} ==="
echo "Limit at 95% CL where 2*deltaNLL > 3.84"
set +e
