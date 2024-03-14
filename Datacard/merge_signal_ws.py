import ROOT
import os, sys

combined_ws = ROOT.RooWorkspace("combined_ws")
combined_ws.imp = getattr(combined_ws,"import")

# # Load existing RooWorkspaces from ROOT files
# file1 = ROOT.TFile.Open("/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/input_output_2022postEE/ws_signal/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H_in.root")
# file2 = ROOT.TFile.Open("/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/input_output_2022postEE/ws_signal/output_TTHToGG_M125_13TeV_amcatnlo_pythia8_TTH_in.root")

# # Access RooWorkspaces from the files
# ws1 = file1.Get("tagsDumper/cms_hgg_13TeV;1")
# ws2 = file2.Get("tagsDumper/cms_hgg_13TeV;1")

# file1.Close()
# file2.Close()


# # Copy variables, datasets, and models from ws1
# combined_ws.imp(ws1)

# # Copy variables, datasets, and models from ws2
# combined_ws.imp(ws2)

# print(ws1.Print())

file1 = ROOT.TFile.Open("/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_10_2_13/src/flashggFinalFit/Signal/outdir_packaged_gg2h/CMS-HGG_sigfit_packaged_gg2h_best_resolution.root")
ws1 = file1.Get("wsig_13TeV;1")

file1.Close()
print(ws1.Print())
