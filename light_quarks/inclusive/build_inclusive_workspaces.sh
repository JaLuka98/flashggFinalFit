#!/bin/bash

# Build all inclusive light-quark workspaces needed for the one-at-a-time and
# float-all inclusive scans.
#
# Usage:
#   bash light_quarks/inclusive/build_inclusive_workspaces.sh
#   bash build_inclusive_workspaces.sh

set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
FLASHGG_DIR=$(cd "${SCRIPT_DIR}/../.." && pwd)

cd "${FLASHGG_DIR}"

bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh ssH
bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh uuH
bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh ddH
bash light_quarks/inclusive/light_quarks_t2w_inclusive_2022_2023_2024.sh float_all
