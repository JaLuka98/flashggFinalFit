#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <variable, eg. pt>"
  exit 1
fi

differential_variable="$1"

# Import bins and pdfindices for considered variable...

source variable_parameters.sh

paramStr_var="paramStr_${differential_variable}"
paramStrNoOne_var="paramStrNoOne_${differential_variable}"
pdfIndeces_var="pdfIndeces_${differential_variable}"
catsStr_var="catsStr_${differential_variable}"

paramStr=$(eval "echo \${$paramStr_var}")
paramStrNoOne=$(eval "echo \${$paramStrNoOne_var}")
pdfIndeces=$(eval "echo \${$pdfIndeces_var}")
catsStr=$(eval "echo \${$catsStr_var}")

python RunPlotter.py --procs all --cats all --years 2022preEE,2022postEE --ext packaged_${differential_variable}

for cat in ${catsStr//\,/\ }
do
  python RunPlotter.py --procs all --cats ${cat}=${cat}_cat0,${cat}_cat1,${cat}_cat2 --years 2022preEE,2022postEE --ext packaged_${differential_variable} --translateCats ../Plots/cats.json
done
