#!/bin/bash

# Submit the 2024 PTH three-flavor differential (rate+BR) NLL scan over
# kappa_u to Condor. kappa_s and kappa_d are profiled at every scan point.
#
# Build the workspace first with:
#   bash light_quarks/floating_all_scenario/t2w_three_flavor_differential.sh
#
# Usage:
#   bash light_quarks/floating_all_scenario/run_limits_kappau_differential_condor.sh

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

PTH_OUTPUT=${FLASHGG_DIR}/outputs_run2_bins_20_04_2026/output_2024_PTH_htcondor_out_fiducial
WORKSPACE=${PTH_OUTPUT}/Combine/LightQuarks_three_flavor_Datacard_PTH_2024.root
OUTPUT_DIR=${PTH_OUTPUT}/LightQuarks_floating_all_kappau_differential_condor

SCAN_POINTS=21
SPLIT_POINTS=1
MASS=125.38
JOB_FLAVOUR=workday
TASK_NAME=LightQuarks_2024_PTH_three_flavor_diff_kappau_scan
COMBINE_NAME=LightQuarks_2024_PTH_three_flavor_diff_kappau_expected
MERGED_OUTPUT=merged_LightQuarks_2024_PTH_three_flavor_diff_kappau_expected.root

if [ ! -f "${WORKSPACE}" ]; then
    echo "ERROR: workspace not found:"
    echo "  ${WORKSPACE}"
    echo "Build it first with:"
    echo "  bash light_quarks/floating_all_scenario/t2w_three_flavor_differential.sh"
    exit 1
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

mkdir -p ${OUTPUT_DIR}
cd ${OUTPUT_DIR}

echo "============================================================"
echo " Three-flavor differential scan: kappa_u"
echo " (profiling kappa_s, kappa_d)"
echo "============================================================"
echo " Workspace:   ${WORKSPACE}"
echo " Output dir:  ${OUTPUT_DIR}"
echo " Scan points: ${SCAN_POINTS}  (one per Condor job)"
echo " POI scanned: kappa_u  in [-3, 3]"
echo " Profiled:    kappa_s, kappa_d"
echo " Flavour:     ${JOB_FLAVOUR}"
echo "============================================================"
echo ""
echo "Submitting to Condor..."

combineTool.py -M MultiDimFit \
    ${WORKSPACE} \
    --algo grid \
    --points ${SCAN_POINTS} \
    --alignEdges 1 \
    --split-points ${SPLIT_POINTS} \
    --setParameterRanges "kappa_s=-2,2:kappa_u=-2,2:kappa_d=-2,2" \
    --setParameters kappa_s=0,kappa_u=0,kappa_d=0 \
    --redefineSignalPOIs kappa_u \
    -t -1 \
    -m ${MASS} \
    --saveNLL \
    --trackParameters kappa_s,kappa_d \
    --cminDefaultMinimizerStrategy 0 \
    --cminApproxPreFitTolerance 0.001 \
    --name ${COMBINE_NAME} \
    --job-mode condor \
    --task-name ${TASK_NAME} \
    --sub-opts='+JobFlavour = "'${JOB_FLAVOUR}'"'

echo ""
echo "Submitted. Monitor with: condor_q"
echo ""
echo "After all jobs finish, merge with:"
echo "  cd ${OUTPUT_DIR}"
echo "  hadd -f ${MERGED_OUTPUT} higgsCombine${COMBINE_NAME}.POINTS.*.MultiDimFit.mH${MASS}.root"
echo ""
echo "Then plot with:"
echo "  python3 ${FLASHGG_DIR}/light_quarks/plot_kappaq_scan.py \\"
echo "      --input ${OUTPUT_DIR}/${MERGED_OUTPUT} \\"
echo "      --output-dir ${OUTPUT_DIR} \\"
echo "      --poi kappa_u"
set +e
