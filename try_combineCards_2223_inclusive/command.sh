cp ../test_law_branch_2023/Combine/Datacard_2023.txt .
cp /.automount/net_rw/net__data_cms3a-1/spaeh/private/PhD/analyses/early_Run3_Hgg/datacards_HIG-23-014/inclusive/Datacard.txt ./Datacard_2022.txt

combineCards.py Y22=Datacard_2022.txt Y23=Datacard_2023.txt > datacard_2022_2023.txt

# Get the models directories
cp -r /.automount/net_rw/net__data_cms3a-1/spaeh/private/PhD/analyses/early_Run3_Hgg/datacards_HIG-23-014/inclusive/Models Models_2022
cp -r ../test_law_branch_2023/Combine/Models Models_2023

# Adjust some paths in the datacard
sed -i -E '/^shapes\s+\S+\s+Y22_/ s|(\s)\./Models/|\1./Models_2022/|g' datacard_2022_2023.txt
sed -i -E '/^shapes\s+\S+\s+Y23_/ s|(\s)\./Models/|\1./Models_2023/|g' datacard_2022_2023.txt

# Run text2workspace
text2workspace.py datacard_2022_2023.txt -m 125.38 -o datacard_2022_2023.root

# Run a simple fit to check if it works
combine -M MultiDimFit -d ./datacard_2022_2023.root --floatOtherPOIs 1 --expectSignal 1 -t -1 -P r --setParameterRanges r=0.5,1.5 --algo grid --alignEdges 1 --saveSpecifiedNuis all --freezeParameters MH,allConstrainedNuisances --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -m 125.38 --points 40 -n statOnly

plot1DScan.py higgsCombinestatOnly.MultiDimFit.mH125.38.root \
  --main-label "Stat-only w/ discrete profiling" \
  -o scan_statOnly