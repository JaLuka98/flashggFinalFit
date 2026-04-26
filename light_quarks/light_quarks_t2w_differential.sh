#!/bin/bash

# Convert the 2024 PTH datacard to a workspace with the differential
# light-quark physics model.
#
# Physics model: light_quarks.py::light_quarks_differential
# POI: kappa_q
# BSM/SM production term: read from SM JSON and ssH CSV in light_quarks/
# Usage: bash light_quarks/light_quarks_t2w_differential.sh

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

PTH_OUTPUT=${FLASHGG_DIR}/outputs_run2_bins_20_04_2026/output_2024_PTH_htcondor_out_fiducial
DATACARD=${PTH_OUTPUT}/Combine/Datacard_PTH_2024.txt
OUTPUT=${PTH_OUTPUT}/Combine/LightQuarks_kappaq_Datacard_PTH_2024.root

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

export PYTHONPATH=${FLASHGG_DIR}/light_quarks:${PYTHONPATH}
export PYTHON3PATH=${FLASHGG_DIR}/light_quarks:${PYTHON3PATH}

echo "Running text2workspace on: ${DATACARD}"
echo "Output workspace:          ${OUTPUT}"

text2workspace.py ${DATACARD} \
    -o ${OUTPUT} \
    -m 125.38 \
    higgsMassRange=122,128 \
    -P light_quarks:light_quarks_differential

echo "Done. Workspace saved to: ${OUTPUT}"
set +e
