#!/bin/bash

# Convert the 2024 inclusive datacard to a workspace with the light quark physics model.
# Physics model: light_quarks.py::light_quarks_inclusive
# POI: kappa_q
# Usage: bash light_quarks_t2w_inclusive.sh

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

DATACARD=${FLASHGG_DIR}/output_Zmmg_SaS_opt_bound/2024_inclusive/Combine/Datacard_2024.txt
OUTPUT=${FLASHGG_DIR}/output_Zmmg_SaS_opt_bound/2024_inclusive/Combine/LightQuarks_kappaq_Datacard_2024_inclusive.root

# Set up CMSSW environment
cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

export PYTHON3PATH=${PYTHON3PATH}:${FLASHGG_DIR}/light_quarks

echo "Running text2workspace on: ${DATACARD}"
echo "Output workspace:          ${OUTPUT}"

text2workspace.py ${DATACARD} \
    -o ${OUTPUT} \
    -m 125.38 \
    higgsMassRange=122,128 \
    -P light_quarks:light_quarks_inclusive

echo "Done. Workspace saved to: ${OUTPUT}"
