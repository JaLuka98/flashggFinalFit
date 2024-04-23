#!/bin/bash
paramStr=r_PTH_200p0_350p0=1,r_PTH_45p0_80p0=1,r_PTH_120p0_200p0=1,r_PTH_30p0_45p0=1,r_PTH_350p0_10000p0=1,r_PTH_80p0_120p0=1,r_PTH_0p0_15p0=1,r_PTH_15p0_30p0=1
paramStrNoOne=r_PTH_200p0_350p0,r_PTH_45p0_80p0,r_PTH_120p0_200p0,r_PTH_30p0_45p0,r_PTH_350p0_10000p0,r_PTH_80p0_120p0,r_PTH_0p0_15p0,r_PTH_15p0_30p0
pdfIndeces=pdfindex_RECO_PTH_0p0_15p0_cat0_2022_13TeV,pdfindex_RECO_PTH_0p0_15p0_cat1_2022_13TeV,pdfindex_RECO_PTH_0p0_15p0_cat2_2022_13TeV,pdfindex_RECO_PTH_120p0_200p0_cat0_2022_13TeV,pdfindex_RECO_PTH_120p0_200p0_cat1_2022_13TeV,pdfindex_RECO_PTH_120p0_200p0_cat2_2022_13TeV,pdfindex_RECO_PTH_15p0_30p0_cat0_2022_13TeV,pdfindex_RECO_PTH_15p0_30p0_cat1_2022_13TeV,pdfindex_RECO_PTH_15p0_30p0_cat2_2022_13TeV,pdfindex_RECO_PTH_200p0_350p0_cat0_2022_13TeV,pdfindex_RECO_PTH_200p0_350p0_cat1_2022_13TeV,pdfindex_RECO_PTH_200p0_350p0_cat2_2022_13TeV,pdfindex_RECO_PTH_30p0_45p0_cat0_2022_13TeV,pdfindex_RECO_PTH_30p0_45p0_cat1_2022_13TeV,pdfindex_RECO_PTH_30p0_45p0_cat2_2022_13TeV,pdfindex_RECO_PTH_350p0_10000p0_cat0_2022_13TeV,pdfindex_RECO_PTH_350p0_10000p0_cat1_2022_13TeV,pdfindex_RECO_PTH_350p0_10000p0_cat2_2022_13TeV,pdfindex_RECO_PTH_45p0_80p0_cat0_2022_13TeV,pdfindex_RECO_PTH_45p0_80p0_cat1_2022_13TeV,pdfindex_RECO_PTH_45p0_80p0_cat2_2022_13TeV,pdfindex_RECO_PTH_80p0_120p0_cat0_2022_13TeV,pdfindex_RECO_PTH_80p0_120p0_cat1_2022_13TeV,pdfindex_RECO_PTH_80p0_120p0_cat2_2022_13TeV

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