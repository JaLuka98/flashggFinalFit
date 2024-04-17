import ROOT
import sys
import os

def getTreeNames(f):
    return [key.GetName() for key in f.GetListOfKeys()]

def getBranchNames(tree):
    return [key.GetName() for key in tree.GetListOfBranches()]

def getRequiredVars():
    required_vars = []

    CMS_hgg_mass = ROOT.RooRealVar("CMS_hgg_mass","CMS_hgg_mass",125.,100.,180.)
    CMS_hgg_mass.setBins(160)
    required_vars.append(CMS_hgg_mass)

    weight = ROOT.RooRealVar("weight","weight",0.)
    required_vars.append(weight)

    weight_central_initial = ROOT.RooRealVar("weight_central_initial","weight_central_initial",0.)
    required_vars.append(weight_central_initial)

    dZ = ROOT.RooRealVar("dZ","dZ",0.,-20.,20.)
    dZ.setBins(40)
    required_vars.append(dZ) 

    return required_vars

def getSystVarNames(tree):
    all_branches = getBranchNames(tree)
    return [branch for branch in all_branches if "sigma" in branch]
    #return ["weight_tau_idDeepTauVSjet_sf_AnalysisTau_syst_2018Down01sigma"]

def getSystVars(tree):
    syst_var_names = getSystVarNames(tree)
    return [ROOT.RooRealVar(name,name,0.) for name in syst_var_names]

def makeArgSet(vars):
    argset = ROOT.RooArgSet()
    for v in vars:
        argset.add(v)
    return argset

def main(args):
    ff = ROOT.TFile(args.inputTreeFile)
    
    if args.TreeDirectory is not None:
        f = ff.Get(args.TreeDirectory)
    else:
        f = ff

    tree_names = getTreeNames(f)

    nominal_names = [name for name in tree_names if ("Up" not in name) & ("Down" not in name)]
    syst_names = [name for name in tree_names if name not in nominal_names]

    nominal_trees = [f.Get(name) for name in nominal_names]
    syst_trees = [f.Get(name) for name in syst_names]

    ws = ROOT.RooWorkspace("cms_hgg_13TeV", "cms_hgg_13TeV")
    required_vars = getRequiredVars()
    syst_vars = getSystVars(nominal_trees[0])
    for var in required_vars + syst_vars:
        getattr(ws, "import")(var)

    all_vars_set = makeArgSet(required_vars + syst_vars)
    nominal_trees[0].Show(0)
    datasets = [ROOT.RooDataSet(name, name, nominal_trees[i], all_vars_set, '', 'weight') for i, name in enumerate(nominal_names)]
    for var in syst_vars:
        print(var.GetName(), datasets[0].get(0).getRealValue(var.GetName()))
    for dataset in datasets:
        getattr(ws, "import")(dataset)

    datahist_vars_set = makeArgSet(required_vars[:2]) # just CMS_hgg_mass
    syst_datasets = [ROOT.RooDataSet(name, name, syst_trees[i], datahist_vars_set, '', 'weight') for i, name in enumerate(syst_names)]
    datahists = [dataset.binnedClone() for dataset in syst_datasets]
    del syst_datasets
    for datahist in datahists:
        name = datahist.GetName().replace("_binned", "")
        datahist.SetNameTitle(name, name)
    for datahist in datahists:
        getattr(ws, "import")(datahist)

    ff.Close()

    fout = ROOT.TFile(args.outputWSFile, "CREATE")
    fout.mkdir("tagsDumper")
    fout.cd("tagsDumper")
    ws.Write()
    fout.Close()

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--inputTreeFile', type=str)
    parser.add_argument('-o', '--outputWSFile', type=str)
    parser.add_argument('-d', '--TreeDirectory', default=None, type=str,
                        help="Directory within root file where the TTree is stored. Default is the root directory")
    args = parser.parse_args()

    main(args)