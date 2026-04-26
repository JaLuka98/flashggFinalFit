#!/bin/bash

cd /work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit

eval `scramv1 runtime -sh`

export PYTHON3PATH=${PYTHON3PATH}:/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/commonTools

text2workspace.py /scratch/niharrin/568272/Combine/Datacard_PTH_2022.txt -o /scratch/niharrin/568272/Combine/EFT_Datacard_PTH_chg_2022.root -m 125.38 higgsMassRange=122,128  -P EFT:smeft_chg