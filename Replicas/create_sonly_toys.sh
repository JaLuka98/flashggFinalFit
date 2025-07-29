#! /bin/bash

# Commands to create s-only toys


python resampling.py 0 /t3home/niharrin/devel/pnfs/ntuples/midRun3/samples/2025_07_17_powheg/src_files/GluGluHtoGG_M-125_2023postBPix/nominal/  /t3home/niharrin/devel/work/analyses/MidRun3_Code/postprocessing/configs/cat_dicts/2023/PTH_MC.json







# Test the s+b toy
 combine -M MultiDimFit -d /t3home/niharrin/devel/work/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Replicas/Datacard_PTH_2023.root --freezeParameters MH -m 125.38 -n TEST --cminDefaultMinimizerStrategy=0 --algo singles --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2  --saveWorkspace --saveFitResult --cminApproxPreFitTolerance 0.01 -D test.root:toys/toy_1