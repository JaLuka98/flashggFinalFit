#!/bin/bash

# Build the 2022+2023+2024 PTH three-flavor shape-only workspace.

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src
PTH_OUTPUT=${FLASHGG_DIR}/output_2022_2023_2024_PTH_old_21_04_26

DATACARD=${PTH_OUTPUT}/Combine/Datacard_PTH_2022_2023_2024.txt
SHAPE_ONLY_DATACARD=${PTH_OUTPUT}/Combine/Datacard_PTH_2022_2023_2024_three_flavor_shape_only.txt
OUTPUT=${PTH_OUTPUT}/Combine/LightQuarks_three_flavor_shape_only_Datacard_PTH_2022_2023_2024.root

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

echo "Building 2022+2023+2024 PTH three-flavor shape-only workspace"
echo "Base datacard:  ${DATACARD}"
echo "Shape datacard: ${SHAPE_ONLY_DATACARD}"
echo "Workspace:      ${OUTPUT}"

cp ${DATACARD} ${SHAPE_ONLY_DATACARD}
if ! grep -q "^BR_hgg[[:space:]]\\+flatParam" ${SHAPE_ONLY_DATACARD}; then
    {
        echo ""
        echo "# Free common signal-rate factor for three-flavor shape-only scan"
        echo "BR_hgg flatParam"
    } >> ${SHAPE_ONLY_DATACARD}
fi

text2workspace.py ${SHAPE_ONLY_DATACARD} \
    -o ${OUTPUT} \
    -m 125.38 \
    higgsMassRange=122,128 \
    -P light_quarks:light_quarks_three_flavor_shape_only

echo "Done"
