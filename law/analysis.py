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
import shutil

import pandas
import numpy as np
import awkward as ak

from commonTools import *
from commonObjects import *

from Datacard.datacard import *

# from framework import Task
# from framework import HTCondorWorkflow

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    
class EarlyRun3(law.Task):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
        
        tasks = [MakeDatacard(variable=self.variable, output_dir=output_dir, year=self.year)]
        
        return tasks    

    def output(self):
        # returns output folder
        
        if self.variable == '':
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_inclusive.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            # configYamlPath = os.path.dirname(os.path.abspath(__file__)) + f"/../config/{self.year}_{self.variable}.yml"
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
            
        datacard_config = config["datacard"]
        
        output_paths = []
        
        if self.variable == '': 
            # output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards"))
            if datacard_config['saveDataFrame']:
                output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Dataframe"))
                output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Dataframe/Datacard_{self.year}.pkl"))
                output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Dataframe/Datacard_{self.year}_unsymmetrized.pkl"))
            output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Datacard_{self.year}.txt"))
        else:
            # output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards"))
            if datacard_config['saveDataFrame']:
                output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Dataframe"))
                output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Dataframe/Datacard_{self.variable}_{self.year}.pkl"))
                output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Dataframe/Datacard_{self.variable}_{self.year}_unsymmetrized.pkl"))
            output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Datacard_{self.variable}_{self.year}.txt"))
            output_paths.append(law.LocalFileTarget(output_dir+ f"/Datacards/Datacard_{self.variable}_{self.year}_unsymmetrized.txt"))
        return output_paths
                
    
    def run(self):
        
        return True