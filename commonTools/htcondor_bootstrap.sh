#!/usr/bin/env bash

# Bootstrap file for batch jobs that is sent with all jobs and
# automatically called by the law remote job wrapper script to find the
# setup.sh file of this example which sets up software and some environment
# variables. The "{{law_dir}}" variable is defined in the workflow
# base tasks in commonTools/framework.py.

action() {
    # Large combined PTH RooWorkspaces need more than the default stack size.
    ulimit -s unlimited || return 1
    source "{{law_dir}}/htcondor_setup.sh" "$@"
}
action "$@"
