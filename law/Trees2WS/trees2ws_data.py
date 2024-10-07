import law
import os
import subprocess
import importlib.util
import ROOT
import re
import uproot
from optparse import OptionParser
from collections import OrderedDict as od
import yaml

# Centre of mass energy string
sqrts__ = "13TeV"

# Luminosity map in fb^-1: for using UL 2018
lumiMap = {
    '2016':36.33, 
    '2017':41.48, 
    '2018':59.83, 
    'combined':137.65, 
    'merged':137.65,
    '2022preEE':8.00,
    '2022postEE':26.70,
    '2022': 34.70
}
# flashgg input WS objects
inputWSName__ = "tagsDumper/cms_hgg_13TeV"

# Helper function to import a module from a file path
def import_module_from_path(file_path):
    module_name = re.sub(r'\.py$', '', file_path.replace(os.sep, '.'))
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load the spec for module {module_name} from {file_path}.")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Trees2WSData(law.Task):
    # input_path = law.Parameter(description="Path to the data input ROOT file")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default='', description="Variable to be used for output folder naming")
    year = law.Parameter(default='2022', description="Year")
    apply_mass_cut = law.Parameter(default=False, description="Apply mass cut")
    mass_cut_range = law.Parameter(default='100,180', description="Mass cut range")

    def output(self):
        # Load the input configuration
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        if not os.path.exists(input_config):
            print(f"[ERROR] {input_config} does not exist. Exiting...")
            return

        # Import the configuration options from the config file
        # config_module = import_module_from_path(input_config)
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        if self.variable == '':
            ws_dir = os.path.join(output_dir, f"input_output_data_{self.year}/ws/")
        else:
            ws_dir = os.path.join(output_dir, f"input_output_data_{self.variable}_{self.year}/ws/")
        return law.LocalFileTarget(os.path.join(ws_dir, "allData.root"))

    def run(self):
        # Load the input configuration
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        if not os.path.exists(input_config):
            print(f"[ERROR] {input_config} does not exist. Exiting...")
            return

        # Import the configuration options from the config file
        # config_module = import_module_from_path(input_config)
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        # Step 1: Create the output directory if it doesn't exist
        if self.variable == '':
            ws_dir = os.path.join(output_dir, f"input_output_data_{self.year}/ws/")
        else:
            ws_dir = os.path.join(output_dir, f"input_output_data_{self.variable}_{self.year}/ws/")
        os.makedirs(ws_dir, exist_ok=True)

        # Load the input configuration
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        if not os.path.exists(input_config):
            print(f"[ERROR] {input_config} does not exist. Exiting...")
            return

        # Import the configuration options from the config file
        # config_module = import_module_from_path(input_config)
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)
            
        # trees2ws_cfg = config_module.trees2wsCfg
        # input_tree_dir = trees2ws_cfg['inputTreeDir']
        # data_vars = trees2ws_cfg['dataVars']
        # categories = trees2ws_cfg['cats']
        input_path = config["inputFiles"]["Trees2WSData"]
        
        config = config[f"trees2wsCfg"]
        input_tree_dir = config['inputTreeDir']
        data_vars = config['dataVars']
        categories = config['cats']
        apply_mass_cut = config["apply_mass_cut"]
        massCutRange = config["mass_cut_range"]
        

        # Step 2: Convert data trees to RooWorkspace
        # Open the input ROOT file
        f = uproot.open(input_path)
        list_of_tree_names = f.keys() if input_tree_dir == '' else f[input_tree_dir].keys()

        if categories == 'auto':
            categories = []
        for tn in list_of_tree_names:
            if "sigma" in tn: continue
            c = tn.split("_%s_"%sqrts__)[-1].split(";")[0]
            categories.append(c)
            
        f = ROOT.TFile(input_path)

        # Create ROOT output workspace
        output_ws_file = os.path.join(ws_dir, "allData_{self.year}.root")
        fout = ROOT.TFile(output_ws_file, "RECREATE")
        # fout_dir = fout.mkdir("ws")
        # fout_dir.cd()
        # ws = ROOT.RooWorkspace("ws", "ws")
        foutdir = fout.mkdir(inputWSName__.split("/")[0])
        foutdir.cd()
        ws = ROOT.RooWorkspace(inputWSName__.split("/")[1],inputWSName__.split("/")[1])

        # Function to add variables to workspace
        def add_vars_to_workspace(_ws, _dataVars):
            intLumi = ROOT.RooRealVar("intLumi", "intLumi", 1000., 0., 999999999.)
            intLumi.setConstant(True)
            getattr(_ws, 'import')(intLumi)
            _vars = od()
            for var in _dataVars:
                if var == "CMS_hgg_mass":
                    _vars[var] = ROOT.RooRealVar(var, var, 125., 100., 180.)
                    _vars[var].setBins(160)
                elif var == "dZ":
                    _vars[var] = ROOT.RooRealVar(var, var, 0., -20., 20.)
                    _vars[var].setBins(40)
                elif var == "weight":
                    _vars[var] = ROOT.RooRealVar(var, var, 0.)
                else:
                    _vars[var] = ROOT.RooRealVar(var, var, 1., -999999, 999999)
                    _vars[var].setBins(1)
                getattr(_ws, 'import')(_vars[var], ROOT.RooFit.Silence())
            return _vars.keys()

        # Add variables to the workspace
        var_names = add_vars_to_workspace(ws, data_vars)

        # Function to make RooArgSet
        def make_argset(_ws, _varNames):
            _aset = ROOT.RooArgSet()
            for v in _varNames:
                _aset.add(_ws.var(v))
            return _aset

        # Make the argument set
        aset = make_argset(ws, var_names)

        # Loop over categories and extract data
        for cat in categories:
            # tree_name = f"Data_13TeV_{cat}" if input_tree_dir == '' else f"{input_tree_dir}/Data_13TeV_{cat}"
            # print(f" --> Extracting events from category: {cat}")
            # t = f[tree_name].arrays(library="np")
            print(" --> Extracting events from category: %s"%cat)
            if input_tree_dir == '': treeName = "Data_%s_%s"%(sqrts__,cat)
            else: treeName = "%s/Data_%s_%s"%(input_tree_dir,sqrts__,cat)
            print("    * tree: %s"%treeName)
            t = f.Get(treeName)

            # Define dataset for the category
            # dname = f"Data_13TeV_{cat}"
            dname = "Data_%s_%s"%(sqrts__,cat)  
            d = ROOT.RooDataSet(dname, dname, aset, 'weight')

            # Loop over events in the tree and add to the dataset
            for ev in t:
                if self.apply_mass_cut:
                    if(getattr(ev,"CMS_hgg_mass") < float(massCutRange.split(",")[0])) | (getattr(ev,"CMS_hgg_mass") > float(massCutRange.split(",")[1])): continue
                for var in data_vars: 
                    if var == "weight": continue
                    ws.var(var).setVal(getattr(ev,var))
                d.add(aset,1.)

            # Add dataset to the workspace
            getattr(ws, 'import')(d)

        # Write the workspace to the output file
        ws.Write()
        fout.Close()

        # Step 3: Rename the output file
        all_data_file = os.path.join(ws_dir, "allData.root")
        os.rename(output_ws_file, all_data_file)
        print(f"Workspace written and renamed to {all_data_file}")

# LAW Task Execution Example:
# law run ConvertTreesToWS --input-path /afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/devel/EOSCMS/2024/ntuples/forPaper_24_09_06/variables/NJets/data_postprocessing/root/Data/allData_2022.root --output-dir /afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/Trees2WS/output --variable Njets2p5 --year 2022