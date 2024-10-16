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
import glob, shutil
import errno
import yaml

import pandas
import numpy as np
import awkward as ak

from commonTools import *
from commonObjects import *
from T2WSTools.STXS_tools import *
from T2WSTools.diff_tools import *

# from framework import Task
# from framework import HTCondorWorkflow

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def leave():
  print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ HGG TREES 2 WS (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  exit(0)

                

class Trees2WSSingleProcess(law.Task):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    input_path = law.Parameter(description="Path to the data input ROOT file")
    output_dir = law.Parameter(description="Path to the output directory")
    variable = law.Parameter(default='', description="Variable to be used for output folder naming")
    year = law.Parameter(default='2022', description="Year")
    apply_mass_cut = law.Parameter(default=False, description="Apply mass cut")
    mass_cut_range = law.Parameter(default='100,180', description="Mass cut range")
    input_mass = law.Parameter(default='125', description="Input mass")
    productionMode = law.Parameter(default='ggh', description="Production mode [ggh,vbf,vh,wh,zh,tth,thq,ggzh,bbh]")
    decayExt = law.Parameter(default='', description="Decay extension")
    doNNLOPS = law.Parameter(default=False, description="Add NNLOPS weight variable: NNLOPSweight")
    doSystematics = law.Parameter(default=False, description="Add systematics datasets to output WS")
    doSTXSSplitting = law.Parameter(default=False, description="Split output WS per STXS bin")
    doDiffSplitting = law.Parameter(default=False, description="Split output WS per differential bin")
    doInOutSplitting = law.Parameter(default=False, description="Split output WS into in/out fiducial based on some variable in the input trees (to be improved).")
    

    # htcondor_job_kwargs_submit = {"spool": True}
    
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")
        varBins = [entry[1] for entry in differentialProcTable_[self.variable]]
        return varBins

    def output(self):
        
        outputFileTargets = []
        if self.doInOutSplitting: fiducialIds = [True, False]
        else: fiducialIds = [0] # If we do not perform in/out splitting, we want to have one inclusive (for particle-level) process definition, our code int for that is zero

        for fiducialId in fiducialIds:
        
            if self.doDiffSplitting: continue

            # In the end, the STXS and fiducial in/out splitting should maybe be harmonised, this looks a bit ugly
            if (self.doSTXSSplitting): continue

            if fiducialId == True: fidTag = "in"
            elif fiducialId == False: fidTag = "out"
            else: fidTag = "incl"

            # Define output workspace file
            if self.output_dir is not None:
                outputWSDir = self.output_dir+"/ws_%s_%s"%(dataToProc(self.productionMode), fidTag) # Multiple slashes are normalised away, no worries ("../test/" and "../test" are equivalent)
            else:
                outputWSDir = "/".join(self.input_path.split("/")[:-1])+"/ws_%s_%s"%(dataToProc(self.productionMode), fidTag)
            if not os.path.exists(outputWSDir): os.system("mkdir %s"%outputWSDir)
            outputWSFile = outputWSDir+"/"+re.sub(".root","_%s_%s.root"%(dataToProc(self.productionMode), fidTag),self.input_path.split("/")[-1])
            outputFileTargets.append(law.LocalFileTarget(outputWSFile))
            
            
        if self.doSTXSSplitting:
            #STXS currently not implemented
            pass
                
        if self.doDiffSplitting:
            varBins = [entry[1] for entry in differentialProcTable_[self.variable]]
            for currentBin in varBins:

                # Extract diffBin
                diffBin = self.productionMode + "_" + currentBin

                # Define output workspace file
                if self.output_dir is not None:
                    outputWSDir = self.output_dir + "/ws_%s"%diffBin
                else:
                    outputWSDir = "/".join(self.input_path.split("/")[:-1])+"/ws_%s"%diffBin
                outputWSFile = outputWSDir+"/"+re.sub(".root","_%s.root"%diffBin,self.input_path.split("/")[-1])
                outputFileTargets.append(law.LocalFileTarget(outputWSFile))

        return outputFileTargets

    def run(self):
        # Create output path if it does not exist
        os.makedirs(self.output_dir, exist_ok=True)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Production modes to skip theory weights: fill with 1's
        modesToSkipTheoryWeights = ['bbh','thq','thw']
        
        if self.variable == '':
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year[:4]}_inclusive.yml"
        else:
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year[:4]}_{self.variable}.yml"

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Extract options from config file:
        options = od()
        if input_config != '':
            if os.path.exists( input_config ):
                
                with open(input_config, 'r') as file:
                    config = yaml.safe_load(file)
                    
                config = config[f"trees2wsCfg"]
                inputTreeDir     = config['inputTreeDir']
                mainVars         = config['mainVars']
                stxsVar          = config['stxsVar']
                diffVar          = config['diffVar']
                systematicsVars  = config['systematicsVars']
                theoryWeightContainers = config['theoryWeightContainers']
                systematics      = config['systematics']
                cats             = config['cats']


            else:
                print( "[ERROR] %s config file does not exist. Leaving..."%input_config)
                leave()
        else:
            print( "[ERROR] Please specify config file to run from. Leaving..."%input_config)
            leave()
            
            
        # Function to add vars to workspace
        def add_vars_to_workspace(_ws=None,_data=None,_stxsVar=None):
            # Add intLumi var
            intLumi = ROOT.RooRealVar("intLumi","intLumi",1000.,0.,999999999.)
            intLumi.setConstant(True)
            getattr(_ws,'import')(intLumi)
            # Add vars specified by dataframe columns: skipping cat, stxsvar and type
            _vars = od()
            for var in _data.columns:
                if var in ['type','cat',_stxsVar]: continue
                if 'fiducial' in var: continue
                if "diff" in var: continue
                if var == "CMS_hgg_mass": 
                    _vars[var] = ROOT.RooRealVar(var,var,125.,100.,180.)
                    _vars[var].setBins(160)
                elif var == "dZ": 
                    _vars[var] = ROOT.RooRealVar(var,var,0.,-20.,20.)
                    _vars[var].setBins(40)
                elif var == "weight": 
                    _vars[var] = ROOT.RooRealVar(var,var,0.)
                else:
                    _vars[var] = ROOT.RooRealVar(var,var,1.,-999999,999999)
                    _vars[var].setBins(1)
                getattr(_ws,'import')(_vars[var],ROOT.RooFit.Silence())
            return _vars.keys()
        
        # Function to make RooArgSet
        def make_argset(_ws=None,_varNames=None):
            _aset = ROOT.RooArgSet()
            for v in _varNames: _aset.add(_ws.var(v))
            return _aset


        def create_workspace(df, sdf, outputWSFile, productionMode_string):
            # Open file and initiate workspace
            fout = ROOT.TFile(outputWSFile,"RECREATE")
            foutdir = fout.mkdir(inputWSName__.split("/")[0])
            foutdir.cd()
            ws = ROOT.RooWorkspace(inputWSName__.split("/")[1],inputWSName__.split("/")[1])
            
            # Add variables to workspace
            varNames = add_vars_to_workspace(ws,df,stxsVar)

            # Loop over cats
            for cat in cats:

                # a) make RooDataSets: type = nominal/notag
                mask = (df['cat']==cat)

                # Define RooDataSet
                dName = "%s_%s_%s_%s"%(productionMode_string,self.input_mass,sqrts__,cat)
                
                # Make argset
                aset = make_argset(ws,varNames)

                # Convert tree to RooDataset and add to workspace
                d = ROOT.RooDataSet(dName,dName,aset,'weight')
                
                # Loop over events in dataframe and add entry
                for row in df[mask][varNames].to_numpy():
                    for i, val in enumerate(row):
                        aset[i].setVal(val)
                    d.add(aset,aset.getRealValue("weight"))
                
                getattr(ws,'import')(d)

                if self.doSystematics:
                    # b) make RooDataHists for systematic variations
                    if cat == "NOTAG": continue
                    for s in systematics:
                        for direction in ['Up','Down']:
                            # Create mask for systematic variation
                            mask = (sdf['type']=='%s%s'%(s,direction))&(sdf['cat']==cat)
                            
                            # Define RooDataHist
                            hName = "%s_%s_%s_%s_%s%s01sigma"%(productionMode_string,self.input_mass,sqrts__,cat,s,direction)

                            # Make argset: drop weight column for histogrammed observables
                            systematicsVarsDropWeight = []
                            for var in systematicsVars:
                                if ('fiducial' in var) or ("diff" in var): continue
                                if var != "weight": systematicsVarsDropWeight.append(var)
                            aset = make_argset(ws,systematicsVarsDropWeight)
                            
                            h = ROOT.RooDataHist(hName,hName,aset)
                            for row, weight in zip(sdf[mask][systematicsVarsDropWeight].to_numpy(),sdf[mask]["weight"].to_numpy()):
                                for i, val in enumerate(row):
                                    aset[i].setVal(val)
                                h.add(aset,weight)
                            
                            # Add to workspace
                            getattr(ws,'import')(h)

            # Write WS to file
            ws.Write()

            # Close file and delete workspace from heap
            fout.Close()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # For theory weights: create vars for each weight
        theoryWeightColumns = {}
        for ts, nWeights in theoryWeightContainers.items(): theoryWeightColumns[ts] = ["%s_%g"%(ts[:-1],i) for i in range(0,nWeights)] # drop final s from container name

        # If year == 2018, add HET
        if self.year == '2018': systematics.append("JetHEM")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # UPROOT file
        f = uproot.open(self.input_path)
        if inputTreeDir == '': listOfTreeNames == f.keys()
        else: listOfTreeNames = f[inputTreeDir].keys()
        # If cats = 'auto' then determine from list of trees
        if cats == 'auto':
            cats = []
            for tn in listOfTreeNames:
                if "sigma" in tn: continue
                c = tn.split("_%s_"%sqrts__)[-1].split(";")[0]
                cats.append(c)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 1) Convert tree to pandas dataframe
        # Create dataframe to store all events in file
        data = pandas.DataFrame()
        if self.doSystematics: sdata = pandas.DataFrame()

        # Loop over categories: fill dataframe
        for cat in cats:
            print( " --> Extracting events from category: %s"%cat)
            if inputTreeDir == '': treeName = "%s_%s_%s_%s"%(self.productionMode,self.input_mass,sqrts__,cat)
            else: treeName = "%s/%s_%s_%s_%s"%(inputTreeDir,self.productionMode,self.input_mass,sqrts__,cat)
            print("    * tree: %s"%treeName)
            # Extract tree from uproot
            t = f[treeName]
            if t.num_entries == 0: continue
            
            # Convert tree to pandas dataframe
            dfs = {}
            
            # Theory weights
            for ts, tsColumns in theoryWeightColumns.items():
                if self.productionMode in modesToSkipTheoryWeights: 
                    dfs[ts] = pandas.DataFrame(np.ones(shape=(t.num_entries,theoryWeightContainers[ts])))
                else:
                    dfs[ts] = pandas.DataFrame(np.reshape(np.array(t[ts].array()),(t.num_entries,len(tsColumns))))
                dfs[ts].columns = tsColumns
                

            # Main variables to add to nominal RooDataSets
            # For wildcards use filter_name functionality
            mainVars_dropWildcards = []
            for var in mainVars:
                if "*" not in var:
                    mainVars_dropWildcards.append(var)
                
            dfs['main'] = t.arrays(mainVars_dropWildcards, library='pd')

            for var in mainVars:
                if "*" in var:
                    dfs[var] = t.arrays(filter_name=var, library='pd')

            # Concatenate current dataframes
            df = pandas.concat(dfs.values(), axis=1)

            # Add STXS splitting var if splitting necessary
            if self.doSTXSSplitting: 
                pass
                # df[stxsVar] = t.arrays(stxsVar, library='pd')

            # For experimental phase space
            df['type'] = 'nominal'
            # Add NNLOPS variable
            if(self.doNNLOPS):
                if self.productionMode == 'ggh': df['NNLOPSweight'] = t.arrays(['NNLOPSweight'], library='pd')
                else: df['NNLOPSweight'] = 1.

            # Add columns specifying category add to overall dataframe
            df['cat'] = cat
            data = pandas.concat([data,df], ignore_index=True, axis=0, sort=False)

            # For systematics trees: only for events in experimental phase space
            if self.doSystematics:
                sdf = pandas.DataFrame()
                for s in systematics:
                    print("    --> Systematic: %s"%re.sub("YEAR",self.year,s))
                    for direction in ['Up','Down']:
                        streeName = "%s_%s%s01sigma"%(treeName,s,direction)
                        # If year in streeName then replace by year being processed
                        streeName = re.sub("YEAR",self.year,streeName)
                        st = f[streeName]
                        if len(st)==0: continue
                        sdf = st.arrays(systematicsVars, library='pd')
                        sdf['type'] = "%s%s"%(s,direction)
                        # Add STXS splitting var if splitting necessary
                        if self.doSTXSSplitting: 
                            pass
                            # sdf[stxsVar] = st.arrays(stxsVar, library='pd')
                    
                        # Add column specifying category and add to systematics dataframe
                        sdf['cat'] = cat
                        sdata = pandas.concat([sdata,sdf], ignore_index=True, axis=0, sort=False)
            
        # If not splitting by STXS bin then add dummy column to dataframe
        if not self.doSTXSSplitting:
            data[stxsVar] = 'nosplit'  
            if self.doSystematics: sdata[stxsVar] = 'nosplit'



        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 2) Convert pandas dataframe to RooWorkspace

        if self.doInOutSplitting: fiducialIds = data['fiducialGeometricFlag'].unique()
        else: fiducialIds = [0] # If we do not perform in/out splitting, we want to have one inclusive (for particle-level) process definition, our code int for that is zero

        for fiducialId in fiducialIds:
        
            if self.doDiffSplitting: continue

            # In the end, the STXS and fiducial in/out splitting should maybe be harmonised, this looks a bit ugly
            if (stxsVar != '') or (self.doSTXSSplitting): continue

            if fiducialId == True: fidTag = "in"
            elif fiducialId == False: fidTag = "out"
            else: fidTag = "incl"

            if self.doInOutSplitting:
                fiducial_mask = data['fiducialGeometricFlag'] == fiducialId
                fiducial_mask_syst = sdata['fiducialGeometricFlag'] == fiducialId
            else:
                fiducial_mask = data['CMS_hgg_mass'] > 0 # Basically a true mask because we are all inclusive
                fiducial_mask_syst = sdata['CMS_hgg_mass'] > 0

            df = data[fiducial_mask]
            if self.doSystematics: 
                sdf = sdata[fiducial_mask_syst]

            # Define output workspace file
            if self.output_dir is not None:
                outputWSDir = self.output_dir+"/ws_%s_%s"%(dataToProc(self.productionMode), fidTag) # Multiple slashes are normalised away, no worries ("../test/" and "../test" are equivalent)
            else:
                outputWSDir = "/".join(self.input_path.split("/")[:-1])+"/ws_%s_%s"%(dataToProc(self.productionMode), fidTag)
            if not os.path.exists(outputWSDir): os.system("mkdir -p %s"%outputWSDir)
            outputWSFile = outputWSDir+"/"+re.sub(".root","_%s_%s.root"%(dataToProc(self.productionMode), fidTag),self.input_path.split("/")[-1])
            print(" --> Creating output workspace: (%s)"%outputWSFile)
            
            productionMode_string = self.productionMode + "_" + fidTag # This is, for example, "ggh_in"

            create_workspace(df, sdf, outputWSFile, productionMode_string)

        if self.doSTXSSplitting:

            for stxsId in data[stxsVar].unique():
                df = data[data[stxsVar]==stxsId]
                sdf = None
                if self.doSystematics: sdf = sdata[sdata[stxsVar]==stxsId]

                # Extract stxsBin
                stxsBin = flashggSTXSDict[int(stxsId)]
                if self.productionMode == "wh": 
                    if "QQ2HQQ" in stxsBin: stxsBin = re.sub("QQ2HQQ","WH2HQQ",stxsBin)
                elif self.productionMode == "zh": 
                    if "QQ2HQQ" in stxsBin: stxsBin = re.sub("QQ2HQQ","ZH2HQQ",stxsBin)
                # ggZH: split by decay mode
                elif self.productionMode == "ggzh":
                    if self.decayExt == "_ZToQQ": stxsBin = re.sub("GG2H","GG2HQQ",stxsBin)
                    elif self.decayExt == "_ZToNuNu": stxsBin = re.sub("GG2HLL","GG2HNUNU",stxsBin)
                # For tHL split into separate bins for tHq and tHW
                elif self.productionMode == "thq": stxsBin = re.sub("TH","THQ",stxsBin)
                elif self.productionMode == 'thw': stxsBin = re.sub("TH","THW",stxsBin)

                # Define output workspace file
                outputWSDir = "/".join(self.input_path.split("/")[:-1])+"/ws_%s"%stxsBin
                if not os.path.exists(outputWSDir): os.system("mkdir -p %s"%outputWSDir)
                outputWSFile = outputWSDir+"/"+re.sub(".root","_%s.root"%stxsBin,self.input_path.split("/")[-1])
                print(" --> Creating output workspace for STXS bin: %s (%s)"%(stxsBin,outputWSFile))

                productionMode_string = self.productionMode

                create_workspace(df, sdf, outputWSFile, productionMode_string)


        if self.doDiffSplitting:
            
            for diffId in data[diffVar].unique():
                # diffId should be a gen-level pt bin
                df = data[data[diffVar]==diffId]
                sdf = None
                if self.doSystematics: sdf = sdata[sdata[diffVar]==diffId]

                # For the moment, skip these events (as their count is usually very small)
                if int(diffId) == 0: continue

                # Extract diffBin
                diffBin = getBinNameByHiggsDNANumber(self.variable, int(diffId))
                diffBin = self.productionMode + "_" + diffBin
                print("diffBin", diffBin)

                # Define output workspace file
                if self.output_dir is not None:
                    outputWSDir = self.output_dir + "/ws_%s"%diffBin
                else:
                    outputWSDir = "/".join(self.input_path.split("/")[:-1])+"/ws_%s"%diffBin
                if not os.path.exists(outputWSDir): os.system("mkdir -p %s"%outputWSDir)
                outputWSFile = outputWSDir+"/"+re.sub(".root","_%s.root"%diffBin,self.input_path.split("/")[-1])
                print(" --> Creating output workspace for differential bin: %s (%s)"%(diffBin,outputWSFile))

                productionMode_string = self.productionMode

                create_workspace(df, sdf, outputWSFile, productionMode_string)

class Trees2WS(law.Task):
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default='', description="Variable to be used for output folder naming")
    year = law.Parameter(default='2022', description="Year")
    
    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        # Load the input configuration
        if self.variable == '':
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)
        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
        input_paths = config["inputFiles"]["Trees2WS"]
        
        config = config["trees2wsCfg"]
        
        doSTXSSplitting = config["doSTXSSplitting"]
        doDiffSplitting = config["doDiffSplitting"]
        doInOutSplitting = config["doInOutSplitting"]
        doSystematics = config["doSystematics"]
        mass_cut = config["apply_mass_cut"]
        mass_cut_r = config["mass_cut_range"]
        
        tasks = []
        mass_era_list = [
        (mass, era, self.variable, input_paths)
        for era in allErasMap[f"{self.year}"]
        for mass in input_masses
        ]
    
        proc_list = [
            (mode, process)
            for mode, process in production_modes
        ]
        
        for mode, process in proc_list:
            
            for mass, era, var, path_to_root_files in mass_era_list:
                if var == '':
                    current_output_path = output_dir + "/input_output_{}{}".format(self.year, era)
                else:
                    current_output_path = output_dir + "/input_output_{}_{}{}".format(var, self.year, era)
                                
                input_path = glob.glob(f"{path_to_root_files}/{process}_M-{mass}_{era}/*.root")[0]
                tasks.append(Trees2WSSingleProcess(input_path=input_path, input_mass=mass, productionMode=mode, apply_mass_cut=mass_cut, mass_cut_range=mass_cut_r, year=f"{self.year}{era}", doSystematics=doSystematics, doDiffSplitting=doDiffSplitting, doSTXSSplitting=doSTXSSplitting, doInOutSplitting=doInOutSplitting, output_dir=current_output_path, variable=var))#, version="v1", workflow="htcondor"))
        
        return tasks    
    def output(self):
        
        # returns output folder
        if self.variable == '':
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)

        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
        
        input_paths = config["inputFiles"]["Trees2WS"]
        
        era_list_with_variable = [
            (era, self.variable)
            for era in allErasMap[f"{self.year}"]
        ]
        outputFolders = []
        for era, var in era_list_with_variable:
            if var == '':
                current_output_path = output_dir + "/input_output_{}{}".format(self.year, era)
            else:
                current_output_path = output_dir + "/input_output_{}_{}{}".format(var, self.year, era)
                
            outputFolders.append(law.LocalFileTarget(current_output_path))
            outputFolders.append(law.LocalFileTarget(current_output_path + '/ws_signal'))
        
        mass_era_list = [
        (mass, era, self.variable, input_paths)
        for era in allErasMap[f"{self.year}"]
        for mass in input_masses
        ]
    
        proc_list = [
            (mode, process)
            for mode, process in production_modes
        ]
        
        for mode, process in proc_list:
            
            for mass, era, var, path_to_root_files in mass_era_list:

                input_path = glob.glob(f"{path_to_root_files}/{process}_M-{mass}_{era}/*.root")[0]
            
                if config['trees2wsCfg']["doInOutSplitting"]: fiducialIds = [True, False]
                else: fiducialIds = [0] # If we do not perform in/out splitting, we want to have one inclusive (for particle-level) process definition, our code int for that is zero

                for fiducialId in fiducialIds:
                
                    if config['trees2wsCfg']["doDiffSplitting"]: continue

                    # In the end, the STXS and fiducial in/out splitting should maybe be harmonised, this looks a bit ugly
                    if (config['trees2wsCfg']["doSTXSSplitting"]): continue

                    if fiducialId == True: fidTag = "in"
                    elif fiducialId == False: fidTag = "out"
                    else: fidTag = "incl"

                    # Define output workspace file
                    if current_output_path is not None:
                        outputWSDir = current_output_path+"/ws_%s_%s"%(dataToProc(mode), fidTag) # Multiple slashes are normalised away, no worries ("../test/" and "../test" are equivalent)
                    else:
                        outputWSDir = "/".join(input_path.split("/")[:-1])+"/ws_%s_%s"%(dataToProc(mode), fidTag)
                    if not os.path.exists(outputWSDir): os.system("mkdir -p %s"%outputWSDir)
                    outputWSFile = outputWSDir+"/"+re.sub(".root","_%s_%s.root"%(dataToProc(mode), fidTag),input_path.split("/")[-1])
                    outputFolders.append(law.LocalFileTarget(outputWSFile))
                    
                    
                if config['trees2wsCfg']["doSTXSSplitting"]:
                    #STXS currently not implemented
                    pass
                        
                if config['trees2wsCfg']["doDiffSplitting"]:
                    varBins = [entry[1] for entry in differentialProcTable_[self.variable]]
                    for currentBin in varBins:

                        # Extract diffBin
                        diffBin = mode + "_" + currentBin

                        # Define output workspace file
                        if current_output_path is not None:
                            outputWSDir = current_output_path + "/ws_%s"%diffBin
                        else:
                            outputWSDir = "/".join(input_path.split("/")[:-1])+"/ws_%s"%diffBin
                        outputWSFile = outputWSDir+"/"+re.sub(".root","_%s.root"%diffBin,input_path.split("/")[-1])
                        outputFolders.append(law.LocalFileTarget(outputWSFile))
                    
        return outputFolders
    
    def run(self):
        
        print("Trees2WS ran through. Moving output to the subdirectory ./ws_signal")
        
        if self.variable == '':
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_inclusive.yml"
        else:
            input_config = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)

        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
        
        era_list_with_variable = [
            (era, self.variable)
            for era in allErasMap[f"{self.year}"]
        ]
        
        outputFolders = []
        for era, var in era_list_with_variable:
            if var == '':
                current_output_path = output_dir + "/input_output_{}{}".format(self.year, era)
            else:
                current_output_path = output_dir + "/input_output_{}_{}{}".format(var, self.year, era)
            outputFolders.append(current_output_path)

            
        for currentEra in outputFolders:
            # Create ws_signal folder
            dst_folder = currentEra + "/ws_signal"
            safe_mkdir(dst_folder)
            
            # Copy files to ws_signal
            src_file_list = glob.glob(currentEra + "/*/*")
            for currentFile in src_file_list:
                shutil.copy2(currentFile, dst_folder)
            
        print("Copy completed.")

        return True
    
    