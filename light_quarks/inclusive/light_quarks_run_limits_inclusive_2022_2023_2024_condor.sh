#!/bin/bash

# Submit the 2022+2023+2024 combined inclusive expected NLL scans to Condor.
# One scan point is submitted per Condor job.
#
# Usage:
#   bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh kappaq
#   bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh ssH
#   bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh uuH
#   bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh ddH
#   bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappas
#   bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappau
#   bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappad

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

MODE=${1:-kappaq}
INCLUSIVE_OUTPUT=${FLASHGG_DIR}/output_2022_2023_2024_inclusive

SCAN_POINTS=30
SPLIT_POINTS=1
MASS=125.38
JOB_FLAVOUR=workday

case "${MODE}" in
    kappaq)
        WORKSPACE=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappaq_Datacard_2022_2023_2024_inclusive.root
        OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappaq_inclusive_condor
        SCAN_RANGE="kappa_q=-1,1"
        SET_PARAMETERS="kappa_q=0.0"
        SCAN_POI=kappa_q
        TRACK_PARAMETERS=""
        TASK_NAME=LightQuarks_2022_2023_2024_inclusive_kappaq_scan
        COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappaq_expected
        ;;
    ssH|kappas)
        WORKSPACE=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappas_Datacard_2022_2023_2024_inclusive.root
        OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappas_inclusive_condor
        SCAN_RANGE="kappa_s=-1,1"
        SET_PARAMETERS="kappa_s=0.0"
        SCAN_POI=kappa_s
        TRACK_PARAMETERS=""
        TASK_NAME=LightQuarks_2022_2023_2024_inclusive_kappas_scan
        COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappas_expected
        ;;
    uuH|kappau)
        WORKSPACE=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappau_Datacard_2022_2023_2024_inclusive.root
        OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappau_inclusive_condor
        SCAN_RANGE="kappa_u=-1,1"
        SET_PARAMETERS="kappa_u=0.0"
        SCAN_POI=kappa_u
        TRACK_PARAMETERS=""
        TASK_NAME=LightQuarks_2022_2023_2024_inclusive_kappau_scan
        COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappau_expected
        ;;
    ddH|kappad)
        WORKSPACE=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_kappad_Datacard_2022_2023_2024_inclusive.root
        OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappad_inclusive_condor
        SCAN_RANGE="kappa_d=-1,1"
        SET_PARAMETERS="kappa_d=0.0"
        SCAN_POI=kappa_d
        TRACK_PARAMETERS=""
        TASK_NAME=LightQuarks_2022_2023_2024_inclusive_kappad_scan
        COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappad_expected
        ;;
    float_all_kappas)
        WORKSPACE=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_three_flavor_Datacard_2022_2023_2024_inclusive.root
        OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_float_all_inclusive_kappas_condor
        SCAN_RANGE="kappa_s=-1,1:kappa_u=-1,1:kappa_d=-1,1"
        SET_PARAMETERS="kappa_s=0.0,kappa_u=0.0,kappa_d=0.0"
        SCAN_POI=kappa_s
        TRACK_PARAMETERS="--trackParameters kappa_u,kappa_d"
        TASK_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappas_scan
        COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappas_expected
        ;;
    float_all_kappau)
        WORKSPACE=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_three_flavor_Datacard_2022_2023_2024_inclusive.root
        OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_float_all_inclusive_kappau_condor
        SCAN_RANGE="kappa_s=-1,1:kappa_u=-1,1:kappa_d=-1,1"
        SET_PARAMETERS="kappa_s=0.0,kappa_u=0.0,kappa_d=0.0"
        SCAN_POI=kappa_u
        TRACK_PARAMETERS="--trackParameters kappa_s,kappa_d"
        TASK_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappau_scan
        COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappau_expected
        ;;
    float_all_kappad)
        WORKSPACE=${INCLUSIVE_OUTPUT}/Combine/LightQuarks_three_flavor_Datacard_2022_2023_2024_inclusive.root
        OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_float_all_inclusive_kappad_condor
        SCAN_RANGE="kappa_s=-1,1:kappa_u=-1,1:kappa_d=-1,1"
        SET_PARAMETERS="kappa_s=0.0,kappa_u=0.0,kappa_d=0.0"
        SCAN_POI=kappa_d
        TRACK_PARAMETERS="--trackParameters kappa_s,kappa_u"
        TASK_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappad_scan
        COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappad_expected
        ;;
    *)
        echo "ERROR: unknown mode '${MODE}'"
        echo "Valid modes: kappaq, ssH, uuH, ddH, float_all_kappas, float_all_kappau, float_all_kappad"
        exit 1
        ;;
esac

MERGED_OUTPUT=merged_${COMBINE_NAME}.root

if [ ! -f "${WORKSPACE}" ]; then
    echo "ERROR: workspace not found:"
    echo "  ${WORKSPACE}"
    echo "Build it first with:"
    if [[ "${MODE}" == float_all_* ]]; then
        echo "  bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh float_all"
    else
        echo "  bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh ${MODE}"
    fi
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
echo " Inclusive light-quark scan (2022+2023+2024)"
echo "============================================================"
echo " Mode:         ${MODE}"
echo " Workspace:    ${WORKSPACE}"
echo " Output dir:   ${OUTPUT_DIR}"
echo " Scan POI:     ${SCAN_POI}"
echo " Scan range:   ${SCAN_RANGE}"
echo " Scan points:  ${SCAN_POINTS}  (one per Condor job)"
echo " Flavour:      ${JOB_FLAVOUR}"
echo "============================================================"
echo ""
echo "Submitting to Condor..."

combineTool.py -M MultiDimFit \
    ${WORKSPACE} \
    --algo grid \
    --points ${SCAN_POINTS} \
    --alignEdges 1 \
    --split-points ${SPLIT_POINTS} \
    --setParameterRanges ${SCAN_RANGE} \
    --setParameters ${SET_PARAMETERS} \
    --redefineSignalPOIs ${SCAN_POI} \
    -t -1 \
    -m ${MASS} \
    --saveNLL \
    --freezeParameters MH \
    ${TRACK_PARAMETERS} \
    --cminDefaultMinimizerStrategy 2 \
    --cminFallbackAlgo Minuit2,Migrad,0:0.1 \
    --cminApproxPreFitTolerance 0.01 \
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
echo "      --mode inclusive \\"
echo "      --poi ${SCAN_POI}"
set +e

#     --cminDefaultMinimizerAlgo Simplex \