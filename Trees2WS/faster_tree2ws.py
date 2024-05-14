import os
import subprocess
from multiprocessing import Pool
import glob
import time

# Define an array of input masses
input_masses = [120, 125, 130]

# Define an array of eras
eras = ["preEE", "postEE"]

# Define an array of production modes and corresponding process strings
production_modes = [
    ("ggh", "GluGluHtoGG"),
    ("vbf", "VBFHtoGG"),
    ("vh", "VHtoGG"),
    ("tth", "ttHtoGG")
]

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != os.errno.EEXIST:
            raise

# Function to run the command
def run_process(args):
    mass, era, mode, process, variable, path_to_root_files = args
    output_dir = "../input_output_{}_2022{}".format(variable, era)
    safe_mkdir(output_dir)  # Create output directory if it doesn't exist
    
    # Construct the command as a single string
    cmd = "python trees2ws.py --inputMass {mass} --productionMode {mode} --year 2022{era} --doSystematics --doDiffSplitting --inputConfig config/config_2022_{variable}.py --inputTreeFile '{path_to_root_files}/{process}_M-{mass}_{era}/'*.root --outputWSDir {output_dir}".format(
        mass=mass, mode=mode, era=era, variable=variable, path_to_root_files=path_to_root_files, process=process, output_dir=output_dir)

    with open(os.devnull, 'wb') as devnull:
        subprocess.call(cmd, shell=True, stdout=devnull, stderr=devnull)
    print("Process for variable {}, mass {}, era {}, and mode {} completed.".format(variable, mass, era, mode))

# Main function to parallelize tasks
def main(variable, path_to_root_files):
    
    num_workers = 24 # masses x 2 eras x 4 production modes = 24
    pool = Pool(processes=num_workers)
    tasks = [
        (mass, era, mode, process, variable, path_to_root_files)
        for mode, process in production_modes
        for era in eras
        for mass in input_masses
    ]
    
    # Lets benchmark the time:
    start_time = time.time()  

    pool.map(run_process, tasks)

    end_time = time.time()  

    # Calculate and print the duration
    duration = end_time - start_time
    print("Process {:.2f} seconds.".format(duration))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: <script.py> <variable> <path_to_root_files>")
        sys.exit(1)
    
    variable = sys.argv[1]
    path_to_root_files = sys.argv[2]
    main(variable, path_to_root_files)
