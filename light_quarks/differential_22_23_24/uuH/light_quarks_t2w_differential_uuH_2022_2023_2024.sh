#!/bin/bash

# Build the 2022+2023+2024 PTH uuH differential workspace.

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src
PTH_OUTPUT=${FLASHGG_DIR}/output_2022_2023_2024_PTH_old_21_04_26

DATACARD=${PTH_OUTPUT}/Combine/Datacard_PTH_2022_2023_2024.txt
OUTPUT=${PTH_OUTPUT}/Combine/LightQuarks_kappau_uuH_Datacard_PTH_2022_2023_2024.root

if [ ! -f "${DATACARD}" ]; then
    echo "ERROR: datacard not found:"
    echo "  ${DATACARD}"
    exit 1
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}
export PYTHONPATH=${FLASHGG_DIR}/light_quarks:${PYTHONPATH}
export PYTHON3PATH=${FLASHGG_DIR}/light_quarks:${PYTHON3PATH}

echo "Building 2022+2023+2024 PTH uuH differential workspace"
echo "Datacard:  ${DATACARD}"
echo "Output:    ${OUTPUT}"

text2workspace.py ${DATACARD} \
    -o ${OUTPUT} \
    -m 125.38 \
    higgsMassRange=122,128 \
    -P light_quarks:light_quarks_differential_uuH

echo "Done: ${OUTPUT}"
