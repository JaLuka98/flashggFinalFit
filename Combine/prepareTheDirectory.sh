#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <variable, eg. pt>"
  exit 1
fi

differential_variable="$1"


mkdir "Models_${differential_variable}"
mkdir "Models_${differential_variable}/signal"
mkdir "Models_${differential_variable}/background"
cp "../Background/outdir_earlyAnalysis_${differential_variable}/CMS-HGG*.root ./Models_${differential_variable}/background/"
#cp ../Background/outdir_earlyAnalysis_2022preEE/CMS-HGG*.root ./Models/background/
# Comment this renaming stuff in/out as needed, I am not totally sure about these year suffixes
#for file in Models/background/*resolution.root; do mv "$file" "${file%.root}_2022preEE.root"; done
#cp ../Background/outdir_earlyAnalysis_2022postEE/CMS-HGG*.root ./Models/background/
#for file in Models/background/*resolution.root; do mv "$file" "${file%.root}_2022postEE.root"; done
cp "../Signal/outdir_packaged_${differential_variable}/CMS-HGG*.root ./Models_${differential_variable}/signal/"
# See above
for file in Models_${differential_variable}/signal/*_2022.root; do
    if [ -f "$file" ]; then
        new_name="${file%_2022.root}.root"
        mv "$file" "$new_name"
        echo "Renamed $file to $new_name"
    fi
done
if [ -e ../Datacard/Datacard_${differential_variable}_cleaned.txt ]; then
    cp "../Datacard/Datacard_${differential_variable}_cleaned.txt Datacard_${differential_variable}.txt"
else
    cp "../Datacard/Datacard_${differential_variable}.txt Datacard_${differential_variable}.txt"
fi
