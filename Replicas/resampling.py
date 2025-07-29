import numpy as np
import pandas as pd
import glob
import os
import json
import pyarrow.parquet as pq
from scipy.stats import poisson
import pyarrow as pa
import sys
import subprocess
import ROOT

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
        
# ====================
# CONFIG / ARGUMENTS
# ====================

# if len(sys.argv) != 4:
#     print(f"Usage: {sys.argv[0]} <replica_idx> <parquet_dir> <output_dir>")
#     sys.exit(1)

if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} <replica_idx> <parquet_dir> <cat_dict> <bonly_toy>")
    sys.exit(1)

replica_idx = int(sys.argv[1])
parquet_dir = sys.argv[2]
cat_dict_path = sys.argv[3]
bonly_toy = sys.argv[4]
# output_dir = sys.argv[3]

print(f"Replica index: {replica_idx}")
print(f"Parquet input dir: {parquet_dir}")
# print(f"Output base dir: {output_dir}")

# Import the category dictionary
with open(cat_dict_path) as pf:
    cat_dict = json.load(pf)

# Open up the b-only toy file and load the toy
bonly_file = ROOT.TFile.Open(bonly_toy)
bonly_file.cd("toys")
myData = ROOT.gDirectory.Get("toy_1")
# Get the variable 'CMS_hgg_mass' from the dataset
mass = myData.get().find("CMS_hgg_mass")
argset = ROOT.RooArgSet(mass)
channel = myData.get().find("CMS_channel")

# Extract CMS channel labels and indices
CMS_channel_dict = {}
for i in range(channel.numTypes()):
    channel.setIndex(i)
    CMS_channel_dict[channel.getLabel()] = i

# np.random.seed(1234)
# # Get the 'CMS_hgg_mass' variable from the reduced dataset
# x_axis_vorher = myData.get().find("CMS_hgg_mass")
# # Create a RooPlot frame with the desired range
# frame_vorher = x_axis_vorher.frame(ROOT.RooFit.Range(100, 180))
# # Plot the reduced dataset on the frame
# myData.plotOn(frame_vorher)
# # Create a TCanvas to draw the plot
# c_vorher = ROOT.TCanvas("myData_vorher", "CMS_hgg_mass Plot", 800, 600)
# # Draw the frame on the canvas
# frame_vorher.Draw()
# # Save the canvas to a PNG file
# c_vorher.SaveAs(f"./validation/myData_vorher.png")


# # Make sure base folder exists
# os.makedirs(output_dir, exist_ok=True)


# Load all Parquet files from the specified directory
parquet_files = glob.glob(os.path.join(parquet_dir, "*.parquet"))

## Read the sum of the weights from metadata without any systematic variation
sum_weight_central = 0.0
for i in range(len(parquet_files)):
    sum_weight_central += float(pq.read_table(parquet_files[i]).schema.metadata[b'sum_weight_central'])

# Extract the sum_genw_presel from the metadata of the Parquet files
# Inpossible to keep it after the "poissonian randomization"
# TODO: Can we always use the same, since in the end we only care about the best fit value?
sum_genw_beforesel = 0
for f in parquet_files:
    sum_genw_beforesel += float(pq.read_table(f).schema.metadata[b'sum_genw_presel'])

for cat in cat_dict:

    df = pd.concat((pd.read_parquet(f, filters=cat_dict[cat]["cat_filter"]) for f in parquet_files), ignore_index=True)

    negative_weights = df[df["weight"] < 0.0].to_numpy()
    if len(negative_weights) > 0:
        # Why the HELL are they there?
        print(f"Warning: Negative weights found in the dataset: {len(negative_weights)}")
    
    df = df[df["weight"] >= 0.0]

    df["weight_norm"] = df["weight"] / sum_weight_central
    ## Probability should be normalised to one
    df["prob"] = df["weight_norm"] / sum(df["weight_norm"])

    ## Compute the expected number of events
    ## This is scaled to the full Run3 lumi and the total production XS (=ggH+VBF+VH+ttH+bbH); Taken from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
    exp = sum(df["weight_norm"]) * 55.65 * 0.2270/100 * 1000 * 27.3 # 55.65

    ## Extract from a Poisson distribution the number of events for each replica
    exp_replicas = poisson.rvs(mu=exp, size=(1))

    ## Indeces corresponding to the events to pick up in each replica
    ## NB! replace MUST be True, otherwise the sampling is not independent anymore and it is no longer a Poisson process
    idx_replicas = [np.random.choice(np.array(df.index), replace=True, size=(exp_replicas[0]), p=df["prob"])]

    ## Extract the events for each replica
    replicas = [df.loc[idx_replicas[0]]]
    print(f"Replica {replica_idx} for category {cat} has {len(replicas[0])} events.")
    
    additional_mass_values = replicas[0]["mass"].to_list()
    additional_probability_values = replicas[0]["prob"].to_list()

    # expr = ROOT.RooFormulaVar("channel_select", "CMS_channel == %d" % CMS_channel_dict[cat], ROOT.RooArgList(channel))

    # reducedData_vorher = myData.reduce(expr)
    # # Get the 'CMS_hgg_mass' variable from the reduced dataset
    # x_axis_vorher = reducedData_vorher.get().find("CMS_hgg_mass")
    # # Create a RooPlot frame with the desired range
    # frame_vorher = x_axis_vorher.frame(ROOT.RooFit.Range(100, 180))
    # # Plot the reduced dataset on the frame
    # reducedData_vorher.plotOn(frame_vorher)
    # # Create a TCanvas to draw the plot
    # c_vorher = ROOT.TCanvas("c_vorher", "CMS_hgg_mass Plot", 800, 600)
    # # Draw the frame on the canvas
    # frame_vorher.Draw()
    # # Save the canvas to a PNG file
    # c_vorher.SaveAs(f"./validation/{cat}_vorher.png")

    for i, val in enumerate(additional_mass_values):
        channel.setIndex(CMS_channel_dict[cat])
        mass.setVal(val)
        myData.add(argset, additional_probability_values[i])
    
    

#     reducedData_nachher = myData.reduce(expr)
#     # Get the 'CMS_hgg_mass' variable from the reduced dataset
#     x_axis_nachher = reducedData_nachher.get().find("CMS_hgg_mass")
#     # Create a RooPlot frame with the desired range
#     frame_nachher = x_axis_nachher.frame(ROOT.RooFit.Range(100, 180))
#     # Plot the reduced dataset on the frame
#     reducedData_nachher.plotOn(frame_nachher)
#     # Create a TCanvas to draw the plot
#     c_nachher = ROOT.TCanvas("c_nachher", "CMS_hgg_mass Plot", 800, 600)
#     # Draw the frame on the canvas
#     frame_nachher.Draw()
#     # Save the canvas to a PNG file
#     c_nachher.SaveAs(f"./validation/{cat}_nachher.png")
    

# # Get the 'CMS_hgg_mass' variable from the reduced dataset
# x_axis_nachher = myData.get().find("CMS_hgg_mass")
# # Create a RooPlot frame with the desired range
# frame_nachher = x_axis_nachher.frame(ROOT.RooFit.Range(100, 180))
# # Plot the reduced dataset on the frame
# myData.plotOn(frame_nachher)
# # Create a TCanvas to draw the plot
# c_nachher = ROOT.TCanvas("myData_nachher", "CMS_hgg_mass Plot", 800, 600)
# # Draw the frame on the canvas
# frame_nachher.Draw()
# # Save the canvas to a PNG file
# c_nachher.SaveAs(f"./validation/myData_nachher.png")

# Open a new ROOT file for writing
output_file = ROOT.TFile("test.root", "RECREATE")

# Create a RooWorkspace (Combine expects datasets inside workspaces or directories)
output_file.mkdir("toys")
output_file.cd("toys")

# Now write the RooDataSet to the toys directory with the name 'toy_1'
myData.SetName("toy_1")   # Important: name must match what Combine expects
myData.Write()

# Close the file
output_file.Close()

print("Saved expanded RooDataSet to 'test.root' in directory 'toys' as 'toy_1'")



"""
# First get the index for your desired channel
channel_index = CMS_channel_dict["RECO_PTH_0p0_15p0_cat0"]

# Build a RooFormulaVar expression to select only that channel
expr = ROOT.RooFormulaVar("channel_select", "CMS_channel == %d" % channel_index, ROOT.RooArgList(channel))

# Get variable & argset
argset = ROOT.RooArgSet(mass)

new_mass_values = [120.5, 125.3, 127.8]

reducedData = myData.reduce(expr)
reducedData.Print()

# Add each new event
for val in new_mass_values:
    channel.setIndex(CMS_channel_dict["RECO_PTH_0p0_15p0_cat0"])
    mass.setVal(val)
    myData.add(argset)

reducedData = myData.reduce(expr)
reducedData.Print()

# Get the 'CMS_hgg_mass' variable from the reduced dataset
x_axis = reducedData.get().find("CMS_hgg_mass")

# Create a RooPlot frame with the desired range
frame = x_axis.frame(ROOT.RooFit.Range(100, 180))

# Plot the reduced dataset on the frame
reducedData.plotOn(frame)

# Create a TCanvas to draw the plot
c = ROOT.TCanvas("c", "CMS_hgg_mass Plot", 800, 600)

# Draw the frame on the canvas
frame.Draw()

# Save the canvas to a PNG file
c.SaveAs("nachher2.png")
"""