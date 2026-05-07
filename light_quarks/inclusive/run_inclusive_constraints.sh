#!/bin/bash

# Submit all inclusive light-quark expected scans to Condor.
#
# Usage:
#   bash light_quarks/inclusive/run_inclusive_constraints.sh
#   bash run_inclusive_constraints.sh

set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
FLASHGG_DIR=$(cd "${SCRIPT_DIR}/../.." && pwd)

cd "${FLASHGG_DIR}"

bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh ssH
bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh uuH
bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh ddH
bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappas
bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappau
bash light_quarks/inclusive/light_quarks_run_limits_inclusive_2022_2023_2024_condor.sh float_all_kappad
