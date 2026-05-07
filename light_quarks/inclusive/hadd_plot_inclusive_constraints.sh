#!/bin/bash

# Merge and plot inclusive light-quark scans after the Condor jobs finish.
#
# Usage:
#   bash light_quarks/inclusive/hadd_plot_inclusive_constraints.sh
#   bash light_quarks/inclusive/hadd_plot_inclusive_constraints.sh ssH
#   bash light_quarks/inclusive/hadd_plot_inclusive_constraints.sh float_all_kappas
#
# With no argument, this processes the same six modes submitted by
# run_inclusive_constraints.sh.

set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
FLASHGG_DIR=$(cd "${SCRIPT_DIR}/../.." && pwd)
CMSSW_SRC=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src

INCLUSIVE_OUTPUT=${FLASHGG_DIR}/output_2022_2023_2024_inclusive
MASS=125.38
SCAN_POINTS=30

if [ "$#" -gt 0 ]; then
    MODES=("$@")
else
    MODES=(ssH uuH ddH float_all_kappas float_all_kappau float_all_kappad)
fi

cd ${CMSSW_SRC}
export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"
source ${VO_CMS_SW_DIR}/cmsset_default.sh
cmsenv

cd "${FLASHGG_DIR}"

configure_mode() {
    local mode=$1

    case "${mode}" in
        kappaq)
            OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappaq_inclusive_condor
            COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappaq_expected
            POI=kappa_q
            ;;
        ssH|kappas)
            OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappas_inclusive_condor
            COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappas_expected
            POI=kappa_s
            ;;
        uuH|kappau)
            OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappau_inclusive_condor
            COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappau_expected
            POI=kappa_u
            ;;
        ddH|kappad)
            OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_limits_kappad_inclusive_condor
            COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_kappad_expected
            POI=kappa_d
            ;;
        float_all_kappas)
            OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_float_all_inclusive_kappas_condor
            COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappas_expected
            POI=kappa_s
            ;;
        float_all_kappau)
            OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_float_all_inclusive_kappau_condor
            COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappau_expected
            POI=kappa_u
            ;;
        float_all_kappad)
            OUTPUT_DIR=${INCLUSIVE_OUTPUT}/LightQuarks_float_all_inclusive_kappad_condor
            COMBINE_NAME=LightQuarks_2022_2023_2024_inclusive_float_all_kappad_expected
            POI=kappa_d
            ;;
        *)
            echo "ERROR: unknown mode '${mode}'"
            echo "Valid modes: kappaq, ssH, uuH, ddH, float_all_kappas, float_all_kappau, float_all_kappad"
            return 1
            ;;
    esac

    MERGED_OUTPUT=merged_${COMBINE_NAME}.root
}

check_scan_files() {
    python3 - "$SCAN_POINTS" "$@" <<'PY'
import os
import sys

expected = int(sys.argv[1])
files = sys.argv[2:]

if len(files) != expected:
    print("ERROR: expected %d scan files, found %d" % (expected, len(files)))
    sys.exit(1)

try:
    import uproot
except Exception as exc:
    print("ERROR: could not import uproot: %s" % exc)
    sys.exit(1)

bad = []
for path in files:
    try:
        root_file = uproot.open(path)
        if "limit" not in [key.split(";")[0] for key in root_file.keys()]:
            bad.append((path, "missing limit tree"))
            continue
        entries = root_file["limit"].num_entries
        if entries < 1:
            bad.append((path, "limit tree has %d entries" % entries))
    except Exception as exc:
        bad.append((path, str(exc)))

if bad:
    for path, reason in bad:
        print("ERROR: bad scan file: %s (%s)" % (os.path.basename(path), reason))
    sys.exit(1)
PY
}

for MODE in "${MODES[@]}"; do
    configure_mode "${MODE}"

    echo "============================================================"
    echo " Merge and plot inclusive scan"
    echo "============================================================"
    echo " Mode:       ${MODE}"
    echo " Output dir: ${OUTPUT_DIR}"
    echo " POI:        ${POI}"
    echo "============================================================"

    if [ ! -d "${OUTPUT_DIR}" ]; then
        echo "WARNING: output directory does not exist, skipping:"
        echo "  ${OUTPUT_DIR}"
        continue
    fi

    shopt -s nullglob
    FILES=("${OUTPUT_DIR}"/higgsCombine"${COMBINE_NAME}".POINTS.*.MultiDimFit.mH"${MASS}".root)
    shopt -u nullglob

    if [ "${#FILES[@]}" -eq 0 ]; then
        echo "WARNING: no split scan files found, skipping."
        echo "Expected pattern:"
        echo "  ${OUTPUT_DIR}/higgsCombine${COMBINE_NAME}.POINTS.*.MultiDimFit.mH${MASS}.root"
        continue
    fi

    if ! check_scan_files "${FILES[@]}"; then
        echo "WARNING: scan is incomplete or contains bad files; skipping ${MODE}."
        continue
    fi

    (
        cd "${OUTPUT_DIR}"
        hadd -f "${MERGED_OUTPUT}" higgsCombine"${COMBINE_NAME}".POINTS.*.MultiDimFit.mH"${MASS}".root
    )

    python3 "${FLASHGG_DIR}/light_quarks/plot_kappaq_scan.py" \
        --input "${OUTPUT_DIR}/${MERGED_OUTPUT}" \
        --output-dir "${OUTPUT_DIR}" \
        --mode inclusive \
        --poi "${POI}"

    echo "Done:"
    echo "  ${OUTPUT_DIR}/${MERGED_OUTPUT}"
    echo ""
done
