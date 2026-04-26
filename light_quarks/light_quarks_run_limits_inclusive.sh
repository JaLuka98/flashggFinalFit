#!/bin/bash

# Run kappa_q limits for light quark enhanced Higgs coupling using 2022 inclusive workspace.
#
# Steps:
#   1. Best-fit kappa_q (singles)
#   2. NLL scan over kappa_q (Asimov / expected)
#   3. NLL scan over kappa_q (observed)
#
# The 95% CL limit is where 2*delta_NLL > 3.84.
# Collect scan output with: hadd merged_scan.root higgsCombine*.MultiDimFit.*.root
#
# Usage: bash light_quarks_run_limits_inclusive.sh

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/flashggFinalFit
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src
WORKSPACE=${FLASHGG_DIR}/output_Zmmg_SaS_opt_bound/2024_inclusive/Combine/LightQuarks_kappaq_Datacard_2024_inclusive.root
OUTPUT_DIR=${FLASHGG_DIR}/output_Zmmg_SaS_opt_bound/2024_inclusive/LightQuarks_limits_kappaq
SCAN_RANGE="kappa_q=0,3"
SCAN_POINTS=20
MASS=125.38

# Set up CMSSW environment
cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd ${FLASHGG_DIR}

mkdir -p ${OUTPUT_DIR}
cd ${OUTPUT_DIR}

echo "Using workspace: ${WORKSPACE}"
echo "Scan range: ${SCAN_RANGE}  Points: ${SCAN_POINTS}"

# -----------------------------------------------------------------------
# Expected NLL scan (Asimov, SM-injected: kappa_q=0 => mu=1)
# Note: --expectSignal only works with the default "r" POI; for custom
# POIs use --setParameters to inject the SM hypothesis (kappa_q=0).
# -----------------------------------------------------------------------
echo ""
echo "=== Expected NLL scan (Asimov) ==="
combine -M MultiDimFit \
    --algo grid \
    --points ${SCAN_POINTS} \
    --setParameterRanges ${SCAN_RANGE} \
    --setParameters kappa_q=0 \
    --redefineSignalPOIs kappa_q \
    -t -1 \
    -m ${MASS} \
    --saveNLL \
    --cminDefaultMinimizerStrategy 0 \
    --cminApproxPreFitTolerance 0.01 \
    --name LightQuarks_2022_expected \
    ${WORKSPACE}

echo ""
echo "=== Done. Output in: ${OUTPUT_DIR} ==="
echo "To plot: python3 light_quarks/plot_kappaq_scan.py"
echo "Limit at 95% CL where 2*deltaNLL > 3.84"
