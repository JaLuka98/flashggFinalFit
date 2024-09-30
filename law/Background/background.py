import law
import os
import subprocess
import importlib.util
import ROOT
import re
import uproot
from optparse import OptionParser
from collections import OrderedDict as od
from importlib import import_module
import glob
import yaml
import errno

import pandas
import numpy as np
import awkward as ak

from commonTools import *
from commonObjects import *
# from tools.STXS_tools import *
# from tools.diff_tools import *

# from framework import Task
# from framework import HTCondorWorkflow


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

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
                

class BackgroundCategory(law.Task):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the alldata input ROOT file")
    output_dir = law.Parameter(description="Path to the output directory")
    ext = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    year = law.Parameter(default='2022', description="Year")
    cat = law.Parameter(description="Current category (e.g. RECO_PTH_0p0_15p0_cat0)")
    cat_offset = law.Parameter(description="Category offset")
    nCats = law.Parameter(description="Number of Categories")
    
    # htcondor_job_kwargs_submit = {"spool": True}
    
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        return {i: num for i, num in enumerate(range(0, self.nCats + 1))}

    def output(self):
        

        bkg_plots = glob.glob(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/*_cat{self.cat_offset}.png')
        bkg_plots += glob.glob(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/*_cat{self.cat_offset}.pdf')
        bkg_plots += glob.glob(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/*_cat{self.cat_offset}.pdf_gofTest.pdf')
        
        outputFileTargets = []
        
        output_paths = [self.output_dir + f'/outdir_{self.ext}/CMS-HGG_multipdf_{self.cat}.root', self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/multipdf_{self.cat}.pdf',self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/multipdf_{self.cat}.png']
        
        output_paths += bkg_plots
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        safe_mkdir(self.output_dir)

        script_path = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/Background/runBackgroundScripts.sh"
        arguments = [
            "-i", self.input_path,
            "-p", "none",
            "-f", self.cat,
            "--outputFolder", f"{self.output_dir}",
            "--ext", self.ext,
            "--catOffset", self.cat_offset,
            "--intLumi", f"{lumiMap[self.year]}",
            "--year", f"{self.year}",
            "--batch", "local",
            "--queue", "microcentury",
            "--sigFile", "none",
            "--isData",
            "--fTest"
        ]
        command = [script_path] + arguments
        # print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)

class Background(law.Task):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    # ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    
    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        #Path should be somewhere centrally...
        configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
        if "2022" in self.year:
            year = "2022"
        else:
            year = self.year
        configYamlPath += f"{year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        config = config["backgroundScriptCfg"]
        
        if config['cats'] == 'auto':
            config['cats'] = (extractListOfCatsFromData(config['inputWS']))
        config['nCats'] = len(config['cats'].split(","))
    
        # Add dummy entries for procs and signalFitWSFile (used in old plotting script)
        config['signalFitWSFile'] = 'none'
        config['procs'] = 'none'
        config['batch'] = 'local'
        config['queue'] = 'none'
        if self.year == 'combined': config['year'] = 'all'
        else: config['year'] = self.year
        
            
        tasks = [BackgroundCategory(input_path=config['inputWS'], output_dir=self.output_dir, year=self.year, cat=config['cats'].split(",")[categoryIndex], cat_offset=str(config['catOffset']+categoryIndex), nCats=config['nCats'], ext=config['ext']) for categoryIndex in range(config['nCats'])]
        return tasks
        

    
    def output(self):
        # returns output folder
        
        output_paths = []
        
        output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{self.ext}_{self.variable}"))
        
        output_paths.append(law.LocalFileTarget(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/fTestResults.txt'))
                        
        return output_paths
                
    
    def run(self):
        
        return True