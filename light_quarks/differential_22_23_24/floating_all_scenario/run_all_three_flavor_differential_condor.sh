#!/bin/bash

# Submit the three floating-all differential scans.

set -e

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

bash ${SCRIPT_DIR}/run_limits_three_flavor_differential_condor.sh kappa_s
bash ${SCRIPT_DIR}/run_limits_three_flavor_differential_condor.sh kappa_u
bash ${SCRIPT_DIR}/run_limits_three_flavor_differential_condor.sh kappa_d
