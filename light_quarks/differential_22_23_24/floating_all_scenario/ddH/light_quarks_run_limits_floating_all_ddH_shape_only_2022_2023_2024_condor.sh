#!/bin/bash

# Scan kappa_d while kappa_s, kappa_u, and BR_hgg are profiled.

set -e

FLASHGG_DIR=/net/data_cms3a-1/daumann/PhD/Final_fits_repo/CMSSW_14_1_0_pre4/src/final_fits_test_folder/flashggFinalFit

bash ${FLASHGG_DIR}/light_quarks/differential_22_23_24/floating_all_scenario/run_limits_three_flavor_shape_only_condor.sh kappa_d
