#!/bin/sh
ulimit -s unlimited
set -e
cd /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd /afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/runFits_mu_fiducial_sm

if [ $1 -eq 0 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 0 --lastPoint 0 -n _profile1D_statonly_r.POINTS.0.0
fi
if [ $1 -eq 1 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 1 --lastPoint 1 -n _profile1D_statonly_r.POINTS.1.1
fi
if [ $1 -eq 2 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 2 --lastPoint 2 -n _profile1D_statonly_r.POINTS.2.2
fi
if [ $1 -eq 3 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 3 --lastPoint 3 -n _profile1D_statonly_r.POINTS.3.3
fi
if [ $1 -eq 4 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 4 --lastPoint 4 -n _profile1D_statonly_r.POINTS.4.4
fi
if [ $1 -eq 5 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 5 --lastPoint 5 -n _profile1D_statonly_r.POINTS.5.5
fi
if [ $1 -eq 6 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 6 --lastPoint 6 -n _profile1D_statonly_r.POINTS.6.6
fi
if [ $1 -eq 7 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 7 --lastPoint 7 -n _profile1D_statonly_r.POINTS.7.7
fi
if [ $1 -eq 8 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 8 --lastPoint 8 -n _profile1D_statonly_r.POINTS.8.8
fi
if [ $1 -eq 9 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 9 --lastPoint 9 -n _profile1D_statonly_r.POINTS.9.9
fi
if [ $1 -eq 10 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 10 --lastPoint 10 -n _profile1D_statonly_r.POINTS.10.10
fi
if [ $1 -eq 11 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 11 --lastPoint 11 -n _profile1D_statonly_r.POINTS.11.11
fi
if [ $1 -eq 12 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 12 --lastPoint 12 -n _profile1D_statonly_r.POINTS.12.12
fi
if [ $1 -eq 13 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 13 --lastPoint 13 -n _profile1D_statonly_r.POINTS.13.13
fi
if [ $1 -eq 14 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 14 --lastPoint 14 -n _profile1D_statonly_r.POINTS.14.14
fi
if [ $1 -eq 15 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 15 --lastPoint 15 -n _profile1D_statonly_r.POINTS.15.15
fi
if [ $1 -eq 16 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 16 --lastPoint 16 -n _profile1D_statonly_r.POINTS.16.16
fi
if [ $1 -eq 17 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 17 --lastPoint 17 -n _profile1D_statonly_r.POINTS.17.17
fi
if [ $1 -eq 18 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 18 --lastPoint 18 -n _profile1D_statonly_r.POINTS.18.18
fi
if [ $1 -eq 19 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 19 --lastPoint 19 -n _profile1D_statonly_r.POINTS.19.19
fi
if [ $1 -eq 20 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 20 --lastPoint 20 -n _profile1D_statonly_r.POINTS.20.20
fi
if [ $1 -eq 21 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 21 --lastPoint 21 -n _profile1D_statonly_r.POINTS.21.21
fi
if [ $1 -eq 22 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 22 --lastPoint 22 -n _profile1D_statonly_r.POINTS.22.22
fi
if [ $1 -eq 23 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 23 --lastPoint 23 -n _profile1D_statonly_r.POINTS.23.23
fi
if [ $1 -eq 24 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 24 --lastPoint 24 -n _profile1D_statonly_r.POINTS.24.24
fi
if [ $1 -eq 25 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 25 --lastPoint 25 -n _profile1D_statonly_r.POINTS.25.25
fi
if [ $1 -eq 26 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 26 --lastPoint 26 -n _profile1D_statonly_r.POINTS.26.26
fi
if [ $1 -eq 27 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 27 --lastPoint 27 -n _profile1D_statonly_r.POINTS.27.27
fi
if [ $1 -eq 28 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 28 --lastPoint 28 -n _profile1D_statonly_r.POINTS.28.28
fi
if [ $1 -eq 29 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 29 --lastPoint 29 -n _profile1D_statonly_r.POINTS.29.29
fi
if [ $1 -eq 30 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 30 --lastPoint 30 -n _profile1D_statonly_r.POINTS.30.30
fi
if [ $1 -eq 31 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 31 --lastPoint 31 -n _profile1D_statonly_r.POINTS.31.31
fi
if [ $1 -eq 32 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 32 --lastPoint 32 -n _profile1D_statonly_r.POINTS.32.32
fi
if [ $1 -eq 33 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 33 --lastPoint 33 -n _profile1D_statonly_r.POINTS.33.33
fi
if [ $1 -eq 34 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 34 --lastPoint 34 -n _profile1D_statonly_r.POINTS.34.34
fi
if [ $1 -eq 35 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 35 --lastPoint 35 -n _profile1D_statonly_r.POINTS.35.35
fi
if [ $1 -eq 36 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 36 --lastPoint 36 -n _profile1D_statonly_r.POINTS.36.36
fi
if [ $1 -eq 37 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 37 --lastPoint 37 -n _profile1D_statonly_r.POINTS.37.37
fi
if [ $1 -eq 38 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 38 --lastPoint 38 -n _profile1D_statonly_r.POINTS.38.38
fi
if [ $1 -eq 39 ]; then
  combine --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -M MultiDimFit -m 125 -d /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Combine/Datacard_mu_fiducial_sm.root --setParameterRanges r=0,2 --points 40 --firstPoint 39 --lastPoint 39 -n _profile1D_statonly_r.POINTS.39.39
fi

