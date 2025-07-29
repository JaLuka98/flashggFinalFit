import law
import os
import subprocess
import glob
import yaml
import errno
import subprocess
import shutil

from commonTools import *
from commonObjects import *

from Trees2WS.law_trees2ws_data import *

from framework import Task
from framework import HTCondorWorkflow, SlurmWorkflow

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def execute_command(command, return_output=False, shell=False):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=shell, env=os.environ)
        print("Script output:", result.stdout)
        print("Script executed successfully.")
        if return_output:
            return (result.stdout).split("\n")[0]
    except subprocess.CalledProcessError as e:
        print("Error executing script:", e.stderr)

class Background(Task, HTCondorWorkflow, SlurmWorkflow, law.LocalWorkflow):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    output_dir = law.Parameter(default="", description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    variable = law.Parameter(default="", description="Variable to be used")

    bootstrap_flag = law.Parameter(default=False, description="Bootstrap flag")
    number_of_bootstraps = law.Parameter(default=1000, description="Number of bootstraps")

    batch_flavor = law.Parameter(default="htcondor", description="Batch system to use")

    # def requires(self):
    def workflow_requires(self):
        workflow_reqs = super().workflow_requires()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)
        
        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_inclusive.yml")
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_{self.variable}.yml")
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
        
        config = config["backgroundScriptCfg"]
            
        tasks["Trees2WSData"] = Trees2WSData(output_dir=output_dir, variable=self.variable, year=self.year, version=self.variable if self.variable != "" else "inclusive", workflow=config['execution'], batch_flavor=self.batch_flavor, slurm_partition=config['batchPartition'], slurm_memory=config['batchMemory'], slurm_max_runtime=config['batchMaxRuntime'], htcondor_partition=config['batchPartition'], htcondor_memory=config['batchMemory'], htcondor_max_runtime=config['batchMaxRuntime'], bootstrap_flag=self.bootstrap_flag, number_of_bootstraps=self.number_of_bootstraps)
        
        return tasks
    
    def create_branch_map(self):
        # Creating a branch map for the categories
        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_inclusive.yml")
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_{self.variable}.yml")
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)

        input_path = config['inputFiles']['Trees2WSData']
                    
        config = config["backgroundScriptCfg"]
        
        if config['cats'] == 'auto':
            config['cats'] = (extractListOfCatsFromHiggsDNAAllData(input_path))

        nCats = len(config['cats'].split(","))
              
        cat_list = [
            (config['cats'].split(",")[categoryIndex], str(int(config['catOffset'])+categoryIndex))
            for categoryIndex in range(nCats)
        ]        
        if convert_boolean_string(self.bootstrap_flag) == True:
            branch_map = {
                i * int(self.number_of_bootstraps) + j: (cat_catOffset, bootstrap_index)
                for i, cat_catOffset in enumerate(cat_list)
                for j, bootstrap_index in enumerate(range(int(self.number_of_bootstraps)))
            }
        else:
            branch_map = {i: cat_catOffset for i, cat_catOffset in enumerate(cat_list)}
        return branch_map

    def output(self):
        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_inclusive.yml")
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_{self.variable}.yml")
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
                    
        config = config["backgroundScriptCfg"]
        
        if convert_boolean_string(self.bootstrap_flag) == True:
            cat_cat_offset, bootstrap_index = self.branch_data
            cat, cat_offset = cat_cat_offset
            outdir_ext = os.path.join(output_dir, 'Background', f'outdir_{config["ext"]}_{bootstrap_index}')
        else:
            cat, cat_offset = self.branch_data
            outdir_ext = os.path.join(output_dir, 'Background', f'outdir_{config["ext"]}')

        
        outputFileTargets = []
        
        if convert_boolean_string(self.bootstrap_flag) == False:
            bkg_plots = glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.png'))
            bkg_plots += glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.pdf'))
            bkg_plots += glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.pdf_gofTest.pdf'))

            output_paths = [os.path.join(outdir_ext, f'CMS-HGG_multipdf_{cat}.root'), os.path.join(outdir_ext, f'bkgfTest-Data/multipdf_{cat}.pdf'), os.path.join(outdir_ext, f'bkgfTest-Data/multipdf_{cat}.png')]

            output_paths += bkg_plots
        else: # Skip the plots for the bootstrap case
             output_paths = [os.path.join(outdir_ext, f'CMS-HGG_multipdf_{cat}.root')]
   
        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):
        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_inclusive.yml")
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"], f"config/{self.year}_{self.variable}.yml")
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
            
        
        input_path = config['inputFiles']['Trees2WSData']
                    
        config = config["backgroundScriptCfg"]
        
        if config['cats'] == 'auto':
            config['cats'] = (extractListOfCatsFromHiggsDNAAllData(input_path))
        config['nCats'] = len(config['cats'].split(","))
    
        # Add dummy entries for procs and signalFitWSFile (used in old plotting script)
        config['signalFitWSFile'] = 'none'
        config['procs'] = 'none'
        config['batch'] = 'local'
        config['queue'] = 'none'
        if self.year == 'combined': config['year'] = 'all'
        else: config['year'] = self.year     
        config['intLumi'] = lumiMap[self.year]

        if self.variable == '':
            if convert_boolean_string(self.bootstrap_flag) == False:
                all_data_input_path = os.path.join(output_dir, "input_output_data", f"input_output_data_{self.year}/ws/allData.root")
            else:
                all_data_input_path = os.path.join(output_dir, "input_output_data", f"input_output_data_{self.year}")
        else:
            if convert_boolean_string(self.bootstrap_flag) == False:
                all_data_input_path = os.path.join(output_dir, "input_output_data", f"input_output_data_{self.variable}_{self.year}/ws/allData.root")
            else:
                all_data_input_path = os.path.join(output_dir, "input_output_data", f"input_output_data_{self.variable}_{self.year}")

        if convert_boolean_string(self.bootstrap_flag) == True:
            cat_cat_offset, bootstrap_index = self.branch_data
            cat, cat_offset = cat_cat_offset
            # In this case self.input_path is self.output_path/input_output_data_{self.year}
            # Have to add the _{bootstrap_index}/ws/allData.root to the path manually, since we need the bootstrap index
            input_path = os.path.join(all_data_input_path+f"_{bootstrap_index}", "ws/allData.root")
        else:
            cat, cat_offset = self.branch_data
            input_path = all_data_input_path
        
        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            temp_output_dir = os.environ["TARGET_PATH"]
            execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {output_dir}/Background'], shell=True)
            if convert_boolean_string(self.bootstrap_flag) == True:
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {output_dir}/Background/outdir_{config["ext"]}_{bootstrap_index}'], shell=True)
            else:
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {output_dir}/Background/outdir_{config["ext"]}'], shell=True)
            safe_mkdir(temp_output_dir)
        else:
            safe_mkdir(output_dir)
            safe_mkdir(os.path.join(output_dir, "Background"))
            safe_mkdir(os.path.join(output_dir, "Background", f"outdir_{config['ext']}"))
            temp_output_dir = os.path.join(output_dir, "Background")
        
        if temp_output_dir[-1] != "/":
            temp_output_dir += "/"

        script_path = os.path.join(os.environ["ANALYSIS_PATH"], "Background/runBackgroundScripts.sh")
        arguments = [
            "-i", input_path,
            "-p", "none",
            "-f", cat,
            "--outputFolder", f"{temp_output_dir}",
            "--ext", f'{config["ext"]}_{bootstrap_index}' if convert_boolean_string(self.bootstrap_flag) == True else f'{config["ext"]}',
            "--catOffset", cat_offset,
            "--intLumi", f"{lumiMap[self.year]}",
            "--year", f"{self.year}",
            "--batch", "local",
            "--queue", "microcentury",
            "--sigFile", "none",
            "--isData",
            "--fTest"
        ]
        command = [script_path] + arguments
        # print("Output:", command)
        
        # Move to background folder
        original_dir = os.getcwd()
        os.chdir(os.path.join(os.environ["ANALYSIS_PATH"], "Background"))
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
            print("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.stderr)
        os.chdir(original_dir)

        if self.batch_flavor == "slurm/psi":
            if convert_boolean_string(self.bootstrap_flag) == True:
                bkg_folder = f"outdir_{config['ext']}_{bootstrap_index}"
            else:
                bkg_folder = f"outdir_{config['ext']}"
            execute_command([f"ls -al {temp_output_dir}/*"], shell=True)
            if "/work" in output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f'{temp_output_dir}/{bkg_folder}',
                     f'{output_dir}/Background/'
                ]
            else:
                # Copying output files to final destination on the /pnfs.
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f'{temp_output_dir}/{bkg_folder}',
                    'root://t3dcachedb03.psi.ch:1094//'+ f'{output_dir}/Background/'
                ]
            execute_command(slurm_copy_command)
            # Cleaning up scratch space.
            shutil.rmtree(temp_output_dir)
        