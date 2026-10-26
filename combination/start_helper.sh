#!/bin/bash
# start_helper.sh <host> <obs> <fit> <law|unblind> <workers> [<"YYYY-mm-dd HH:MM">]: a second law process for a run
# that local_farm.py already runs elsewhere (the fit branches are shared through the _shared_fit locks), on <host>,
# optionally from the given time on. The memory guard of the checkout (node_guard.py) is started on <host> first.
# Run it detached when it has to wait, e.g.
#   setsid nohup bash combination/start_helper.sh lxbatch11 rapidity comb law 10 "2026-10-26 20:00" < /dev/null > /dev/null 2>&1 &
HOST=$1 OBS=$2 FIT=$3 STEP=$4 WORKERS=$5 WHEN=$6
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${REPO}/logs/helpers.log
export SSH_AUTH_SOCK=/tmp/farm-agent-${USER}/agent.sock
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "${LOG}"; }

if [ -n "${WHEN}" ]; then
  log "${HOST} ${OBS}:${FIT}:${STEP}: waiting until ${WHEN}"
  while [ "$(date '+%Y-%m-%d %H:%M')" \< "${WHEN}" ]; do sleep 60; done
fi
out=$(timeout 300 ssh -o BatchMode=yes "${HOST}" "cd ${REPO} && setsid -f python3 combination/node_guard.py < /dev/null > /dev/null 2>&1;
  EXECUTION=local WORKERS=${WORKERS} FITS=${FIT} LOG_SUFFIX=_${HOST} combination/run_combination.sh ${OBS} ${STEP}" 2>&1 | tail -1)
log "${HOST} ${OBS}:${FIT}:${STEP} with ${WORKERS} workers: ${out}"
