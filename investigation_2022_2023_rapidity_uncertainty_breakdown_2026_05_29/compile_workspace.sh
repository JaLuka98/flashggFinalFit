#!/bin/bash
set -euo pipefail

if ! command -v scramv1 >/dev/null 2>&1; then
  source /cvmfs/cms.cern.ch/cmsset_default.sh
fi

eval `scramv1 runtime -sh`

text2workspace.py Datacard_rapidity_2022_2023_with_groups.txt \
  -o Datacard_rapidity_2022_2023_with_groups.root \
  -m 125.38 \
  higgsMassRange=122,128 \
  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
  --PO "map=.*/ggh_YH_0p0_0p15.*:r_YH_0p0_0p15[1,-3,3]" \
  --PO "map=.*/tth_YH_0p0_0p15.*:r_YH_0p0_0p15[1,-3,3]" \
  --PO "map=.*/vh_YH_0p0_0p15.*:r_YH_0p0_0p15[1,-3,3]" \
  --PO "map=.*/vbf_YH_0p0_0p15.*:r_YH_0p0_0p15[1,-3,3]" \
  --PO "map=.*/ggh_YH_0p15_0p3.*:r_YH_0p15_0p3[1,-3,3]" \
  --PO "map=.*/tth_YH_0p15_0p3.*:r_YH_0p15_0p3[1,-3,3]" \
  --PO "map=.*/vh_YH_0p15_0p3.*:r_YH_0p15_0p3[1,-3,3]" \
  --PO "map=.*/vbf_YH_0p15_0p3.*:r_YH_0p15_0p3[1,-3,3]" \
  --PO "map=.*/ggh_YH_0p3_0p6.*:r_YH_0p3_0p6[1,-3,3]" \
  --PO "map=.*/tth_YH_0p3_0p6.*:r_YH_0p3_0p6[1,-3,3]" \
  --PO "map=.*/vh_YH_0p3_0p6.*:r_YH_0p3_0p6[1,-3,3]" \
  --PO "map=.*/vbf_YH_0p3_0p6.*:r_YH_0p3_0p6[1,-3,3]" \
  --PO "map=.*/ggh_YH_0p6_0p9.*:r_YH_0p6_0p9[1,-3,3]" \
  --PO "map=.*/tth_YH_0p6_0p9.*:r_YH_0p6_0p9[1,-3,3]" \
  --PO "map=.*/vh_YH_0p6_0p9.*:r_YH_0p6_0p9[1,-3,3]" \
  --PO "map=.*/vbf_YH_0p6_0p9.*:r_YH_0p6_0p9[1,-3,3]" \
  --PO "map=.*/ggh_YH_0p9_2p5.*:r_YH_0p9_2p5[1,-3,3]" \
  --PO "map=.*/tth_YH_0p9_2p5.*:r_YH_0p9_2p5[1,-3,3]" \
  --PO "map=.*/vh_YH_0p9_2p5.*:r_YH_0p9_2p5[1,-3,3]" \
  --PO "map=.*/vbf_YH_0p9_2p5.*:r_YH_0p9_2p5[1,-3,3]"
