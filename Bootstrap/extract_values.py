import uproot
import os
import glob
import matplotlib.pyplot as plt
import mplhep as hep
import seaborn as sns
import ROOT
import pandas as pd
from scipy import stats
import numpy as np
from scipy.optimize import minimize
from scipy.stats import moment
import json
from itertools import combinations  

translation = {
    "r_PTH_0p0_15p0": r"$r_{p_{T}^{\gamma\gamma} \in [0,15) \text{ GeV}}$",
    "r_PTH_15p0_30p0": r"$r_{p_{T}^{\gamma\gamma} \in [15,30) \text{ GeV}}$",
    "r_PTH_30p0_45p0": r"$r_{p_{T}^{\gamma\gamma} \in [30,45) \text{ GeV}}$",
    "r_PTH_45p0_80p0": r"$r_{p_{T}^{\gamma\gamma} \in [45,80) \text{ GeV}}$",
    "r_PTH_80p0_120p0": r"$r_{p_{T}^{\gamma\gamma} \in [80,120) \text{ GeV}}$",
    "r_PTH_120p0_200p0": r"$r_{p_{T}^{\gamma\gamma} \in [120,200) \text{ GeV}}$",
    "r_PTH_200p0_350p0": r"$r_{p_{T}^{\gamma\gamma} \in [200,350) \text{ GeV}}$",
    "r_PTH_350p0_10000p0": r"$r_{p_{T}^{\gamma\gamma} \in [350,+\infty) \text{ GeV}}$",
    "r_YH_0p0_0p15": r"$r_{|y_{\gamma\gamma}| \in [0,0.15)}$",
    "r_YH_0p15_0p3": r"$r_{|y_{\gamma\gamma}| \in [0.15,0.3)}$",
    "r_YH_0p3_0p6": r"$r_{|y_{\gamma\gamma}| \in [0.3,0.6)}$",
    "r_YH_0p6_0p9": r"$r_{|y_{\gamma\gamma}| \in [0.6,0.9)}$",
    "r_YH_0p9_2p5": r"$r_{|y_{\gamma\gamma}| \in [0.9,2.5)}$",
    "r_NJ_0p0_1p0": r"$r_{N_{\text{Jets}} \in [0,1)}$",
    "r_NJ_1p0_2p0": r"$r_{N_{\text{Jets}} \in [1,2)}$",
    "r_NJ_2p0_3p0": r"$r_{N_{\text{Jets}} \in [2,3)}$",
    "r_NJ_3p0_100p0": r"$r_{N_{\text{Jets}} \in [3,+\infty)}$",
    "r_PTJ0_0p0_30p0": r"$r_{p_{T,j0}} (N_{\text{Jets}} = 0)$",
    "r_PTJ0_30p0_75p0": r"$r_{p_{T,j0} \in [30,75) \text{ GeV}}$",
    "r_PTJ0_75p0_120p0": r"$r_{p_{T,j0} \in [75,120) \text{ GeV}}$",
    "r_PTJ0_120p0_200p0": r"$r_{p_{T,j0} \in [120,200) \text{ GeV}}$",
    "r_PTJ0_200p0_10000p0": r"$r_{p_{T,j0} \in [200,+\infty) \text{ GeV}}$",
    "r_PTJ0_30p0_10000p0": r"$r_{p_{T,j0} \in [30,+\infty) \text{ GeV}}$"
}

bf_first_order = [1.00025688, 1.0305514, 1.04672141, 1.03037609, 1.03741104, 0.98694191, 1.01272421, 0.92261124]

def coefficients(_m1, _m2ii, _m3):
    # Eq 2.9: coefficient c
    c = -np.sign(_m3) * np.sqrt(2*_m2ii) * np.cos( (4*np.pi/3) + (1/3)*np.arctan( np.sqrt(8*_m2ii**3/_m3**2 - 1) ) )
    
    # c = 0
    
    # Eq 2.10: coefficient b
    b = np.sqrt(_m2ii - 2*c**2)   
    # Eq 2.11: coefficient a
    a = (_m1 - c)
        
    return a, b, c

def compute_rho_ij(_ci, _cj, _bi, _bj, _m2ij):
    if _ci==0 or _cj==0:
        return _m2ij / (_bi*_bj)
    else:
        return (1/(4*_ci*_cj)) * (np.sqrt((_bi*_bj)**2 + 8*_ci*_cj*(_m2ij)) - _bi*_bj)

def chi_vector(x_exp, x_obs, _a, _b, _c):
    if _c == 0:
        chi_exp = (x_exp - _a) / _b
        chi_obs = (x_obs - _a) / _b
    else:
        chi_exp = (np.sqrt(_b**2 - 4*(_a-x_exp)*_c) - _b) / (2*_c)
        chi_obs = (np.sqrt(_b**2 - 4*(_a-x_obs)*_c) - _b) / (2*_c)
    
    chi_diff = (chi_obs - chi_exp) # Chi_Obs is very small compared to chi_exp
    return chi_diff

def chi(x, pois_, poi_list_, rho, abc_values=None, first_order=False):
    chi_vector_ = []

    if first_order:
        for i, current_poi in enumerate(poi_list_):

            # Convert to numpy arrays for easier computation
            # r = np.array(pois_[current_poi])

            # 1. Mean values
            # mean = np.mean(r)
            # chi_vector_.append([mean - x[i]])
            
            chi_vector_.append([(bf_first_order[i] - x[i])])
    
    else:
        for i, current_poi in enumerate(poi_list_):

            # Convert to numpy arrays for easier computation
            r = np.array(pois_[current_poi])

            # 1. Mean values
            mean = np.mean(r)

            if abc_values is None:
                print("Provide abc_values")
                return None
            a, b, c = abc_values[current_poi]

            chi_vector_.append([chi_vector(x[i], mean, a, b, c)])

    chi_vector_ = np.array(chi_vector_).flatten()

    # print("chi_vector:", chi_vector_)
    
    if first_order:
        print("Ingredients: ", bf_first_order - x)
        print("chi2_vector: ", chi_vector_)
        print("chi2:", chi_vector_.T @ np.linalg.inv(rho) @ chi_vector_)

    return chi_vector_.T @ np.linalg.inv(rho) @ chi_vector_

def find_crossings(x_vals, y_vals, threshold=1.0):
    # Find where the difference changes sign
    signs = np.sign(y_vals - threshold)
    crossings = []
    for i in range(len(signs)-1):
        if signs[i] * signs[i+1] <= 0:  # Sign change detected
            # Linear interpolation
            x1, x2 = x_vals[i], x_vals[i+1]
            y1, y2 = y_vals[i], y_vals[i+1]
            if y1 != y2:  # Avoid division by zero
                x_cross = x1 + (x2-x1) * (threshold-y1)/(y2-y1)
                crossings.append(x_cross)
    return crossings

def extract_covariance_matrix(root_file_path, poi_list):
    # Open the ROOT file
    root_file = ROOT.TFile.Open(root_file_path, "READ")
    
    # Retrieve the correlation matrix histogram
    # h_correlation = root_file.Get("h_correlation")
    h_covariance = root_file.Get("h_covariance") # SIC! This is the covariance matrix, not the correlation matrix
    
    floatParsFinal = root_file.Get("floatParsFinal")
    # Extract parameter names and values
    params = {}
    for i in range(floatParsFinal.getSize()):
        param = floatParsFinal.at(i)  # Access the i-th parameter
        if isinstance(param, ROOT.RooRealVar):  # Ensure it's a RooRealVar
            params[param.GetName()] = param.getVal()
    floatParsFinal = params.keys()
    # print(floatParsFinal)

    if not h_covariance:
        print("Error: 'h_covariance' not found in the ROOT file.")
        return None

    # Get number of bins (parameters)
    n_params = h_covariance.GetNbinsX()
    
    # Extract correlation values into a NumPy array
    covariance_matrix = np.zeros((n_params, n_params))

    for i in range(1, n_params + 1):
        for j in range(1, n_params + 1):
            covariance_matrix[i-1, j-1] = h_covariance.GetBinContent(i, j)

    # Convert to Pandas DataFrame for easy plotting
    df_covariance = pd.DataFrame(covariance_matrix, index=floatParsFinal, columns=floatParsFinal)
    
    # Filter only the POI rows/columns
    df_filtered = df_covariance.loc[poi_list, poi_list]
        
    root_file.Close()
            
    return df_filtered

def plot_individual_correlation(x_vals, y_vals, x_name, y_name, rho, folder=""):
    # rho is here a number
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)
    plt.style.use(hep.style.CMS)
    _, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x_vals, y_vals)
    ax.set_xlabel(translation[x_name])
    ax.set_ylabel(translation[y_name])
    ax.text(0.1, 0.9, f"$\\rho = {rho:.3f}$", transform=ax.transAxes)
    plt.savefig(os.path.join(folder, f"{x_name}_vs_{y_name}.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(folder, f"{x_name}_vs_{y_name}.png"), bbox_inches='tight')
    # plt.show()

def plot_covariance_matrix(rho, poi_list, folder="", title="Covariance Matrix", output_name="covariance_matrix.png"):
    # rho is here a matrix
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)
        
    plt.style.use(hep.style.CMS)
    _, ax = plt.subplots(figsize=(10, 6))
    
    labels = [translation[poi] for poi in poi_list]
    
    # Create heatmap
    sns.heatmap(
        rho, 
        annot=True, 
        fmt=".2f", 
        cmap="coolwarm", 
        xticklabels=labels, 
        yticklabels=labels, 
        cbar=True, 
        linewidths=0.5, 
        annot_kws={"size": 18},  # Adjust font size of annotations
        ax=ax
    )

    ax.set_title(title, fontsize=20)

    # Save plot if folder is specified
    if folder:
        file_path = os.path.join(folder, output_name)
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
    
    plt.show()

def produce_rho(pois_, poi_list_):

    # Covariance matrix
    cov_matrix = np.cov([pois_[r] for r in poi_list_])

    print("\nCovariance matrix:")
    print(cov_matrix)
    
    abc_values = {}
    
    rho = []

    # Loop through all POIs
    for i, current_poi in enumerate(poi_list_):

        # Convert to numpy arrays for easier computation
        r = np.array(pois_[current_poi])

        # 1. Mean values
        mean = np.mean(r)

        # Diagonal components of the third moment
        # Computing E[(X - μ)³]
        third_moment = np.mean((r - mean)**3)

        a, b, c = coefficients(mean, cov_matrix[i,i], third_moment)
        
        abc_values[current_poi] = [a, b, c]

        # Print results
        print("\nMean values:")
        print(f"{current_poi}: {mean:.3f}")

        print("\nDiagonal components of third moment:")
        print(f"{current_poi}: {third_moment:.3f}")

    for i, current_poi in enumerate(poi_list_):
        reihe_i = []
        for j, other_poi in enumerate(poi_list_):
            reihe_i.append(compute_rho_ij(abc_values[current_poi][2], abc_values[other_poi][2], abc_values[current_poi][1], abc_values[other_poi][1], cov_matrix[i,j]))
        rho.append(reihe_i)
    
    print("rho", rho)

    return rho, abc_values

def correlation_to_covariance(corr_matrix, std_devs):
    """
    Converts a correlation matrix to a covariance matrix.
    
    Parameters:
    corr_matrix (numpy.ndarray): Correlation matrix
    std_devs (numpy.ndarray): Standard deviations of variables
    
    Returns:
    numpy.ndarray: Covariance matrix
    """
    # outer_std_dev = np.outer(std_devs, std_devs) # Outer product of standard deviations
    # print("outer_std_dev: ", outer_std_dev)
    # covariance_matrix = corr_matrix * outer_std_dev  # Element-wise multiplication
    covariance_matrix = std_devs.T * corr_matrix * std_devs  # Element-wise multiplication
    
    return covariance_matrix

def produce_and_minimize_chi(pois_, poi_list_, first_order=False):
    
    if first_order:
        rho = extract_covariance_matrix('/t3home/niharrin/devel/pnfs/ntuples/midRun3/samples/January/2025_01_20_intermediateNTuples_2023/finalfits/PTH/Combine/runFits_PTH/hesse/robustHessefirstStep.root', poi_list_)
        
        # print(np.linalg.inv(rho))
        # _, abc_values = produce_rho(pois_, poi_list_)
        
        # x0 = np.array([1. for i in range(len(poi_list_))])
        x0 = np.array([bf_first_order[i] for i in range(len(poi_list_))])
        # x0 = np.array(bf_first_order)
        abc_values = None
        # first_order = False
        res = minimize(chi, x0, args=(pois_, poi_list_, rho, abc_values, first_order))
        
        print("res.x", res.x)
        
    else:
        rho, abc_values = produce_rho(pois_, poi_list_)

        # rho = correlation_to_covariance(np.array(rho), np.sqrt(np.diag(np.cov([pois_[r] for r in poi_list_]))))

        x0 = np.array([1. for i in range(len(poi_list_))])
        res = minimize(chi, x0, args=(pois_, poi_list_, rho, abc_values, first_order))
        
        # print(res.x)
    
    # Get optimal values from minimization
    optimal_values = res.x
    
    x0_ranges = []
    chi_x0_scans = []
    optimal_values_list = []
    
    for i, current_poi in enumerate(poi_list_):
        print(f"{current_poi}: {optimal_values[i]:.3f}")

        # Create a grid of points
        x0_range = np.linspace(-1, 3, 100)  # Adjust range as needed
        
        opt_value_with_fixed_rest = optimal_values.copy()
        
        # for opt_value in opt_value_with_fixed_rest:
        #     print("Chi2 evaluated at: ", opt_value)
        #     print(float(chi(opt_value, pois_, poi_list_, rho, abc_values, first_order=True)))

        chi_x0_scan = []
        for x0 in x0_range:
            for j in range(len(poi_list_)):
                if j!=i:
                    opt_value_with_fixed_rest[j] = bf_first_order[j]
                if j == i:
                    opt_value_with_fixed_rest[j] = x0
            if first_order:
                print("opt_value_with_fixed_rest", opt_value_with_fixed_rest)
                chi_x0_scan.append(float(chi(opt_value_with_fixed_rest, pois_, poi_list_, rho, abc_values, first_order=True)))
            else:
                chi_x0_scan.append(float(chi(opt_value_with_fixed_rest, pois_, poi_list_, rho, abc_values, first_order=False)))
        
        chi_x0_scan = np.array(chi_x0_scan)

        # Find crossing points at for 68% interval 
        crossings_x0 = find_crossings(x0_range, chi_x0_scan)
        print('crossings_x0', crossings_x0-optimal_values[i])
        
        x0_ranges.append(x0_range)
        chi_x0_scans.append(chi_x0_scan)
        optimal_values_list.append(optimal_values[i])
    
    return x0_ranges, chi_x0_scans, optimal_values_list

def produce_LLPlots(pois_, poi_list_, combineLL_dir_, folder="", print_first_order=False):
    
    x0_ranges, chi_x0_scans, optimal_values = produce_and_minimize_chi(pois_, poi_list_)
    if print_first_order:
        x0_ranges_fo, chi_x0_scans_fo, optimal_values_fo = produce_and_minimize_chi(pois_, poi_list_, first_order=True)
    
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)

    
    cov_matrix = np.cov([pois_[r] for r in poi_list_])
    
    for i, current_poi in enumerate(poi_list_):
        
        # Check if condition is satisfied
        mean = np.mean(pois_[current_poi])
        variance = cov_matrix[i,i]
        third_moment = np.mean((pois_[current_poi] - mean)**3)
        
        condition = (8*variance**3 >= third_moment**2)
        print(f"Condition for {current_poi}: {condition}")
        if not condition:
            print(f"Skipping {current_poi} as condition is not satisfied")
            continue
    
        # Create plots
        plt.style.use(hep.style.CMS)
        _, ax1 = plt.subplots(1, 1, figsize=(12, 8))

        # Plot x0 scan
        ax1.plot(x0_ranges[i], chi_x0_scans[i], label='Simplified likelihood (ABC)')
        ax1.axvline(optimal_values[i], color='grey', linestyle='--', label=f'Minimum: {optimal_values[i]:.3f}')
        # print("Simplified likelihood (ABC): ", chi_x0_scans[i])
        if print_first_order:
            ax1.plot(x0_ranges_fo[i], chi_x0_scans_fo[i], label='Simplified likelihood (Hesse)')
            # ax1.axvline(optimal_values_fo[i], color='grey', linestyle='--', label=f'Minimum: {optimal_values_fo[i]:.3f}')
            # print(chi_x0_scans_fo[i])
        with uproot.open(os.path.join(combineLL_dir_, "scans", f"scan_{current_poi}.root")) as file:
            # Get the TGraphs - note that uproot reads them as pairs of arrays
            graph = file[f"scan_{current_poi};1"]  # Replace with your TGraph name
            # Extract x and y values
            x0_points = graph.member("fX")  # Gets x values
            y0_points = graph.member("fY")  # Gets y values
        ax1.plot(x0_points, y0_points, 'r--', label='Combine likelihood')
        ax1.set_xlabel(translation[current_poi])
        ax1.set_ylabel('2ΔNLL')
        ax1.grid(True)
        # ax1.set_ylim(0, max(y0_points))
        ax1.legend()
        
        ax1.set_ylim(0, 10)
        ax1.set_xlim(-1, 3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(folder, f"chi_scan_{current_poi}.pdf"))
        plt.savefig(os.path.join(folder, f"chi_scan_{current_poi}.png"))
    
    rho, _ = produce_rho(pois_, poi_list_)
    plot_covariance_matrix(rho, poi_list_, folder=folder, title="Covariance Matrix (Simplified Likelihood)", output_name="covariance_matrix_sl.png")
    
    covariance_df = extract_covariance_matrix('/t3home/niharrin/devel/pnfs/ntuples/midRun3/samples/January/2025_01_20_intermediateNTuples_2023/finalfits/PTH/Combine/runFits_PTH/hesse/robustHessefirstStep.root', poi_list)
    plot_covariance_matrix(covariance_df, poi_list_, folder=folder, title="Covariance Matrix (Hessian)", output_name="covariance_matrix_hesse.png")
    
def create_poiJson(base_dir, poi_list):
    pois = {}

    for current_poi in poi_list:
        
        pois[current_poi] = []
        
        print(f"Processing {current_poi}")

        for i in range(len(glob.glob(os.path.join(base_dir, "toy_*")))):
            
            if i%100==0:
                print(f"Processing fit_{i}")
            
            seed = 123456 + i
            
            try:
                current_root_files = uproot.open(f"{base_dir}/toy_{i}/higgsCombineToyBestFit_{current_poi}.MultiDimFit.mH125.38.{seed}.root")
            except:
                print(f"Skipping fit_{i}: Required scan files not found")
                continue

            current_tree = current_root_files["limit"]
            
            current_limit_values = current_tree[current_poi].array()
            
            try:
                if current_limit_values[0]<-4:
                    print(current_limit_values[0])
                    print(i)
            except:
                print("Empty ROOT file for bootstrap: ", i)
                continue

            pois[current_poi].append(current_limit_values[0])
    return pois

# Define the base directory path
# base_dir = "/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/January/2025_01_20_intermediateNTuples_2023/finalfits/PTH_bootstrap/Combine/runFits_PTH/dataFit"

base_dir = "/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/January/2025_01_20_intermediateNTuples_2023/finalfits/PTH/Combine/runFits_PTH/toyFit"
combineLL_dir = "/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/January/2025_01_20_intermediateNTuples_2023/finalfits/PTH/Combine/runFits_PTH/asimov"

poi_list = ["r_PTH_0p0_15p0", "r_PTH_15p0_30p0", "r_PTH_30p0_45p0", "r_PTH_45p0_80p0", "r_PTH_80p0_120p0", "r_PTH_120p0_200p0", "r_PTH_200p0_350p0", "r_PTH_350p0_10000p0"]
# poi_list = ["r_PTH_15p0_30p0", "r_PTH_30p0_45p0"]
# poi_list = ["r_PTH_0p0_15p0", "r_PTH_15p0_30p0", "r_PTH_30p0_45p0"]

# Loop through all fit directories (fit_0, fit_1, etc.)
# for i in range(len(glob.glob(os.path.join(base_dir, "bootstrap_*")))):
        
if not os.path.exists('pois.json'):
    pois = create_poiJson(base_dir, poi_list)
    # Save the POIs to a JSON file
    with open('pois.json', 'w') as f:
        json.dump(pois, f)
else:
    # Load the POIs from the JSON file
    with open('pois.json', 'r') as f:
        pois = json.load(f)
    
unique_pairings = list(combinations(poi_list, 2))

for current_tuple in unique_pairings:
    r_1, r_2 = current_tuple
    
    plot_individual_correlation(pois[r_1], pois[r_2], r_1, r_2, np.corrcoef(pois[r_1], pois[r_2])[0,1], folder="Plots/PTH")
    
produce_LLPlots(pois, poi_list, combineLL_dir, folder="Plots/PTH/SL", print_first_order=True)


 