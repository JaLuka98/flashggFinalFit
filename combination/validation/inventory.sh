#!/bin/bash
# Inventory of the running combination fits and law runs on all login nodes (input of check_runs.py).
for h in lxbatch01 lxbatch02 lxbatch03 lxbatch04 lxbatch05; do
  timeout 30 ssh -o BatchMode=yes $h 'for p in $(pgrep -u $USER -x combine); do c=$(readlink /proc/$p/cwd 2>/dev/null); n=$(tr "\0" " " < /proc/$p/cmdline 2>/dev/null | grep -oE "\-n [^ ]+" | cut -c4-); echo "fit '$h' $p $(ps -o etimes=,rss=,stat= -p $p | tr -s " " " ") $c $n"; done
    for p in $(pgrep -u $USER -f "^/cvmfs.*law run FinalFitsYear"); do a=$(tr "\0" " " < /proc/$p/cmdline 2>/dev/null); [ "$(ps -o pgid= -p $p | tr -d " ")" = "$p" ] || continue; echo "law '$h' $p $(echo $a | grep -oE "output_combination_[A-Za-z0-9]+/[a-z0-9]+") $(echo $a | grep -oE "(asimov|unblinded)-fits") $(ps -o etimes= -p $p | tr -d " ")"; done' 2>/dev/null
done
