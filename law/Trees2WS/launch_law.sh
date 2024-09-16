#!/usr/bin/env bash

source setup.sh

law index --verbose

law run Trees2WSData --input-path /afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/devel/EOSCMS/2024/ntuples/forPaper_24_09_06/variables/NJets/data_postprocessing/root/Data/allData_2022.root --output-dir /afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/Trees2WS/output --variable Njets2p5 --year 2022

# To delete stuff: law run Trees2WSData --input-path /afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/devel/EOSCMS/2024/ntuples/forPaper_24_09_06/variables/NJets/data_postprocessing/root/Data/allData_2022.root --output-dir /afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/Trees2WS/output --variable Njets2p5 --year 2022 --remove-output -1