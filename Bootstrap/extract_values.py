import uproot
import os
import glob
import matplotlib.pyplot as plt
import mplhep as hep
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

def coefficients(_m1, _m2ii, _m3):
    # Eq 2.9: coefficient a
    c = -np.sign(_m3) * np.sqrt(2*_m2ii) * np.cos( (4*np.pi/3) + (1/3)*np.arctan( np.sqrt(8*_m2ii**3/_m3**2 - 1) ) )
    
    # Eq 2.10: coefficient b
    b = np.sqrt(_m2ii - 2*c**2)
    
    # Eq 2.11: coefficient c
    a = _m1 - c
        
    return a, b, c

def compute_rho_ij(_ci, _cj, _bi, _bj, _m2ij):
    return (1/(4*_ci*_cj)) * (np.sqrt((_bi*_bj)**2 + 8*_ci*_cj*_m2ij) - _bi*_bj)

def chi_vector(x_exp, x_obs, _a, _b, _c):
    chi_exp = (np.sqrt(_b**2 - 4*(_a-x_exp)*_c) - _b) / (2*_c)
    chi_obs = (np.sqrt(_b**2 - 4*(_a-x_obs)*_c) - _b) / (2*_c)
    
    chi_diff = chi_obs - chi_exp
    return chi_diff

# def chi(x, _a_high, _b_high, _c_high, _a_low, _b_low, _c_low, _rho):
#     chi_high = (np.sqrt(_b_high**2 - 4*(_a_high-x[0])*_c_high) - _b_high) / (2*_c_high)
#     chi_low = (np.sqrt(_b_low**2 - 4*(_a_low-x[1])*_c_low) - _b_low) / (2*_c_low)

#     chi_high_meas = (np.sqrt(_b_high**2 - 4*(_a_high-1.821)*_c_high) - _b_high) / (2*_c_high)
#     chi_low_meas = (np.sqrt(_b_low**2 - 4*(_a_low-0.803)*_c_low) - _b_low) / (2*_c_low)

#     chi_vector = np.array([[chi_high_meas - chi_high],
#                            [chi_low_meas - chi_low]])
#     return chi_vector.T @ _rho @ chi_vector

def chi(x, pois_, poi_list_, rho, abc_values):
    chi_vector_ = []
    
    for i, current_poi in enumerate(poi_list_):

        # Convert to numpy arrays for easier computation
        r = np.array(pois_[current_poi])

        # 1. Mean values
        mean = np.mean(r)
        
        a, b, c = abc_values[current_poi]
        
        chi_vector_.append([chi_vector(x[i], mean, a, b, c)])
    
    chi_vector_ = np.array(chi_vector_).flatten()
    
    return chi_vector_.T @ rho @ chi_vector_

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

def plot_correlation(x_vals, y_vals, x_name, y_name, rho, folder=""):
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

def produce_rho(pois_, poi_list_, folder=""):

    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)

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

    return rho, abc_values

def produce_and_minimize_chi(pois_, poi_list_, folder=""):
    
    rho, abc_values = produce_rho(pois_, poi_list_, folder="Plots/PTH/SL")
    
    x0 = np.array([1. for i in range(len(poi_list_))])
    res = minimize(chi, x0, args=(pois_, poi_list_, rho, abc_values))
    
    print(res.x)
    
    # Get optimal values from minimization
    optimal_values = res.x
    
    x0_ranges = []
    chi_x0_scans = []
    optimal_values_list = []
    
    for i, current_poi in enumerate(poi_list_):
        print(f"{current_poi}: {optimal_values[i]:.3f}")

        # Create a grid of points
        x0_range = np.linspace(-10, 10, 100)  # Adjust range as needed
        
        opt_value_with_fixed_rest = optimal_values.copy()

        chi_x0_scan = []
        for x0 in x0_range:
            for j in range(len(poi_list_)):
                if j!=i:
                    opt_value_with_fixed_rest[j] = x0
            chi_x0_scan.append(float(chi(opt_value_with_fixed_rest, pois_, poi_list_, rho, abc_values)))
        
        
        chi_x0_scan = np.array(chi_x0_scan)
        
        # Calculate chi values for x0 scan (keeping x1 fixed at optimal value)
        # chi_x0_scan = np.array([float(chi(np.array([x0, optimal_x1]), 
        #                         a_x, b_x, c_x, 
        #                         a_y, b_y, c_y, 
        #                         rho_x_y)) for x0 in x0_0_range])

        print(chi_x0_scan)
        # Find crossing points at for 68% interval 
        crossings_x0 = find_crossings(x0_range, chi_x0_scan)
        print('crossings_x0', crossings_x0-optimal_values[i])
        
        x0_ranges.append(x0_range)
        chi_x0_scans.append(chi_x0_scan)
        optimal_values_list.append(optimal_values[i])
    
    return x0_ranges, chi_x0_scans, optimal_values_list

def produce_LLPlots(pois_, poi_list_, folder=""):
    
    x0_ranges, chi_x0_scans, optimal_values = produce_and_minimize_chi(pois_, poi_list_, folder)
    
    for i, current_poi in enumerate(poi_list_):
    
        # Create plots
        plt.style.use(hep.style.CMS)
        fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))

        # Plot x0 scan
        ax1.plot(x0_ranges[i], chi_x0_scans[i], label='Simplified likelihood')
        # with uproot.open("scan_ggH_x.root") as file:
        #     # Get the TGraphs - note that uproot reads them as pairs of arrays
        #     graph = file["scan_ggH_x"]  # Replace with your TGraph name
        #     # Extract x and y values
        #     x0_points = graph.member("fX")  # Gets x values
        #     y0_points = graph.member("fY")  # Gets y values
        # ax1.plot(x0_points, y0_points, 'r--', label='Combine likelihood')
        ax1.set_xlabel(translation[current_poi])
        ax1.set_ylabel('2ΔNLL')
        ax1.grid(True)
        # ax1.set_ylim(0, max(y0_points))
        ax1.axvline(optimal_values[i], color='grey', linestyle='--', label=f'Minimum: {optimal_values[i]:.3f}')
        ax1.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(folder, f"chi_scan_{current_poi}.pdf"))
        plt.savefig(os.path.join(folder, f"chi_scan_{current_poi}.png"))

def produce_simplifiedLL(x_vals, y_vals, x_name, y_name, folder=""):
    
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)

    # Convert to numpy arrays for easier computation
    r_x = np.array(x_vals)
    r_y = np.array(y_vals)

    # 1. Mean values
    mean_x = np.mean(r_x)
    mean_y = np.mean(r_y)

    # 2. Covariance matrix
    cov_matrix = np.cov((r_x, r_y))

    # 3. Diagonal components of the third moment
    # Computing E[(X - μ)³]
    third_moment_x = np.mean((r_x - mean_x)**3)
    third_moment_y = np.mean((r_y - mean_y)**3)

    a_x, b_x, c_x = coefficients(mean_x, cov_matrix[0,0], third_moment_x)
    a_y, b_y, c_y = coefficients(mean_y, cov_matrix[1,1], third_moment_y)

    rho_x_y = rho(c_x, c_y, b_x, b_y, cov_matrix[0,1], cov_matrix[0,0], cov_matrix[1,1])

    x0 = np.array([1., 1.])
    res = minimize(chi, x0, args=(a_x, b_x, c_x, a_y, b_y, c_y, rho_x_y))

    # Get optimal values from minimization
    optimal_x0, optimal_x1 = res.x

    # Create a grid of points
    x0_0_range = np.linspace(-10, 10, 100)  # Adjust range as needed
    x0_1_range = np.linspace(-10, 10, 100)  # Adjust range as needed

    # Calculate chi values for x0 scan (keeping x1 fixed at optimal value)
    chi_x0_scan = np.array([float(chi(np.array([x0, optimal_x1]), 
                            a_x, b_x, c_x, 
                            a_y, b_y, c_y, 
                            rho_x_y)) for x0 in x0_0_range])
    # Calculate chi values for x1 scan (keeping x0 fixed at optimal value)
    chi_x1_scan = np.array([float(chi(np.array([optimal_x0, x1]), 
                            a_x, b_x, c_x, 
                            a_y, b_y, c_y, 
                            rho_x_y)) for x1 in x0_1_range])

    print(chi_x0_scan)
    # Find crossing points at for 68% interval 
    crossings_x0 = find_crossings(x0_0_range, chi_x0_scan)
    crossings_x1 = find_crossings(x0_1_range, chi_x1_scan)
    print('crossings_x0', crossings_x0-optimal_x0)
    print('crossings_x1', crossings_x1-optimal_x1)

    # Create plots
    plt.style.use(hep.style.CMS)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Plot x0 scan
    ax1.plot(x0_0_range, chi_x0_scan, label='Simplified likelihood')
    # with uproot.open("scan_ggH_x.root") as file:
    #     # Get the TGraphs - note that uproot reads them as pairs of arrays
    #     graph = file["scan_ggH_x"]  # Replace with your TGraph name
    #     # Extract x and y values
    #     x0_points = graph.member("fX")  # Gets x values
    #     y0_points = graph.member("fY")  # Gets y values
    # ax1.plot(x0_points, y0_points, 'r--', label='Combine likelihood')
    ax1.set_xlabel(translation[x_name])
    ax1.set_ylabel('2ΔNLL')
    ax1.grid(True)
    # ax1.set_ylim(0, max(y0_points))
    ax1.axvline(optimal_x0, color='grey', linestyle='--', label=f'Minimum: {optimal_x0:.3f}')
    ax1.legend()

    # Plot x1 scan
    ax2.plot(x0_1_range, chi_x1_scan, label='Simplified likelihood')
    # with uproot.open("scan_ggH_y.root") as file:
    #     # Get the TGraphs - note that uproot reads them as pairs of arrays
    #     graph = file["scan_ggH_y"]  # Replace with your TGraph name
    #     # Extract x and y values
    #     x0_points = graph.member("fX")  # Gets x values
    #     y0_points = graph.member("fY")  # Gets y values
    # ax2.plot(x0_points, y0_points, 'r--', label='Combine likelihood')
    ax2.set_xlabel(translation[y_name])
    ax2.set_ylabel('2ΔNLL')
    ax2.grid(True)
    # ax2.set_ylim(0, max(y0_points))
    # ax2.set_xlim(min(x0_points), max(x0_points))
    ax2.axvline(optimal_x1, color='grey', linestyle='--', label=f'Minimum: {optimal_x1:.3f}')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(folder, f"chi_scans_{x_name}_and_{y_name}.pdf"))
    plt.savefig(os.path.join(folder, f"chi_scans_{x_name}_and_{y_name}.png"))
    # plt.show()

    # Print results
    print("\nMean values:")
    print(f"{x_name}: {mean_x:.3f}")
    print(f"{y_name}: {mean_y:.3f}")

    print("\nCovariance matrix:")
    print(cov_matrix)

    print("\nDiagonal components of third moment:")
    print(f"{x_name}: {third_moment_x:.3f}")
    print(f"{y_name}: {third_moment_y:.3f}")

    
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

poi_list = ["r_PTH_0p0_15p0", "r_PTH_15p0_30p0", "r_PTH_30p0_45p0", "r_PTH_45p0_80p0", "r_PTH_80p0_120p0", "r_PTH_120p0_200p0", "r_PTH_200p0_350p0", "r_PTH_350p0_10000p0"]

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
    
    # plot_correlation(pois[r_1], pois[r_2], r_1, r_2, np.corrcoef(pois[r_1], pois[r_2])[0,1], folder="Plots/PTH")
    
    # produce_simplifiedLL(pois[r_1], pois[r_2], r_1, r_2, folder="Plots/PTH/SL")

produce_LLPlots(pois, poi_list, folder="Plots/PTH/SL")


 