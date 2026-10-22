# Script to list the signal proc x cat which the datacard will prune, before the signal models are fitted
#  * Applies the pruning rule of makeDatacard.py (--prune --doTrueYield): N = Product(XS,BR,eff*acc,lumi) below
#    pruneThreshold of the total signal yield of the category
#  * Needs only the nominal mass input workspaces (Trees2WS output), so the pruned fits never have to be run
#  * Output: one json per era, read by SignalFitCategoryProcess in Signal/law_signal.py

import os, sys
import glob
import json
from optparse import OptionParser
from collections import OrderedDict as od
import ROOT
import pandas as pd

from commonObjects import *
from commonTools import *
from XSBRMap import *

def get_options():
  parser = OptionParser()
  parser.add_option('--inputWSDirMap', dest='inputWSDirMap', default='', help="Map. Format: year=inputWSDir (separate years by comma)")
  parser.add_option('--outputMap', dest='outputMap', default='', help="Map. Format: year=output json (separate years by comma)")
  parser.add_option('--cats', dest='cats', default='', help="Comma separated list of analysis categories")
  parser.add_option('--procs', dest='procs', default='auto', help="Comma separated list of signal processes. auto = automatically inferred from input workspaces")
  parser.add_option('--mass', dest='mass', default='125', help="Input workspace mass")
  parser.add_option('--analysis', dest='analysis', default='STXS', help="Analysis extension for XS*BR (see commonTools/XSBRMap.py)")
  parser.add_option('--mergeYears', dest='mergeYears', default=False, action="store_true", help="Category merged across years in the datacard")
  parser.add_option('--skipZeroes', dest='skipZeroes', default=False, action="store_true", help="Signal processes with 0 sum of weights are not in the datacard")
  parser.add_option('--pruneThreshold', dest='pruneThreshold', default=0.001, type='float', help="Datacard pruning threshold")
  parser.add_option('--safetyFactor', dest='safetyFactor', default=0.5, type='float', help="Fit the model if yield >= safetyFactor*pruneThreshold*(category yield). 1 = exactly the datacard rule, below 1 = margin of extra fits")
  return parser.parse_args()
(opt,args) = get_options()

if not 0. < opt.safetyFactor <= 1.:
  print(" --> [ERROR] safetyFactor must be in (0,1]: a value above 1 would skip models which the datacard needs")
  sys.exit(1)

inputWSDirMap, outputMap = od(), od()
for i in opt.inputWSDirMap.split(","): inputWSDirMap[i.split("=")[0]] = i.split("=")[1]
for i in opt.outputMap.split(","): outputMap[i.split("=")[0]] = i.split("=")[1]
years = list(inputWSDirMap.keys())
if set(years) != set(outputMap.keys()):
  print(" --> [ERROR] inputWSDirMap and outputMap must have the same years")
  sys.exit(1)
cats = opt.cats.split(",")

# Same list of procs as makeYields.py
if opt.procs == 'auto': procs = extractListOfProcs(extractWSFileNames(inputWSDirMap[years[0]])).split(",")
else: procs = opt.procs.split(",")
procs.sort()

# XS*BR as in makeDatacard.py
XSBR = extractXSBR(pd.DataFrame({'type':['sig']*len(procs),'procOriginal':procs}),mass=opt.mass,analysis=opt.analysis)

# Yields: one pass over the nominal mass workspaces, same dataset as makeYields.py
rows = []
for year in years:
  for ip,proc in enumerate(procs):
    print(" --> Extracting yields: (%s,%s) [%.1f%%]"%(proc,year,100*float(ip)/len(procs)))
    _proc_s0 = procToData(proc.split("_")[0])
    f = ROOT.TFile(glob.glob("%s/*M%s*_%s.root"%(inputWSDirMap[year],opt.mass,proc))[0])
    w = f.Get(inputWSName__)
    for cat in cats:
      if (len(proc.split("_")) <= 2) and (proc.split("_")[-1] in ["in", "out"]):
        _nominalDataName = "%s_%s_%s_%s_%s"%(_proc_s0,procToData(proc.split("_")[-1]),opt.mass,sqrts__,cat)
      else:
        _nominalDataName = "%s_%s_%s_%s"%(_proc_s0,opt.mass,sqrts__,cat)
      d = w.data(_nominalDataName)
      if not d:
        print(" --> [ERROR] dataset %s missing in %s"%(_nominalDataName,f.GetName()))
        sys.exit(1)
      sumw = d.sumEntries()
      _cat = cat if opt.mergeYears else "%s_%s"%(cat,year)
      rows.append({'year':year,'proc':proc,'cat':cat,'datacardCat':_cat,'sumw':sumw,'true_yield':XSBR["XS_%s"%proc]*XSBR['BR']*sumw*float(lumiMap[year])*1000})
    w.Delete()
    f.Close()
data = pd.DataFrame(rows)

# Rows which makeYields.py does not add (--skipZeroes) do not count in the category yield and need no model
inCard = (data['sumw']!=0.) if opt.skipZeroes else pd.Series(True,index=data.index)
catTrueYields = data[inCard].groupby('datacardCat')['true_yield'].sum()
data['catYield'] = data['datacardCat'].map(catTrueYields).fillna(0.)
data['prunedInCard'] = (~inCard)|(data['true_yield']<opt.pruneThreshold*data['catYield'])
data['skipFit'] = (~inCard)|(data['true_yield']<opt.safetyFactor*opt.pruneThreshold*data['catYield'])
# Signal packaging takes the merged datasets from one model per era and category: always keep the largest
for (year,cat),g in data[inCard].groupby(['year','cat']):
  data.loc[g['true_yield'].idxmax(),'skipFit'] = False

if (data['skipFit']&~data['prunedInCard']).any():
  print(" --> [ERROR] a model needed by the datacard would be skipped")
  sys.exit(1)

for year in years:
  dy = data[data['year']==year]
  out = od()
  out['pruneThreshold'] = opt.pruneThreshold
  out['safetyFactor'] = opt.safetyFactor
  out['mass'] = opt.mass
  out['analysis'] = opt.analysis
  out['nTotal'] = int(len(dy))
  out['nInDatacard'] = int((~dy['prunedInCard']).sum())
  out['nFit'] = int((~dy['skipFit']).sum())
  out['skip'] = od()
  for cat in cats: out['skip'][cat] = sorted(dy[(dy['cat']==cat)&dy['skipFit']]['proc'].tolist())
  print(" --> %s: %g proc x cat, %g kept by the datacard, %g to fit, %g skipped"%(year,out['nTotal'],out['nInDatacard'],out['nFit'],out['nTotal']-out['nFit']))
  outDir = os.path.dirname(outputMap[year])
  if not os.path.isdir(outDir): os.makedirs(outDir)
  # Complete file or no file: the fit workflow treats an existing list as final
  with open(outputMap[year]+".tmp","w") as jf: json.dump(out,jf,indent=1)
for year in years: os.rename(outputMap[year]+".tmp",outputMap[year])
