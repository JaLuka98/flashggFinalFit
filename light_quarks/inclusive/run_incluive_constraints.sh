#!/bin/bash

# Backward-compatible wrapper for the misspelled script name.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
exec bash "${SCRIPT_DIR}/run_inclusive_constraints.sh" "$@"
