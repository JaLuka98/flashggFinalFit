import law
import os
import ROOT
import uproot
from collections import OrderedDict as od
import yaml
import subprocess
import shutil

from commonTools import *
from commonObjects import *

from framework import Task
from framework import HTCondorWorkflow, SlurmWorkflow

def convert_boolean_string(string):
    if (string == "True") or (string == "true") or (string == True):
        return True
    else:
        return False

def execute_command(command, return_output=False, shell=False):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=shell, env=os.environ)
        print("Script output:", result.stdout)
        print("Script executed successfully.")
        if return_output:
            return (result.stdout).split("\n")[0]
    except subprocess.CalledProcessError as e:
        print("Error executing script:", e.stderr)

class Trees2WSData(Task, HTCondorWorkflow, SlurmWorkflow, law.LocalWorkflow):
    # input_path = law.Parameter(description="Path to the data input ROOT file")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default='', description="Variable to be used for output folder naming")
    year = law.Parameter(default='2022', description="Year")
    apply_mass_cut = law.Parameter(default=False, description="Apply mass cut")
    mass_cut_range = law.Parameter(default='100,180', description="Mass cut range")
    batch_flavor = law.Parameter(default="htcondor", description="Batch system to use")

    bootstrap_flag = law.Parameter(default=False, description="Bootstrap flag")
    toy_flag = law.Parameter(default=False, description="Toy flag")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    number_of_bootstraps = law.Parameter(default=1000, description="Number of bootstraps")
    number_of_toys = law.Parameter(default=1000, description="Number of toys")

    _class_cache = {}
    
    def _init_once(self):
        key = (self.year, self.variable, self.output_dir)
        if key in self._class_cache:
            (
                self.configYamlPath,
                self.config,
                self.resolved_output_dir,
                self.fitFolderName
            ) = self._class_cache[key]
            return

        # compute config path
        if self.variable == "":
            configYamlPath = os.path.join(
                os.environ["ANALYSIS_PATH"], "config", f"{self.year}_inclusive.yml"
            )
        else:
            configYamlPath = os.path.join(
                os.environ["ANALYSIS_PATH"], "config", f"{self.year}_{self.variable}.yml"
            )

        with open(configYamlPath, "r") as f:
            config = yaml.safe_load(f)

        resolved_output_dir = self.output_dir or config["outputFolder"]
        fitFolderName = "runFits_mu_fiducial" if self.variable == "" else f"runFits_{self.variable}"

        self.configYamlPath = configYamlPath
        self.config = config
        self.resolved_output_dir = resolved_output_dir
        self.fitFolderName = fitFolderName

        # store in class-level cache
        self._class_cache[key] = (configYamlPath, config, resolved_output_dir, fitFolderName)
    
    def workflow_requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        workflow_reqs = super().workflow_requires()
        
        self._init_once()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
        fitConfig = self.config["combine_fit"]
        
        if (convert_boolean_string(self.toy_flag) == True):
            from Replicas.law_replica import GenerateAllReplicaData
            tasks["GenerateAllReplicaData"] = GenerateAllReplicaData(output_dir=self.resolved_output_dir, variable=self.variable if self.variable != "" else "inclusive", version=self.variable if self.variable != "" else "inclusive", year=self.year, number_of_replicas=self.number_of_toys, seed=self.seed, starting_value=self.starting_value, workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition=fitConfig['batchPartition'], slurm_memory=fitConfig['batchMemory'], slurm_max_runtime=fitConfig['batchMaxRuntime'], htcondor_partition=fitConfig['batchPartition'], htcondor_memory=fitConfig['batchMemory'], htcondor_max_runtime=fitConfig['batchMaxRuntime'])
            
            return tasks
        
        else:
            return True

    def create_branch_map(self):
        if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
            branch_map = {i: val for i, val in enumerate(range(1))}
            return branch_map
        elif convert_boolean_string(self.toy_flag) == True:
            branch_map = {i: toy_index for i, toy_index in enumerate(range(int(self.number_of_toys)))}
        else:
            branch_map = {i: bootstrap_index for i, bootstrap_index in enumerate(range(int(self.number_of_bootstraps)))}

        return branch_map

    def output(self):
        
        self._init_once()
        
        if convert_boolean_string(self.bootstrap_flag) == True:
            bootstrap_index = self.branch_data
        elif convert_boolean_string(self.toy_flag) == True:
            toy_index = self.branch_data
            
        if self.variable == '':
            if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.year}/ws/")
            elif convert_boolean_string(self.toy_flag) == True:
                ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.year}_{toy_index}/ws/")
            else:
                ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.year}_{bootstrap_index}/ws/")
        else:
            if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}/ws/")
            elif convert_boolean_string(self.toy_flag) == True:
                ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}_{toy_index}/ws/")
            else:
                ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}_{bootstrap_index}/ws/")
                
        return law.LocalFileTarget(os.path.join(ws_dir, "allData.root"))

    def run(self):
        
        self._init_once()
        
        if convert_boolean_string(self.bootstrap_flag) == True:
            bootstrap_index = self.branch_data
        elif convert_boolean_string(self.toy_flag) == True:
            toy_index = self.branch_data
        
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            temp_output_dir = os.environ["TARGET_PATH"]
        else:
            temp_output_dir = self.resolved_output_dir
            
        # Step 1: Create the output directory if it doesn't exist
        if self.variable == '':
            if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                temp_ws_dir = os.path.join(temp_output_dir, 'input_output_data', f"input_output_data_{self.year}/ws/")
            elif convert_boolean_string(self.toy_flag) == True:
                temp_ws_dir = os.path.join(temp_output_dir, 'input_output_data', f"input_output_data_{self.year}_{toy_index}/ws/")
            else:
                temp_ws_dir = os.path.join(temp_output_dir, 'input_output_data', f"input_output_data_{self.year}_{bootstrap_index}/ws/")
        else:
            if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                temp_ws_dir = os.path.join(temp_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}/ws/")
            elif convert_boolean_string(self.toy_flag) == True:
                temp_ws_dir = os.path.join(temp_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}_{toy_index}/ws/")
            else:
                temp_ws_dir = os.path.join(temp_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}_{bootstrap_index}/ws/")

        if self.batch_flavor == "slurm/psi":
            if self.variable == '':
                if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                    final_ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.year}/ws/")
                elif convert_boolean_string(self.toy_flag) == True:
                    final_ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.year}_{toy_index}/ws/")
                else:
                    final_ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.year}_{bootstrap_index}/ws/")
            else:
                if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                    final_ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}/ws/")
                elif convert_boolean_string(self.toy_flag) == True:
                    final_ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}_{toy_index}/ws/")
                else:
                    final_ws_dir = os.path.join(self.resolved_output_dir, 'input_output_data', f"input_output_data_{self.variable}_{self.year}_{bootstrap_index}/ws/")

            # Have to use the xrdfs for the pnfs file system while on PSI Tier 3.
            execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {final_ws_dir}'], shell=True)

        os.makedirs(temp_ws_dir, exist_ok=True)
            
        input_path = self.config["inputFiles"]["Trees2WSData"]
        
        config = self.config[f"trees2wsCfg"]
        input_tree_dir = config['inputTreeDir']
        data_vars = config['dataVars']
        categories = config['cats']
        apply_mass_cut = config["apply_mass_cut"]
        massCutRange = config["mass_cut_range"]
        

        # Step 2: Convert data trees to RooWorkspace
        # Open the input ROOT file
        if convert_boolean_string(self.toy_flag) == True:
            seed = int(self.seed) + int(toy_index)
            f = uproot.open(os.path.join(self.resolved_output_dir, "Replicas", "allReplicas", f"allReplica_{int(toy_index)}.{seed}.root"))
        else:
            f = uproot.open(input_path)
        list_of_tree_names = f.keys() if input_tree_dir == '' else f[input_tree_dir].keys()

        if categories == 'auto':
            categories = []
        for tn in list_of_tree_names:
            if "sigma" in tn: continue
            c = tn.split("_%s_"%sqrts__)[-1].split(";")[0]
            categories.append(c)

        if convert_boolean_string(self.toy_flag) == True:
            f = ROOT.TFile(os.path.join(self.resolved_output_dir, "Replicas", "allReplicas", f"allReplica_{int(toy_index)}.{seed}.root"))
        else:
            f = ROOT.TFile(input_path)

        # Create ROOT output workspace
        output_ws_file = os.path.join(temp_ws_dir, f"allData_{self.year}.root")
        fout = ROOT.TFile(output_ws_file, "RECREATE")
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
                    _vars[var].setBins(80) # 160
                elif var == "dZ":
                    _vars[var] = ROOT.RooRealVar(var, var, 0., -20., 20.)
                    _vars[var].setBins(40)
                elif (var == "weight"):
                    _vars[var] = ROOT.RooRealVar(var, var, 0.)
                elif (convert_boolean_string(self.bootstrap_flag) == True):
                    if var == "weight_bootstrap_%s"%bootstrap_index:
                        _vars[var] = ROOT.RooRealVar(var, var, 0.)
                else:
                    _vars[var] = ROOT.RooRealVar(var, var, 1., -999999, 999999)
                    _vars[var].setBins(1)
                getattr(_ws, 'import')(_vars[var], ROOT.RooFit.Silence())
            return _vars.keys()

        if convert_boolean_string(self.bootstrap_flag) == True:
            # Rename the weight columns for bootstrapping        
            data_vars = [f"weight_bootstrap_{bootstrap_index}" if "weight_bootstrap" in item else item for item in data_vars]
            data_vars.remove("weight")

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
            print(" --> Extracting events from category: %s"%cat)
            if input_tree_dir == '': treeName = "Data_%s_%s"%(sqrts__,cat)
            else: treeName = "%s/Data_%s_%s"%(input_tree_dir,sqrts__,cat)
            print("    * tree: %s"%treeName)
            t = f.Get(treeName)

            # Define dataset for the category
            dname = "Data_%s_%s"%(sqrts__,cat)  
            if convert_boolean_string(self.bootstrap_flag) == True:
                d = ROOT.RooDataSet(dname, dname, aset, 'weight_bootstrap_%s'%bootstrap_index)
            else:
                d = ROOT.RooDataSet(dname, dname, aset, 'weight')
                
            # Loop over events in the tree and add to the dataset
            for ev in t:
                if self.apply_mass_cut:
                    if(getattr(ev,"CMS_hgg_mass") < float(massCutRange.split(",")[0])) | (getattr(ev,"CMS_hgg_mass") > float(massCutRange.split(",")[1])): continue
                for var in data_vars: 
                    if var == "weight": continue
                    # if convert_boolean_string(self.bootstrap_flag) == True:
                    #     if var == "weight_bootstrap_%s"%bootstrap_index: continue
                    if "weight_bootstrap" in var:
                        branch = t.GetBranch(var)
                        leaf = branch.GetLeaf(var)
                        branch.GetEntry(ev.GetReadEntry())
                        value = int(leaf.GetValue())
                    else:
                        value = getattr(ev, var)
                    ws.var(var).setVal(value)
                if convert_boolean_string(self.bootstrap_flag) == True:
                    d.add(aset,aset.getRealValue("weight_bootstrap_%s"%bootstrap_index))
                else:
                    d.add(aset,1.)


            # Add dataset to the workspace
            getattr(ws, 'import')(d)

        # Write the workspace to the output file
        ws.Write()
        fout.Close()

        # Step 3: Rename the output file
        all_data_file = os.path.join(temp_ws_dir, "allData.root")
        os.rename(output_ws_file, all_data_file)
        print(f"Workspace written and renamed to {all_data_file}")
        
        if self.batch_flavor == "slurm/psi":
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f'{all_data_file}',
                    f'{final_ws_dir}/allData.root'
                ]
            else:
                # Copying output files to final destination on the /pnfs.
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f'{all_data_file}',
                    'root://t3dcachedb03.psi.ch:1094//' + f'{final_ws_dir}' + 'allData.root'
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Cleaning up scratch space.
            shutil.rmtree(temp_output_dir)