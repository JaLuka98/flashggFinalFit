#!/bin/bash

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit
SCAN_POINTS=${1:-auto}

bash ${FLASHGG_DIR}/light_quarks/differential_22_23_24/floating_all_scenario/hadd_plot_three_flavor_differential.sh kappa_u ${SCAN_POINTS}
