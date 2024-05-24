#!/bin/bash

# Get the list of job IDs that are on hold
held_jobs=$(condor_q -constraint 'JobStatus == 5' -format '%d' ClusterId -format '.%d\n' ProcId | awk '{print $1""$2}')

# Transfer data for each held job
for job_id in $held_jobs; do
    condor_rm $job_id
done
