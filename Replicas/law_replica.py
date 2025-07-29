import law
import luigi
import os
import yaml
import errno

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

class GenerateBOnlyToys(Task, SlurmWorkflow, HTCondorWorkflow, law.LocalWorkflow):
    variable = law.Parameter(default="", description="Variable to be used")
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    year = law.Parameter(default='2022', description="Year")
    
    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    # batch_system = law.Parameter(default="slurm", description="Batch system to use")
    number_of_replicas = law.Parameter(default=2000, description="Number of replicas to run. If empty, will run the standard workflow.")
    starting_value = law.Parameter(default=0, description="Starting replica computation from this index. This can be useful for preventing overloading schedds.")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

    def requires(self):
        # req() is defined on all tasks and handles the passing of all parameter values that are
        # common between the required task and the instance (self)
        
        tasks = {}
        
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
        
        print("Generating B-Only replica with seed {}".format(seed))

        arguments = [
            "combine",
            "-M", "GenerateOnly",
            "-d", ws_path,
            "-t", "1",
            "-s", f"{seed}",
            "--setParameters", ",".join(combineVariableDict[f'{self.year}'][f'{self.variable}']['paramStrZero']),
            "--saveToys",
            "--freezeParameters", "MH",
            "-m", "125.38",
            "-n", f"Toy_{int(replica_index)}",
        ]
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

# combine -M GenerateOnly -d /t3home/niharrin/devel/pnfs/ntuples/midRun3/samples/2025_07_17_powheg/finalfits/PTH/Combine/Datacard_PTH_2023.root -t 1 --setParameters r_PTH_0p0_15p0=0,r_PTH_15p0_30p0=0,r_PTH_30p0_45p0=0,r_PTH_45p0_80p0=0,r_PTH_80p0_120p0=0,r_PTH_120p0_200p0=0,r_PTH_200p0_350p0=0,r_PTH_350p0_10000p0=0 --saveToys --freezeParameters MH -m 125.38   
        

# class GenerateSOnlyToys(law.Task):
#     variable = law.Parameter(default="", description="Variable to be used")
#     output_dir = law.Parameter(default = '', description="Path to the output directory")
#     year = law.Parameter(default='2022', description="Year")
    
#     batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
#     number_of_replicas = law.Parameter(default=10, description="Number of replicas to run. If empty, will run the standard workflow.")
    