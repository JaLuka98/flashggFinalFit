#!/bin/bash
set -euo pipefail

if ! command -v scramv1 >/dev/null 2>&1; then
  source /cvmfs/cms.cern.ch/cmsset_default.sh
fi

eval `scramv1 runtime -sh`

WS=Datacard_rapidity_2022_2023_with_groups.root
POI=r_YH_0p0_0p15
MH=125.38
POINTS=${POINTS:-40}
RANGE=${RANGE:-${POI}=0.8,2.0}
BESTFIT=higgsCombine.bestfit_${POI}.MultiDimFit.mH${MH}.root

common_opts=(
  -w w
  -m "${MH}"
  -P "${POI}"
  --floatOtherPOIs 1
  --setParameters MH="${MH}"
  --setParameterRanges "${RANGE}"
  --cminDefaultMinimizerStrategy 0
  --cminDefaultMinimizerTolerance 0.01
  --cminFallbackAlgo Minuit2,Simplex,0:0.1
  --cminFallbackAlgo Minuit2,Combined,0:0.1
  --X-rtd MINIMIZER_freezeDisassociatedParams
  --X-rtd MINIMIZER_multiMin_hideConstants
  --X-rtd MINIMIZER_multiMin_maskConstraints
  --X-rtd MINIMIZER_multiMin_maskChannels=2
)

scan_opts=(
  --algo grid
  --points "${POINTS}"
  --alignEdges 1
  --saveNLL
  --snapshotName MultiDimFit
)

combine -M MultiDimFit "${WS}" \
  "${common_opts[@]}" \
  --freezeParameters MH \
  --saveWorkspace \
  --saveFitResult \
  -n ".bestfit_${POI}"

combine -M MultiDimFit "${BESTFIT}" \
  "${common_opts[@]}" \
  "${scan_opts[@]}" \
  --freezeParameters MH \
  -n ".scan_total_${POI}"

combine -M MultiDimFit "${BESTFIT}" \
  "${common_opts[@]}" \
  "${scan_opts[@]}" \
  --freezeParameters MH \
  --freezeNuisanceGroups photonScale,photonResolution \
  -n ".scan_freeze_photonEnergy_${POI}"

combine -M MultiDimFit "${BESTFIT}" \
  "${common_opts[@]}" \
  "${scan_opts[@]}" \
  --freezeParameters MH \
  --freezeNuisanceGroups photonScale,photonResolution,photonSF \
  -n ".scan_freeze_photonEnergy_photonSF_${POI}"

combine -M MultiDimFit "${BESTFIT}" \
  "${common_opts[@]}" \
  "${scan_opts[@]}" \
  --freezeParameters MH \
  --freezeNuisanceGroups photonScale,photonResolution,photonSF,pileup,lumi \
  -n ".scan_freeze_photonEnergy_photonSF_pileup_lumi_${POI}"

combine -M MultiDimFit "${BESTFIT}" \
  "${common_opts[@]}" \
  "${scan_opts[@]}" \
  --freezeParameters MH \
  --freezeNuisanceGroups photonScale,photonResolution,photonSF,pileup,lumi,theory \
  -n ".scan_freeze_photonEnergy_photonSF_pileup_lumi_theory_${POI}"

combine -M MultiDimFit "${BESTFIT}" \
  "${common_opts[@]}" \
  "${scan_opts[@]}" \
  --freezeParameters MH \
  --freezeNuisanceGroups photonScale,photonResolution,photonSF,pileup,lumi,theory,mcStat \
  -n ".scan_freeze_photonEnergy_photonSF_pileup_lumi_theory_mcStat_${POI}"

combine -M MultiDimFit "${BESTFIT}" \
  "${common_opts[@]}" \
  "${scan_opts[@]}" \
  --freezeParameters MH,allConstrainedNuisances \
  -n ".scan_statonly_${POI}"

plot1DScan.py "higgsCombine.scan_total_${POI}.MultiDimFit.mH${MH}.root" \
  --POI "${POI}" \
  --main-label Total \
  --main-color 1 \
  --others \
    "higgsCombine.scan_freeze_photonEnergy_${POI}.MultiDimFit.mH${MH}.root:Freeze photon energy:4" \
    "higgsCombine.scan_freeze_photonEnergy_photonSF_${POI}.MultiDimFit.mH${MH}.root:Freeze photon energy+SF:6" \
    "higgsCombine.scan_freeze_photonEnergy_photonSF_pileup_lumi_${POI}.MultiDimFit.mH${MH}.root:Freeze photon energy+SF+PU+lumi:7" \
    "higgsCombine.scan_freeze_photonEnergy_photonSF_pileup_lumi_theory_${POI}.MultiDimFit.mH${MH}.root:Freeze photon energy+SF+PU+lumi+theory:8" \
    "higgsCombine.scan_freeze_photonEnergy_photonSF_pileup_lumi_theory_mcStat_${POI}.MultiDimFit.mH${MH}.root:Freeze photon energy+SF+PU+lumi+theory+MC stat:9" \
    "higgsCombine.scan_statonly_${POI}.MultiDimFit.mH${MH}.root:Stat-only:2" \
  -o "breakdown_${POI}" \
  --breakdown "photon energy,photon SF,pileup+lumi,theory,MC stat,other syst,stat"
