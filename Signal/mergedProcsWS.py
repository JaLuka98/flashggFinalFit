# Script to package individual signal models for a single category in one ROOT file
# Option to merge different extensions (years)

import os, re, sys
import glob
import ROOT
from optparse import OptionParser

def get_options():
  parser = OptionParser()
  parser.add_option("--cat", dest='cat', default='best_resolution', help="RECO category to package")
  parser.add_option("--exts", dest='exts', default='', help="Comma separate list of extensions")
  parser.add_option("--outputExt", dest='outputExt', default='packaged', help="Output extension")
  parser.add_option("--massPoints", dest='massPoints', default='125', help="Comma separated list of mass points")
  parser.add_option("--mergeYears", dest='mergeYears', default=False, action="store_true", help="Merge specified categories across years")
  parser.add_option("--year", dest="year", default="2016", help="If not merging, then specify year for output file name")
  return parser.parse_args()
(opt,args) = get_options()

def rooiter(x):
  iter = x.iterator()
  ret = iter.Next()
  while ret:
    yield ret
    ret = iter.Next()

# Extract all files to be merged
fNames = {}
for ext in opt.exts.split(","): fNames[ext] = glob.glob("outdir_%s/CMS-HGG_sigfit_packaged_%s.root"%(opt.outputExt,opt.cat))
# for ext in opt.exts.split(","): fNames[ext] = glob.glob("outdir_packaged_gg2h/CMS-HGG_sigfit_packaged_gg2h_%s.root"%opt.cat)



# Define ouput packaged workspace
print " --> Packaging output workspaces"
mergedWS = ROOT.RooWorkspace("wsig_13TeV","wsig_13TeV")
mergedWS.imp = getattr(mergedWS,"import")


# Extract merged datasets
data_merged = {}
data_merged_names = []
for mp in opt.massPoints.split(","): 
  print(fNames)
  data_merged["m%s"%mp] = ROOT.TFile(fNames[opt.exts.split(",")[0]][0]).Get("wsig_13TeV").data("sig_mass_m%s_%s"%(mp,opt.cat)).emptyClone("sig_mass_m%s_%s"%(mp,opt.cat))
  # data_merged["m%s"%mp] = ROOT.TFile(fNames[opt.exts.split(",")[0]][0]).Get("wsig_13TeV")
  data_merged_names.append( data_merged["m%s"%mp].GetName() )




for ext, fNames_by_ext in fNames.iteritems():
  for fName in fNames_by_ext:
    for mp in opt.massPoints.split(","):
      d = ROOT.TFile(fName).Get("wsig_13TeV").data("sig_mass_m%s_%s"%(mp,opt.cat))
      for i in range(d.numEntries()):
        p = d.get(i)
        w = d.weight()
        data_merged["m%s"%mp].add(p,w)
  


for _data in data_merged.itervalues(): mergedWS.imp(_data)
        
# Loop over input signal fit workspaces
for ext, fNames_by_ext in fNames.iteritems(): # Iterate over pre and post EE
  for fName in fNames_by_ext:
    fin = ROOT.TFile(fName)
    wsin = fin.Get("wsig_13TeV")
    if not wsin: continue
    allVars, allFunctions, allPdfs = {}, {}, {}
    for _var in rooiter(wsin.allVars()): allVars[_var.GetName()] = _var
    for _func in rooiter(wsin.allFunctions()): allFunctions[_func.GetName()] = _func
    for _pdf in rooiter(wsin.allPdfs()): allPdfs[_pdf.GetName()] = _pdf
    allData = wsin.allData()
    print(ext, fNames_by_ext)

    #Set the evaluation point (125.11 GeV, https://atlas.cern/Updates/Briefing/Run2-Higgs-Mass)
    mass_value = 125.11
    wsin.var("MH").setVal(mass_value)

    weighted_ea_in_numerator = 0
    xs_sum = 0

    for key, value in allFunctions.items():
      if ("_in" in key) and ("fea_" in key) and (ext.split("_")[-1] in key):
        current_proc = key.split("_")[1]
        print(key.split("_"), current_proc)
        current_xs = allFunctions['fxs_'+current_proc+'_in_13TeV'].getVal()
        current_ea = allFunctions[key].getVal()
        weighted_ea_in_numerator += (current_ea*current_xs)
        xs_sum += current_xs
    ea_in_sm = weighted_ea_in_numerator/xs_sum



    weighted_ea_out_numerator = 0

    for key, value in allFunctions.items():
      if ("_out" in key) and ("fea_" in key) and (ext.split("_")[-1] in key):
        current_proc = key.split("_")[1]
        print(current_proc)
        current_xs = allFunctions['fxs_'+current_proc+'_out_13TeV'].getVal()
        current_ea = allFunctions[key].getVal()
        weighted_ea_out_numerator += (current_ea*current_xs)
    ea_out_sm = weighted_ea_out_numerator/xs_sum

    br = allFunctions["fbr_13TeV"].getVal()
    if "2022" in ext:  # Used normtag: https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#Year_2022
      if "pre" in ext:
        lumi = 7.98
      else:
        lumi = 26.67
    else:
      lumi = 1
      print("Update Lumi information. Using substitute value 1.")
    normalization_in = ea_in_sm * xs_sum * br * lumi
    normalization_out = ea_out_sm * xs_sum * br * lumi
    print(normalization_in, normalization_out, ea_in_sm, ea_out_sm)
    print("Norm_in", normalization_in)
    print("Norm_out", normalization_out)
    print("XS_Sum: ", xs_sum)
    print("ea_in_sm: ", ea_in_sm)
    print("ea_out_sm: ", ea_out_sm)
    # print(allFunctions["fea_GG2H_in_2022postEE_best_resolution_13TeV"].getVal())
    # print(allFunctions["fbr_13TeV"].getVal())

    # Create the normalization factor
    norm_in = ROOT.RooRealVar("norm_in", "norm_in", normalization_in)
    norm_out = ROOT.RooRealVar("norm_out", "norm_out", normalization_out)

    # Get pdf
    for key, value in allPdfs.items():
      if ("GG2H_in" in key) and ("hggpdfsmrel" == key.split("_")[0]) and ("13TeV" == key.split("_")[-1]) and (ext.split("_")[-1] in key):
        #print(key)
        current_pdf = allPdfs[key]
        pdf_name = key.split("_")
        pdf_name.pop(0)
        pdf_name.pop(0)
        pdf_name.insert(0, "hggpdfsmrel_SM")
        new_name = "_".join(pdf_name)
        # sm_in_pdf = ROOT.RooProduct(new_name, new_name, ROOT.RooArgList(current_pdf, norm_in))
        sm_in_pdf = ROOT.RooAddPdf(new_name, new_name, ROOT.RooArgList(current_pdf), ROOT.RooArgList(norm_in))

    for key, value in allPdfs.items():
      if ("GG2H_out" in key) and ("hggpdfsmrel" == key.split("_")[0]) and ("13TeV" == key.split("_")[-1]) and (ext.split("_")[-1] in key):
        # print(key)
        current_pdf = allPdfs[key]
        pdf_name = key.split("_")
        pdf_name.pop(0)
        pdf_name.pop(0)
        pdf_name.insert(0, "hggpdfsmrel_SM")
        new_name = "_".join(pdf_name)
        # sm_out_pdf = ROOT.RooProduct(new_name, new_name, ROOT.RooArgList(current_pdf, norm_out))
        sm_out_pdf = ROOT.RooAddPdf(new_name, new_name, ROOT.RooArgList(current_pdf), ROOT.RooArgList(norm_out))
  
    # Import objects into output workspace
    for _varName, _var in allVars.iteritems(): mergedWS.imp(_var,ROOT.RooFit.RecycleConflictNodes(),ROOT.RooFit.Silence())
    for _funcName, _func in allFunctions.iteritems(): mergedWS.imp(_func,ROOT.RooFit.RecycleConflictNodes(),ROOT.RooFit.Silence())
    for _pdfName, _pdf in allPdfs.iteritems(): mergedWS.imp(_pdf,ROOT.RooFit.RecycleConflictNodes(),ROOT.RooFit.Silence())

    mergedWS.imp(sm_in_pdf, ROOT.RooFit.RecycleConflictNodes(),ROOT.RooFit.Silence())
    mergedWS.imp(sm_out_pdf, ROOT.RooFit.RecycleConflictNodes(),ROOT.RooFit.Silence())

    for _data in allData:
      # Skip merged datasets
      if _data.GetName() in data_merged_names: continue
      else: mergedWS.imp(_data)

# Save to file
if not os.path.isdir("outdir_%s"%opt.outputExt): os.system("mkdir outdir_%s"%opt.outputExt)
if opt.mergeYears:
  print " --> Writing to: ./outdir_%s/CMS-HGG_sigfit_merged_%s_%s.root"%(opt.outputExt,opt.outputExt,opt.cat)
  f = ROOT.TFile("./outdir_%s/CMS-HGG_sigfit_merged_%s_%s.root"%(opt.outputExt,opt.outputExt,opt.cat),"RECREATE")
else:
  print " --> Writing to: ./outdir_%s/CMS-HGG_sigfit_merged_%s_%s_%s.root"%(opt.outputExt,opt.outputExt,opt.cat,opt.year)
  f = ROOT.TFile("./outdir_%s/CMS-HGG_sigfit_merged_%s_%s_%s.root"%(opt.outputExt,opt.outputExt,opt.cat,opt.year),"RECREATE")

# print(mergedWS.Print())
mergedWS.Write()
mergedWS.Delete()
f.Delete()
f.Close()
