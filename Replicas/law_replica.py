import law
import luigi
import os
import yaml
import errno
import subprocess
import ROOT
import json
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.stats import poisson
import glob
import numpy as np
import pandas as pd

from commonTools import *
from commonObjects import *

from Combine.law_combine import *

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

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

def create_folder(folder):
    if "/pnfs" in os.path.realpath(folder):
        execute_command([f"xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {os.realpath(folder)}"], shell=True)
    else:
        os.makedirs(folder, exist_ok=True)

def get_replica(parquet_files):
    
    process_name = parquet_files[0].split("/")[-3].split("_")[0]
    
    era = parquet_files[0].split("/")[-3].split("_")[-1]
    
    sum_weight_central = 0.0
    sum_genw_beforesel = 0
    for i in range(len(parquet_files)):
        # print(f"Processing parquet file {parquet_files[i]}")
        sum_weight_central += float(pq.read_table(parquet_files[i]).schema.metadata[b'sum_weight_central'])
        sum_genw_beforesel += float(pq.read_table(parquet_files[i]).schema.metadata[b'sum_genw_presel'])
    
    # print(sum_weight_central, sum_genw_beforesel)
    
    columns_to_load = ["mass", "weight", "genWeight", "pt", "PTJ0", "NJ", "DPhiJ0J1", "rapidity", "lead_mvaID", "sublead_mvaID", "sigma_m_over_m_corr_smeared_decorr"]
    
    df = pd.concat((pd.read_parquet(f, columns=columns_to_load) for f in parquet_files), ignore_index=True)

    negative_weights = df[df["weight"] < 0.0].to_numpy()
    if len(negative_weights) > 0:
        # Why the HELL are they there?
        print(f"Warning: Negative weights found in the dataset: {len(negative_weights)}")
    
    df = df[df["weight"] >= 0.0]

    # df["weight_norm"] = df["weight"] / sum_weight_central
    df["weight_norm"] = df["weight"] / sum_genw_beforesel# (sum_genw_beforesel * sum_weight_central)
    ## Probability should be normalised to one
    df["prob"] = df["weight_norm"] / sum(df["weight_norm"])

    ## Compute the expected number of events
    ## This is scaled to the full Run3 lumi and the individual production XS (=ggH or VBF or VH or ttH or bbH); Taken from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
    # exp = sum(df["weight_norm"]) * production_XS[process_name] * 0.2270/100 * 1000 * lumiMap[era] # 55.65
    exp = sum(df["weight_norm"]) * (production_XS["GluGluHtoGG"] + production_XS["VBFHtoGG"] + production_XS["VHtoGG"] + production_XS["ttHtoGG"] + production_XS["bbHtoGG"]) * 0.2270/100 * 1000 * 27.3

    ## Extract from a Poisson distribution the number of events for each replica
    exp_replicas = poisson.rvs(mu=exp, size=(1))

    ## Indeces corresponding to the events to pick up in each replica
    ## NB! replace MUST be True, otherwise the sampling is not independent anymore and it is no longer a Poisson process
    idx_replicas = [np.random.choice(np.array(df.index), replace=True, size=(exp_replicas[0]), p=df["prob"])]

    ## Extract the events for each replica
    replica = df.loc[idx_replicas[0]]
        
    return replica

class GetAsimovBestFit(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")

    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")

    def workflow_requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)

        workflow_reqs = super().workflow_requires()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
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
        
        fitConfig = config["combine_fit"]
        
        tasks["RunT2WS"] = RunText2Workspace(output_dir=output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition=fitConfig['batchPartition'], slurm_memory=fitConfig['batchMemory'], slurm_max_runtime=fitConfig['batchMaxRuntime'], htcondor_partition=fitConfig['batchPartition'], htcondor_memory=fitConfig['batchMemory'], htcondor_max_runtime=fitConfig['batchMaxRuntime'])

        return tasks

    def create_branch_map(self):
        branch_map = {i: i for i in range(1)}
        return branch_map

    def output(self):
        
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
        
        output_paths = []

        output_paths.append(os.path.join(output_dir, 'Replicas', f'higgsCombineFirstStep.MultiDimFit.mH125.38.root'))

        outputFileTargets = []
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))
        
        return outputFileTargets

    def run(self):
        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_inclusive.yml")            
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")

        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
        
        cwd = os.getcwd()
        
        if self.variable == '':
            ws_path = os.path.join(output_dir, 'Combine', f'Datacard_{self.year}.root')
        else:
            ws_path = os.path.join(output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in output_dir:
                execute_command([f'mkdir -p {output_dir}/Replicas'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {output_dir}/Replicas'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas'))
        else:
            execute_command([f'mkdir -p {output_dir}/Replicas'], shell=True)
            os.chdir(os.path.join(output_dir, 'Replicas'))

        arguments = [
            "combine",
            "-M", "MultiDimFit",
            ws_path,
            "--freezeParameters", "MH",
            "-m", "125.38",
            "-n", f"FirstStep",
            "--cminDefaultMinimizerStrategy=0",
            "--expectSignal", "1",
            "--saveWorkspace",
            "--X-rtd", "MINIMIZER_freezeDisassociatedParams",
            "--X-rtd", "MINIMIZER_multiMin_hideConstants",
            "--X-rtd", "MINIMIZER_multiMin_maskConstraints",
            "--X-rtd", "MINIMIZER_multiMin_maskChannels=2",
            "-t", "-1",
            "--saveFitResult",
            "--saveSpecifiedIndex", f"""{",".join(combineVariableDict(self.variable, self.year)['pdfIndeces'])}""",
            "--floatOtherPOIs", "1"
        ]

        # Execute the command and capture the output
        command = arguments
        print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)
    
        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)

class GenerateBOnlyToys(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    # batch_system = law.Parameter(default="slurm", description="Batch system to use")
    number_of_replicas = law.Parameter(default=2000, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

    def workflow_requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        workflow_reqs = super().workflow_requires()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
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
        
        fitConfig = config["combine_fit"]
        
        tasks["RunT2WS"] = RunText2Workspace(output_dir=output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition=fitConfig['batchPartition'], slurm_memory=fitConfig['batchMemory'], slurm_max_runtime=fitConfig['batchMaxRuntime'], htcondor_partition=fitConfig['batchPartition'], htcondor_memory=fitConfig['batchMemory'], htcondor_max_runtime=fitConfig['batchMaxRuntime'])

        return tasks

    def create_branch_map(self):
        branch_map = {
            i: replica_index
            for i, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map

    def output(self):
        # returns output folder
        replica_index = self.branch_data
        
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
        
        output_paths = []
        
        seed = int(self.seed) + int(replica_index)

        output_paths.append(os.path.join(output_dir, 'Replicas', 'bonly', f'higgsCombineToy_{int(replica_index)}'+f'.GenerateOnly.mH125.38.{seed}.root'))

        outputFileTargets = []
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))
        
        return outputFileTargets

    def run(self):
        replica_index = self.branch_data

        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_inclusive.yml")            
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")

        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
        
        cwd = os.getcwd()
        
        if self.variable == '':
            ws_path = os.path.join(output_dir, 'Combine', f'Datacard_{self.year}.root')
        else:
            ws_path = os.path.join(output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in output_dir:
                execute_command([f'mkdir -p {output_dir}/Replicas/bonly'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {output_dir}/Replicas/bonly'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/bonly'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'bonly'))
        else:
            execute_command([f'mkdir -p {output_dir}/Replicas/bonly'], shell=True)
            os.chdir(os.path.join(output_dir, 'Replicas', 'bonly'))

        seed = int(self.seed) + int(replica_index)
        
        first_output = os.path.join(output_dir, 'Replicas')

        def check_pdf_idx(param):
            # Run the ROOT command
            command = f'root -l -q \'{os.environ["ANALYSIS_PATH"]}/Combine/checkPdfIdx.C("{first_output}/higgsCombinefirstStep.MultiDimFit.mH125.38.root")\''
            
            # Execute the command and capture the output
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Get the output and check for errors
            pdfIdx = result.stdout.strip()
            
            if result.returncode != 0:
                print("Error executing the command:", result.stderr)
                return None
            
            if pdfIdx.startswith("Processing"):
                pdfIdx = pdfIdx.split('X', 1)[-1]  # Split on the first 'X'
            
            # Remove the last comma
            pdfIdx = pdfIdx.rstrip(',')

            # Print the final result
            print(pdfIdx)
            return pdfIdx
        
        print("Generating B-Only replica with seed {}".format(seed))

        # arguments = [
        #     "combine",
        #     "-M", "GenerateOnly",
        #     "-d", ws_path,
        #     "-t", "1",
        #     "-s", f"{seed}",
        #     "--setParameters", ",".join(combineVariableDict(self.variable, self.year)['paramStrZero']),
        #     "--saveToys",
        #     "--freezeParameters", "MH",
        #     "--toysNoSystematics", # Just try it and see if it screws up the correlation matrix
        #     "-m", "125.38",
        #     "-n", f"Toy_{int(replica_index)}",
        # ]

        # Run the ROOT command
        background_model_folder_name = config['datacard_yields']['bkgModelWSDir'].split('/')[-2]
        bkg_input_folder = os.path.join(output_dir, "Combine", background_model_folder_name, "background")
        toy_output_file = f"./higgsCombineToy_{int(replica_index)}"+f".GenerateOnly.mH125.38.{seed}.root"
        arguments = ['root', '-l', '-q', f"{os.environ['ANALYSIS_PATH']}/Replicas/toy_Bonly.C(\"{bkg_input_folder}\", \"{toy_output_file}\", {seed})"]
        
        # Execute the command and capture the output
        command = arguments
        # print(command)
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)
    
        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)

class GenerateSplusBToys(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    # Don't be afraid. It's just a toy.
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")

    # parquet_dir = law.Parameter(default='', description="Path to the parquet directory, used to create the s-only replicas")
    
    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    number_of_replicas = law.Parameter(default=10, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

    def workflow_requires(self):
        
        workflow_reqs = super().workflow_requires()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
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
        
        fitConfig = config["combine_fit"]
        
        if self.variable == '':
            print("Running S+B toys for inclusive variable not implemented. Exiting...")
            exit(1)
        
        tasks["GenerateBOnlyToys"] = GenerateBOnlyToys(output_dir=output_dir, variable=self.variable, year=self.year, version=self.variable, workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition="short", slurm_memory=2000, slurm_max_runtime="00:15:00", htcondor_partition="espresso", htcondor_memory=2000, htcondor_max_runtime="00:20:00", seed=self.seed, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value)

        return tasks

    def create_branch_map(self):
        branch_map = {
            i: replica_index
            for i, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map

    def output(self):
        # returns output folder
        replica_index = self.branch_data
        
        if self.variable == '':
            print("Running S+B toys for inclusive variable not implemented. Exiting...")
            exit(1)
        else:
            configYamlPath = os.environ["ANALYSIS_PATH"] + f"/config/{self.year}_{self.variable}.yml"
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
            
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
        
        output_paths = []
        
        seed = int(self.seed) + int(replica_index)

        output_paths.append(os.path.join(output_dir, 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root'))

        outputFileTargets = []

        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        replica_index = self.branch_data

        if self.variable == '':
            print("Running S+B toys for inclusive variable not implemented. Exiting...")
            exit(1)           
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")

        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)

        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir

        # Need to load the categorization dictionary
        # Location hardcoded, as I want to use the "common" categorization dictionary from the Analysis Git Repo
        cat_dict_path = os.path.join("/work/niharrin/analyses/MidRun3_Code/postprocessing/configs/cat_dicts", f"{self.year}", config['inputFiles']['catDict_timestamp'], f"{self.variable}_MC.json")
        if not os.path.exists(cat_dict_path):
            print(f"Category dictionary {cat_dict_path} does not exist. Check path in law_replica.py. Exiting...")
            exit(1)
        else:
            with open(cat_dict_path) as pf:
                cat_dict = json.load(pf)

        cwd = os.getcwd()

        main_parquet_dir = config['inputFiles']['src_files']

        # Load all Parquet files from the main_parquet_dir
        # Note, that I have to load the nominal parquet files from all the procs, as the systematics are already accounted for in the signal model
        # Select only 125 GeV Higgs mass point (idk how I should interpolate the different datasets on an event basis...)
        proc_folders = glob.glob(os.path.join(main_parquet_dir, "*125*"))

        # Fix a seed for reproducibility
        seed = int(self.seed) + int(replica_index)
        np.random.seed(seed)
        
        # Load the b-only toy file
        bonly_toy_path = os.path.join(output_dir, 'Replicas', 'bonly', f'higgsCombineToy_{int(replica_index)}.GenerateOnly.mH125.38.{seed}.root')
        if not os.path.exists(bonly_toy_path):
            print(f"B-only toy file {bonly_toy_path} does not exist. Something went wrong. Exiting...")
            exit(1)

        bonly_file = ROOT.TFile.Open(bonly_toy_path)
        bonly_file.cd("toys")
        bonly_toy = ROOT.gDirectory.Get("toy_1")

        # Get the variable 'CMS_hgg_mass' from the dataset
        mass = bonly_toy.get().find("CMS_hgg_mass")
        argset = ROOT.RooArgSet(mass)
        channel = bonly_toy.get().find("CMS_channel")

        # Extract CMS channel labels and indices
        # This corresponds to the categories in the category dictionary
        CMS_channel_dict = {}
        for i in range(channel.numTypes()):
            channel.setIndex(i)
            CMS_channel_dict[channel.getLabel()] = i

        # Create the replica dataset
        
        replica_separated_procs = []
        
        # Get the replica for each process / category
        for proc_folder in proc_folders:
            # print(f"Processing parquet files from {proc_folder}")
            # Load the parquet files for the current process
            proc_parquet_files = glob.glob(os.path.join(proc_folder, "nominal", "*.parquet"))
            
            if len(proc_parquet_files) == 0:
                print(f"No parquet files found in {proc_folder}. Skipping...")
                continue
            
            replica_separated_procs.append(get_replica(proc_parquet_files))
        
        # Now merge the procs per category
        for cat in cat_dict:
            try:
                query_str = " and ".join(
                    f"{col} {op} {val}" for col, op, val in cat_dict[cat]["cat_filter"]
                )
            except:
                # Have a variable using absolute values.
                query_str = ""
                for k, set_of_conditions in enumerate(cat_dict[cat]["cat_filter"]):
                    if k > 0:
                        query_str += " and "
                    query_str += " and ".join(
                        f"{col} {op} {val}" for col, op, val in set_of_conditions
                    )
            print(f"Processing category {cat} with query: {query_str}")
            # Merge the replicas for the current category
            merged_replica = pd.concat([replica_separated_procs[i].query(query_str) for i in range(len(replica_separated_procs))], ignore_index=True)
                                        
            additional_mass_values = merged_replica["mass"].to_list()
            # additional_probability_values = merged_replica["prob"].to_list()

            for i, val in enumerate(additional_mass_values):
                channel.setIndex(CMS_channel_dict[cat])
                mass.setVal(val)
                # bonly_toy.add(argset, additional_probability_values[i])
                bonly_toy.add(argset, 1.)

        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in output_dir:
                execute_command([f'mkdir -p {output_dir}/Replicas/SplusB'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {output_dir}/Replicas/SplusB'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/SplusB'], shell=True)
            output_root_path = os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root')
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', "SplusB"))
        else:
            execute_command([f'mkdir -p {output_dir}/Replicas/SplusB'], shell=True)
            output_root_path = os.path.join(output_dir, 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root')
            os.chdir(os.path.join(output_dir, 'Replicas', 'SplusB'))
        
        # Open a new ROOT file for writing
        output_file = ROOT.TFile(output_root_path, "RECREATE")

        # Create a RooWorkspace (Combine expects datasets inside workspaces or directories)
        output_file.mkdir("toys")
        output_file.cd("toys")

        # Now write the RooDataSet to the toys directory with the name 'toy_1'
        bonly_toy.SetName("toy_1")   # Important: name must match what Combine expects
        bonly_toy.Write()

        # Close the file
        output_file.Close()
        
        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])
        
        os.chdir(cwd)

class FitSplusBToy(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow): #(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default="", description="Variable to be used")
    year = law.Parameter(default='2022', description="Year")

    number_of_replicas = law.Parameter(default=1000, description="Number of replicas to run.")
    starting_value = law.Parameter(default=0, description="Starting toy computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the toy generation")
    
    batch_flavor = law.Parameter(default="slurm", description="Batch system to use")
    
    def workflow_requires(self):
        workflow_reqs = super().workflow_requires()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
        if self.variable == '':
            print("Running S+B toys for inclusive variable not implemented. Exiting...")
            exit(1)
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
        
        SplusB_config = config["combine_SplusB_toys"]
        
        tasks["GenerateSplusBToys"] = GenerateSplusBToys(output_dir=output_dir, variable=self.variable, year=self.year, version=self.variable, workflow=SplusB_config["execution"], batch_flavor=self.batch_flavor, slurm_partition=SplusB_config['batchPartition'], slurm_memory=SplusB_config['batchMemory'], slurm_max_runtime=SplusB_config['batchMaxRuntime'], htcondor_partition=SplusB_config['batchPartition'], htcondor_memory=SplusB_config['batchMemory'], htcondor_max_runtime=SplusB_config['batchMaxRuntime'], seed=self.seed, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value)
        
        return tasks
    
    def create_branch_map(self):
        branch_map = {
            j: replica_index
            for j, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map

    def output(self):
        replica_index = self.branch_data
        
        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_inclusive.yml")
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir

        if self.variable == '':
            print("Running S+B toys for inclusive variable not implemented. Exiting...")
            exit(1)
        else:
            fitFolderName = f'runFits_{self.variable}'

        output = []

        if self.variable != '':
            output += [os.path.join(output_dir, 'Combine', fitFolderName, f'toyFit', f'toy_{replica_index}', f'higgsCombinefirstStep.MultiDimFit.mH125.38.root')]
            output += [os.path.join(output_dir, 'Combine', fitFolderName, f'toyFit', f'toy_{replica_index}', f'multidimfitfirstStep.root')]

        outputFileTargets = []

        for _, current_output_path in enumerate(output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        replica_index = self.branch_data
        
        if self.variable == '':
            print("Running S+B toys for inclusive variable not implemented. Exiting...")
            exit(1)
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")
            fitFolderName = f'runFits_{self.variable}'
                    
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
        
        cwd = os.getcwd()

        if self.variable == '':
            ws_path = os.path.join(output_dir, 'Combine', f'Datacard_{self.year}.root')
        else:
            ws_path = os.path.join(output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in output_dir:
                execute_command([f'mkdir -p {output_dir}/Combine/{fitFolderName}/toyFit/toy_{replica_index}'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {output_dir}/Combine/{fitFolderName}/toyFit/toy_{replica_index}'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Combine/{fitFolderName}/toyFit/toy_{replica_index}'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Combine', fitFolderName, f'toyFit', f'toy_{replica_index}'))
        else:
            execute_command([f'mkdir -p {output_dir}/Combine/{fitFolderName}/toyFit/toy_{replica_index}'], shell=True)
            os.chdir(os.path.join(output_dir, 'Combine', fitFolderName, f'toyFit', f'toy_{replica_index}'))

        seed = int(self.seed) + int(replica_index)
                
        # pdfIndicesStr = ",".join(combineVariableDict(self.variable, self.year)['pdfIndeces'])
        
        splusb_toy = os.path.join(output_dir, 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root')

        if self.variable != '':
            arguments = [
                "combine",
                "-M", "MultiDimFit",
                ws_path,
                "-m", "125.38",
                "-n", f"firstStep",
                "--cminDefaultMinimizerStrategy=0",
                "--saveWorkspace",
                "--cminApproxPreFitTolerance", f"{config['combine_fit']['cminApproxPreFitTolerance']}",
                "--X-rtd", "MINIMIZER_freezeDisassociatedParams",
                "--X-rtd", "MINIMIZER_multiMin_hideConstants",
                "--X-rtd", "MINIMIZER_multiMin_maskConstraints",
                "--X-rtd", "MINIMIZER_multiMin_maskChannels=2",
                "--algo", "singles",
                "--saveFitResult",
                "--freezeParameters", f"""MH""",
                "-D", f"{splusb_toy}:toys/toy_1",
            ]
            command = arguments
            print(command)
            try:
                result = subprocess.run(command, check=True, text=True, capture_output=True)
                print("Script output:", result.stdout)
                print("Script executed successfully.")
            except subprocess.CalledProcessError as e:
                print("Error executing script:", e.stderr)

        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Combine/",
                    output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Combine/",
                    'root://t3dcachedb03.psi.ch:1094//'+output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)