import law
import os, sys
import subprocess
import importlib.util
# import ROOT
import re
# import uproot
# from optparse import OptionParser
# from collections import OrderedDict as od
# from importlib import import_module
import glob
import yaml
import errno

# import pandas
# import numpy as np
# import awkward as ak

from commonTools import *
from commonObjects import *
# from tools.STXS_tools import *
# from tools.diff_tools import *

# from framework import Task
# from framework import HTCondorWorkflow

sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "/tools")



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

# Define an array of eras
TwentyTwentyTwoEras = ["preEE", "postEE"]

allErasMap = {
    '2022': TwentyTwentyTwoEras
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
                

class FTestCategory(law.Task): #(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the alldata input ROOT file")
    output_dir = law.Parameter(description="Path to the output directory")
    ext = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    cat = law.Parameter(description="Current category (e.g. RECO_PTH_0p0_15p0_cat0)")
    procs = law.Parameter(description="Processes")
    
    # htcondor_job_kwargs_submit = {"spool": True}
    
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        return {i: num for i, num in enumerate(range(0, self.nCats + 1))}

    def output(self):
        safe_mkdir(self.output_dir)

        ftest_output = [self.output_dir + f'/outdir_{self.ext}/fTest/json/nGauss_{self.cat}.json']
        ftest_output += glob.glob(self.output_dir + f'/outdir_{self.ext}/fTest/Plots/fTest_{self.cat}*')
                
        outputFileTargets = []
        
                
        for _, current_output_path in enumerate(ftest_output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "/tools")
        
        safe_mkdir(self.output_dir)
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/fTest")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/fTest/Plots")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/fTest/json")

        script_path = os.environ["ANALYSIS_PATH"] + "/Signal/scripts/fTest.py"
        arguments = [
            "python3",
            script_path,
            "--cat", self.cat,
            "--procs", self.procs,
            "--ext", self.ext,
            "--outputDir", f"{self.output_dir}",
            "--inputWSDir", f"{self.input_path}",
            "--doPlots"
        ]
        command = arguments
        # print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)

class FTest(law.Task):
    input_path = law.Parameter(default = '', description="Path to the WS from Trees2WS.")
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    era = law.Parameter(default='None', description="Current era (eg. preEE, postEE for 2022), if any.")
    
    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        # #Path should be somewhere centrally...
        # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
        # if "2022" in self.year:
        #     year = "2022"
        # else:
        #     year = self.year
        # configYamlPath += f"{year}_{self.variable}.yml"
        
        # Path should be somewhere centrally...
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)


        if self.era != "None":
            config = config[f"signalScriptCfg_{self.year}_{self.era}"]
        else:
            config = config[f"signalScriptCfg_{self.year}"]
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Extract list of filenames
        WSFileNames = extractWSFileNames(self.input_path)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # If proc/cat == auto. Extract processes and categories
        if config['procs'] == "auto":
            config['procs'] = extractListOfProcs(WSFileNames)
            config['nProcs'] = len(config['procs'].split(","))

        if config['cats'] == "auto":
            config['cats'] = extractListOfCats(WSFileNames)
            config['nCats'] = len(config['cats'].split(","))
        
        # Extract low and high MH values
        mps = []
        for mp in config['massPoints'].split(","): mps.append(int(mp))
        config['massLow'], config['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                    
        config['batch'] = 'local'
        config['queue'] = 'none'
        
        tasks = []
        
        for categoryIndex in range(config['nCats']):
            category = config['cats'].split(",")[categoryIndex]
            tasks.append(FTestCategory(input_path=self.input_path, output_dir=self.output_dir, ext=config['ext'], cat=category, procs=config['procs']))
        

        return tasks
        

    
    def output(self):
        
        #Path should be somewhere centrally...
        # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
        # if "2022" in self.year:
        #     year = "2022"
        # else:
        #     year = self.year
        # configYamlPath += f"{year}_{self.variable}.yml"
        
        # Path should be somewhere centrally...
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)


        if self.era != "None":
            config = config[f"signalScriptCfg_{self.year}_{self.era}"]
        else:
            config = config[f"signalScriptCfg_{self.year}"]
        # returns output folder
        
        output_paths = []
        
        output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/fTest"))
        output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/fTest/json"))
        output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/fTest/Plots"))
        
        # output_paths.append(law.LocalFileTarget(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/fTestResults.txt'))
                        
        return output_paths
                
    
    def run(self):
        
        return True
    
    
class CalcPhotonSystCategory(law.Task):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the alldata input ROOT file")
    output_dir = law.Parameter(description="Path to the output directory")
    ext = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    cat = law.Parameter(description="Current category (e.g. RECO_PTH_0p0_15p0_cat0)")
    procs = law.Parameter(description="Processes")
    scales = law.Parameter(description="Scales")
    scalesCorr = law.Parameter(description="Scale corrections")
    scalesGlobal = law.Parameter(description="Global scales")
    smears = law.Parameter(description="Smearings")
    
    # htcondor_job_kwargs_submit = {"spool": True}
    
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        return {i: num for i, num in enumerate(range(0, self.nCats + 1))}

    def output(self):
        safe_mkdir(self.output_dir)

        ftest_output = [self.output_dir + f'/outdir_{self.ext}/calcPhotonSyst/pkl/{self.cat}.pkl']
        # ftest_output += glob.glob(self.output_dir + f'/outdir_{self.ext}/fTest/Plots/fTest_{self.cat}*')
                
        outputFileTargets = []
        
                
        for _, current_output_path in enumerate(ftest_output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "/tools")
        
        safe_mkdir(self.output_dir)
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/calcPhotonSyst")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/calcPhotonSyst/pkl")

        script_path = os.environ["ANALYSIS_PATH"] + "/Signal/scripts/calcPhotonSyst.py"
        arguments = [
            "python3",
            script_path,
            "--cat", self.cat,
            "--procs", self.procs,
            "--ext", self.ext,
            "--outputDir", f"{self.output_dir}",
            "--inputWSDir", f"{self.input_path}",
            "--scales", f"{self.scales}",
            "--scalesCorr", f"{self.scalesCorr}",
            "--scalesGlobal", f"{self.scalesGlobal}",
            "--smears", f"{self.smears}"
        ]
        command = arguments
        # print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)

class CalcPhotonSyst(law.Task):
    input_path = law.Parameter(description="Path to the WS from Trees2WS.")
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    era = law.Parameter(default='None', description="Current era (eg. preEE, postEE for 2022), if any.")

    
    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        # #Path should be somewhere centrally...
        # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
        # if "2022" in self.year:
        #     year = "2022"
        # else:
        #     year = self.year
        # configYamlPath += f"{year}_{self.variable}.yml"
        
        # Path should be somewhere centrally...
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)


        if self.era != "":
            config = config[f"signalScriptCfg_{self.year}_{self.era}"]
        else:
            config = config[f"signalScriptCfg_{self.year}"]
                
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Extract list of filenames
        WSFileNames = extractWSFileNames(self.input_path)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # If proc/cat == auto. Extract processes and categories
        if config['procs'] == "auto":
            config['procs'] = extractListOfProcs(WSFileNames)
            config['nProcs'] = len(config['procs'].split(","))

        if config['cats'] == "auto":
            config['cats'] = extractListOfCats(WSFileNames)
            config['nCats'] = len(config['cats'].split(","))
        
        # Extract low and high MH values
        mps = []
        for mp in config['massPoints'].split(","): mps.append(int(mp))
        config['massLow'], config['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                    
        config['batch'] = 'local'
        config['queue'] = 'none'
        
        tasks = []
        
        for categoryIndex in range(config['nCats']):
            category = config['cats'].split(",")[categoryIndex]
            tasks.append(CalcPhotonSystCategory(input_path=self.input_path, output_dir=self.output_dir, ext=config['ext'], cat=category, procs=config['procs'], scales=config['scales'], scalesCorr=config['scalesCorr'], scalesGlobal=config['scalesGlobal'], smears=config['smears']))

        return tasks
        

    
    def output(self):
        
        # #Path should be somewhere centrally...
        # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
        # if "2022" in self.year:
        #     year = "2022"
        # else:
        #     year = self.year
        # configYamlPath += f"{year}_{self.variable}.yml"
        
        # Path should be somewhere centrally...
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)


        if self.era != "None":
            config = config[f"signalScriptCfg_{self.year}_{self.era}"]
        else:
            config = config[f"signalScriptCfg_{self.year}"]
        # returns output folder
        
        output_paths = []
        
        # output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{self.ext}"))
        output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/calcPhotonSyst"))
        output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/calcPhotonSyst/pkl"))
        
        # output_paths.append(law.LocalFileTarget(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/fTestResults.txt'))
                        
        return output_paths
                
    
    def run(self):
        
        return True
    
    
class SignalFitCategoryProcess(law.Task):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the alldata input ROOT file")
    output_dir = law.Parameter(description="Path to the output directory")
    ext = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    cat = law.Parameter(description="Current category (e.g. RECO_PTH_0p0_15p0_cat0)")
    proc = law.Parameter(description="Current process")
    scales = law.Parameter(description="Scales")
    scalesCorr = law.Parameter(description="Scale corrections")
    scalesGlobal = law.Parameter(description="Global scales")
    smears = law.Parameter(description="Smearings")
    year = law.Parameter(description="Year")    
    analysis = law.Parameter(description="Analysis")    
    massPoints = law.Parameter(description="Mass Points")
    beamspotWidthData = law.Parameter(description="Beamspot width in Data")
    beamspotWidthMC = law.Parameter(description="Beamspot width in MC")
    
    variable = law.Parameter(default="", description="Variable to be used")
    
    # htcondor_job_kwargs_submit = {"spool": True}
    
    def requires(self):
        
        year = self.year[:4]
        
        # Path should be somewhere centrally...
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_{self.variable}.yml"
        
        # configYamlPath += f"{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        tasks = []
            
        # Loop over a years era
        for currentEra in allErasMap[f"{year}"]:
            
            input_path = config["outputFolder"] + f"/input_output_{year}{currentEra}/ws_signal"


            currentConfig = config[f"signalScriptCfg_{year}_{currentEra}"]
                    
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Extract list of filenames
            WSFileNames = extractWSFileNames(input_path)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If proc/cat == auto. Extract processes and categories
            if currentConfig['procs'] == "auto":
                currentConfig['procs'] = extractListOfProcs(WSFileNames)
                currentConfig['nProcs'] = len(currentConfig['procs'].split(","))

            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCats(WSFileNames)
                currentConfig['nCats'] = len(currentConfig['cats'].split(","))
            
            # Extract low and high MH values
            mps = []
            for mp in currentConfig['massPoints'].split(","): mps.append(int(mp))
            currentConfig['massLow'], currentConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                        
            currentConfig['batch'] = 'local'
            currentConfig['queue'] = 'none'
            
            
            tasks.append(FTest(input_path=input_path, variable=self.variable, output_dir=output_dir, year=year, ext=currentConfig['ext'], era=currentEra))
            tasks.append(CalcPhotonSyst(input_path=input_path, variable=self.variable, output_dir=output_dir, year=year, ext=currentConfig['ext'], era=currentEra))
                    
                
        return tasks
    
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        return {i: num for i, num in enumerate(range(0, (self.nCats*self.nProcs) + 1))}

    def output(self):
        safe_mkdir(self.output_dir)

        signal_output = [self.output_dir + f'/outdir_{self.ext}/signalFit/output/CMS-HGG_sigfit_{self.ext}_{self.proc}_{self.year}_{self.cat}.root']
        signal_output += glob.glob(self.output_dir + f'/outdir_{self.ext}/signalFit/Plots/{self.proc}_{self.year}_{self.cat}*')
                
        outputFileTargets = []
        
                
        for _, current_output_path in enumerate(signal_output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "/tools")
        
        safe_mkdir(self.output_dir)
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/signalFit")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/signalFit/output")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/signalFit/Plots")

        script_path = os.environ["ANALYSIS_PATH"] + "/Signal/scripts/signalFit.py"
        arguments = [
            "python3",
            script_path,
            "--cat", self.cat,
            "--proc", self.proc,
            "--ext", self.ext,
            "--outputDir", f"{self.output_dir}",
            "--inputWSDir", f"{self.input_path}",
            "--year", f"{self.year}",
            "--scales", f"{self.scales}",
            "--scalesCorr", f"{self.scalesCorr}",
            "--scalesGlobal", f"{self.scalesGlobal}",
            "--smears", f"{self.smears}",
            "--analysis", f"{self.analysis}",
            "--massPoints", f"{self.massPoints}",
            "--beamspotWidthData", f"{self.beamspotWidthData}",
            "--beamspotWidthMC", f"{self.beamspotWidthMC}"
        ]
        command = arguments
        # print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)

# class SignalFitRequirements(law.Task):
#     input_path = law.Parameter(description="Path to the WS from Trees2WS.")
#     variable = law.Parameter(default="", description="Variable to be used")
#     output_dir = law.Parameter(description="Path to the output directory")
#     year = law.Parameter(default='2022', description="Year")
#     era = law.Parameter(default='None', description="Current era (eg. preEE, postEE for 2022), if any.")
#     ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    
#     def requires(self):
        
#         # #Path should be somewhere centrally...
#         # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
#         # if "2022" in self.year:
#         #     year = "2022"
#         # else:
#         #     year = self.year
#         # configYamlPath += f"{year}_{self.variable}.yml"
        
#         # Path should be somewhere centrally...
#         if self.variable == '':
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
#         else:
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
#         #Load central config file
#         with open(configYamlPath, 'r') as file:
#             config = yaml.safe_load(file)

#         if self.era != "None":
#             config = config[f"signalScriptCfg_{self.year}_{self.era}"]
#         else:
#             config = config[f"signalScriptCfg_{self.year}"]
                
#         # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#         # Extract list of filenames
#         WSFileNames = extractWSFileNames(self.input_path)

#         # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#         # If proc/cat == auto. Extract processes and categories
#         if config['procs'] == "auto":
#             config['procs'] = extractListOfProcs(WSFileNames)
#             config['nProcs'] = len(config['procs'].split(","))

#         if config['cats'] == "auto":
#             config['cats'] = extractListOfCats(WSFileNames)
#             config['nCats'] = len(config['cats'].split(","))
        
#         # Extract low and high MH values
#         mps = []
#         for mp in config['massPoints'].split(","): mps.append(int(mp))
#         config['massLow'], config['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                    
#         config['batch'] = 'local'
#         config['queue'] = 'none'
        
        
#         tasks = []
#         tasks.append(FTest(input_path=self.input_path, variable=self.variable, output_dir=self.output_dir, year=self.year, ext=config['ext'], era=self.era))
#         tasks.append(CalcPhotonSyst(input_path=self.input_path, variable=self.variable, output_dir=self.output_dir, year=self.year, ext=config['ext'], era=self.era))
        
#         return tasks
        

    
#     def output(self):
        
#         # #Path should be somewhere centrally...
#         # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
#         # if "2022" in self.year:
#         #     year = "2022"
#         # else:
#         #     year = self.year
#         # configYamlPath += f"{year}_{self.variable}.yml"
        
#         # Path should be somewhere centrally...
#         if self.variable == '':
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
#         else:
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
#         #Load central config file
#         with open(configYamlPath, 'r') as file:
#             config = yaml.safe_load(file)


#         if self.era != "None":
#             config = config[f"signalScriptCfg_{self.year}_{self.era}"]
#         else:
#             config = config[f"signalScriptCfg_{self.year}"]
#         # returns output folder
        
#         output_paths = []
        
#         # output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{self.ext}"))
#         output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/calcPhotonSyst"))
#         output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/calcPhotonSyst/pkl"))
#         output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/fTest"))
#         output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/fTest/Plots"))
#         output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{config['ext']}/fTest/json"))
        
#         # output_paths.append(law.LocalFileTarget(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/fTestResults.txt'))
                        
#         return output_paths
                
    
#     def run(self):
#         return True
    
# class SignalFit(law.Task):
#     # input_path = law.Parameter(default = '', description="Path to the WS from Trees2WS.")
#     variable = law.Parameter(default="", description="Variable to be used")
#     output_dir = law.Parameter(default = '', description="Path to the output directory")
#     year = law.Parameter(default='2022', description="Year")
#     # ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    
#     def requires(self):
        
#         # #Path should be somewhere centrally...
#         # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
#         # if "2022" in self.year:
#         #     year = "2022"
#         # else:
#         #     year = self.year
#         # configYamlPath += f"{year}_{self.variable}.yml"
        
#         # Path should be somewhere centrally...
#         if self.variable == '':
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
#         else:
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
#         # configYamlPath += f"{self.year}_{self.variable}.yml"

        
#         #Load central config file
#         with open(configYamlPath, 'r') as file:
#             config = yaml.safe_load(file)
            
#         if self.output_dir == '':
#             output_dir = config["outputFolder"]
#         else:
#             output_dir = self.output_dir
            
#         tasks = []
            
#         # Loop over a years era
#         for currentEra in allErasMap[f"{self.year}"]:
            
#             input_path = config["outputFolder"] + f"/input_output_{self.year}{currentEra}/ws_signal"


#             currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
                    
#             # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             # Extract list of filenames
#             WSFileNames = extractWSFileNames(input_path)

#             # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             # If proc/cat == auto. Extract processes and categories
#             if currentConfig['procs'] == "auto":
#                 currentConfig['procs'] = extractListOfProcs(WSFileNames)
#                 currentConfig['nProcs'] = len(currentConfig['procs'].split(","))

#             if currentConfig['cats'] == "auto":
#                 currentConfig['cats'] = extractListOfCats(WSFileNames)
#                 currentConfig['nCats'] = len(currentConfig['cats'].split(","))
            
#             # Extract low and high MH values
#             mps = []
#             for mp in currentConfig['massPoints'].split(","): mps.append(int(mp))
#             currentConfig['massLow'], currentConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                        
#             currentConfig['batch'] = 'local'
#             currentConfig['queue'] = 'none'
            
            
            
#             tasks.append(SignalFitRequirements(input_path=input_path, variable=self.variable, output_dir=output_dir, year=self.year, ext=currentConfig['ext'], era=currentEra))   
            
#             for processIndex in range(currentConfig['nProcs']):
#                 for categoryIndex in range(currentConfig['nCats']):
#                     # processCategoryIndex = processIndex*config['nCats']+categoryIndex
#                     category = currentConfig['cats'].split(",")[categoryIndex]
#                     process = currentConfig['procs'].split(",")[processIndex]
#                     tasks.append(SignalFitCategoryProcess(input_path=input_path, output_dir=output_dir, ext=currentConfig['ext'], cat=category, proc=process, scales=currentConfig['scales'], scalesCorr=currentConfig['scalesCorr'], scalesGlobal=currentConfig['scalesGlobal'], smears=currentConfig['smears'], year=currentConfig['year'], analysis=currentConfig['analysis'], massPoints=currentConfig['massPoints'], beamspotWidthData=currentConfig['beamspotWidthData'], beamspotWidthMC=currentConfig['beamspotWidthMC']))
#                     # SignalFitCategoryProcess(input_path=self.input_path, output_dir=self.output_dir, ext=config['ext'], cat=category, proc=process, scales=config['scales'], scalesCorr=config['scalesCorr'], scalesGlobal=config['scalesGlobal'], smears=config['smears'], year=config['year'], analysis=config['analysis'], massPoints=config['massPoints'])
                    
                
#         return tasks
        

    
#     def output(self):
        
#         # #Path should be somewhere centrally...
#         # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
#         # if "2022" in self.year:
#         #     year = "2022"
#         # else:
#         #     year = self.year
#         # configYamlPath += f"{year}_{self.variable}.yml"
        
#         # Path should be somewhere centrally...
#         if self.variable == '':
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
#         else:
#             # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
#             configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
#         # configYamlPath += f"{self.year}_{self.variable}.yml"

        
#         #Load central config file
#         with open(configYamlPath, 'r') as file:
#             config = yaml.safe_load(file)
            
#         if self.output_dir == '':
#             output_dir = config["outputFolder"]
#         else:
#             output_dir = self.output_dir
            
#         output_paths = []
                    
#         # Loop over a years era
#         for currentEra in allErasMap[f"{self.year}"]:

#             currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
#             # returns output folder
            
#             # output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{self.ext}"))
#             output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit"))
#             output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/output"))
#             output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/Plots"))
            
#             output_paths += glob.glob(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/output/CMS-HGG_sigfit*.root")
            
#             # output_paths.append(law.LocalFileTarget(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/fTestResults.txt'))
                        
#         return output_paths
                
#     def run(self):
        
#         return True


class SignalFit(law.Task):
    # input_path = law.Parameter(default = '', description="Path to the WS from Trees2WS.")
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    # ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    
    def requires(self):
        
                # Path should be somewhere centrally...
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        # configYamlPath += f"{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        tasks = []
            
        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:
            
            input_path = config["outputFolder"] + f"/input_output_{self.year}{currentEra}/ws_signal"


            currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
                    
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Extract list of filenames
            WSFileNames = extractWSFileNames(input_path)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If proc/cat == auto. Extract processes and categories
            if currentConfig['procs'] == "auto":
                currentConfig['procs'] = extractListOfProcs(WSFileNames)
                currentConfig['nProcs'] = len(currentConfig['procs'].split(","))

            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCats(WSFileNames)
                currentConfig['nCats'] = len(currentConfig['cats'].split(","))
            
            # Extract low and high MH values
            mps = []
            for mp in currentConfig['massPoints'].split(","): mps.append(int(mp))
            currentConfig['massLow'], currentConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                        
            currentConfig['batch'] = 'local'
            currentConfig['queue'] = 'none'
            
                        
            for processIndex in range(currentConfig['nProcs']):
                for categoryIndex in range(currentConfig['nCats']):
                    # processCategoryIndex = processIndex*config['nCats']+categoryIndex
                    category = currentConfig['cats'].split(",")[categoryIndex]
                    process = currentConfig['procs'].split(",")[processIndex]
                    tasks.append(SignalFitCategoryProcess(input_path=input_path, output_dir=output_dir, ext=currentConfig['ext'], cat=category, proc=process, scales=currentConfig['scales'], scalesCorr=currentConfig['scalesCorr'], scalesGlobal=currentConfig['scalesGlobal'], smears=currentConfig['smears'], year=currentConfig['year'], analysis=currentConfig['analysis'], massPoints=currentConfig['massPoints'], beamspotWidthData=currentConfig['beamspotWidthData'], beamspotWidthMC=currentConfig['beamspotWidthMC']))
                    # SignalFitCategoryProcess(input_path=self.input_path, output_dir=self.output_dir, ext=config['ext'], cat=category, proc=process, scales=config['scales'], scalesCorr=config['scalesCorr'], scalesGlobal=config['scalesGlobal'], smears=config['smears'], year=config['year'], analysis=config['analysis'], massPoints=config['massPoints'])
                    
        # output = self.output()
        # output.dump(tasks)
                    
                
        return tasks

    
    def output(self):
        
        # #Path should be somewhere centrally...
        # configYamlPath = "/afs/cern.ch/user/n/niharrin/cernbox/PhD/Higgs/CMSSW_14_1_0_pre4/src/flashggFinalFit/law/config/"
        # if "2022" in self.year:
        #     year = "2022"
        # else:
        #     year = self.year
        # configYamlPath += f"{year}_{self.variable}.yml"
        
        # Path should be somewhere centrally...
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        # configYamlPath += f"{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        output_paths = []
                    
        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:

            currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
            # returns output folder
            
            # output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{self.ext}"))
            output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit"))
            output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/output"))
            output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/Plots"))
            
            output_paths += glob.glob(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/output/CMS-HGG_sigfit*.root")
            
            # output_paths.append(law.LocalFileTarget(self.output_dir + f'/outdir_{self.ext}/bkgfTest-Data/fTestResults.txt'))
                        
        return output_paths
                
    def run(self):
        return True