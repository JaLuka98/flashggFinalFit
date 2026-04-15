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
    number_of_replicas = law.Parameter(default=1000, description="Number of replicas")

    toy_flag = law.Parameter(default=False, description="Toy flag")
    seed = law.Parameter(default=123456, description="Seed for the replica generation")

    batch_flavor = law.Parameter(default="htcondor", description="Batch system to use")

    _class_cache = {}

    def _init_once(self):
        key = (self.year, self.variable, self.output_dir)
        if key in self._class_cache:
            (
                self.configYamlPath,
                self.config,
                self.resolved_output_dir,
                self.fitFolderName,
                self.bkgConfig
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

        input_path = config['inputFiles']['Trees2WSData']

        bkgConfig = config["backgroundScriptCfg"]
        if bkgConfig['cats'] == 'auto':
            bkgConfig['cats'] = (extractListOfCatsFromHiggsDNAAllData(input_path))

        self.bkgConfig = bkgConfig

        # store in class-level cache
        self._class_cache[key] = (configYamlPath, config, resolved_output_dir, fitFolderName, bkgConfig)

    # def requires(self):
    def workflow_requires(self):
        workflow_reqs = super().workflow_requires()

        self._init_once()

        tasks = {}

        if workflow_reqs:
            tasks.update(workflow_reqs)

        config = self.config["backgroundScriptCfg"]

        tasks["Trees2WSData"] = Trees2WSData(output_dir=self.resolved_output_dir, variable=self.variable, year=self.year, version=self.variable+"_"+self.year if self.variable != "" else "inclusive", workflow=config['execution'], batch_flavor=self.batch_flavor, slurm_partition=config['batchPartition'], slurm_memory=config['batchMemory'], slurm_max_runtime=config['batchMaxRuntime'], htcondor_partition=config['batchPartition'], htcondor_memory=config['batchMemory'], htcondor_max_runtime=config['batchMaxRuntime'], bootstrap_flag=self.bootstrap_flag, number_of_replicas=self.number_of_replicas, toy_flag=self.toy_flag, seed=self.seed)

        return tasks

    def create_branch_map(self):

        self._init_once()

        config = self.bkgConfig

        nCats = len(config['cats'].split(","))
              
        cat_list = [
            (config['cats'].split(",")[categoryIndex], str(int(config['catOffset'])+categoryIndex))
            for categoryIndex in range(nCats)
        ]
        if (convert_boolean_string(self.bootstrap_flag) == True) or (convert_boolean_string(self.toy_flag) == True):
            branch_map = {
                i: replica_index
                for i, replica_index in enumerate(range(int(self.number_of_replicas)))
            }
        else:
            branch_map = {i: cat_catOffset for i, cat_catOffset in enumerate(cat_list)}
        return branch_map

    def output(self):

        self._init_once()

        config = self.bkgConfig

        if (convert_boolean_string(self.bootstrap_flag) == True) or (convert_boolean_string(self.toy_flag) == True):
            replica_index = self.branch_data
            outdir_ext = os.path.join(self.resolved_output_dir, 'Background', f'outdir_{config["ext"]}_{replica_index}')
        else:
            cat, cat_offset = self.branch_data
            outdir_ext = os.path.join(self.resolved_output_dir, 'Background', f'outdir_{config["ext"]}')

        outputFileTargets = []

        if convert_boolean_string(self.bootstrap_flag) == False:
            if convert_boolean_string(self.toy_flag) == False:
                bkg_plots = glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.png'))
                bkg_plots += glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.pdf'))
                bkg_plots += glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.pdf_gofTest.pdf'))

                output_paths = [os.path.join(outdir_ext, f'CMS-HGG_multipdf_{cat}.root'), os.path.join(outdir_ext, f'bkgfTest-Data/multipdf_{cat}.pdf'), os.path.join(outdir_ext, f'bkgfTest-Data/multipdf_{cat}.png')]

                output_paths += bkg_plots
            else:
                # Process everything for each toy using one node to avoid overloading the SLURM schedd
                bkg_plots = []
                output_paths = []
                config = self.bkgConfig

                nCats = len(config['cats'].split(","))

                cat_list = [
                    (config['cats'].split(",")[categoryIndex], str(int(config['catOffset'])+categoryIndex))
                    for categoryIndex in range(nCats)
                ]

                for cat_cat_offset in cat_list:
                    cat, cat_offset = cat_cat_offset
                    bkg_plots += glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.png'))
                    bkg_plots += glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.pdf'))
                    bkg_plots += glob.glob(os.path.join(outdir_ext, f'bkgfTest-Data/*_cat{cat_offset}.pdf_gofTest.pdf'))

                    output_paths.append(os.path.join(outdir_ext, f'CMS-HGG_multipdf_{cat}.root'))
                    output_paths.append(os.path.join(outdir_ext, f'bkgfTest-Data/multipdf_{cat}.pdf'))
                    output_paths.append(os.path.join(outdir_ext, f'bkgfTest-Data/multipdf_{cat}.png'))

                output_paths += bkg_plots

        else: # Skip the plots for the bootstrap case
                # Process everything for each toy using one node to avoid overloading the SLURM schedd
                bkg_plots = []
                output_paths = []
                config = self.bkgConfig

                nCats = len(config['cats'].split(","))

                cat_list = [
                    (config['cats'].split(",")[categoryIndex], str(int(config['catOffset'])+categoryIndex))
                    for categoryIndex in range(nCats)
                ]

                for cat_cat_offset in cat_list:
                    cat, cat_offset = cat_cat_offset
                    output_paths.append(os.path.join(outdir_ext, f'CMS-HGG_multipdf_{cat}.root'))
                    output_paths.append(os.path.join(outdir_ext, 'bkgfTest-Data', f'multipdf_{cat}.png'))
                    output_paths.append(os.path.join(outdir_ext, 'bkgfTest-Data', f'multipdf_{cat}.pdf'))

        for _, current_output_path in enumerate(output_paths):
            outputFileTargets.append(law.LocalFileTarget(current_output_path))

        return outputFileTargets

    def run(self):

        self._init_once()

        config = self.bkgConfig
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
            if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                all_data_input_path = os.path.join(self.resolved_output_dir, "input_output_data", f"input_output_data_{self.year}/ws/allData.root")
            else:
                all_data_input_path = os.path.join(self.resolved_output_dir, "input_output_data", f"input_output_data_{self.year}")
        else:
            if (convert_boolean_string(self.bootstrap_flag) == False) and (convert_boolean_string(self.toy_flag) == False):
                all_data_input_path = os.path.join(self.resolved_output_dir, "input_output_data", f"input_output_data_{self.variable}_{self.year}/ws/allData.root")
            else:
                all_data_input_path = os.path.join(self.resolved_output_dir, "input_output_data", f"input_output_data_{self.variable}_{self.year}")

        if (convert_boolean_string(self.bootstrap_flag) == True) or (convert_boolean_string(self.toy_flag) == True):
            replica_index = self.branch_data
            # In this case self.input_path is self.output_path/input_output_data_{self.year}
            # Have to add the _{replica_index}/ws/allData.root to the path manually, since we need the bootstrap index
            input_path = os.path.join(all_data_input_path+f"_{replica_index}", "ws/allData.root")
        else:
            cat, cat_offset = self.branch_data
            input_path = all_data_input_path

        if self.batch_flavor == "slurm/psi":
            # Have to use /scratch/batch_username/ for slurm/psi
            os.environ["TARGET_PATH"] = f"/scratch/{os.environ['USER']}/{os.environ['SLURM_JOB_ID']}"
            temp_output_dir = os.environ["TARGET_PATH"]
            execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Background'], shell=True)
            if (convert_boolean_string(self.bootstrap_flag) == True) or (convert_boolean_string(self.toy_flag) == True):
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Background/outdir_{config["ext"]}_{replica_index}'], shell=True)
            else:
                execute_command([f'xrdfs root://t3dcachedb03.psi.ch:1094/ mkdir -p {self.resolved_output_dir}/Background/outdir_{config["ext"]}'], shell=True)
            safe_mkdir(temp_output_dir)
        else:
            safe_mkdir(self.resolved_output_dir)
            safe_mkdir(os.path.join(self.resolved_output_dir, "Background"))
            safe_mkdir(os.path.join(self.resolved_output_dir, "Background", f"outdir_{config['ext']}"))
            temp_output_dir = os.path.join(self.resolved_output_dir, "Background")

        if temp_output_dir[-1] != "/":
            temp_output_dir += "/"

        script_path = os.path.join(os.environ["ANALYSIS_PATH"], "Background/runBackgroundScripts.sh")

        if (convert_boolean_string(self.toy_flag) == False) & (convert_boolean_string(self.bootstrap_flag) == False):
            arguments = [
                "-i", input_path,
                "-p", "none",
                "-f", cat,
                "--outputFolder", f"{temp_output_dir}",
                "--catOffset", cat_offset,
                "--intLumi", f"{lumiMap[self.year]}",
                "--year", f"{self.year}",
                "--batch", "local",
                "--queue", "microcentury",
                "--sigFile", "none",
                "--isData",
                "--fTest"
            ]
            arguments += ["--ext", f'{config["ext"]}']
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
        else:
            config = self.bkgConfig

            nCats = len(config['cats'].split(","))

            cat_list = [
                (config['cats'].split(",")[categoryIndex], str(int(config['catOffset'])+categoryIndex))
                for categoryIndex in range(nCats)
            ]

            for cat_cat_offset in cat_list:
                cat, cat_offset = cat_cat_offset

                arguments = [
                    "-i", input_path,
                    "-p", "none",
                    "-f", cat,
                    "--outputFolder", f"{temp_output_dir}",
                    "--catOffset", cat_offset,
                    "--intLumi", f"{lumiMap[self.year]}",
                    "--year", f"{self.year}",
                    "--batch", "local",
                    "--queue", "microcentury",
                    "--sigFile", "none",
                    "--isData",
                    "--fTest"
                ]
                if (convert_boolean_string(self.bootstrap_flag) == True) or (convert_boolean_string(self.toy_flag) == True):
                    arguments += ["--ext", f'{config["ext"]}_{replica_index}']
                else:
                    arguments += ["--ext", f'{config["ext"]}']
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
            if (convert_boolean_string(self.bootstrap_flag) == True) or (convert_boolean_string(self.toy_flag) == True):
                bkg_folder = f"outdir_{config['ext']}_{replica_index}"
            else:
                bkg_folder = f"outdir_{config['ext']}"
            execute_command([f"ls -al {temp_output_dir}/*"], shell=True)
            if "/work" in self.resolved_output_dir:
                slurm_copy_command = [
                    'cp', '-rf',
                    f'{temp_output_dir}/{bkg_folder}',
                     f'{self.resolved_output_dir}/Background/'
                ]
            else:
                # Copying output files to final destination on the /pnfs.
                slurm_copy_command = [
                    'xrdcp', '-rf',
                    f'{temp_output_dir}/{bkg_folder}',
                    'root://t3dcachedb03.psi.ch:1094//'+ f'{self.resolved_output_dir}/Background/'
                ]
            execute_command(slurm_copy_command)
            # Cleaning up scratch space.
            shutil.rmtree(temp_output_dir)
