#!/bin/bash

# Merge and plot the three floating-all differential scans.

set -e

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SCAN_POINTS=${1:-auto}

bash ${SCRIPT_DIR}/hadd_plot_three_flavor_differential.sh kappa_s ${SCAN_POINTS}
bash ${SCRIPT_DIR}/hadd_plot_three_flavor_differential.sh kappa_u ${SCAN_POINTS}
bash ${SCRIPT_DIR}/hadd_plot_three_flavor_differential.sh kappa_d ${SCAN_POINTS}
