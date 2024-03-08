#!/bin/bash
ulimit -s unlimited
set -e
cd /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Datacard
export PYTHONPATH=$PYTHONPATH:/eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/tools:/eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Datacard/tools

python /eos/home-n/niharrin/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Datacard/makeYields.py --cat medium_resolution --procs auto --ext earlyAnalysis --mass 125 --inputWSDirMap 2022preEE=../input_output_2022preEE/ws_signal,2022postEE=../input_output_2022postEE/ws_signal --sigModelWSDir ./Models/signal --sigModelExt packaged --bkgModelWSDir ./Models/background --bkgModelExt multipdf  --mergeYears --skipZeroes --doSystematics
