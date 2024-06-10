#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <variable, eg. pt>"
  exit 1
fi

differential_variable="$1"

folder_name="runFits_${differential_variable}"

source variable_parameters.sh

paramStrNoOne_var="paramStrNoOne_${differential_variable}"
paramStrNoOne=$(eval "echo \${$paramStrNoOne_var}")


cd "./runFits_${differential_variable}/SplusBModels_stage3"

for param in ${paramStrNoOne//\,/\ }
do

    python ../../../makeSplusBModelPlot.py --inputWSFile ../unblinded/higgsCombineDataPostFitScanFit_${param}.MultiDimFit.mH125.38.root --loadSnapshot MultiDimFit --ext _${param} --cats all --doZeroes --unblind --translateCats ../../../cats.json --doBands --doToyVeto --saveToyYields --doSumCategories --doCatWeights --saveWeights

done
