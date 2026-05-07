#!/bin/bash

# Convert the 2022+2023+2024 combined inclusive datacard to a workspace with
# one of the inclusive light-quark physics models.
#
# Usage:
#   bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh kappaq
#   bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh ssH
#   bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh uuH
#   bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh ddH
#   bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh float_all

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

MODE=${1:-kappaq}
INCLUSIVE_OUTPUT=${FLASHGG_DIR}/output_2022_2023_2024_inclusive
DATACARD=${INCLUSIVE_OUTPUT}/Combine/Datacard_2022_2023_2024.txt

case "${MODE}" in
    kappaq)
        MODEL=light_quarks_inclusive
        POIS=kappa_q
        OUTPUT=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappaq_Datacard_2022_2023_2024_inclusive.root
        ;;
    ssH|kappas)
        MODEL=light_quarks_inclusive_ssH
        POIS=kappa_s
        OUTPUT=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappas_Datacard_2022_2023_2024_inclusive.root
        ;;
    uuH|kappau)
        MODEL=light_quarks_inclusive_uuH
        POIS=kappa_u
        OUTPUT=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappau_Datacard_2022_2023_2024_inclusive.root
        ;;
    ddH|kappad)
        MODEL=light_quarks_inclusive_ddH
        POIS=kappa_d
        OUTPUT=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappad_Datacard_2022_2023_2024_inclusive.root
        ;;
    float_all|three_flavor)
        MODEL=light_quarks_three_flavor_inclusive
        POIS=kappa_s,kappa_u,kappa_d
        OUTPUT=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_three_flavor_Datacard_2022_2023_2024_inclusive.root
        ;;
    *)
        echo "ERROR: unknown mode '${MODE}'"
        echo "Valid modes: kappaq, ssH, uuH, ddH, float_all"
        exit 1
        ;;
esac

if [ ! -f "${DATACARD}" ]; then
    echo "ERROR: datacard not found:"
    echo "  ${DATACARD}"
    exit 1
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

export PYTHONPATH=${FLASHGG_DIR}/light_quarks:${PYTHONPATH}
export PYTHON3PATH=${FLASHGG_DIR}/light_quarks:${PYTHON3PATH}

echo "============================================================"
echo " Inclusive light-quark text2workspace (2022+2023+2024)"
echo "============================================================"
echo " Mode:             ${MODE}"
echo " Datacard:         ${DATACARD}"
echo " Output workspace: ${OUTPUT}"
echo " Physics model:    ${MODEL}"
echo " POIs:             ${POIS}"
echo "============================================================"

text2workspace.py ${DATACARD} \
    -o ${OUTPUT} \
    -m 125.38 \
    higgsMassRange=122,128 \
    -P light_quarks:${MODEL}

echo ""
echo "Done. Workspace saved to:"
echo "  ${OUTPUT}"
echo ""
echo "Next step:"
if [ "${MODE}" = "float_all" ] || [ "${MODE}" = "three_flavor" ]; then
    echo "  bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappas"
    echo "  bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappau"
    echo "  bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappad"
else
    echo "  bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh ${MODE}"
fi
set +e
