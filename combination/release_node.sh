#!/bin/bash
# release_node.sh <host> <"YYYY-mm-dd HH:MM">: at that time, stop the law runs of this checkout on <host> without
# losing fits. The law parents are paused (SIGSTOP), so no new fit starts; every fit already running finishes and
# writes its result; a paused law run is removed once none of its fits is left. local_farm.py then sees the run
# as ended and starts its next pass on another node (logs/farm_node_caps.json gives <host> no new runs).
# Run it detached on a node that stays up (it needs the farm agent for ssh), e.g.
#   setsid nohup bash combination/release_node.sh lxbatch16 "2026-10-27 07:00" < /dev/null > /dev/null 2>&1 &
HOST=$1
WHEN=$2
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${REPO}/logs/release_${HOST}.log
export SSH_AUTH_SOCK=/tmp/farm-agent-${USER}/agent.sock
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "${LOG}"; }

log "waiting until ${WHEN} to release ${HOST}"
while [ "$(date '+%Y-%m-%d %H:%M')" \< "${WHEN}" ]; do sleep 60; done

# law parents of this checkout (process group leaders), paused; never this remote shell, whose command line matches
# the pattern too (it paused itself first on lxbatch19/20 on 2026-10-27 and their law runs went on)
groups=$(timeout 60 ssh -o BatchMode=yes "${HOST}" "for p in \$(pgrep -u \$USER -f 'law run FinalFitsYear'); do
  [ \$p = \$\$ ] && continue
  [ \"\$(ps -o pgid= -p \$p | tr -d ' ')\" = \"\$p\" ] || continue
  case \"\$(tr '\\0' ' ' < /proc/\$p/cmdline)\" in *${REPO}*) kill -STOP \$p && echo \$p;; esac; done")
log "paused law runs (process groups): ${groups:-none}"

while [ -n "${groups}" ]; do
  sleep 300
  left=""
  for g in ${groups}; do
    n=$(timeout 60 ssh -o BatchMode=yes "${HOST}" "for p in \$(pgrep -u \$USER -x combine); do [ \"\$(ps -o pgid= -p \$p | tr -d ' ')\" = ${g} ] && echo \$p; done | wc -l") || { left="${left} ${g}"; continue; }
    if [ "${n}" = 0 ]; then
      timeout 60 ssh -o BatchMode=yes "${HOST}" "kill -KILL -${g}" 2>/dev/null
      log "law run ${g}: all fits finished, removed"
    else
      left="${left} ${g}"
    fi
  done
  groups=$(echo ${left})
done
log "${HOST} released"
