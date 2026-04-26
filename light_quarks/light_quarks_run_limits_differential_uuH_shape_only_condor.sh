#!/bin/bash

# Submit the 2024 PTH differential shape-only kappa_u expected NLL scan to Condor.
#
# Build the workspace first with:
#   bash light_quarks/light_quarks_t2w_differential_uuH_shape_only.sh
#
# Usage:
#   bash light_quarks/light_quarks_run_limits_differential_uuH_shape_only_condor.sh

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

PTH_OUTPUT=${FLASHGG_DIR}/outputs_run2_bins_20_04_2026/output_2024_PTH_htcondor_out_fiducial
WORKSPACE=${PTH_OUTPUT}/Combine/LightQuarks_kappau_shape_only_Datacard_PTH_2024.root
OUTPUT_DIR=${PTH_OUTPUT}/LightQuarks_limits_kappau_PTH_shape_only_condor
SCAN_RANGE="kappa_u=-3,3:BR_hgg=0,10"
SCAN_POINTS=21
SPLIT_POINTS=1
MASS=125.38
JOB_FLAVOUR=workday
TASK_NAME=LightQuarks_2024_PTH_shape_only_kappau_scan
COMBINE_NAME=LightQuarks_2024_PTH_shape_only_kappau_expected
MERGED_OUTPUT=merged_LightQuarks_2024_PTH_shape_only_kappau_expected.root

if [ ! -f "${WORKSPACE}" ]; then
    echo "ERROR: workspace not found:"
    echo "  ${WORKSPACE}"
    echo "Build it first with:"
    echo "  bash light_quarks/light_quarks_t2w_differential_uuH_shape_only.sh"
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
echo "Split points:    ${SPLIT_POINTS}"
echo "Condor flavour:  ${JOB_FLAVOUR}"
echo "Shape-only:      profiled BR_hgg common signal rate"
echo ""
echo "Submitting split uuH shape-only grid scan to Condor..."

combineTool.py -M MultiDimFit \
    ${WORKSPACE} \
    --algo grid \
    --points ${SCAN_POINTS} \
    --alignEdges 1 \
    --split-points ${SPLIT_POINTS} \
    --setParameterRanges ${SCAN_RANGE} \
    --setParameters kappa_u=0,BR_hgg=1 \
    --redefineSignalPOIs kappa_u \
    -t -1 \
    -m ${MASS} \
    --saveNLL \
    --trackParameters BR_hgg \
    --cminDefaultMinimizerStrategy 0 \
    --cminApproxPreFitTolerance 0.01 \
    --name ${COMBINE_NAME} \
    --job-mode condor \
    --task-name ${TASK_NAME} \
    --sub-opts='+JobFlavour = "'${JOB_FLAVOUR}'"'

echo ""
echo "Submitted. Monitor jobs with:"
echo "  condor_q"
echo ""
echo "After all jobs finish, merge outputs with:"
echo "  cd ${OUTPUT_DIR}"
echo "  hadd -f ${MERGED_OUTPUT} higgsCombine${COMBINE_NAME}.POINTS.*.MultiDimFit.mH${MASS}.root"
echo ""
echo "Then plot with:"
echo "  python3 ${FLASHGG_DIR}/light_quarks/plot_kappaq_scan.py --input ${OUTPUT_DIR}/${MERGED_OUTPUT} --output-dir ${OUTPUT_DIR} --poi kappa_u"
set +e
