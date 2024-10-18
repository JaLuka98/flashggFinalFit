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
from Trees2WS.trees2ws import *
# from tools.STXS_tools import *
# from tools.diff_tools import *

from framework import Task
from framework import HTCondorWorkflow

sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "/tools")

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def count_files_in_directory(directory='.'):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
                

class FTestCategory(Task, HTCondorWorkflow, law.LocalWorkflow): #(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the input ROOT files (/ws_signal)")
    output_dir = law.Parameter(description="Path to the output directory")
    ext = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    cats = law.Parameter(description="Category string")
    procs = law.Parameter(description="Processes")
    variable = law.Parameter(default="", description="Variable to be used")
    year = law.Parameter(description="Year")    


    
    htcondor_job_kwargs_submit = {"spool": True}
    
    def requires(self):
        
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
            
        tasks = [Trees2WS(output_dir=output_dir, variable=self.variable, year=self.year)]
        
        return tasks
    
    # def create_branch_map(self):
    #     # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
    #     return {i: num for i, num in enumerate(range(0, self.nCats + 1))}
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        nCats = len(self.cats.split(","))
        
        cat_list = [
            self.cats.split(",")[categoryIndex]
            for categoryIndex in range(nCats)
        ]
        
        branch_map = {i: cat for i, cat in enumerate(cat_list)}
        return branch_map

    def output(self):
        
        cat = self.branch_data

        safe_mkdir(self.output_dir)

        ftest_output = [self.output_dir + f'/outdir_{self.ext}/fTest/json/nGauss_{cat}.json']
                
        outputFileTargets = []
                
        for _, current_output_path in enumerate(ftest_output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        cat = self.branch_data
        
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
            "--cat", cat,
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
    # input_path = law.Parameter(description="Path to the input ROOT files (/ws_signal)")
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    # ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    # era = law.Parameter(default='None', description="Current era (eg. preEE, postEE for 2022), if any.")
    
    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        # Use allData.root from HiggsDNA to automatically determine categories
        data_input_path = config['inputFiles']['Trees2WSData']  
        inOutSplittingFlag = config['trees2wsCfg']['doInOutSplitting'] or config['trees2wsCfg']['doDiffSplitting'] # We do the in out splitting for the differentials in HIG-23-014
        signal_input_path = glob.glob(config['inputFiles']['Trees2WS']+'/*')
        
        tasks = []
        
        i = 1
        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:
            
            
            if self.variable == '':
                input_path = config["outputFolder"] + f"/input_output_{self.year}{currentEra}/ws_signal"
            else:
                input_path = config["outputFolder"] + f"/input_output_{self.variable}_{self.year}{currentEra}/ws_signal"


            if currentEra != "None":
                currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
            else:
                currentConfig = config[f"signalScriptCfg_{self.year}"]

            # Extract low and high MH values
            mps = []
            for mp in currentConfig['massPoints'].split(","): mps.append(int(mp))
            currentConfig['massLow'], currentConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                        
            currentConfig['batch'] = 'local'
            currentConfig['queue'] = 'none'

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If proc/cat == auto. Extract processes and categories
            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
            currentConfig['nCats'] = len(currentConfig['cats'].split(","))

            if currentConfig['procs'] == "auto":
                currentConfig['procs'] = extractListOfProcsFromHiggsDNASignal(signal_input_path, self.variable, inOutSplittingFlag)
            currentConfig['nProcs'] = len(currentConfig['procs'].split(","))
            
            
            tasks.append(FTestCategory(input_path=input_path, output_dir=self.output_dir, ext=currentConfig['ext'], cats=currentConfig['cats'], procs=currentConfig['procs'], variable=self.variable, year=self.year, version=f"v{i}", workflow="htcondor"))
            i += 1
        
        return tasks
        

    
    def output(self):
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        data_input_path = config['inputFiles']['Trees2WSData']  

        output_paths = []

        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:

            if currentEra != "None":
                currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
            else:
                currentConfig = config[f"signalScriptCfg_{self.year}"]
            # returns output folder
            
            
            output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{currentConfig['ext']}/fTest"))
            output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{currentConfig['ext']}/fTest/json"))
            output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{currentConfig['ext']}/fTest/Plots"))
            
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If proc/cat == auto. Extract processes and categories
            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
                
            cat_list = currentConfig['cats'].split(",")
            for cat in cat_list:
                output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{currentConfig['ext']}/fTest/json/nGauss_{cat}.json"))

        return output_paths
                
    
    def run(self):
        
        return True
    
    
class CalcPhotonSystCategory(Task, HTCondorWorkflow, law.LocalWorkflow):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the input ROOT files (/ws_signal)")
    output_dir = law.Parameter(description="Path to the output directory")
    ext = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    cats = law.Parameter(description="Category string")
    procs = law.Parameter(description="Processes")
    scales = law.Parameter(description="Scales")
    scalesCorr = law.Parameter(description="Scale corrections")
    scalesGlobal = law.Parameter(description="Global scales")
    smears = law.Parameter(description="Smearings")
    variable = law.Parameter(default="", description="Variable to be used")
    year = law.Parameter(description="Year")    
    
    htcondor_job_kwargs_submit = {"spool": True}
    def requires(self):
        
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
            
        tasks = [Trees2WS(output_dir=output_dir, variable=self.variable, year=self.year)]
        
        return tasks
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        nCats = len(self.cats.split(","))
        
        cat_list = [
            self.cats.split(",")[categoryIndex]
            for categoryIndex in range(nCats)
        ]
        
        branch_map = {i: cat for i, cat in enumerate(cat_list)}
        return branch_map

    def output(self):
        
        cat = self.branch_data
        
        safe_mkdir(self.output_dir)

        ftest_output = [self.output_dir + f'/outdir_{self.ext}/calcPhotonSyst/pkl/{cat}.pkl']
                
        outputFileTargets = []
        
                
        for _, current_output_path in enumerate(ftest_output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        
        cat = self.branch_data

        sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "/tools")
        
        safe_mkdir(self.output_dir)
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/calcPhotonSyst")
        safe_mkdir(self.output_dir+f"/outdir_{self.ext}/calcPhotonSyst/pkl")

        script_path = os.environ["ANALYSIS_PATH"] + "/Signal/scripts/calcPhotonSyst.py"
        arguments = [
            "python3",
            script_path,
            "--cat", cat,
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
    # input_path = law.Parameter(description="Path to the input ROOT files (/ws_signal)")
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    # ext = law.Parameter(default="earlyAnalysis", description="Descriptor of the background output folder.")
    # era = law.Parameter(default='None', description="Current era (eg. preEE, postEE for 2022), if any.")

    
    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        # Use allData.root from HiggsDNA to automatically determine categories
        data_input_path = config['inputFiles']['Trees2WSData']  
        inOutSplittingFlag = config['trees2wsCfg']['doInOutSplitting'] or config['trees2wsCfg']['doDiffSplitting']
        
        signal_input_path = glob.glob(config['inputFiles']['Trees2WS']+'/*')
        
        tasks = []
        
        i = 1
        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:
            
            if self.variable == '':
                input_path = config["outputFolder"] + f"/input_output_{self.year}{currentEra}/ws_signal"
            else:
                input_path = config["outputFolder"] + f"/input_output_{self.variable}_{self.year}{currentEra}/ws_signal"


            if currentEra != "None":
                currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
            else:
                currentConfig = config[f"signalScriptCfg_{self.year}"]
                
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If proc/cat == auto. Extract processes and categories
            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
            currentConfig['nCats'] = len(currentConfig['cats'].split(","))
            
            if currentConfig['procs'] == "auto":
                currentConfig['procs'] = extractListOfProcsFromHiggsDNASignal(signal_input_path, self.variable, inOutSplittingFlag)
            currentConfig['nProcs'] = len(currentConfig['procs'].split(","))
            
            # Extract low and high MH values
            mps = []
            for mp in currentConfig['massPoints'].split(","): mps.append(int(mp))
            currentConfig['massLow'], currentConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                        
            currentConfig['batch'] = 'local'
            currentConfig['queue'] = 'none'
                    
            tasks.append(CalcPhotonSystCategory(input_path=input_path, output_dir=self.output_dir, ext=currentConfig['ext'], cats=currentConfig['cats'], procs=currentConfig['procs'], scales=currentConfig['scales'], scalesCorr=currentConfig['scalesCorr'], scalesGlobal=currentConfig['scalesGlobal'], smears=currentConfig['smears'], variable=self.variable, year=self.year, version=f"v{i}", workflow="htcondor"))
            i += 1

        return tasks
        

    
    def output(self):
              
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"

        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        data_input_path = config['inputFiles']['Trees2WSData']  
        
        output_paths = []
        
        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:
            
            if currentEra != "None":
                currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
            else:
                currentConfig = config[f"signalScriptCfg_{self.year}"]
            # returns output folder
            
            output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{currentConfig['ext']}/calcPhotonSyst"))
            output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{currentConfig['ext']}/calcPhotonSyst/pkl"))
        
        
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If proc/cat == auto. Extract processes and categories
            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
                
            cat_list = currentConfig['cats'].split(",")
            for cat in cat_list:
                output_paths.append(law.LocalFileTarget(self.output_dir + f"/outdir_{currentConfig['ext']}/calcPhotonSyst/pkl/{cat}.pkl"))
                                    
        return output_paths
                
    
    def run(self):
        
        return True
    
    
class SignalFitCategoryProcess(Task, HTCondorWorkflow, law.LocalWorkflow):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the input ROOT files (/ws_signal)")
    output_dir = law.Parameter(description="Path to the output directory")
    ext = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    cats = law.Parameter(description="Category list")
    procs = law.Parameter(description="Process list")
    scales = law.Parameter(description="Scales")
    scalesCorr = law.Parameter(description="Scale corrections")
    scalesGlobal = law.Parameter(description="Global scales")
    smears = law.Parameter(description="Smearings")
    year = law.Parameter(description="Year")    
    analysis = law.Parameter(description="Analysis")    
    massPoints = law.Parameter(description="Mass Points")
    beamspotWidthData = law.Parameter(description="Beamspot width in Data")
    beamspotWidthMC = law.Parameter(description="Beamspot width in MC")
    doPlots = law.Parameter(description="Printing the signal models.")
    
    variable = law.Parameter(default="", description="Variable to be used")
    
    htcondor_job_kwargs_submit = {"spool": True}
    
    def requires(self):
        
        year = self.year[:4]
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        tasks = []
            
        # # Loop over a years era
        # for currentEra in allErasMap[f"{year}"]:
            
            
        #     if self.variable == '':
        #         input_path = config["outputFolder"] + f"/input_output_{year}{currentEra}/ws_signal"
        #     else:
        #         input_path = config["outputFolder"] + f"/input_output_{self.variable}_{year}{currentEra}/ws_signal"

        #     currentConfig = config[f"signalScriptCfg_{year}_{currentEra}"]

        #     # Extract low and high MH values
        #     mps = []
        #     for mp in currentConfig['massPoints'].split(","): mps.append(int(mp))
        #     currentConfig['massLow'], currentConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                        
        #     currentConfig['batch'] = 'local'
        #     currentConfig['queue'] = 'none'
            
            
        #     tasks.append(FTest(input_path=input_path, variable=self.variable, output_dir=output_dir, year=year, ext=currentConfig['ext'], era=currentEra))
        #     tasks.append(CalcPhotonSyst(input_path=input_path, variable=self.variable, output_dir=output_dir, year=year, ext=currentConfig['ext'], era=currentEra))
            
        tasks.append(FTest(variable=self.variable, output_dir=output_dir, year=year))
        tasks.append(CalcPhotonSyst(variable=self.variable, output_dir=output_dir, year=year))
                    
                
        return tasks
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        nCats = len(self.cats.split(","))
        nProcs = len(self.procs.split(","))
        
        cat_proc_list = [
            (self.cats.split(",")[categoryIndex], self.procs.split(",")[processIndex])
            for categoryIndex in range(nCats)
            for processIndex in range(nProcs)
        ]
        
        branch_map = {i: cat_proc for i, cat_proc in enumerate(cat_proc_list)}
        
        return branch_map

    def output(self):
        
        cat, proc = self.branch_data
        
        safe_mkdir(self.output_dir)

        signal_output = [self.output_dir + f'/outdir_{self.ext}/signalFit/output/CMS-HGG_sigfit_{self.ext}_{proc}_{self.year}_{cat}.root']
        signal_output += glob.glob(self.output_dir + f'/outdir_{self.ext}/signalFit/Plots/{proc}_{self.year}_{cat}*')
                
        outputFileTargets = []
            
        for _, current_output_path in enumerate(signal_output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        
        cat, proc = self.branch_data
        
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
            "--cat", cat,
            "--proc", proc,
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
        if self.doPlots:
            arguments += ["--doPlots"]
        command = arguments
        # print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)

class SignalFit(law.Task):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    def requires(self):
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        signal_input_path = glob.glob(config['inputFiles']['Trees2WS']+'/*')
        
        inOutSplittingFlag = config['trees2wsCfg']['doInOutSplitting']  or config['trees2wsCfg']['doDiffSplitting']
            
        tasks = []
            
        i = 1
        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:
            
            if self.variable == "":
                input_path = config["outputFolder"] + f"/input_output_{self.year}{currentEra}/ws_signal"
            else:
                input_path = config["outputFolder"] + f"/input_output_{self.variable}_{self.year}{currentEra}/ws_signal"

            currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If proc/cat == auto. Extract processes and categories
            # Use allData.root from HiggsDNA to automatically determine categories
            data_input_path = config['inputFiles']['Trees2WSData']  
            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
            currentConfig['nCats'] = len(currentConfig['cats'].split(","))

            if currentConfig['procs'] == "auto":
                currentConfig['procs'] = extractListOfProcsFromHiggsDNASignal(signal_input_path, self.variable, inOutSplittingFlag)
            currentConfig['nProcs'] = len(currentConfig['procs'].split(","))
            
            # Extract low and high MH values
            mps = []
            for mp in currentConfig['massPoints'].split(","): mps.append(int(mp))
            currentConfig['massLow'], currentConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)
                        
            currentConfig['batch'] = 'local'
            currentConfig['queue'] = 'none'            
                        

            tasks.append(SignalFitCategoryProcess(input_path=input_path, output_dir=output_dir, ext=currentConfig['ext'], cats=currentConfig['cats'], procs=currentConfig['procs'], scales=currentConfig['scales'], scalesCorr=currentConfig['scalesCorr'], scalesGlobal=currentConfig['scalesGlobal'], smears=currentConfig['smears'], year=currentConfig['year'], analysis=currentConfig['analysis'], massPoints=currentConfig['massPoints'], beamspotWidthData=currentConfig['beamspotWidthData'], beamspotWidthMC=currentConfig['beamspotWidthMC'], doPlots=currentConfig['doPlots'], variable=self.variable, version=f"v{i}", workflow="htcondor"))
            i += 1
                
        return tasks

    
    def output(self):
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        output_paths = []
        
        inOutSplittingFlag = config['trees2wsCfg']['doInOutSplitting']  or config['trees2wsCfg']['doDiffSplitting']
        
        signal_input_path = glob.glob(config['inputFiles']['Trees2WS']+'/*')
        
        data_input_path = config['inputFiles']['Trees2WSData']  

        # Loop over a years era
        for currentEra in allErasMap[f"{self.year}"]:

            currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
            
            # returns output folder
            output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit"))
            output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/output"))
            output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/Plots"))
            
            
            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
            currentConfig['nCats'] = len(currentConfig['cats'].split(","))

            if currentConfig['procs'] == "auto":
                currentConfig['procs'] = extractListOfProcsFromHiggsDNASignal(signal_input_path, self.variable, inOutSplittingFlag)
            currentConfig['nProcs'] = len(currentConfig['procs'].split(","))

            for processIndex in range(currentConfig['nProcs']):
                for categoryIndex in range(currentConfig['nCats']):
                    category = currentConfig['cats'].split(",")[categoryIndex]
                    process = currentConfig['procs'].split(",")[processIndex]
                    output_paths += [law.LocalFileTarget(output_dir + f"/outdir_{currentConfig['ext']}/signalFit/output/CMS-HGG_sigfit_{currentConfig['ext']}_{process}_{currentConfig['year']}_{category}.root")]
            
        return output_paths
                
    def run(self):
        return True
    
    
class SignalPackagingCategory(law.Task):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    output_dir = law.Parameter(description="Path to the output directory")
    exts = law.Parameter(default="earlyAnalysis", description="Extension to be used for output folder naming")
    outputExt = law.Parameter(default="", description="Extension to be used for packaged folder naming")
    cat = law.Parameter(description="Current category (e.g. RECO_PTH_0p0_15p0_cat0)")
    year = law.Parameter(description="Year")    
    massPoints = law.Parameter(description="Mass Points")
    mergeYears = law.Parameter(default=True, description="Flag if one should merge the years or eras.")

    variable = law.Parameter(default="", description="Variable to be used")
    
    # htcondor_job_kwargs_submit = {"spool": True}
    
    def requires(self):
        
        year = self.year[:4]
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        signal_input_path = glob.glob(config['inputFiles']['Trees2WS']+'/*')
            
        tasks = []
        
        tasks.append(SignalFit(variable=self.variable, output_dir=output_dir, year=year))
                    
        return tasks
    
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")

        year = self.year[:4]
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{year}_{self.variable}.yml"
        
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
                    
            # Use allData.root from HiggsDNA to automatically determine categories
            data_input_path = config['inputFiles']['Trees2WSData']  
            if currentConfig['cats'] == "auto":
                currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
            currentConfig['nCats'] = len(currentConfig['cats'].split(","))     
        return {i: num for i, num in enumerate(range(0, (currentConfig['nCats']) + 1))}

    def output(self):
        safe_mkdir(self.output_dir)
        
        signal_output = [self.output_dir + f'/outdir_packaged{self.outputExt}/CMS-HGG_sigfit_packaged{self.outputExt}_{self.cat}.root']
                
        outputFileTargets = []
            
        for _, current_output_path in enumerate(signal_output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "/tools")
        
        safe_mkdir(self.output_dir)
        safe_mkdir(self.output_dir+f"/outdir_packaged{self.outputExt}")
        safe_mkdir(self.output_dir+f"/outdir_packaged{self.outputExt}/packageSignal")

        script_path = os.environ["ANALYSIS_PATH"] + "/Signal/scripts/packageSignal.py"
        arguments = [
            "python3",
            script_path,
            "--cat", self.cat,
            "--outputExt", self.outputExt,
            "--exts", self.exts,
            "--outputDir", f"{self.output_dir}",
            "--year", f"{self.year}",
            "--massPoints", f"{self.massPoints}",
            "--mergeYears", f"{self.mergeYears}",
        ]
        command = arguments
        # print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)

class SignalPackaging(law.Task):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    def requires(self):
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        tasks = []
        
        packagedConfig = config[f"packaged_{self.year}"]
        
        outputExt = packagedConfig['ext']
        mergeYears = packagedConfig['mergeYears']
        
        
        # Use allData.root from HiggsDNA to automatically determine categories
        data_input_path = config['inputFiles']['Trees2WSData']  
        if packagedConfig['cats'] == "auto":
            packagedConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
        packagedConfig['nCats'] = len(packagedConfig['cats'].split(","))

        # Extract low and high MH values
        mps = []
        for mp in packagedConfig['massPoints'].split(","): mps.append(int(mp))
        packagedConfig['massLow'], packagedConfig['massHigh'] = '%s'%min(mps), '%s'%max(mps)

        exts = []
            
        # Loop over a years era and extract the ext string in a list
        for currentEra in allErasMap[f"{self.year}"]:

            currentConfig = config[f"signalScriptCfg_{self.year}_{currentEra}"]
            
            exts.append(currentConfig['ext'])
        
        exts_string = ''
        for i, currentExt in enumerate(exts):
            exts_string += currentExt
            if i < (len(exts) - 1):
                exts_string += ','
            
                        
        for categoryIndex in range(packagedConfig['nCats']):
            category = packagedConfig['cats'].split(",")[categoryIndex]
            tasks.append(SignalPackagingCategory(output_dir=output_dir, exts=exts_string, outputExt=outputExt, cat=category, year=self.year, massPoints=packagedConfig['massPoints'], mergeYears=mergeYears, variable=self.variable))
                
        return tasks

    
    def output(self):
        
        # Path should be somewhere centrally...
        if self.variable == '':
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
            
        output_paths = []
        
        currentConfig = config[f"packaged_{self.year}"]
                    
            
        output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_packaged{currentConfig['ext']}"))
        output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_packaged{currentConfig['ext']}/packageSignal"))
        

        # Use allData.root from HiggsDNA to automatically determine categories
        data_input_path = config['inputFiles']['Trees2WSData']  
        if currentConfig['cats'] == "auto":
            currentConfig['cats'] = extractListOfCatsFromHiggsDNAAllData(data_input_path)
        currentConfig['nCats'] = len(currentConfig['cats'].split(","))
        
        for categoryIndex in range(currentConfig['nCats']):
            category = currentConfig['cats'].split(",")[categoryIndex]

            output_paths.append(law.LocalFileTarget(output_dir + f"/outdir_packaged{currentConfig['ext']}/CMS-HGG_sigfit_packaged{currentConfig['ext']}_{category}.root"))
            
                        
        return output_paths
                
    def run(self):
        return True
    
    