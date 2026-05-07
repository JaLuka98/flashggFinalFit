#!/bin/bash

# Submit the 2022+2023+2024 PTH uuH differential expected scan.

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src
PTH_OUTPUT=${FLASHGG_DIR}/output_2022_2023_2024_PTH_old_21_04_26

WORKSPACE=${PTH_OUTPUT}/Combine/LightQuarks_kappau_uuH_Datacard_PTH_2022_2023_2024.root
OUTPUT_DIR=${PTH_OUTPUT}/LightQuarks_limits_kappau_uuH_PTH_2022_2023_2024_condor

SCAN_RANGE="kappa_u=-2,2"
SCAN_POINTS=21
SPLIT_POINTS=1
MASS=125.38
MEMORY=12000
JOB_FLAVOUR=workday
CONDOR_OPTS="request_memory = ${MEMORY}
+JobFlavour = \"${JOB_FLAVOUR}\""
TASK_NAME=LightQuarks_2022_2023_2024_PTH_uuH_kappau_scan
COMBINE_NAME=LightQuarks_2022_2023_2024_PTH_uuH_kappau_expected
MERGED_OUTPUT=merged_${COMBINE_NAME}.root

if [ ! -f "${WORKSPACE}" ]; then
    echo "ERROR: workspace not found:"
    echo "  ${WORKSPACE}"
    echo "Build it first with:"
    echo "  bash light_quarks/differential_22_23_24/uuH/light_quarks_t2w_differential_uuH_2022_2023_2024.sh"
    exit 1
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}
mkdir -p ${OUTPUT_DIR}
cd ${OUTPUT_DIR}

echo "Submitting 2022+2023+2024 PTH uuH scan"
echo "Workspace: ${WORKSPACE}"
echo "Output:    ${OUTPUT_DIR}"
echo "Range:     ${SCAN_RANGE}"
echo "Points:    ${SCAN_POINTS}"
echo "Memory:    ${MEMORY} MB"

combineTool.py -M MultiDimFit \
    ${WORKSPACE} \
    --algo grid \
    --points ${SCAN_POINTS} \
    --alignEdges 1 \
    --split-points ${SPLIT_POINTS} \
    --setParameterRanges ${SCAN_RANGE} \
    --setParameters kappa_u=0 \
    --redefineSignalPOIs kappa_u \
    -t -1 \
    -m ${MASS} \
    --saveNLL \
    --freezeParameters MH \
    --cminDefaultMinimizerAlgo Simplex \
    --cminDefaultMinimizerStrategy 0 \
    --cminFallbackAlgo Minuit2,Migrad,0:0.1 \
    --cminApproxPreFitTolerance 0.01 \
    --X-rtd MINIMIZER_freezeDisassociatedParams \
    --X-rtd MINIMIZER_multiMin_hideConstants \
    --X-rtd MINIMIZER_multiMin_maskConstraints \
    --X-rtd MINIMIZER_multiMin_maskChannels=2 \
    --name ${COMBINE_NAME} \
    --job-mode condor \
    --task-name ${TASK_NAME} \
    --sub-opts "${CONDOR_OPTS}"

echo "Submitted. Merge and plot later with:"
echo "  bash ${FLASHGG_DIR}/light_quarks/differential_22_23_24/uuH/light_quarks_hadd_plot_differential_uuH_2022_2023_2024.sh"
