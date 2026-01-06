#!/bin/bash
paramStr=r_YH_0p0_0p15=1,r_YH_0p15_0p3=1,r_YH_0p3_0p45=1,r_YH_0p45_0p6=1,r_YH_0p6_0p75=1,r_YH_0p75_0p9=1,r_YH_0p9_1p2=1,r_YH_1p2_1p6=1,r_YH_1p6_2p0=1,r_YH_2p0_2p5=1
paramStrNoOne=r_YH_0p0_0p15,r_YH_0p15_0p3,r_YH_0p3_0p45,r_YH_0p45_0p6,r_YH_0p6_0p75,r_YH_0p75_0p9,r_YH_0p9_1p2,r_YH_1p2_1p6,r_YH_1p6_2p0,r_YH_2p0_2p5
pdfIndeces=pdfindex_RECO_YH_0p0_0p15_cat0_2022_13TeV,pdfindex_RECO_YH_0p0_0p15_cat1_2022_13TeV,pdfindex_RECO_YH_0p0_0p15_cat2_2022_13TeV,pdfindex_RECO_YH_0p15_0p3_cat0_2022_13TeV,pdfindex_RECO_YH_0p15_0p3_cat1_2022_13TeV,pdfindex_RECO_YH_0p15_0p3_cat2_2022_13TeV,pdfindex_RECO_YH_0p3_0p45_cat0_2022_13TeV,pdfindex_RECO_YH_0p3_0p45_cat1_2022_13TeV,pdfindex_RECO_YH_0p3_0p45_cat2_2022_13TeV,pdfindex_RECO_YH_0p45_0p6_cat0_2022_13TeV,pdfindex_RECO_YH_0p45_0p6_cat1_2022_13TeV,pdfindex_RECO_YH_0p45_0p6_cat2_2022_13TeV,pdfindex_RECO_YH_0p6_0p75_cat0_2022_13TeV,pdfindex_RECO_YH_0p6_0p75_cat1_2022_13TeV,pdfindex_RECO_YH_0p6_0p75_cat2_2022_13TeV,pdfindex_RECO_YH_0p75_0p9_cat0_2022_13TeV,pdfindex_RECO_YH_0p75_0p9_cat1_2022_13TeV,pdfindex_RECO_YH_0p75_0p9_cat2_2022_13TeV,pdfindex_RECO_YH_0p9_1p2_cat0_2022_13TeV,pdfindex_RECO_YH_0p9_1p2_cat1_2022_13TeV,pdfindex_RECO_YH_0p9_1p2_cat2_2022_13TeV,pdfindex_RECO_YH_1p2_1p6_cat0_2022_13TeV,pdfindex_RECO_YH_1p2_1p6_cat1_2022_13TeV,pdfindex_RECO_YH_1p2_1p6_cat2_2022_13TeV,pdfindex_RECO_YH_1p6_2p0_cat0_2022_13TeV,pdfindex_RECO_YH_1p6_2p0_cat1_2022_13TeV,pdfindex_RECO_YH_1p6_2p0_cat2_2022_13TeV,pdfindex_RECO_YH_2p0_2p5_cat0_2022_13TeV,pdfindex_RECO_YH_2p0_2p5_cat1_2022_13TeV,pdfindex_RECO_YH_2p0_2p5_cat2_2022_13TeV


for param in ${paramStrNoOne//\,/\ }
do
  combine -M MultiDimFit Datacard_differential_pt.root -m 125.38 -n firstStep_${param} \
  --cminDefaultMinimizerStrategy=0 --expectSignal 1 --saveWorkspace \
  --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants \
  --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 \
  -t -1 --setParameters ${paramStr} -P ${param} --saveFitResult --saveSpecifiedIndex ${pdfIndeces} --floatOtherPOIs 1

  pdfIdx=$(root -l -q 'checkPdfIdx.C("higgsCombinefirstStep_'"${param}"'.MultiDimFit.mH125.38.root")')
  substring=='Processing checkPdfIdx.C("higgsCombinefirstStep_'"${param}"'.MultiDimFit.mH125.38.root")... '
  # Remove "Processing checkPdfIdx.C... " from the beginning
  pdfIdx=$(echo "$pdfIdx" | awk -F'X' '{print $2}')
  # Remove the last comma
  pdfIdx="${pdfIdx%,}"
  echo ${pdfIdx}

  combineTool.py -M MultiDimFit Datacard_differential_pt.root -m 125.38 -n AsimovPostFitScanFit_${param} \
  --cminDefaultMinimizerStrategy=0 --algo grid --points 30 --split-points 1 --expectSignal 1 \
  --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants \
  --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 \
  -t -1 -P ${param} --saveFitResult \
  --job-mode condor --task-name AsimovScan_${param} --sub-opts='+JobFlavour = "workday"' \
  --setParameters${pdfIdx},${paramStr} --floatOtherPOIs 1 --alignEdges 1 --saveSpecifiedIndex ${pdfIndeces}

  combineTool.py -M MultiDimFit higgsCombinefirstStep_${param}.MultiDimFit.mH125.38.root -m 125.38 -n AsimovPostFitScanStat_${param} --split-points 1 \
  --cminDefaultMinimizerStrategy=0 --expectSignal 1 \
  --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants \
  --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 \
  --freezeParameters allConstrainedNuisances-t -1 --setParameters${pdfIdx},${paramStr} \
  --job-mode condor --task-name AsimovPostFitScanStat_${param} --sub-opts='+JobFlavour = "workday"' \
  -P ${param} --saveFitResult --snapshotName MultiDimFit --floatOtherPOIs 1 --alignEdges 1 --saveSpecifiedIndex ${pdfIndeces}

done
