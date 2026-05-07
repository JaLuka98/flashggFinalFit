#!/bin/bash

# Merge and plot the 2022+2023+2024 PTH ddH differential shape-only scan.

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src
PTH_OUTPUT=${FLASHGG_DIR}/output_2022_2023_2024_PTH_old_21_04_26

OUTPUT_DIR=${PTH_OUTPUT}/LightQuarks_limits_kappad_ddH_PTH_shape_only_2022_2023_2024_condor
COMBINE_NAME=LightQuarks_2022_2023_2024_PTH_ddH_shape_only_kappad_expected
MERGED_OUTPUT=merged_${COMBINE_NAME}.root
MASS=125.38
SCAN_POINTS=${1:-auto}
POI=kappa_d

if [ ! -d "${OUTPUT_DIR}" ]; then
    echo "ERROR: output directory not found:"
    echo "  ${OUTPUT_DIR}"
    exit 1
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${OUTPUT_DIR}

INPUT_FILES=""
PLOT_INPUT_DIR=$(mktemp -d /tmp/${COMBINE_NAME}_plot_XXXXXX)
trap 'rm -rf "${PLOT_INPUT_DIR}"' EXIT

if [ "${SCAN_POINTS}" = "auto" ]; then
    POINTS=$(ls higgsCombine${COMBINE_NAME}.POINTS.*.*.MultiDimFit.mH${MASS}.root 2>/dev/null | sed -n 's/.*POINTS\.\([0-9][0-9]*\)\.\1\.MultiDimFit.*/\1/p' | sort -n)
else
    POINTS=$(seq 0 $((SCAN_POINTS - 1)))
fi

USED_POINTS=0
for POINT in ${POINTS}; do
    FILE=higgsCombine${COMBINE_NAME}.POINTS.${POINT}.${POINT}.MultiDimFit.mH${MASS}.root
    if [ ! -s "${FILE}" ]; then
        echo "WARNING: skipping missing or empty scan file:"
        echo "  ${OUTPUT_DIR}/${FILE}"
        continue
    fi
    if ! python3 -c "import sys, uproot; f=uproot.open(sys.argv[1]); t=f['limit']; a=t.arrays(['${POI}','quantileExpected'], library='np'); assert len(a['${POI}'][a['quantileExpected'] > -0.5]) > 0" "${FILE}" >/dev/null 2>&1; then
        echo "WARNING: skipping incomplete scan file:"
        echo "  ${OUTPUT_DIR}/${FILE}"
        continue
    fi
    INPUT_FILES="${INPUT_FILES} ${FILE}"
    ln -sf ${OUTPUT_DIR}/${FILE} ${PLOT_INPUT_DIR}/${FILE}
    USED_POINTS=$((USED_POINTS + 1))
done

if [ ${USED_POINTS} -lt 2 ]; then
    echo "ERROR: need at least two complete scan points to plot; found ${USED_POINTS}"
    exit 1
fi

echo "Merging ${USED_POINTS} complete scan files"
echo "Output: ${OUTPUT_DIR}/${MERGED_OUTPUT}"
hadd -f ${MERGED_OUTPUT} ${INPUT_FILES}

echo "Plotting"
python3 ${FLASHGG_DIR}/light_quarks/plot_kappaq_scan.py \
    --input ${PLOT_INPUT_DIR} \
    --output-dir ${OUTPUT_DIR} \
    --mode differential \
    --poi ${POI}

echo "Done"
