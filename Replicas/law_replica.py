import law
import os
import yaml
import errno
import subprocess
import ROOT
import json
import pyarrow.parquet as pq
from scipy.stats import poisson
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
import re
import array
from itertools import islice

from commonTools import *
from commonObjects import *

from Combine.law_combine import *

# Flow stuff
import random
from scipy import stats
from Replicas.hgg_kinflow.dataset_loader import load_dataset
import Replicas.hgg_kinflow.dataset_loader as dataset_loader
import zuko
from zuko.nn import MLP
import torch.nn as nn
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, random_split, Subset
from torch.utils.data import DataLoader
import cloudpickle

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

def roo_dataset_to_pandas(roo_data):
    """Convert a RooDataSet into a pandas DataFrame."""
    data = {var.GetName(): [] for var in roo_data.get()}   # initialize columns

    # Loop over entries
    for i in range(roo_data.numEntries()):
        obs = roo_data.get(i)  # RooArgSet for this event
        for var in data.keys():
            data[var].append(obs[var].getVal())

    return pd.DataFrame(data)

def getCategoryName(filename: str) -> str:
    """
    Extract category name from filename: CMS-HGG_multipdf_<catname>.root
    """
    key = "CMS-HGG_multipdf_"
    start = filename.find(key)
    if start == -1:
        return ""
    start += len(key)
    end = filename.rfind(".root")
    if end == -1 or end <= start:
        return ""
    return filename[start:end]

def parse_pdf_indices(input_str):
    result = []
    items = input_str.split(',')

    for item in items:
        if '=' in item:
            name, value_str = item.split('=', 1)
            result.append((name, int(value_str)))

    return result

def getDataHistName(filename: str, inclusive_file: bool) -> str:
    if inclusive_file:
        # Find "_cat"
        cat_pos = filename.find("_cat")
        if cat_pos == -1:
            return ""

        # Start of category name
        cat_start = cat_pos + 4  # len("_cat")

        # End before ".root"
        root_pos = filename.rfind(".root")
        if root_pos == -1 or root_pos <= cat_start:
            return ""

        cat = filename[cat_start:root_pos]
        return f"roohist_data_mass_cat{cat}"

    else:
        # Find "RECO_"
        reco_pos = filename.find("RECO_")
        if reco_pos == -1:
            return ""

        cat_start = reco_pos + 5  # len("RECO_")

        root_pos = filename.rfind(".root")
        if root_pos == -1 or root_pos <= cat_start:
            return ""

        cat = filename[cat_start:root_pos]
        return f"roohist_data_mass_RECO_{cat}"

def get_replica_bin_by_bin(mc_parquet_files, cat_dict_, parquet_files, columns_to_load):
        
    process_name = mc_parquet_files[0].split("/")[-3].split("_")[0]
    
    era = mc_parquet_files[0].split("/")[-3].split("_")[-1]
    
    mc_sum_genw_beforesel = 0
    for i in range(len(mc_parquet_files)):
        mc_sum_genw_beforesel += float(pq.read_table(mc_parquet_files[i]).schema.metadata[b'sum_genw_presel'])

    sum_genw_beforesel = 0
    for i in range(len(parquet_files)):
        sum_genw_beforesel += float(pq.read_table(parquet_files[i]).schema.metadata[b'sum_genw_presel'])
    
    mc_df = pd.concat((pd.read_parquet(f, columns=columns_to_load) for f in mc_parquet_files), ignore_index=True)
    
    df = pd.concat((pd.read_parquet(f, columns=columns_to_load) for f in parquet_files), ignore_index=True)
    
    all_binned_df = []
    
    # Now merge the procs per category
    for cat in cat_dict_:
        try:
            query_str = " and ".join(
                f"{col} {op} {val}" for col, op, val in cat_dict_[cat]["cat_filter"]
            )
        except:
            # Have a variable using absolute values.
            query_str = "("
            for k, set_of_conditions in enumerate(cat_dict_[cat]["cat_filter"]):
                if k > 0:
                    query_str += ") or ("
                query_str += " and ".join(
                    f"{col} {op} {val}" for col, op, val in set_of_conditions
                )
            query_str += ")"
        # Merge the replicas for the current category
        binned_mc_df = pd.concat([mc_df.query(query_str)], ignore_index=True)
                
        binned_mc_df["weight_norm"] = binned_mc_df["weight"] / mc_sum_genw_beforesel# (sum_genw_beforesel * sum_weight_central)
        
        # binned_mc_df["genWeight_norm"] = binned_mc_df["genWeight"] / mc_sum_genw_beforesel
        ## Probability should be normalised to one
        # binned_mc_df["prob"] = binned_mc_df["weight_norm"] / sum(binned_mc_df["weight_norm"])

        ## Compute the expected number of events
        ## This is scaled to the full Run3 lumi and the individual production XS (=ggH or VBF or VH or ttH or bbH); Taken from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
        binned_mc_exp = sum(binned_mc_df["weight_norm"]) * production_XS[process_name] * 0.2270/100 * 1000 * lumiMap[era] # 55.65
    
        binned_df = pd.concat([df.query(query_str)], ignore_index=True)
        
        negative_weights = binned_df[binned_df["weight"] < 0.0].to_numpy()
        if len(negative_weights) > 0:
            # Why the HELL are they there?
            print(f"Warning: Negative weights found in the dataset: {len(negative_weights)}")
        
        binned_df = binned_df[binned_df["weight"] >= 0.0]
        
        binned_df = binned_df[(binned_df["lead_mvaID"] > photonMVA_cut[era]) & (binned_df["sublead_mvaID"] > photonMVA_cut[era])]

        binned_df["weight_norm"] = binned_df["weight"] / sum_genw_beforesel
        binned_df["prob"] = binned_df["weight_norm"] / sum(binned_df["weight_norm"])
        
        ## Extract from a Poisson distribution the number of events for each replica
        binned_exp_replicas = poisson.rvs(mu=binned_mc_exp, size=(1))
        
        ## Indeces corresponding to the events to pick up in each replica
        ## NB! replace MUST be True, otherwise the sampling is not independent anymore and it is no longer a Poisson process
        binned_idx_replicas = [np.random.choice(np.array(binned_df.index), replace=True, size=(binned_exp_replicas[0]), p=binned_df["prob"])]

        ## Extract the events for each replica
        binned_replica = binned_df.loc[binned_idx_replicas[0]]
        
        
        all_binned_df.append(binned_replica)

    replica = pd.concat(all_binned_df, ignore_index=True)

    return replica

def get_replica(mc_parquet_files, parquet_files, columns_to_load):
    
    process_name = parquet_files[0].split("/")[-3].split("_")[0]
    
    era = parquet_files[0].split("/")[-3].split("_")[-1]
    
    mc_sum_genw_beforesel = 0
    for i in range(len(mc_parquet_files)):
        mc_sum_genw_beforesel += float(pq.read_table(mc_parquet_files[i]).schema.metadata[b'sum_genw_presel'])

    sum_genw_beforesel = 0
    for i in range(len(parquet_files)):
        sum_genw_beforesel += float(pq.read_table(parquet_files[i]).schema.metadata[b'sum_genw_presel'])
    
    # print(sum_weight_central, sum_genw_beforesel)
    
    # columns_to_load = ["mass", "weight", "genWeight", "pt", "PTJ0", "NJ", "DPhiJ0J1", "rapidity", "lead_mvaID", "sublead_mvaID", "sigma_m_over_m_corr_smeared_decorr"]
    
    mc_df = pd.concat((pd.read_parquet(f, columns=columns_to_load) for f in mc_parquet_files), ignore_index=True)
    
    mc_df["weight_norm"] = mc_df["weight"] / mc_sum_genw_beforesel
    ## Compute the expected number of events
    ## This is scaled to the full Run3 lumi and the individual production XS (=ggH or VBF or VH or ttH or bbH); Taken from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
    mc_exp = sum(mc_df["weight_norm"]) * production_XS[process_name] * 0.2270/100 * 1000 * lumiMap[era]
    
    df = pd.concat((pd.read_parquet(f, columns=columns_to_load) for f in parquet_files), ignore_index=True)

    negative_weights = df[df["weight"] < 0.0].to_numpy()
    if len(negative_weights) > 0:
        # Why the HELL are they there?
        print(f"Warning: Negative weights found in the dataset: {len(negative_weights)}")
    
    df = df[df["weight"] >= 0.0]
    
    df = df[(df["lead_mvaID"] > photonMVA_cut[era]) & (df["sublead_mvaID"] > photonMVA_cut[era])]

    df["weight_norm"] = df["weight"] / sum_genw_beforesel# (sum_genw_beforesel * sum_weight_central)
    ## Probability should be normalised to one
    df["prob"] = df["weight_norm"] / sum(df["weight_norm"])

    ## Extract from a Poisson distribution the number of events for each replica
    mc_exp_replicas = poisson.rvs(mu=mc_exp, size=(1))

    ## Indeces corresponding to the events to pick up in each replica
    ## NB! replace MUST be True, otherwise the sampling is not independent anymore and it is no longer a Poisson process
    idx_replicas = [np.random.choice(np.array(df.index), replace=True, size=(mc_exp_replicas[0]), p=df["prob"])]

    ## Extract the events for each replica
    replica = df.loc[idx_replicas[0]]

    return replica

def get_mg5_exp(mc_parquet_files):
    """
    Load Parquet data in memory-efficient chunks with a progress bar.
    Computes a weighted replica sample of events.
    """

    columns_to_load = [
        "mass", "weight", "lead_mvaID", "sublead_mvaID"
    ]

    # --- Step 1: Function to iterate over Parquet files by row group ---
    def iter_parquet_rows(files, columns):
        for file in files:
            parquet_file = pq.ParquetFile(file)
            for rg in range(parquet_file.num_row_groups):
                yield parquet_file.read_row_group(rg, columns=columns).to_pandas()
    
    df_list = []
    
    for parquet_files in mc_parquet_files:
    
        process_name = parquet_files[0].split("/")[-3].split("_")[0]
        
        era = parquet_files[0].split("/")[-3].split("_")[-1]
        
        # --- Step 3: Compute total gen weight before selection ---
        sum_genw_beforesel = 0.0
        for f in parquet_files:
            meta = pq.read_table(f).schema.metadata
            sum_genw_beforesel += float(meta[b'sum_genw_presel'])

        # --- Step 4: Load physics data in chunks with progress bar ---
        df_chunks = []
        total_files = sum(pq.ParquetFile(f).num_row_groups for f in parquet_files)
        print("\nLoading main physics data...")
        for chunk in tqdm(iter_parquet_rows(parquet_files, columns_to_load), total=total_files, unit="rowgroup"):
            chunk = chunk[chunk["weight"] >= 0.0]
            chunk["weight"] = (chunk["weight"] * lumiMap[era] * production_XS[process_name] * 0.2270/100 * 1000) / sum_genw_beforesel
            df_chunks.append(chunk)

        current_df = pd.concat(df_chunks, ignore_index=True)
        current_df = current_df[(current_df["lead_mvaID"] > photonMVA_cut[era]) & (current_df["sublead_mvaID"] > photonMVA_cut[era])]
        df_list.append(current_df)
    
    df = pd.concat(df_list, ignore_index=True)
    
    df = df[(df["mass"] >= 100) & (df["mass"] <= 180)]
    
    mc_exp = sum(df["weight"]) 
    
    return mc_exp

def get_data_exp(data_parquet_files):
    
    columns_to_load_data = ["mass", "lead_mvaID", "sublead_mvaID"]

    # --- Step 1: Function to iterate over Parquet files by row group ---
    def iter_parquet_rows(files, columns):
        for file in files:
            parquet_file = pq.ParquetFile(file)
            for rg in range(parquet_file.num_row_groups):
                yield parquet_file.read_row_group(rg, columns=columns).to_pandas()

    # --- Step 2: Load sideband data (mass only) with progress bar ---
    data_df_chunks = []
    print("\nLoading sideband mass data...")
    for chunk in tqdm(iter_parquet_rows(data_parquet_files, columns_to_load_data), total=len(data_parquet_files), unit="file"):
        data_df_chunks.append(chunk)
        
    data_df = pd.concat(data_df_chunks, ignore_index=True)
    
    era = data_parquet_files[0].split("/")[-3].split("_")[-1]
    
    reduced_data_df = data_df[((data_df["mass"] >= 100) & (data_df["mass"] <= 180)) & (data_df["lead_mvaID"] > photonMVA_cut[era]) & (data_df["sublead_mvaID"] > photonMVA_cut[era])]

    return len(reduced_data_df), reduced_data_df

def get_bkg_replica(sidebands_exp, parquet_files_divided_in_processes, columns_to_load):
    """
    Load Parquet data in memory-efficient chunks with a progress bar.
    Computes a weighted replica sample of events.
    """

    # --- Step 1: Function to iterate over Parquet files by row group ---
    def iter_parquet_rows(files, columns):
        for file in files:
            parquet_file = pq.ParquetFile(file)
            for rg in range(parquet_file.num_row_groups):
                yield parquet_file.read_row_group(rg, columns=columns).to_pandas()
    
    df_list = []
    
    for parquet_files in parquet_files_divided_in_processes:
    
        process_name = parquet_files[0].split("/")[-3].split("_")[0]
        
        era = parquet_files[0].split("/")[-3].split("_")[-1]
        
        # --- Step 2: Compute total gen weight before selection ---
        sum_genw_beforesel = 0.0
        for f in parquet_files:
            meta = pq.read_table(f).schema.metadata
            sum_genw_beforesel += float(meta[b'sum_genw_presel'])

        # --- Step 3: Load physics data in chunks with progress bar ---
        df_chunks = []
        total_files = sum(pq.ParquetFile(f).num_row_groups for f in parquet_files)
        print("\nLoading main physics data...")
        for chunk in tqdm(iter_parquet_rows(parquet_files, columns_to_load), total=total_files, unit="rowgroup"):
            chunk = chunk[chunk["weight"] >= 0.0]
            chunk["weight_norm"] = (chunk["weight"] * bkg_normalizing_factor[era][process_name] * lumiMap[era] * production_XS[process_name]) / sum_genw_beforesel
            df_chunks.append(chunk)

        current_df = pd.concat(df_chunks, ignore_index=True)

        # Apply a mask
        mask = (current_df["mass"] >= 100) & (current_df["mass"] <= 180) & (current_df["lead_mvaID"] > photonMVA_cut[era]) & (current_df["sublead_mvaID"] > photonMVA_cut[era])
        current_df = current_df[mask]

        df_list.append(current_df)
    
    df = pd.concat(df_list, ignore_index=True)

    df["prob"] = df["weight_norm"] / df["weight_norm"].sum()

    # --- Step 5: Poisson sampling of replicas ---
    print("\nGenerating one background replica sample...")
    sidebands_exp_replicas = poisson.rvs(mu=sidebands_exp, size=1)
    idx_replicas = np.random.choice(
        df.index,
        replace=True,
        size=sidebands_exp_replicas[0],
        p=df["prob"]
    )

    replica = df.loc[idx_replicas]

    print("✅ Background replica generation complete!")
    return replica

def natural_sort_key(name):
    # Split string into text and number chunks
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', name)]

# Helper function to extract the category name
def get_category_name(filename: str) -> str:
    pattern = r"CMS-HGG_multipdf_(.+)\.root$"
    match = re.search(pattern, filename)
    if not match:
        return ""
    return match.group(1)

def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)

def load_ensemble(ensemble_size=4, base_seed=42):
    models = []

    for i in range(ensemble_size):
        print(f"\n🚀 Loading model {i+1}/{ensemble_size}")
        current_seed = base_seed + i
        set_seed(current_seed)

        g = torch.Generator().manual_seed(current_seed)

        model = MLP(
            in_features=5,
            out_features=13,
            hidden_features=[128,128,128],
            activation=nn.GELU,
            normalize=True
        ).to("cpu")

        model.load_state_dict(torch.load(f"/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Replicas/hgg_kinflow/model_NJ_NN_{i}.pth", map_location=torch.device('cpu')))

        models.append(model)

    return models

def ensemble_predict(models, dataset_):
    all_probs = []
    all_pred_class = []

    for model in models:
        model.eval()

    with torch.no_grad():
        logits = []
        for i, model in enumerate(models):
            logits.append(model(dataset_))

        logits_mean = torch.stack(logits).mean(dim=0)
        probs = F.softmax(logits_mean, dim=1)

        pred_class = probs.argmax(dim=1)

        all_pred_class.append(pred_class.cpu())
        all_probs.append(probs.cpu())

    return torch.cat(all_probs), torch.cat(all_pred_class)

class GetAsimovBestFit(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")

    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    
    toy_flag = law.Parameter(default=False, description="Toy flag")
    number_of_replicas = law.Parameter(default=10, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

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
        
        tasks["RunT2WS"] = RunText2Workspace(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition=fitConfig['batchPartition'], slurm_memory=fitConfig['batchMemory'], slurm_max_runtime=fitConfig['batchMaxRuntime'], htcondor_partition=fitConfig['batchPartition'], htcondor_memory=fitConfig['batchMemory'], htcondor_max_runtime=fitConfig['batchMaxRuntime'], toy_flag=self.toy_flag, number_of_toys=self.number_of_replicas, seed=self.seed)

        return tasks

    def create_branch_map(self):
        if convert_boolean_string(self.toy_flag) == True:
            branch_map = {
                i: toy_index
                for i, toy_index in enumerate(range(int(self.number_of_replicas)))
            }
        else:
            branch_map = {i: i for i in range(1)}
        return branch_map

    def output(self):

        if convert_boolean_string(self.toy_flag) == True:
            index = self.branch_data
        
        self._init_once()
        
        output_paths = []

        if convert_boolean_string(self.toy_flag) == True:
            output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'AsimovBestFit', f'higgsCombineFirstStep_{index}.MultiDimFit.mH125.38.root'))
        else:
            output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', f'higgsCombineFirstStep.MultiDimFit.mH125.38.root'))

        outputFileTargets = []
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))
        
        return outputFileTargets

    def run(self):
        if convert_boolean_string(self.toy_flag) == True:
            index = self.branch_data
        
        self._init_once()
        
        cwd = os.getcwd()

        if convert_boolean_string(self.toy_flag) == True:
            if self.variable == '':
                ws_path = os.path.join(self.resolved_output_dir, 'Combine', 'Workspaces', f'Datacard_{self.year}_{index}.root')
            else:
                ws_path = os.path.join(self.resolved_output_dir, 'Combine', 'Workspaces', f'Datacard_{self.variable}_{self.year}_{index}.root')
        else:
            if self.variable == '':
                ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.year}.root')
            else:
                ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')

        if convert_boolean_string(self.toy_flag) == True:
            if self.batch_flavor == "slurm/psi":
                # Have to use /scratch/batch_username/ for slurm/psi
                if "/work" in self.resolved_output_dir:
                    execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/AsimovBestFit'], shell=True)
                else:   
                    execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/AsimovBestFit'], shell=True)

                os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
                execute_command([f'mkdir -p $TARGET_PATH/Replicas/AsimovBestFit'], shell=True)
                os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'AsimovBestFit'))
            else:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/AsimovBestFit'], shell=True)
                os.chdir(os.path.join(self.resolved_output_dir, 'Replicas', 'AsimovBestFit'))
        else:
            if self.batch_flavor == "slurm/psi":
                # Have to use /scratch/batch_username/ for slurm/psi
                if "/work" in self.resolved_output_dir:
                    execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas'], shell=True)
                else:   
                    execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas'], shell=True)

                os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
                execute_command([f'mkdir -p $TARGET_PATH/Replicas'], shell=True)
                os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas'))
            else:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas'], shell=True)
                os.chdir(os.path.join(self.resolved_output_dir, 'Replicas'))

        arguments = [
            "combine",
            "-M", "MultiDimFit",
            ws_path,
            "--freezeParameters", "MH",
            "-m", "125.38",
            "-n", f"FirstStep",
            "--cminDefaultMinimizerStrategy=0",
            "--saveWorkspace",
            "--X-rtd", "MINIMIZER_freezeDisassociatedParams",
            "--X-rtd", "MINIMIZER_multiMin_hideConstants",
            "--X-rtd", "MINIMIZER_multiMin_maskConstraints",
            "--X-rtd", "MINIMIZER_multiMin_maskChannels=2",
            "-t", "-1",
            "--saveFitResult",
            "--floatOtherPOIs", "1"
        ]
        if self.variable == "":
            arguments += ["--saveSpecifiedIndex", ",".join([f"pdfindex_{bmw}_{self.year}_13TeV" for bmw in BMW])]
            arguments += ["--setParameters", "r=1"]
        else:
            arguments += ["--saveSpecifiedIndex", ",".join(combineVariableDict(self.variable, self.year)['pdfIndeces'])]
            arguments += ["--setParameters", ",".join(combineVariableDict(self.variable, self.year)['paramStr'])]

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
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)

class GenerateAllReplicaData(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    # Generate a SplusB replica dataset
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    # batch_system = law.Parameter(default="slurm", description="Batch system to use")
    number_of_replicas = law.Parameter(default=2000, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

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

    def create_branch_map(self):
        branch_map = {
            i: replica_index
            for i, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map

    def output(self):
        # returns output folder
        replica_index = self.branch_data
        
        self._init_once()
        
        output_paths = []
        
        seed = int(self.seed) + int(replica_index)

        output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'allReplicas', f'allReplica_{int(replica_index)}.{seed}.root'))

        outputFileTargets = []
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))
        
        return outputFileTargets

    def run(self):
        replica_index = self.branch_data
        
        self._init_once()
        
        cwd = os.getcwd()
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in self.resolved_output_dir:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/allReplicas'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/allReplicas'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/allReplicas'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'allReplicas'))
        else:
            execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/allReplicas'], shell=True)
            os.chdir(os.path.join(self.resolved_output_dir, 'Replicas', 'allReplicas'))

        seed = int(self.seed) + int(replica_index)
                
        print("Generating B-Only replica with seed {}".format(seed))
        
        bkg_proc_dirs = glob.glob(os.path.join(self.config['inputFiles']['bkg_src_files'], "*"))
        mg5_proc_dirs = glob.glob(os.path.join(self.config['inputFiles']['mc_src_files'], "*"))
        powheg_proc_dirs = glob.glob(os.path.join(self.config['inputFiles']['powheg_src_files'], "*"))
        data_parquet_files = glob.glob(os.path.join(self.config['inputFiles']['data_src_files'], "*/nominal/*.parquet"))
        
        # all_parquet_files = []
        # for proc_dir in bkg_proc_dirs:
        #     # if "GG-Box-3Jets" in proc_dir: continue
        #     parquet_files = glob.glob(os.path.join(proc_dir, "nominal", "*.parquet"))
        #     all_parquet_files.append(parquet_files)

        # all_MC_parquet_files = []
        # for proc_dir in mg5_proc_dirs:
        #     # if "GG-Box-3Jets" in proc_dir: continue
        #     parquet_files = glob.glob(os.path.join(proc_dir, "nominal", "*.parquet"))
        #     all_MC_parquet_files.append(parquet_files)
        
        # # Extract the expected number of events from MC (MG5)
        # inclusive_signal_yield = get_mg5_exp(all_MC_parquet_files)
        
        # # Extract the expected number of sideband events from data
        # yield_with_signal, _ = get_data_exp(data_parquet_files)

        # # For the moment like this
        # yield_without_signal = yield_with_signal - inclusive_signal_yield
        
        # print("inclusive_signal_yield:", inclusive_signal_yield)
        # print("yield_with_signal:", yield_with_signal)

        
        columns_to_load = [
            "mass", "weight", "lead_mvaID", "sublead_mvaID",
            "sigma_m_over_m_corr_smeared_decorr"
        ]

        if self.variable == "PTH":
            columns_to_load += ["pt"]
        elif (self.variable in jetVariables) and (self.variable != "NJ"):
            columns_to_load += [self.variable, "NJ"]
        else:
            columns_to_load += [self.variable]
        
        np.random.seed(seed)
        # inclusive_bkg_replica = get_bkg_replica(yield_without_signal, all_parquet_files, columns_to_load)

        # Get first the mass distribution that serves as the input for the flows

        def check_pdf_idx():
            # Run the ROOT command
            command = f'root -l -q \'{os.environ["ANALYSIS_PATH"]}/Combine/checkPdfIdx.C("/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_09_16/earlyRun3/finalfits/inclusive/Replicas/higgsCombineFirstStep.MultiDimFit.mH125.38.root")\''
            
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

        indices_str = check_pdf_idx()
        input_folder = glob.glob("/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_09_16/earlyRun3/finalfits/inclusive/Background/outdir_Run3FidXSAnalysis/*.root")
        
        cats_df = []

        for idx, file in enumerate(input_folder):
            
            filename = file
            fileIdx = idx + 1

            sideband_file = ROOT.TFile(filename)
            ws = sideband_file.Get("multipdf")

            mass = ws.var("CMS_hgg_mass")
            mass.setBins(320)
            
            catName = getCategoryName(filename)

            indices = parse_pdf_indices(indices_str)

            bestFit_idx = -1
            for name, val in indices:
                if catName in name:      # same as name.find(catName) != -1
                    bestFit_idx = val
                    break

            pdfs = ws.allPdfs()

            multipdf = None
            pdf_iter = pdfs.createIterator()

            pdf_obj = pdf_iter.Next()
            while pdf_obj:
                # In PyROOT, use IsA() or ClassName() to check inheritance/type
                if pdf_obj.InheritsFrom("RooMultiPdf"):
                    multipdf = pdf_obj
                    break
                pdf_obj = pdf_iter.Next()

            bestFit_pdf = multipdf.getPdf(bestFit_idx)

            # Inclusive file flag
            inclusive_file = catName in ["cat0", "cat1", "cat2"]

            # Get the data histogram name
            dataHistName = getDataHistName(filename, inclusive_file)

            data = ws.data(dataHistName)

            # Create yield parameter
            n_yield = ROOT.RooRealVar("n_yield", "Fitted yield", 1000, 0, 1e6)

            # Create extended PDF
            extPdf = ROOT.RooExtendPdf("extPdf", "extended pdf", bestFit_pdf, n_yield)

            # Fit
            extPdf.fitTo(
                data,
                ROOT.RooFit.Extended(),
                ROOT.RooFit.PrintLevel(-1)
            )

            fitted_yield = n_yield.getVal()

            # Category-specific seed
            catSeed = seed + 1_000_000 * fileIdx

            # RNG for Poisson
            rng = ROOT.TRandom3(catSeed)
            nToys = rng.Poisson(fitted_yield)

            # Generate toys using only obs
            genVars = ROOT.RooArgSet(mass)
            
            cat_index = int(catName.split("cat")[-1])
            
            # Get the flow mapping for the year
            # note, if in the allErasMap there is only one era selected, do NOT scale the lumi
            eras = allErasMap[self.year]
            
            current_allEra_df = pd.DataFrame()

            for era in eras: # note we have max only two eras per year
                lumi_scale = lumiMap[self.year+era] / sum([lumiMap[self.year+era] for era in eras])

                current_flowEraIdx = flowEraMap[self.year][era]

                # Category-specific seed
                catSeed = seed + (1_000_000 * fileIdx) + (2_000_000 * current_flowEraIdx)

                ROOT.RooRandom.randomGenerator().SetSeed(catSeed)

                era_toyData = bestFit_pdf.generate(genVars, nToys*lumi_scale)

                current_era_df = roo_dataset_to_pandas(era_toyData)

                current_era_df['cat'] = cat_index
                current_era_df['year'] = current_flowEraIdx

                current_allEra_df = pd.concat([current_allEra_df, current_era_df], ignore_index=True)

            cats_df.append(current_allEra_df)

        mass_df = pd.concat(cats_df, ignore_index=True)
        # Rename the mass column in order to be compatible with the flows
        mass_df.rename(columns={"CMS_hgg_mass": "mass"}, inplace=True)
        
        input_mass = pd.DataFrame(mass_df, columns=['mass', 'cat', 'year'])
        input_mass['cat'] = input_mass['cat'].astype(int)
        
        # Set a seed
        set_seed(seed)

        # Load the flows
        pt_eta_H_flow = zuko.flows.spline.NSF(features=2, # PTH, Eta
                                              context=3, # mass, cat, year
                                              bins=50,
                                              passes=4,
                                              hidden_features=[128,128,128],
                                              transforms=3
                                              ).to("cpu")

        models_b = load_ensemble(ensemble_size=4, base_seed=seed)

        ptj_flow = zuko.flows.spline.NSF(features=1,
                                              context=6,
                                              bins=30,
                                              passes=1, 
                                              hidden_features=[128,128,128,128],
                                              transforms=1
                                              ).to("cpu")
        
        DPhiJ0J1_flow = zuko.flows.spline.NSF(features=1,
                                              context=7,
                                              bins=30,
                                              passes=None, 
                                              hidden_features=[128,128,128,128],
                                              transforms=1
                                              ).to("cpu")

        pt_eta_H_flow.load_state_dict(torch.load("/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Replicas/hgg_kinflow/model_flow_pt_eta_H.pth", map_location=torch.device('cpu')))
        ptj_flow.load_state_dict(torch.load("/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Replicas/hgg_kinflow/model_flow_ptj0.pth", map_location=torch.device('cpu')))
        DPhiJ0J1_flow.load_state_dict(torch.load("/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Replicas/hgg_kinflow/model_flow_dphij0j1.pth", map_location=torch.device('cpu')))
        
        dataset = dataset_loader.PandasDataset(input_mass, ["mass", "cat", "year"], ["mass", "cat", "year"], "/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Replicas/hgg_kinflow/preprocessing_pipeline_v1.pkl", device="cpu")

        number_of_samples = 1

        pt_eta_H_flow = pt_eta_H_flow.cpu()
        mass = dataset.c.cpu()

        BATCH_SIZE = 1024
        all_samples = []

        with torch.no_grad():
            for i in range(0, mass.shape[0], BATCH_SIZE):
                batch_mass = mass[i:i+BATCH_SIZE]
                flow = pt_eta_H_flow(batch_mass)

                # samples: (num_samples, batch_size, D)
                samples = flow.sample((number_of_samples,))

                # flatten the first 2 dims → (num_samples * batch_size, D)
                samples = samples.reshape(-1, samples.shape[-1])

                all_samples.append(samples)

        pt_eta = torch.cat(all_samples, dim=0)

        pt_eta_mass = torch.concat([pt_eta, mass], dim=1)

        probs, pred = ensemble_predict(models_b, pt_eta_mass)

        probs = probs.cpu() # ensure CPU
        BATCH_SIZE = 1024
        all_samples = []

        with torch.no_grad():
            for i in range(0, probs.shape[0], BATCH_SIZE):
                batch_probs = probs[i:i + BATCH_SIZE]     # already on CPU

                batch_samples = torch.multinomial(
                    input=batch_probs,
                    num_samples=number_of_samples,
                    replacement=False 
                )

                all_samples.append(batch_samples)

        sampled_NJ = torch.cat(all_samples, dim=0)

        ptj_flow = ptj_flow.cpu()
        DPhiJ0J1_flow = DPhiJ0J1_flow.cpu()
        pt_eta_mass_NJ = torch.concat([sampled_NJ.float(), pt_eta_mass], dim=1)

        sampled_NJ = sampled_NJ.cpu()
        pt_eta_mass_NJ = pt_eta_mass_NJ.cpu()

        BATCH_SIZE = 256
        all_ptj0 = []
        all_dphij0j1 = []

        with torch.no_grad():
            for i in range(0, sampled_NJ.shape[0], BATCH_SIZE):
                # --------------------
                # 1) Batch inputs
                # --------------------
                batch_NJ = sampled_NJ[i:i+BATCH_SIZE].float()
                batch_pt_eta_mass_NJ = pt_eta_mass_NJ[i:i+BATCH_SIZE]

                # --------------------
                # 2) Sample ptj0
                # --------------------
                batch_ptj0 = ptj_flow(batch_pt_eta_mass_NJ).sample((1,)).squeeze(0)
                all_ptj0.append(batch_ptj0)

                # --------------------
                # 3) Sample dphij0j1
                # --------------------
                batch_ptj0_nj_pt_eta_mass = torch.cat([batch_ptj0, batch_pt_eta_mass_NJ], dim=1)
                batch_dphij0j1 = DPhiJ0J1_flow(batch_ptj0_nj_pt_eta_mass).sample((1,)).squeeze(0)
                all_dphij0j1.append(batch_dphij0j1)

        # --------------------
        # 4) Combine all results
        # --------------------
        sample_ptj0 = torch.cat(all_ptj0, dim=0)
        sample_dphij0j1 = torch.cat(all_dphij0j1, dim=0)
        
        ptj0_nj_pt_eta_mass = torch.concat([sample_ptj0, pt_eta_mass_NJ], dim=1)

        final_sample = torch.concat([sample_dphij0j1, ptj0_nj_pt_eta_mass], dim=1)
        
        tensor = final_sample.clone()
        NJ = tensor[:, 2]
        # Masks
        mask_NJ0 = (NJ == 0)
        mask_NJ1 = (NJ == 1)

        # 1) For NJ == 0 --- set DPhiJ0J1 = -999
        tensor[mask_NJ0, 0] = -999.0

        # 2) For NJ == 0 --- set PTJ0 to some x that YOU choose
        # Replace this with the correct value once equation is clarified
        # x = torch.tensor([-990.0], device=tensor.device)  
        x = torch.tensor([float("nan")], device=tensor.device)  
        tensor[mask_NJ0, 1] = x

        # 3) For NJ == 1 --- set DPhiJ0J1 = -999
        tensor[mask_NJ1, 0] = -999.0
        
        pipelines = cloudpickle.load(open("/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Replicas/hgg_kinflow/preprocessing_pipeline_v1.pkl", "rb"))

        columns = ["DPhiJ0J1", "PTJ0","NJ","pt","rapidity","mass","cat","year"]
        out = [] 
        for d, col in enumerate(columns):
            out.append(pipelines[col].inverse_transform(tensor[:, d].cpu().numpy().reshape(-1,1)).squeeze())
        unscaled_dataset = torch.from_numpy(np.stack(out).T)

        NJ = unscaled_dataset[:, 2]

        # Masks
        mask_NJ0 = (NJ == 0)
        mask_NJ1 = (NJ == 1)

        x = torch.tensor([-999.0], device=tensor.device)  
        unscaled_dataset[mask_NJ0, 1] = x

        inclusive_bkg_replica = pd.DataFrame(unscaled_dataset.detach().cpu().numpy(), columns=["DPhiJ0J1", "PTJ0","NJ","pt","rapidity","CMS_hgg_mass","cat","year"])

        # add lead_mvaID column with constant 1.0 (float32 to match replica dtypes) (mvaID cut in this approach not relevant)
        inclusive_bkg_replica['lead_mvaID'] = np.ones(len(inclusive_bkg_replica), dtype=np.float32)
        inclusive_bkg_replica['sublead_mvaID'] = np.ones(len(inclusive_bkg_replica), dtype=np.float32)
        inclusive_bkg_replica['weight'] = np.ones(len(inclusive_bkg_replica), dtype=np.float32)

        # depending on the cat, assign a sensible sigmaMoverM value such that the category is chosen in the next step
        sigmaMoverM_values = {
            "2022": {
                "cat0": 0.00525,  # cat 0
                "cat1": 0.01175,  # cat 1
                "cat2": 0.02225   # cat 2
            },
            "2023": {
                "cat0": 0.0055,  # cat 0
                "cat1": 0.0125,  # cat 1
                "cat2": 0.02275   # cat 2
            },
            "2024": {
                "cat0": 0.0055,  # cat 0
                "cat1": 0.0125,  # cat 1
                "cat2": 0.02275   # cat 2
            }
        }

        inclusive_bkg_replica['cat'] = inclusive_bkg_replica['cat'].astype(int)

        inclusive_bkg_replica.loc[inclusive_bkg_replica["cat"] == 0,'sigma_m_over_m_corr_smeared_decorr'] = sigmaMoverM_values[self.year]["cat0"]
        inclusive_bkg_replica.loc[inclusive_bkg_replica["cat"] == 1,'sigma_m_over_m_corr_smeared_decorr'] = sigmaMoverM_values[self.year]["cat1"]
        inclusive_bkg_replica.loc[inclusive_bkg_replica["cat"] == 2,'sigma_m_over_m_corr_smeared_decorr'] = sigmaMoverM_values[self.year]["cat2"]

        # Load the considered variable
        cat_dict_path = os.path.join("/work/niharrin/analyses/MidRun3_Code/postprocessing/configs/cat_dicts", f"{self.year}", self.config['inputFiles']['catDict_timestamp'], f"{self.variable}_MC.json")
        if not os.path.exists(cat_dict_path):
            print(f"Category dictionary {cat_dict_path} does not exist. Check path in law_replica.py. Exiting...")
            exit(1)
        else:
            with open(cat_dict_path) as pf:
                cat_dict = json.load(pf)
        
        # Generate Signal Only
        replica_separated_procs = []

        # Get the replica for each process / category
        for i, powheg_proc_folder in enumerate(powheg_proc_dirs):
            # print(f"Processing parquet files from {proc_folder}")
            # Load the parquet files for the current process
            powheg_proc_parquet_files = glob.glob(os.path.join(powheg_proc_folder, "nominal", "*.parquet"))
            current_proc_name = powheg_proc_folder.split("/")[-1]
            mc_proc_parquet_files = glob.glob(os.path.join(self.config['inputFiles']['mc_src_files'], current_proc_name, "nominal", "*.parquet"))

            if len(powheg_proc_parquet_files) == 0:
                print(f"No parquet files found in {powheg_proc_folder}. Skipping...")
                continue
            current_proc_replica = get_replica(mc_proc_parquet_files, powheg_proc_parquet_files, columns_to_load=columns_to_load)
            # current_proc_replica = get_replica_bin_by_bin(mc_parquet_files=mc_proc_parquet_files, cat_dict_=cat_dict, parquet_files=powheg_proc_parquet_files, columns_to_load=columns_to_load)

            replica_separated_procs.append(current_proc_replica)

        output_bkg_rootfile = ROOT.TFile(f"./allReplica_{int(replica_index)}.{seed}.root", "RECREATE")

        output_bkg_rootfile.mkdir("DiphotonTree")
        output_bkg_rootfile.cd("DiphotonTree")

        # inclusive_bkg_replica.rename(columns={"mass": "CMS_hgg_mass"}, inplace=True)

        signal_replica = []
        background_replica = []
        splusb_replica = []
            
        # Now categorize the replica
        for cat in cat_dict:
            try:
                query_str = " and ".join(
                    f"{col} {op} {val}" for col, op, val in cat_dict[cat]["cat_filter"]
                )
            except:
                # Have a variable using absolute values.
                query_str = "("
                for k, set_of_conditions in enumerate(cat_dict[cat]["cat_filter"]):
                    if k > 0:
                        query_str += ") or ("
                    query_str += " and ".join(
                        f"{col} {op} {val}" for col, op, val in set_of_conditions
                    )
                query_str += ")"
            print(f"Processing category {cat} with query: {query_str} and number of events: {len(inclusive_bkg_replica.query(query_str))}")

            current_cat_background_replica = pd.concat([inclusive_bkg_replica.query(query_str)], ignore_index=True)
            
            current_cat_signal_replica = pd.concat([replica_separated_procs[i].query(query_str) for i in range(len(replica_separated_procs))], ignore_index=True)
            
            current_cat_signal_replica = current_cat_signal_replica[columns_to_load]
            current_cat_signal_replica.rename(columns={"mass": "CMS_hgg_mass"}, inplace=True)
            
            signal_replica.append(current_cat_signal_replica)
            background_replica.append(current_cat_background_replica)
            
            print("Background replica index unique:", current_cat_background_replica.index.is_unique)
            print("Signal replica index unique:", current_cat_signal_replica.index.is_unique)
            print("Background replica columns unique:", current_cat_background_replica.columns.is_unique)
            print("Signal replica columns unique:", current_cat_signal_replica.columns.is_unique)

            
            # Merge both dataframes
            current_cat_replica = pd.concat([current_cat_background_replica, current_cat_signal_replica], ignore_index=True)
            # current_cat_replica = pd.concat([current_cat_background_replica], ignore_index=True)

            splusb_replica.append(current_cat_replica)
            
            # Create a ROOT TTree to hold the data (using columns of `current_cat_replica`)
            tree = ROOT.TTree("Data_13TeV_"+cat, "")

            # Dictionary zum Speichern von Buffern (muss im Speicher bleiben!)
            buffers = {}

            for col in current_cat_replica.columns:
                # Float-Array (ROOT erwartet C-Puffer)
                buffers[col] = array.array('f', [0])
                tree.Branch(col, buffers[col], f"{col}/F")

            # Füllen
            for _, row in current_cat_replica.iterrows():
                for col in current_cat_replica.columns:
                    buffers[col][0] = float(row[col])  # cast erzwingt korrekten Typ
                tree.Fill()

            tree.Write()
                
        # Close the file
        output_bkg_rootfile.Close()
    
        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)

class GenerateBootstrapData(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    # Generate a SplusB replica dataset
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    # batch_system = law.Parameter(default="slurm", description="Batch system to use")
    number_of_replicas = law.Parameter(default=2000, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

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

    def create_branch_map(self):
        branch_map = {
            i: replica_index
            for i, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map

    def output(self):
        # returns output folder
        replica_index = self.branch_data
        
        self._init_once()
        
        output_paths = []
        
        seed = int(self.seed) + int(replica_index)

        output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'Bootstrap', f'bootstrapData_{int(replica_index)}.{seed}.root'))

        outputFileTargets = []
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))
        
        return outputFileTargets

    def run(self):
        replica_index = self.branch_data
        
        self._init_once()
        
        cwd = os.getcwd()
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in self.resolved_output_dir:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/Bootstrap'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/Bootstrap'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/Bootstrap'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'Bootstrap'))
        else:
            execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/Bootstrap'], shell=True)
            os.chdir(os.path.join(self.resolved_output_dir, 'Replicas', 'Bootstrap'))

        seed = int(self.seed) + int(replica_index)
                
        print("Generating Bootstrap replica with seed {}".format(seed))

        # Load the considered variable
        cat_dict_path = os.path.join("/work/niharrin/analyses/MidRun3_Code/postprocessing/configs/cat_dicts", f"{self.year}", self.config['inputFiles']['catDict_timestamp'], f"{self.variable}_data.json")
        if not os.path.exists(cat_dict_path):
            print(f"Category dictionary {cat_dict_path} does not exist. Check path in law_replica.py. Exiting...")
            exit(1)
        else:
            with open(cat_dict_path) as pf:
                cat_dict = json.load(pf)

        def chunked(iterable, size):
            it = iter(iterable)
            while True:
                batch = list(islice(it, size))
                if not batch:
                    break
                yield batch

        data_parquet_files = glob.glob(os.path.join(self.config['inputFiles']['data_src_files'], "*/nominal/*.parquet"))

        chunks = []

        for file_batch in tqdm(
            chunked(data_parquet_files, size=10),
            total=(len(data_parquet_files) + 9) // 10,
            desc="Loading parquet chunks"
        ):
            df_chunk = pd.concat(
                (pd.read_parquet(f) for f in file_batch),
                ignore_index=True
            )
            chunks.append(df_chunk)

        data_df = pd.concat(chunks, ignore_index=True)

        # Now create Poissonian weights
        rng = np.random.default_rng(seed=seed)
        weight_poissonian = rng.poisson(1, size=len(data_df))
        data_df["weight"] = weight_poissonian
        data_df["weight_central"] = weight_poissonian
        
        data_df = data_df.rename(columns={"mass": "CMS_hgg_mass"})

        if "nweight_LHEScale" not in data_df.columns:
            data_df["nweight_LHEScale"] = np.full(len(data_df), 9, dtype=np.int32)

        with uproot.recreate(f'./bootstrapData_{int(replica_index)}.{seed}.root') as f:
            # Create directory
            f.mkdir("DiphotonTree")

            # Now categorize the background replica
            for cat in cat_dict:
                try:
                    query_str = " and ".join(
                        f"{col} {op} {val}" for col, op, val in cat_dict[cat]["cat_filter"]
                    )
                except:
                    # Have a variable using absolute values.
                    query_str = "("
                    for k, set_of_conditions in enumerate(cat_dict[cat]["cat_filter"]):
                        if k > 0:
                            query_str += ") or ("
                        query_str += " and ".join(
                            f"{col} {op} {val}" for col, op, val in set_of_conditions
                        )
                    query_str += ")"
                print(f"Processing category {cat} with query: {query_str}")

                current_cat_bootstrap = data_df.query(query_str).copy()
                
                print("Sum of weights:", current_cat_bootstrap["weight"].sum())

                tree_name = "Data_13TeV_" + cat
                # Convert pandas DataFrame to dict of lists
                data_dict = current_cat_bootstrap.to_dict(orient="list")

                # Determine branch types (float32 is safe for HEP)
                branches = {col: "float32" for col in data_dict.keys()}

                # Create the tree inside the DiphotonTree directory
                tree = f.mktree(f"DiphotonTree/{tree_name}", branches)

                # Fill the tree with your data
                tree.extend(data_dict)

            f.close()
    
        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
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
    toy_flag = law.Parameter(default=False, description="Toy flag")
    number_of_replicas = law.Parameter(default=2000, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

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
        
        tasks["GetAsimovBestFit"] = GetAsimovBestFit(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition=fitConfig['batchPartition'], slurm_memory=fitConfig['batchMemory'], slurm_max_runtime=fitConfig['batchMaxRuntime'], htcondor_partition=fitConfig['batchPartition'], htcondor_memory=fitConfig['batchMemory'], htcondor_max_runtime=fitConfig['batchMaxRuntime'], toy_flag=self.toy_flag, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value, seed=self.seed)

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
        
        self._init_once()
        
        output_paths = []
        
        seed = int(self.seed) + int(replica_index)

        output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'bonly', f'bkgReplica_{int(replica_index)}.{seed}.root'))

        outputFileTargets = []
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))
        
        return outputFileTargets

    def run(self):
        replica_index = self.branch_data
        
        self._init_once()
        
        cwd = os.getcwd()
        
        # if self.variable == '':
        #     ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.year}.root')
        # else:
        #     ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in self.resolved_output_dir:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/bonly'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/bonly'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/bonly'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'bonly'))
        else:
            execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/bonly'], shell=True)
            os.chdir(os.path.join(self.resolved_output_dir, 'Replicas', 'bonly'))

        seed = int(self.seed) + int(replica_index)
        
        first_output = os.path.join(self.resolved_output_dir, 'Replicas')

        def check_pdf_idx():
            # Run the ROOT command
            command = f'root -l -q \'{os.environ["ANALYSIS_PATH"]}/Combine/checkPdfIdx.C("{first_output}/higgsCombineFirstStep.MultiDimFit.mH125.38.root")\''
            
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
        
        # pdfIdx = check_pdf_idx()

        # # Run the ROOT command
        # background_model_folder_name = self.config['datacard_yields']['bkgModelWSDir'].split('/')[-2]
        # bkg_input_folder = os.path.join(self.resolved_output_dir, "Combine", background_model_folder_name, "background")
        # toy_output_file = f"./higgsCombineToy_{int(replica_index)}"+f".GenerateOnly.mH125.38.{seed}.root"
        # arguments = ['root', '-l', '-q', f"{os.environ['ANALYSIS_PATH']}/Replicas/toy_Bonly.C(\"{bkg_input_folder}\", \"{toy_output_file}\", \"{pdfIdx}\", {seed})"]
        
        # # Execute the command and capture the output
        # command = arguments
        # print(command)
        # try:
        #     result = subprocess.run(command, check=True, text=True, capture_output=True)
        #     print("Script output:", result.stdout)
        #     print("Script executed successfully.")
        # except subprocess.CalledProcessError as e:
        #     print("Error executing script:", e.stderr)
        
        bkg_proc_dirs = glob.glob(os.path.join(self.config['inputFiles']['bkg_src_files'], "*"))
        data_parquet_files = glob.glob(os.path.join(self.config['inputFiles']['data_src_files'], "*/nominal/*.parquet"))
        
        all_parquet_files = []
        for proc_dir in bkg_proc_dirs:
            # if "GG-Box-3Jets" in proc_dir: continue
            parquet_files = glob.glob(os.path.join(proc_dir, "nominal", "*.parquet"))
            all_parquet_files.append(parquet_files)
        
        # Extract the expected number of sideband events from data
        sideband_exp, _ = get_data_exp(data_parquet_files)
        
        columns_to_load = [
            "mass", "weight", "lead_mvaID", "sublead_mvaID",
            "sigma_m_over_m_corr_smeared_decorr"
        ]
        
        if self.variable == "PTH":
            columns_to_load += ["pt"]
        elif self.variable in jetVariables:
            columns_to_load += [self.variable, "NJ"]
        else:
            columns_to_load += [self.variable]
        
        np.random.seed(seed)
        inclusive_bkg_replica = get_bkg_replica(sideband_exp, all_parquet_files, columns_to_load)
        
        # Apply a mass mask
        mass_mask = (inclusive_bkg_replica["mass"] >= 100) & (inclusive_bkg_replica["mass"] <= 180)
        inclusive_bkg_replica = inclusive_bkg_replica[mass_mask]
        
        # Get background file list
        background_model_folder_name = self.config['datacard_yields']['bkgModelWSDir'].split('/')[-2]
        bkg_file_list = glob.glob(os.path.join(self.resolved_output_dir, "Combine", background_model_folder_name, "background", "*.root"))

        # Create RooCategory (same as in C++)
        CMS_channel = ROOT.RooCategory("CMS_channel", "Channel name")

        # Collect category names
        cat_names = [get_category_name(filename) for filename in bkg_file_list]
        cat_names.sort(key=natural_sort_key)


        # Define the types in the RooCategory
        for i, cat_name in enumerate(cat_names):
            if cat_name:  # skip empty names
                CMS_channel.defineType(cat_name, i)

        # Extract CMS channel labels and indices
        # This corresponds to the categories in the category dictionary
        CMS_channel_dict = {}
        for i in range(CMS_channel.numTypes()):
            CMS_channel.setIndex(i)
            CMS_channel_dict[CMS_channel.getLabel()] = i
        
        # Load the considered variable
        cat_dict_path = os.path.join("/work/niharrin/analyses/MidRun3_Code/postprocessing/configs/cat_dicts", f"{self.year}", self.config['inputFiles']['catDict_timestamp'], f"{self.variable}_MC.json")
        if not os.path.exists(cat_dict_path):
            print(f"Category dictionary {cat_dict_path} does not exist. Check path in law_replica.py. Exiting...")
            exit(1)
        else:
            with open(cat_dict_path) as pf:
                cat_dict = json.load(pf)
                
        # Now create the output ROOT file and the associated variables (Combine konform)
                
        output_bkg_rootfile = ROOT.TFile(f'./bkgReplica_{int(replica_index)}.{seed}.root', "RECREATE")

        # Create the CMS_hgg_mass variable
        CMS_hgg_mass = ROOT.RooRealVar("CMS_hgg_mass", "CMS_hgg_mass", 100.0, 100.0, 180.0)
        CMS_hgg_mass.setBins(320) # 320
        argset = ROOT.RooArgSet(CMS_hgg_mass, CMS_channel)

        output_bkg_rootfile.mkdir("toys")
        output_bkg_rootfile.cd("toys")

        # Create empty RooDataSet 
        toy_1 = ROOT.RooDataSet("toy_1", "toy_1", argset)
                
        # Now categorize the background replica
        for cat in cat_dict:
            try:
                query_str = " and ".join(
                    f"{col} {op} {val}" for col, op, val in cat_dict[cat]["cat_filter"]
                )
            except:
                # Have a variable using absolute values.
                query_str = "("
                for k, set_of_conditions in enumerate(cat_dict[cat]["cat_filter"]):
                    if k > 0:
                        query_str += ") or ("
                    query_str += " and ".join(
                        f"{col} {op} {val}" for col, op, val in set_of_conditions
                    )
                query_str += ")"
            print(f"Processing category {cat} with query: {query_str}")

            current_cat_replica = pd.concat([inclusive_bkg_replica.query(query_str)], ignore_index=True)
            
            mass_value_list = current_cat_replica["mass"].to_list()
            
            # Loop to add the events to the RooDataSet
            for i, val in enumerate(mass_value_list):
                CMS_channel.setIndex(CMS_channel_dict[cat])
                CMS_hgg_mass.setVal(val)
                # bonly_toy.add(argset, additional_probability_values[i])
                toy_1.add(argset, 1.)
            
        toy_1.SetName("toy_1")   # Important: name must match what Combine expects
        toy_1.Write()

        # Close the file
        output_bkg_rootfile.Close()
    
        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
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
    
    save_sonly = law.Parameter(default=False, description="If True, will save the s-only replica as well.")

    # parquet_dir = law.Parameter(default='', description="Path to the parquet directory, used to create the s-only replicas")
    
    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    number_of_replicas = law.Parameter(default=10, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

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
        
        workflow_reqs = super().workflow_requires()
        
        self._init_once()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
        fitConfig = self.config["combine_fit"]
        
        tasks["GenerateBOnlyToys"] = GenerateBOnlyToys(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition="short", slurm_memory=2000, slurm_max_runtime="00:15:00", htcondor_partition="espresso", htcondor_memory=2000, htcondor_max_runtime="00:20:00", seed=self.seed, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value)

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

        self._init_once()

        output_paths = []

        seed = int(self.seed) + int(replica_index)

        output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root'))

        if convert_boolean_string(self.save_sonly):
            powheg_main_parquet_dir = self.config['inputFiles']['powheg_src_files']
            dir_list = glob.glob(os.path.join(powheg_main_parquet_dir, "*"))
            proc_list = [d.split("/")[-1] for d in dir_list if os.path.isdir(d)]
            for proc in proc_list:   
                output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'Sonly', proc, f'Sonly_Toy_{int(replica_index)}.{seed}.parquet'))

        outputFileTargets = []

        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        replica_index = self.branch_data
        
        self._init_once()

        # Need to load the categorization dictionary
        # Location hardcoded, as I want to use the "common" categorization dictionary from the Analysis Git Repo
        if self.variable == '':
            cat_dict_path = os.path.join("/work/niharrin/analyses/MidRun3_Code/postprocessing/configs/cat_dicts", f"{self.year}", self.config['inputFiles']['catDict_timestamp'], f"inclusive_MC.json")
        else:
            cat_dict_path = os.path.join("/work/niharrin/analyses/MidRun3_Code/postprocessing/configs/cat_dicts", f"{self.year}", self.config['inputFiles']['catDict_timestamp'], f"{self.variable}_MC.json")
        if not os.path.exists(cat_dict_path):
            print(f"Category dictionary {cat_dict_path} does not exist. Check path in law_replica.py. Exiting...")
            exit(1)
        else:
            with open(cat_dict_path) as pf:
                cat_dict = json.load(pf)

        cwd = os.getcwd()

        powheg_main_parquet_dir = self.config['inputFiles']['powheg_src_files']
        mc_main_parquet_dir = self.config['inputFiles']['mc_src_files']

        # Load all Parquet files from the main_parquet_dir
        # Note, that I have to load the nominal parquet files from all the procs, as the systematics are already accounted for in the signal model
        # Select only 125 GeV Higgs mass point (idk how I should interpolate the different datasets on an event basis...)
        powheg_proc_folders = glob.glob(os.path.join(powheg_main_parquet_dir, "*125*"))

        # Fix a seed for reproducibility
        seed = int(self.seed) + int(replica_index)
        np.random.seed(seed)
        
        # Load the b-only toy file
        bonly_toy_path = os.path.join(self.resolved_output_dir, 'Replicas', 'bonly', f'bkgReplica_{int(replica_index)}.{seed}.root')
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
        for i, powheg_proc_folder in enumerate(powheg_proc_folders):
            # print(f"Processing parquet files from {proc_folder}")
            # Load the parquet files for the current process
            powheg_proc_parquet_files = glob.glob(os.path.join(powheg_proc_folder, "nominal", "*.parquet"))
            current_proc_name = powheg_proc_folder.split("/")[-1]
            mc_proc_parquet_files = glob.glob(os.path.join(mc_main_parquet_dir, current_proc_name, "nominal", "*.parquet"))

            if len(powheg_proc_parquet_files) == 0:
                print(f"No parquet files found in {powheg_proc_folder}. Skipping...")
                continue
            
            current_proc_replica = get_replica(mc_proc_parquet_files, powheg_proc_parquet_files)

            replica_separated_procs.append(current_proc_replica)
        
        # Now merge the procs per category
        for cat in cat_dict:
            try:
                query_str = " and ".join(
                    f"{col} {op} {val}" for col, op, val in cat_dict[cat]["cat_filter"]
                )
            except:
                # Have a variable using absolute values.
                query_str = "("
                for k, set_of_conditions in enumerate(cat_dict[cat]["cat_filter"]):
                    if k > 0:
                        query_str += ") or ("
                    query_str += " and ".join(
                        f"{col} {op} {val}" for col, op, val in set_of_conditions
                    )
                query_str += ")"
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
            if "/work" in self.resolved_output_dir:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/SplusB'], shell=True)
                if convert_boolean_string(self.save_sonly):
                    dir_list = glob.glob(os.path.join(powheg_main_parquet_dir, "*"))
                    proc_list = [d.split("/")[-1] for d in dir_list if os.path.isdir(d)]
                    for proc in proc_list:
                        execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/Sonly/{proc}'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/SplusB'], shell=True)
                if convert_boolean_string(self.save_sonly):
                    dir_list = glob.glob(os.path.join(powheg_main_parquet_dir, "*"))
                    proc_list = [d.split("/")[-1] for d in dir_list if os.path.isdir(d)]
                    for proc in proc_list:
                        execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/Sonly/{proc}'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/SplusB'], shell=True)
            if convert_boolean_string(self.save_sonly):
                dir_list = glob.glob(os.path.join(powheg_main_parquet_dir, "*"))
                proc_list = [d.split("/")[-1] for d in dir_list if os.path.isdir(d)]
                for proc in proc_list:
                    execute_command([f'mkdir -p $TARGET_PATH/Replicas/Sonly/{proc}'], shell=True)
            output_root_path = os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root')
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', "SplusB"))
        else:
            execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/SplusB'], shell=True)
            if convert_boolean_string(self.save_sonly):
                dir_list = glob.glob(os.path.join(powheg_main_parquet_dir, "*"))
                proc_list = [d.split("/")[-1] for d in dir_list if os.path.isdir(d)]
                for proc in proc_list:
                    execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/Sonly/{proc}'], shell=True)
            output_root_path = os.path.join(self.resolved_output_dir, 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root')
            os.chdir(os.path.join(self.resolved_output_dir, 'Replicas', 'SplusB'))
        
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
        
        # Now save the s-only replica if requested
        if convert_boolean_string(self.save_sonly):
            dir_list = glob.glob(os.path.join(powheg_main_parquet_dir, "*"))
            proc_list = [d.split("/")[-1] for d in dir_list if os.path.isdir(d)]

            for i, powheg_proc_folder in enumerate(powheg_proc_folders):
                # print(f"Processing parquet files from {proc_folder}")
                # Load the parquet files for the current process
                current_proc_name = powheg_proc_folder.split("/")[-1]
                
                current_proc_replica = replica_separated_procs[i]

                output_sonly_path = os.path.join(self.resolved_output_dir, 'Replicas', 'Sonly', current_proc_name, f'Sonly_Toy_{int(replica_index)}.{seed}.parquet')
                if self.batch_flavor == "slurm/psi":
                    output_sonly_path = os.path.join(os.environ["TARGET_PATH"], 'Replicas', 'Sonly', current_proc_name, f'Sonly_Toy_{int(replica_index)}.{seed}.parquet')
                
                current_proc_replica.to_parquet(output_sonly_path)
    
        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])
        
        os.chdir(cwd)

class RandomizeGlobalObs(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow): #(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default="", description="Variable to be used")
    year = law.Parameter(default='2022', description="Year")

    bootstrap_flag = law.Parameter(default=False, description="Bootstrap flag")
    toy_flag = law.Parameter(default=False, description="Toy flag")
    number_of_replicas = law.Parameter(default=1000, description="Number of replicas to run.")
    starting_value = law.Parameter(default=0, description="Starting toy computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the toy generation")
    
    batch_flavor = law.Parameter(default="slurm", description="Batch system to use")

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
        workflow_reqs = super().workflow_requires()
        
        self._init_once()
        
        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)

        if convert_boolean_string(self.toy_flag) == True:        

            SplusB_config = self.config["combine_SplusB_toys"]
            
            tasks["GenerateAllReplicaData"] = GenerateAllReplicaData(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=SplusB_config["execution"], batch_flavor=self.batch_flavor, slurm_partition=SplusB_config['batchPartition'], slurm_memory=SplusB_config['batchMemory'], slurm_max_runtime=SplusB_config['batchMaxRuntime'], htcondor_partition=SplusB_config['batchPartition'], htcondor_memory=SplusB_config['batchMemory'], htcondor_max_runtime=SplusB_config['batchMaxRuntime'], seed=self.seed, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value)
            
        if convert_boolean_string(self.bootstrap_flag) == True:
            fitConfig = self.config["combine_fit"]

            tasks["GenerateBootstrapData"] = GenerateBootstrapData(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition=fitConfig['batchPartition'], slurm_memory=fitConfig['batchMemory'], slurm_max_runtime=fitConfig['batchMaxRuntime'], htcondor_partition=fitConfig['batchPartition'], htcondor_memory=fitConfig['batchMemory'], htcondor_max_runtime=fitConfig['batchMaxRuntime'], seed=self.seed, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value)

        return tasks
    
    def create_branch_map(self):
        branch_map = {
            j: replica_index
            for j, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map

    def output(self):
        replica_index = self.branch_data
        
        self._init_once()
        
        output = []

        if (convert_boolean_string(self.toy_flag) == True):
            output += [os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombineAsimovFirstStep_{replica_index}.MultiDimFit.mH125.root')]
        
        elif (convert_boolean_string(self.bootstrap_flag) == True):
            output += [os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'DatacardRandomizedAux_{replica_index}.MultiDimFit.mH125.root')]

        outputFileTargets = []

        for _, current_output_path in enumerate(output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        replica_index = self.branch_data

        self._init_once()

        cwd = os.getcwd()
        
        
        if (convert_boolean_string(self.toy_flag) == True):
            ws_path = os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombineAsimovFirstStep.MultiDimFit.mH125.root')
        elif (convert_boolean_string(self.bootstrap_flag) == True):
            ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.year}.root') if self.variable == '' else os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in self.resolved_output_dir:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/pdfIndices'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/pdfIndices'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/pdfIndices/'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', "pdfIndices"))
            temp_output_dir = os.environ["TARGET_PATH"]
        else:
            execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/pdfIndices'], shell=True)
            os.chdir(os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices'))
            temp_output_dir = self.resolved_output_dir

        seed = int(self.seed) + int(replica_index)

        file_in = ROOT.TFile(ws_path, "READ")
        ws_in = file_in.Get("w")

        # Set a seed for reproducibility
        rng = ROOT.TRandom3(seed)        

        # Randomize auxiliary measurements
        global_obs = ws_in.set("ModelConfig_GlobalObservables")

        for obs in global_obs:
            # Sample from a gaussian distribution 
            new_aux_value = rng.Gaus(0.0, 1.0)
            var = ws_in.var(obs.GetName())
            if var is not None:
                var.setRange(-100.0, 100.0)
                var.setVal(new_aux_value)
                print(f"After randomization {var.GetName()}: new value = {var.getVal()}")

        # Save the modified workspace to a new file
        if (convert_boolean_string(self.toy_flag) == True):
            file_out = ROOT.TFile(os.path.join(temp_output_dir, 'Replicas', 'pdfIndices', f'higgsCombineAsimovFirstStep_{replica_index}.MultiDimFit.mH125.root'), "RECREATE")
        elif (convert_boolean_string(self.bootstrap_flag) == True):
            file_out = ROOT.TFile(os.path.join(temp_output_dir, 'Replicas', 'pdfIndices', f'DatacardRandomizedAux_{replica_index}.MultiDimFit.mH125.root'), "RECREATE")
        ws_in.Write()

        file_out.Close()
        file_in.Close()

        # Copy the files back to pnfs if we are on slurm/psi
        if self.batch_flavor == "slurm/psi":
            # Have to copy over the output to the final directory
            # Don't forget to VOMS!
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)

class AsimovFirstStep(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    # save_sonly = law.Parameter(default=False, description="If True, will save the s-only replica as well.")

    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")

    toy_flag = law.Parameter(default=False, description="Toy flag")
    number_of_replicas = law.Parameter(default=10, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

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
        workflow_reqs = super().workflow_requires()

        self._init_once()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
        SplusB_config = self.config["combine_SplusB_toys"]
        
        # tasks["GenerateSplusBToys"] = GenerateSplusBToys(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=SplusB_config["execution"], batch_flavor=self.batch_flavor, slurm_partition=SplusB_config['batchPartition'], slurm_memory=SplusB_config['batchMemory'], slurm_max_runtime=SplusB_config['batchMaxRuntime'], htcondor_partition=SplusB_config['batchPartition'], htcondor_memory=SplusB_config['batchMemory'], htcondor_max_runtime=SplusB_config['batchMaxRuntime'], seed=self.seed, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value, save_sonly=self.save_sonly)
        
        tasks["RunText2Workspace"] = RunText2Workspace(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=SplusB_config["execution"], batch_flavor=self.batch_flavor, slurm_partition=SplusB_config['batchPartition'], slurm_memory=SplusB_config['batchMemory'], slurm_max_runtime=SplusB_config['batchMaxRuntime'], htcondor_partition=SplusB_config['batchPartition'], htcondor_memory=SplusB_config['batchMemory'], htcondor_max_runtime=SplusB_config['batchMaxRuntime'], number_of_toys=self.number_of_replicas, seed=self.seed, toy_flag=self.toy_flag)
        
        return tasks

    def create_branch_map(self):
        branch_map = {
            i: replica_index
            for i, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map

    def output(self):
        replica_index = self.branch_data
        
        self._init_once()
        
        output_paths = []

        # output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombineAsimovFirstStep_Toy_{int(replica_index)}.MultiDimFit.mH125.38.root'))
        output_paths.append(os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombineAsimovFirstStep_Toy_{int(replica_index)}.MultiDimFit.mH125.root'))

        outputFileTargets = []
                
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))
        
        return outputFileTargets

    def run(self):
        replica_index = self.branch_data
        
        self._init_once()
        
        cwd = os.getcwd()
        
        if self.variable == '':
            # ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.year}.root')
            ws_path = os.path.join(self.resolved_output_dir, 'Combine', 'Workspaces', f'Datacard_{self.year}_{replica_index}.root')
        else:
            # ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')
            ws_path = os.path.join(self.resolved_output_dir, 'Combine', 'Workspaces', f'Datacard_{self.variable}_{self.year}_{replica_index}.root')
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in self.resolved_output_dir:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/pdfIndices'], shell=True)
            else:   
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Replicas/pdfIndices'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Replicas/pdfIndices/'], shell=True)
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Replicas', "pdfIndices"))
        else:
            execute_command([f'mkdir -p {self.resolved_output_dir}/Replicas/pdfIndices'], shell=True)
            os.chdir(os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices'))
        
        seed = int(self.seed) + int(replica_index)
        
        # arguments = [
        #     "combine",
        #     "-M", "MultiDimFit",
        #     ws_path,
        #     "--freezeParameters", "MH",
        #     "-m", "125.38",
        #     "-n", f"PdfIndices_Toy_{int(replica_index)}",
        #     "--cminDefaultMinimizerStrategy=0",
        #     "--saveWorkspace",
        #     "--X-rtd", "MINIMIZER_freezeDisassociatedParams",
        #     "--X-rtd", "MINIMIZER_multiMin_hideConstants",
        #     "--X-rtd", "MINIMIZER_multiMin_maskConstraints",
        #     "--X-rtd", "MINIMIZER_multiMin_maskChannels=2",
        #     "--floatOtherPOIs", "1",
        #     # "-D", f"{splusb_toy}:toys/toy_1",
        # ]

        arguments = [
            "combine",
            "-M", "MultiDimFit",
            ws_path,
            "--freezeParameters", "MH",
            # "-m", "125.38",
            "-m", "125",
            "-n", f"AsimovFirstStep_Toy_{int(replica_index)}",
            "--cminDefaultMinimizerStrategy=0",
            "--saveWorkspace",
            "--X-rtd", "MINIMIZER_freezeDisassociatedParams",
            "--X-rtd", "MINIMIZER_multiMin_hideConstants",
            "--X-rtd", "MINIMIZER_multiMin_maskConstraints",
            "--X-rtd", "MINIMIZER_multiMin_maskChannels=2",
            "--floatOtherPOIs", "1",
            "--robustFit=1",
            "-t", "-1",
        ]
        if self.variable == "":
            arguments += ["--saveSpecifiedIndex", ",".join([f"pdfindex_{bmw}_{self.year}_13TeV" for bmw in BMW])]
            arguments += ["--setParameters", "r=1"]
        else:
            # arguments += ["--saveSpecifiedIndex", ",".join(combineVariableDict(self.variable, self.year)['pdfIndeces'])]

            arguments += ["--setParameters", ",".join(combineVariableDict(self.variable, self.year)['paramStr'])]
            # arguments += ["--setParameters", ",".join(combineVariableDict(self.variable, self.year)['paramStrZero'])]

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
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Replicas/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)

class FitDataset(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow): #(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default="", description="Variable to be used")
    year = law.Parameter(default='2022', description="Year")
    
    # save_sonly = law.Parameter(default=False, description="If True, will save the s-only replica as well.")

    bootstrap_flag = law.Parameter(default=False, description="Bootstrap flag")
    toy_flag = law.Parameter(default=False, description="Toy flag")
    number_of_replicas = law.Parameter(default=1000, description="Number of replicas to run.")
    starting_value = law.Parameter(default=0, description="Starting toy computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the toy generation")
    
    batch_flavor = law.Parameter(default="slurm", description="Batch system to use")

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
        workflow_reqs = super().workflow_requires()
        
        self._init_once()
        
        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)

        if convert_boolean_string(self.toy_flag) == True:        

            SplusB_config = self.config["combine_SplusB_toys"]
            
            tasks["AsimovFirstStep"] = AsimovFirstStep(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=SplusB_config["execution"], batch_flavor=self.batch_flavor, slurm_partition=SplusB_config['batchPartition'], slurm_memory=SplusB_config['batchMemory'], slurm_max_runtime=SplusB_config['batchMaxRuntime'], htcondor_partition=SplusB_config['batchPartition'], htcondor_memory=SplusB_config['batchMemory'], htcondor_max_runtime=SplusB_config['batchMaxRuntime'], seed=self.seed, number_of_replicas=self.number_of_replicas, starting_value=self.starting_value, toy_flag=self.toy_flag)
            
        if convert_boolean_string(self.bootstrap_flag) == True:
            fitConfig = self.config["combine_fit"]
            
            tasks["RunT2WS"] = RunText2Workspace(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=fitConfig["execution"], batch_flavor=self.batch_flavor, slurm_partition=fitConfig['batchPartition'], slurm_memory=fitConfig['batchMemory'], slurm_max_runtime=fitConfig['batchMaxRuntime'], htcondor_partition=fitConfig['batchPartition'], htcondor_memory=fitConfig['batchMemory'], htcondor_max_runtime=fitConfig['batchMaxRuntime'], bootstrap_flag=self.bootstrap_flag, number_of_bootstraps=self.number_of_replicas, seed=self.seed)
        
        return tasks
    
    def create_branch_map(self):
        branch_map = {
            j: replica_index
            for j, replica_index in enumerate(range(int(self.starting_value), (int(self.starting_value) + int(self.number_of_replicas))))
        }
        return branch_map
    
    def output(self):
        replica_index = self.branch_data
        
        self._init_once()
        
        output = []
        if convert_boolean_string(self.bootstrap_flag) == True:
            output += [os.path.join(self.resolved_output_dir, 'Combine', self.fitFolderName, f'bootstrapFit', f'bootstrap_{replica_index}', f'higgsCombineBootstrapFit.MultiDimFit.mH125.38.root')]
        
        if convert_boolean_string(self.toy_flag) == True:
            # output += [os.path.join(self.resolved_output_dir, 'Combine', self.fitFolderName, f'toyFit', f'toy_{replica_index}', f'higgsCombineToyFit.MultiDimFit.mH125.38.root')]
            output += [os.path.join(self.resolved_output_dir, 'Combine', self.fitFolderName, f'toyFit', f'toy_{replica_index}', f'higgsCombineToyFit.MultiDimFit.mH125.root')]

        outputFileTargets = []

        for _, current_output_path in enumerate(output):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        replica_index = self.branch_data

        if convert_boolean_string(self.toy_flag) == True:
            dataset_type_folder_name = "toyFit"
            dataset_type_prefix = "toy"
        else:
            dataset_type_folder_name = "bootstrapFit"
            dataset_type_prefix = "bootstrap"

        self._init_once()

        cwd = os.getcwd()

        if self.variable == '':
            # ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.year}.root')
            ws_path = os.path.join(self.resolved_output_dir, 'Combine', 'Workspaces', f'Datacard_{self.year}_{replica_index}.root')
        else:
            # ws_path = os.path.join(self.resolved_output_dir, 'Combine', f'Datacard_{self.variable}_{self.year}.root')
            ws_path = os.path.join(self.resolved_output_dir, 'Combine', 'Workspaces', f'Datacard_{self.variable}_{self.year}_{replica_index}.root')
                    
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            if "/work" in self.resolved_output_dir:
                execute_command([f'mkdir -p {self.resolved_output_dir}/Combine/{self.fitFolderName}/{dataset_type_folder_name}/{dataset_type_prefix}_{replica_index}'], shell=True)
            else:
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Combine/{self.fitFolderName}/{dataset_type_folder_name}/{dataset_type_prefix}_{replica_index}'], shell=True)

            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            execute_command([f'mkdir -p $TARGET_PATH/Combine/{self.fitFolderName}/{dataset_type_folder_name}/{dataset_type_prefix}_{replica_index}'], shell=True)                
            os.chdir(os.path.join(os.environ["TARGET_PATH"], 'Combine', self.fitFolderName, dataset_type_folder_name, f'{dataset_type_prefix}_{replica_index}'))
        else:
            execute_command([f'mkdir -p {self.resolved_output_dir}/Combine/{self.fitFolderName}/{dataset_type_folder_name}/{dataset_type_prefix}_{replica_index}'], shell=True)
            os.chdir(os.path.join(self.resolved_output_dir, 'Combine', self.fitFolderName, dataset_type_folder_name, f'{dataset_type_prefix}_{replica_index}'))

        seed = int(self.seed) + int(replica_index)
                
        # pdfIndicesStr = ",".join(combineVariableDict(self.variable, self.year)['pdfIndeces'])

        # pdfindex_file = os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombinePdfIndices_Toy_{int(replica_index)}.MultiDimFit.mH125.38.root')
        if convert_boolean_string(self.toy_flag) == True:
            pdfindex_file = os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombinePdfIndices_Toy_{int(replica_index)}.MultiDimFit.mH125.root')

            def check_pdf_idx():
                # Run the ROOT command
                command = f'root -l -q \'{os.environ["ANALYSIS_PATH"]}/Combine/checkPdfIdx.C("{pdfindex_file}")\''
                
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
            
            pdfIdx = check_pdf_idx()
        
            # splusb_toy = os.path.join(self.resolved_output_dir, 'Replicas', 'SplusB', f'SplusB_Toy_{int(replica_index)}.{seed}.root')

            arguments = [
                "combine",
                "-M", "MultiDimFit",
                # ws_path,
                # os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombineAsimovFirstStep_Toy_{int(replica_index)}.MultiDimFit.mH125.38.root'),
                os.path.join(self.resolved_output_dir, 'Replicas', 'pdfIndices', f'higgsCombineAsimovFirstStep_Toy_{int(replica_index)}.MultiDimFit.mH125.root'),
                # "-m", "125.38",
                "-m", "125",
                "--snapshotName", "MultiDimFit",
                "-n", f"ToyFit",
                "--cminDefaultMinimizerStrategy=0",
                "--saveWorkspace",
                # "--cminApproxPreFitTolerance", f"{self.config['combine_fit']['cminApproxPreFitTolerance']}",
                "--robustFit=1",
                "--X-rtd", "MINIMIZER_freezeDisassociatedParams",
                "--X-rtd", "MINIMIZER_multiMin_hideConstants",
                "--X-rtd", "MINIMIZER_multiMin_maskConstraints",
                "--X-rtd", "MINIMIZER_multiMin_maskChannels=2",
                "--algo", "singles",
                # "--algo", "none", # Bekomme shit korrelierte Parameter zurueck ヽ(｀Д´)ﾉ
                "--saveFitResult",
                # "--setParameters", f"""{pdfIdx}""",
                "--freezeParameters", "MH",
                # "--freezeParameters", f"""MH,{",".join(combineVariableDict(self.variable, self.year)['pdfIndeces']) if self.variable != "" else ",".join([f"pdfindex_{bmw}_{self.year}_13TeV" for bmw in BMW])}""",
                # "--X-rtd", "MINIMIZER_skipDiscreteIterations",
                # "-D", f"{splusb_toy}:toys/toy_1",
                # --toysFrequentist --bypassFrequentistFit
            ]
        else:
            arguments = [
                "combine",
                "-M", "MultiDimFit",
                ws_path,
                "-m", "125.38",
                "-n", f"BootstrapFit",
                "--cminDefaultMinimizerStrategy=0",
                "--saveWorkspace",
                # "--cminApproxPreFitTolerance", f"{self.config['combine_fit']['cminApproxPreFitTolerance']}",
                "--robustFit=1",
                "--X-rtd", "MINIMIZER_freezeDisassociatedParams",
                "--X-rtd", "MINIMIZER_multiMin_hideConstants",
                "--X-rtd", "MINIMIZER_multiMin_maskConstraints",
                "--X-rtd", "MINIMIZER_multiMin_maskChannels=2",
                "--algo", "singles",
                # "--algo", "none", # Bekomme shit korrelierte Parameter zurueck ヽ(｀Д´)ﾉ
                "--saveFitResult",
                # "--setParameters", f"""{pdfIdx}""",
                "--freezeParameters", "MH",
                # "--freezeParameters", f"""MH,{",".join(combineVariableDict(self.variable, self.year)['pdfIndeces']) if self.variable != "" else ",".join([f"pdfindex_{bmw}_{self.year}_13TeV" for bmw in BMW])}""",
                # "--X-rtd", "MINIMIZER_skipDiscreteIterations",
                # "-D", f"{splusb_toy}:toys/toy_1",
                # --toysFrequentist --bypassFrequentistFit
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
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Combine/",
                    self.resolved_output_dir
                ]
            else:
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f"{os.environ['TARGET_PATH']}/Combine/",
                    'root://t3dcachedb03.psi.ch:1094//'+self.resolved_output_dir
                ]
            print(slurm_copy_command)
            execute_command(slurm_copy_command)
            # Clean up the temporary directory
            shutil.rmtree(os.environ["TARGET_PATH"])

        os.chdir(cwd)