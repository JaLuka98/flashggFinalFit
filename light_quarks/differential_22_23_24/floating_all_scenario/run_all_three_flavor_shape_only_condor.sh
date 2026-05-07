#!/bin/bash

# Submit the three floating-all shape-only scans.

set -e

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

bash ${SCRIPT_DIR}/run_limits_three_flavor_shape_only_condor.sh kappa_s
bash ${SCRIPT_DIR}/run_limits_three_flavor_shape_only_condor.sh kappa_u
bash ${SCRIPT_DIR}/run_limits_three_flavor_shape_only_condor.sh kappa_d
