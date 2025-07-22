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
from scipy.optimize import minimize, curve_fit
from scipy.stats import moment
import json
from itertools import combinations  

from scipy.stats import gaussian_kde
from scipy.optimize import minimize_scalar

def gaus(x, amp, mu, sigma):
    return amp * np.exp(-(x - mu)**2 / (2 * sigma**2))

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
    "r_PTJ0_30p0_10000p0": r"$r_{p_{T,j0} \in [30,+\infty) \text{ GeV}}$",
    "chg": r"$c_{HG}$",
}

# bf_first_order_initial = [1.01193511, 1.0320153, 1.01647957, 1.04631383, 1.04529894, 0.97435069, 0.99224993, 0.98527168]

# The paths
# main_dir = '/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/January/2025_01_20_intermediateNTuples_2023/finalfits/PTH/Combine/runFits_PTH'
main_dir = '/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_06_12/intermediateRun3/finalfits/PTH/Combine/runFits_chg'
# main_dir = '/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_05_12_intermediateNTuples_2023/finalfits/NJ/Combine/runFits_NJ'
# main_dir = '/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_05_12_intermediateNTuples_2023/finalfits/PTJ0/Combine/runFits_PTJ0'
# main_dir = '/work/niharrin/CMSSW_14_1_0_pre4/src/flashggFinalFit/output/2025_05_12_intermediateNTuples_2023/finalfits/PTH/Combine/runFits_PTH'
path_to_hesse = os.path.join(main_dir, 'hesse/robustHessefirstStep.root')
base_dir = os.path.join(main_dir, "toyFit_chg")
combineLL_dir = os.path.join(main_dir, "eft_asimov")

variable = (main_dir.split("/")[-1]).split("_")[-1]

if variable == "PTH":
    poi_list = ["r_PTH_0p0_15p0", "r_PTH_15p0_30p0", "r_PTH_30p0_45p0", "r_PTH_45p0_80p0", "r_PTH_80p0_120p0", "r_PTH_120p0_200p0", "r_PTH_200p0_350p0", "r_PTH_350p0_10000p0"]
elif variable == "NJ":
    poi_list = ["r_NJ_0p0_1p0", "r_NJ_1p0_2p0", "r_NJ_2p0_3p0", "r_NJ_3p0_100p0"]
elif variable == "PTJ0":
    poi_list = ["r_PTJ0_0p0_30p0", "r_PTJ0_30p0_75p0", "r_PTJ0_75p0_120p0", "r_PTJ0_120p0_200p0", "r_PTJ0_200p0_10000p0"]
elif variable == "chg":
    poi_list = ['chg']


subfolder = "SL_chg"

bf_combine = []
for i, current_poi in enumerate(poi_list):

    with uproot.open(os.path.join(combineLL_dir, f"higgsCombinefirstStep_{current_poi}.MultiDimFit.mH125.38.root")) as file:
        # Get the TGraphs - note that uproot reads them as pairs of arrays
        tree = file[f"limit;1"]
        # Extract minimum value
        bf_combine.append(tree[current_poi].array(library="np")[0])

def coefficients(_m1, _m2ii, _m3):
    # Eq 2.9: coefficient c
    # _m3 = _m3 / 2
    c = -np.sign(_m3) * np.sqrt(2*_m2ii) * np.cos( (4*np.pi/3) + (1/3)*np.arctan( np.sqrt(8*_m2ii**3/_m3**2 - 1) ) )
    # c = +np.sign(_m3) * np.sqrt(2*_m2ii) * np.cos( (4*np.pi/3) + (1/3)*np.arctan( np.sqrt(8*_m2ii**3/_m3**2 - 1) ) )
    
    
    # print("ACHTUNG: c == 0")
    # c = 0
    
    # Eq 2.10: coefficient b
    b = np.sqrt(_m2ii - 2*c**2)   
    # Eq 2.11: coefficient a
    a = (_m1 - c)
        
    return a, b, c

def coefficients_crossingMethod(z_hat, sigma_min, sigma_plus):
    a = z_hat
    b = (sigma_min + sigma_plus) / 2
    c = (sigma_plus - sigma_min) / 2
        
    return a, b, c

def compute_rho_ij(_ci, _cj, _bi, _bj, _m2ij):
    if _ci==0 or _cj==0:
        return _m2ij / (_bi*_bj)
    else:
        return (1/(4*_ci*_cj)) * (np.sqrt(abs((_bi*_bj)**2 + 8*_ci*_cj*(_m2ij))) - _bi*_bj)

def chi_vector(x_exp, x_obs, _a, _b, _c):
    if _c == 0:
        chi_exp = (x_exp - _a) / _b
        chi_obs = (x_obs - _a) / _b
    else:
        chi_exp = (np.sqrt(_b**2 - 4*(_a-x_exp)*_c) - _b) / (2*_c)
        chi_obs = (np.sqrt(_b**2 - 4*(_a-x_obs)*_c) - _b) / (2*_c)
    
    chi_diff = (chi_obs - chi_exp) # Chi_Obs is very small compared to chi_exp
    return chi_diff

def chi(x, pois_, poi_list_, rho_, abc_values=None, first_order=False):
    chi_vector_ = []

    if first_order:
        for i, current_poi in enumerate(poi_list_):

            # Convert to numpy arrays for easier computation
            # r = np.array(pois_[current_poi])

            # 1. Mean values
            # mean = np.mean(r)
            # chi_vector_.append([mean - x[i]])
            
            chi_vector_.append([(bf_combine[i] - x[i])])
    
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
            
            # print("((x[i] - mean) / b)**2", ((x[i] - mean) / b)**2)

            chi_vector_.append([chi_vector(x[i], mean, a, b, c)])
            # mean_trim = stats.trim_mean(r, proportiontocut=0.1)
            # chi_vector_.append([chi_vector(x[i], mean_trim, a, b, c)])
            # chi_vector_.append([chi_vector(x[i], 1.025, a, b, c)]) # 1.025

    chi_vector_ = np.array(chi_vector_).flatten()

    # if first_order:
    #     print("chi_vector:", chi_vector_)
    
    # if first_order:
    #     print("Ingredients: ", bf_first_order - x)
    #     print("chi2_vector: ", chi_vector_)
    #     print("chi2:", chi_vector_.T @ np.linalg.inv(rho) @ chi_vector_
    
    # if not first_order:
    #     print("chi2_vector: ", chi_vector_)
    #     print("matrix x chi_vector: ", np.linalg.inv(rho_) @ chi_vector_)

    return chi_vector_.T @ np.linalg.inv(rho_) @ chi_vector_

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
    h_covariance = root_file.Get("h_covariance") # SIC! This is the covariance matrix, not the correlation matrix. We have the Gaussian approximation, in which corr == cov
    
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

def plot_individual_correlation(x_vals, y_vals, x_name, y_name, rho_, folder=""):
    # rho is here a number
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)
    plt.style.use(hep.style.CMS)
    _, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x_vals, y_vals)
    ax.set_xlabel(translation[x_name])
    ax.set_ylabel(translation[y_name])
    ax.text(0.1, 0.9, f"$\\rho = {rho_:.3f}$", transform=ax.transAxes)
    plt.savefig(os.path.join(folder, f"{x_name}_vs_{y_name}.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(folder, f"{x_name}_vs_{y_name}.png"), bbox_inches='tight')
    # plt.show()
    plt.close()

def plot_covariance_matrix(rho_, poi_list, folder="", title="Covariance Matrix", output_name="covariance_matrix.png"):
    # rho is here a matrix
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)
        
    plt.style.use(hep.style.CMS)
    _, ax = plt.subplots(figsize=(10, 6))
    
    labels = [translation[poi] for poi in poi_list]
    
    # Create heatmap
    sns.heatmap(
        rho_, 
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

def estimate_mode_kde(data):
    """
    Estimate the mode of an unbinned dataset using Kernel Density Estimation (KDE).

    Parameters:
    data (1D array-like): Continuous data.

    Returns:
    float: Estimated mode (location of the peak of the KDE).
    """
    kde = gaussian_kde(data)

    # Negative of KDE (since we want to maximize, and scipy minimizes)
    neg_kde = lambda x: -kde(x)

    # Search within the data range
    result = minimize_scalar(neg_kde, bounds=(min(data), max(data)), method='bounded')

    return result.x

def compute_covariance_mode(data_list):
    """
    Compute a 'covariance-like' matrix using the mode (estimated via KDE) instead of the mean.

    Parameters:
    data_list (List[1D array-like]): List of 1D arrays (each array is one variable over all samples).
                                     All arrays must be of the same length.

    Returns:
    np.ndarray: Covariance-like matrix using the mode as the center.
    """
    data = np.array(data_list)

    if data.ndim != 2:
        raise ValueError("Input must be a list of 1D arrays of equal length.")

    _, n_samples = data.shape

    # Estimate the mode for each feature (variable)
    modes = np.apply_along_axis(estimate_mode_kde, axis=1, arr=data).reshape(-1, 1)

    # Center the data using the mode
    centered_data = data - modes
    
    # Compute the covariance-like matrix
    cov_like_matrix = (centered_data @ centered_data.T) / (n_samples - 1)

    return cov_like_matrix

def produce_rho(pois_, poi_list_):

    # Covariance matrix
    cov_matrix = np.cov([pois_[current_poi] for current_poi in poi_list_])
    # cov_matrix = compute_covariance_mode([pois_[current_poi] for current_poi in poi_list_])

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
        # mean = np.apply_along_axis(estimate_mode_kde, axis=0, arr=r).reshape(-1, 1)[0][0]

        # Diagonal components of the third moment
        # Computing E[(X - μ)³]
        third_moment = np.mean((r - mean)**3)
        # third_moment = np.apply_along_axis(estimate_mode_kde, axis=0, arr=(r - mean)**3).reshape(-1, 1)[0][0]


        # a, b, c = coefficients(mean, cov_matrix[i,i], third_moment)
        a, b, c = coefficients(mean, cov_matrix, third_moment)
    
        plt.figure()
        if current_poi == "r_PTH_350p0_10000p0":
            # plt.hist((r - np.mean(r))**3, bins=50, edgecolor='black')
            plt.hist(r, bins=50, edgecolor='black', range=(-2, 5)) # range=(-1, 3)
        else:
            # plt.hist((r - np.mean(r))**3, bins=50, edgecolor='black')
            # plt.hist(r, bins=30, edgecolor='black', range=(-1, 3))
            plt.hist(r, bins=50, edgecolor='black')
        # plt.title('Distribution of the third moment')
        plt.title('Distribution of r')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.grid(True)
        # plt.savefig(f"./Plots/PTH/SL/thirdMoment/{current_poi}.png")
        plt.savefig(f"./Plots/{variable}/{subfolder}/{current_poi}.png")
        plt.close()
                
        abc_values[current_poi] = [a, b, c]

        # Print results
        print(f"Current POI: {current_poi}")    
        
        # rho_II = compute_rho_ij(abc_values[current_poi][2], abc_values[current_poi][2], abc_values[current_poi][1], abc_values[current_poi][1], cov_matrix[i,i])
        rho_II = compute_rho_ij(abc_values[current_poi][2], abc_values[current_poi][2], abc_values[current_poi][1], abc_values[current_poi][1], cov_matrix)
        
        print(f"Mean values: {mean:.3f}")
        print(f"Diagonal components of third moment: {third_moment:.3f}")
        
        print(f"m_I according to equation 2.6: {(a + c):.3f}")
        print(f"m_II according to equation 2.7: {((b**2 * rho_II) + (2*c**2 * rho_II**2)):.3f}")
        print(f"m_III according to equation 2.8: {(6*(b**2)*c + (8*c**3)):.3f}")
        
        print(f"Skewness: {stats.skew(r):.3f}")
        # print(f"m_I according to stats.moment: {moment(r, moment=1):.3f}")
        print(f"m_II according to stats.moment: {moment(r, moment=2):.3f}")
        print(f"m_III according to stats.moment: {moment(r, moment=3):.3f}")
        print(f"ABC values: {a:.3f}, {b:.3f}, {c:.3f}\n")

    for i, current_poi in enumerate(poi_list_):
        reihe_i = []
        for j, other_poi in enumerate(poi_list_):
            # reihe_i.append(compute_rho_ij(abc_values[current_poi][2], abc_values[other_poi][2], abc_values[current_poi][1], abc_values[other_poi][1], cov_matrix[i,j]))
            reihe_i.append(compute_rho_ij(abc_values[current_poi][2], abc_values[other_poi][2], abc_values[current_poi][1], abc_values[other_poi][1], cov_matrix))
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

def covariance_to_correlation(cov_matrix):
    """
    Converts a covariance matrix to a correlation matrix.
    
    Parameters:
    corr_matrix (numpy.ndarray): Correlation matrix
    std_devs (numpy.ndarray): Standard deviations of variables
    
    Returns:
    numpy.ndarray: Covariance matrix
    """
    # outer_std_dev = np.outer(std_devs, std_devs) # Outer product of standard deviations
    # print("outer_std_dev: ", outer_std_dev)
    # covariance_matrix = corr_matrix * outer_std_dev  # Element-wise multiplication
    # Compute the outer product of standard deviations
    std_devs = np.sqrt(np.diag(cov_matrix))  # Standard deviations
    outer_std_dev = np.outer(std_devs, std_devs)
    
    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        corr_matrix = np.divide(cov_matrix, outer_std_dev)
        corr_matrix[outer_std_dev == 0] = 0  # Handle zeros in outer product

    return corr_matrix

def produce_and_minimize_chi_crossingMethod(pois_, poi_list_, combineLL_dir_):
    abc_values_crossingMethod = {}
    
    if len(poi_list_) == 1:
        print("Only one POI provided. Using cov_matrix = 1")
        cov_matrix = 1
    else:
        cov_matrix = np.cov([pois_[r] for r in poi_list_])

    for i, current_poi in enumerate(poi_list_):
                
        with uproot.open(os.path.join(combineLL_dir_, "scans", f"scan_{current_poi}.root")) as file:
            # Get the TGraphs - note that uproot reads them as pairs of arrays
            graph = file[f"scan_{current_poi};1"]  # Replace with your TGraph name
            # Extract x and y values
            x0_points = graph.member("fX")  # Gets x values
            y0_points = graph.member("fY")  # Gets y values
        
        z_hat = x0_points[np.argmin(y0_points)] # Consider an Asimov dataset
        print(find_crossings(x0_points, y0_points))
        if len(find_crossings(x0_points, y0_points)) != 2:
            print(f"Warning: Expected two crossings for {current_poi}, found {len(find_crossings(x0_points, y0_points))}. Using the last two crossings.")
            crossing_minus, crossing_plus = find_crossings(x0_points, y0_points)[-2:]  # Use the last two crossings
        else:
            crossing_minus, crossing_plus = find_crossings(x0_points, y0_points)
        sigma_plus = crossing_plus - z_hat
        sigma_minus = z_hat - crossing_minus
        
        a, b, c = coefficients_crossingMethod(z_hat, sigma_minus, sigma_plus)
                    
        abc_values_crossingMethod[current_poi] = [a, b, c]
    
    print(cov_matrix)
    if cov_matrix == 1:
        rho_crossingMethod = np.array([[1.]])  # If only one POI, correlation is 1
    else:
        rho_crossingMethod = covariance_to_correlation(np.array(cov_matrix))

    x0 = np.array([0. for i in range(len(poi_list_))])
    res = minimize(chi, x0, args=(pois_, poi_list_, rho_crossingMethod, abc_values_crossingMethod))

    # Get optimal values from minimization
    optimal_values = res.x
    
    x0_ranges = []
    chi_x0_scans = []
    
    for i, current_poi in enumerate(poi_list_):
        print(f"{current_poi}: {optimal_values[i]:.3f}")

        # Create a grid of points
        # x0_range = np.linspace(-1, 3, 100)  # Adjust range as needed
        x0_range = np.linspace(-0.2, 0.2, 100)
        
        optimal_values_copy = optimal_values.copy()
        
        chi_x0_scan = []
        for x0 in x0_range:
            for j in range(len(poi_list_)):
                if j!=i:
                    optimal_values_copy[j] = optimal_values[j]
                if j == i:
                    optimal_values_copy[j] = x0
            chi_x0_scan.append(float(chi(optimal_values_copy, pois_, poi_list_, rho_crossingMethod, abc_values_crossingMethod, first_order=False)))
        
        chi_x0_scan = np.array(chi_x0_scan)

        
        x0_ranges.append(x0_range)
        chi_x0_scans.append(chi_x0_scan)
    
    return x0_ranges, chi_x0_scans, optimal_values

def produce_and_minimize_chi(pois_, poi_list_, first_order=False):
    
    cov_matrix = np.cov([pois_[r] for r in poi_list_])
    # cov_matrix = compute_covariance_mode([pois_[current_poi] for current_poi in poi_list_])
    
    
    if first_order:
        rho = extract_covariance_matrix(path_to_hesse, poi_list_)
        
        # rho = covariance_to_correlation(np.array(cov_matrix))
        
        # bf_first_order_initial = [1. for i in range(len(poi_list_))]
        x0 = np.array([0. for i in range(len(poi_list_))])
        abc_values = None
        
        res = minimize(chi, x0, args=(pois_, poi_list_, rho, abc_values, first_order))
        
        print("res.x for first order", res.x)
        
    else:
        
        print("cov_matrix", cov_matrix)
        rho, abc_values = produce_rho(pois_, poi_list_)
        
        # rho = covariance_to_correlation(np.array(cov_matrix))

        # rho = correlation_to_covariance(np.array(rho), np.sqrt(np.diag(np.cov([pois_[r] for r in poi_list_]))))

        # x0 = np.array([1. for i in range(len(poi_list_))])
        x0 = np.array([0. for i in range(len(poi_list_))])
        # x0 = np.array([bf_first_order[i] for i in range(len(poi_list_))])
        res = minimize(chi, x0, args=(pois_, poi_list_, rho, abc_values, first_order))
        
        # print(res.x)
    
    # Get optimal values from minimization
    optimal_values = res.x
    
    print("Optimal values: ", optimal_values)
    
    x0_ranges = []
    chi_x0_scans = []
    # optimal_values_list = []
    
    for i, current_poi in enumerate(poi_list_):
        print(f"{current_poi}: {optimal_values[i]:.3f}")

        # Create a grid of points
        # x0_range = np.linspace(-1, 3, 100)  # Adjust range as needed
        x0_range = np.linspace(-0.2, 0.2, 100)  # Adjust range as needed
        
        optimal_values_copy = optimal_values.copy()

        chi_x0_scan = []
        for x0 in x0_range:
            for j in range(len(poi_list_)):
                if j!=i:
                    # if first_order:
                    #     optimal_values_copy[j] = bf_first_order[j]
                    # else:
                    #     optimal_values_copy[j] = optimal_values[j]
                    optimal_values_copy[j] = optimal_values[j]
                if j == i:
                    optimal_values_copy[j] = x0
            if first_order:
                # print("opt_value_with_fixed_rest", optimal_values_copy)
                chi_x0_scan.append(float(chi(optimal_values_copy, pois_, poi_list_, rho, abc_values, first_order=True)))
            else:
                # print("opt_value_with_fixed_rest", optimal_values_copy)
                chi_x0_scan.append(float(chi(optimal_values_copy, pois_, poi_list_, rho, abc_values, first_order=False)))
        
        chi_x0_scan = np.array(chi_x0_scan)

        # Find crossing points at for 68% interval 
        # crossings_x0 = find_crossings(x0_range, chi_x0_scan)
        # print('crossings_x0', crossings_x0)
        
        x0_ranges.append(x0_range)
        chi_x0_scans.append(chi_x0_scan)
        # optimal_values_list.append(optimal_values[i])
    
    return x0_ranges, chi_x0_scans, optimal_values

def produce_LLPlots(pois_, poi_list_, combineLL_dir_, folder="", print_first_order=False, with_crossingMethod=False):
    
    x0_ranges, chi_x0_scans, optimal_values = produce_and_minimize_chi(pois_, poi_list_)
    
    # print("Optimal values: ", optimal_values)
    if print_first_order:
        x0_ranges_fo, chi_x0_scans_fo, optimal_values_fo = produce_and_minimize_chi(pois_, poi_list_, first_order=True)
    
    if with_crossingMethod:
        x0_ranges_cm, chi_x0_scans_cm, optimal_values_cm = produce_and_minimize_chi_crossingMethod(pois_, poi_list_, combineLL_dir_)
    
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)
    
    cov_matrix = np.cov([pois_[r] for r in poi_list_])
    # cov_matrix = compute_covariance_mode([pois_[current_poi] for current_poi in poi_list_])
    
    for i, current_poi in enumerate(poi_list_):
         
        # Check if condition is satisfied
        mean = np.mean(pois_[current_poi])
        # variance = cov_matrix[i,i]
        variance = cov_matrix
        third_moment = np.mean((pois_[current_poi] - mean)**3)
        
        condition = (8*variance**3 >= third_moment**2)
        print(f"Condition for {current_poi}: {condition}")
        print(f"8*variance**3 / third_moment**2 for {current_poi}: {(8*variance**3) / (third_moment**2)}\n")
        # print(f"Variance for {current_poi}: {variance}")
        # print(f"Third moment for {current_poi}: {third_moment}\n")
        if not condition:
            print(f"Skipping {current_poi} as condition is not satisfied")
            continue
    
        # Create plots
        plt.style.use(hep.style.CMS)
        _, ax1 = plt.subplots(1, 1, figsize=(12, 8))

        # Plot x0 scan
        ax1.plot(x0_ranges[i], chi_x0_scans[i], label='Simplified likelihood', color="green")
        ax1.axvline(optimal_values[i], color='red', linestyle='--', label=f'Minimum: {optimal_values[i]:.3f}')
        if print_first_order:
            ax1.plot(x0_ranges_fo[i], chi_x0_scans_fo[i], label='Gaussian likelihood', color="teal")

        if with_crossingMethod:
            ax1.plot(x0_ranges_cm[i], chi_x0_scans_cm[i], label='Crossing Method', color="darkmagenta")
        with uproot.open(os.path.join(combineLL_dir_, "scans", f"scan_{current_poi}.root")) as file:
            # Get the TGraphs - note that uproot reads them as pairs of arrays
            graph = file[f"scan_{current_poi};1"]  # Replace with your TGraph name
            # Extract x and y values
            x0_points = graph.member("fX")  # Gets x values
            y0_points = graph.member("fY")  # Gets y values
            
        with uproot.open(os.path.join(combineLL_dir_, f"higgsCombinefirstStep_{current_poi}.MultiDimFit.mH125.38.root")) as file:
            # Get the TGraphs - note that uproot reads them as pairs of arrays
            tree = file[f"limit;1"]
            # Extract minimum value
            optimal_values_combine = tree[current_poi].array(library="np")[0]
            
        # print("Element closest to 1 in x0_ranges", np.argmin(np.abs(x0_ranges[i] - 1)))
        # idx_closest = np.argmin(np.abs(x0_ranges[i] - 1))
        # x_at_peak = x0_ranges[i][idx_closest]
        # shift = 1 - x_at_peak
        # x0_ranges_centered = x0_ranges[i] + shift
        # print("current_shift", shift)
        # ax1.plot(x0_ranges_centered, chi_x0_scans[i], label='Simplified likelihood (ABC)')
        
        ax1.plot(x0_points, y0_points, 'r--', label='Full likelihood', color="black")
        
        print(f"SL Minimum and Crossings: {optimal_values[i]:.3f}, {find_crossings(x0_ranges[i], chi_x0_scans[i])}") 
        if print_first_order:
            print(f"Hesse Minimum and Crossings: {optimal_values_fo[i]:.3f}, {find_crossings(x0_ranges_fo[i], chi_x0_scans_fo[i])}") 
        print(f"Combine Minimum and Crossings: {optimal_values_combine}, {find_crossings(x0_points, y0_points)}") 


        ax1.set_xlabel(translation[current_poi])
        ax1.set_ylabel('2ΔNLL')
        ax1.grid(True)
        # ax1.set_ylim(0, max(y0_points))
        ax1.legend()
        
        ax1.set_ylim(0, 10)
        # ax1.set_xlim(-1, 3)
        ax1.set_xlim(-0.2, 0.2)
        
        plt.tight_layout()
        plt.savefig(os.path.join(folder, f"chi_scan_{current_poi}.pdf"))
        plt.savefig(os.path.join(folder, f"chi_scan_{current_poi}.png"))
    
    rho, _ = produce_rho(pois_, poi_list_)
    plot_covariance_matrix(rho, poi_list_, folder=folder, title="Covariance Matrix (Simplified Likelihood)", output_name="covariance_matrix_sl.png")
    
    # covariance_df = extract_covariance_matrix(path_to_hesse, poi_list)
    # plot_covariance_matrix(covariance_df, poi_list_, folder=folder, title="Covariance Matrix (Hessian)", output_name="covariance_matrix_hesse.png")
    

def create_poiJson_untrimmed(base_dir, poi_list):
    pois = {}
    
    for current_poi in poi_list:
            
        pois[current_poi] = []
        
    for i in range(len(glob.glob(os.path.join(base_dir, "toy_*")))):
            
        if i%100==0:
            print(f"Processing fit_{i}")
        
        seed = 123456 + i
        
        try:
            # current_root_files = uproot.open(f"{base_dir}/toy_{i}/higgsCombineToyBestFit_{current_poi}.MultiDimFit.mH125.38.{seed}.root")
            current_root_files = uproot.open(f"{base_dir}/toy_{i}/higgsCombinefirstStep.MultiDimFit.mH125.38.{seed}.root")
        except:
            print(f"Skipping fit_{i}: Required scan files not found")
            continue
        
        for j, current_poi in enumerate(poi_list):

            try: 
                current_tree = current_root_files["limit"]
            except:
                print(f"Skipping fit_{i}: Tree 'limit' not found in ROOT file")
                continue

            current_limit_values = current_tree[current_poi].array()

            try:
                if current_limit_values[0]<-4:
                    print("Value out of boundary", current_limit_values[0], i)
            except:
                if j == 0:
                    print("Empty ROOT file for bootstrap: ", i)
                continue

            pois[current_poi].append(float(current_limit_values[0]))
    return pois

def create_poiJson_trimmed(base_dir, poi_list, trimming_value_left, trimming_value_right):
    pois = {}
    
    for current_poi in poi_list:
            
        pois[current_poi] = []
        
    for i in range(len(glob.glob(os.path.join(base_dir, "toy_*")))):
            
        if i%100==0:
            print(f"Processing fit_{i}")
        
        seed = 123456 + i
        
        try:
            # current_root_files = uproot.open(f"{base_dir}/toy_{i}/higgsCombineToyBestFit_{current_poi}.MultiDimFit.mH125.38.{seed}.root")
            current_root_files = uproot.open(f"{base_dir}/toy_{i}/higgsCombinefirstStep.MultiDimFit.mH125.38.{seed}.root")
        except:
            print(f"Skipping fit_{i}: Required scan files not found")
            continue
        
        kill_event = False
        
        # First loop to check if there are outliers (outliers are events smaller than -4 and bigger than 4)
        for j, current_poi in enumerate(poi_list):
            try: 
                current_tree = current_root_files["limit"]
            except:
                print(f"Skipping fit_{i}: Tree 'limit' not found in ROOT file")
                continue
            
            current_limit_values = current_tree[current_poi].array()
            
            try:
                if (current_limit_values[0] > trimming_value_right) or (current_limit_values[0] < trimming_value_left):
                    kill_event = True
                    break
            except:
                if j == 0:
                    print("Empty ROOT file for bootstrap: ", i)
                continue
        
        if kill_event:
            print(f"Skipping fit_{i} with {current_limit_values}: Outlier found")
            continue

        for j, current_poi in enumerate(poi_list):

            try: 
                current_tree = current_root_files["limit"]
            except:
                print(f"Skipping fit_{i}: Tree 'limit' not found in ROOT file")
                continue

            current_limit_values = current_tree[current_poi].array()

            try:
                if current_limit_values[0]<-4:
                    print("Value out of boundary", current_limit_values[0], i)
            except:
                if j == 0:
                    print("Empty ROOT file for bootstrap: ", i)
                continue

            pois[current_poi].append(float(current_limit_values[0]))
    return pois
# Loop through all fit directories (fit_0, fit_1, etc.)
        
if not os.path.exists(f'pois_untrimmed_{variable}.json'):
    pois_untrimmed = create_poiJson_untrimmed(base_dir, poi_list)
    # Save the POIs to a JSON file
    with open(f'pois_untrimmed_{variable}.json', 'w') as f:
        json.dump(pois_untrimmed, f)
else:
    # Load the POIs from the JSON file
    with open(f'pois_untrimmed_{variable}.json', 'r') as f:
        pois_untrimmed = json.load(f)

# Now we have to fit a gaussian core to all the categories to get the values where we cut. z is the number of standard deviations we want to cut away
trimming_value_left = 0
trimming_value_right = 0
largest_sigma = 0
mu_to_largest_sigma = 0
z = 4
for i, current_poi in enumerate(poi_list):
    r = np.array(pois_untrimmed[current_poi])
    mean = np.mean(r)
    s = np.std(r)
    
    counts, bin_edges = np.histogram(r, bins=50, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    popt, _ = curve_fit(gaus, bin_centers, counts, p0=[1, mean, s])
    amp_fit, mu_fit, sigma_fit = popt
    # print(f"Fitted Parameters for {current_poi}:\nAmplitude = {amp_fit:.3f}\nMean = {mu_fit:.3f}\nSigma = {sigma_fit:.3f}")
    
    if i == 0:
        largest_sigma = sigma_fit
        mu_to_largest_sigma = mu_fit
    else:
        if (sigma_fit > largest_sigma):
            largest_sigma = sigma_fit
            mu_to_largest_sigma = mu_fit
            
    if (not os.path.exists(f"./Plots/{variable}/{subfolder}")) & (f"./Plots/{variable}/{subfolder}"!=""):
        os.makedirs(f"./Plots/{variable}/{subfolder}")
            
    plt.figure()
    plt.hist(r, bins=30, density=True, alpha=0.6, label='Histogram')
    plt.plot(bin_centers, gaus(bin_centers, *popt), color='red', label='Fitted Gaussian')
    plt.legend()
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title('Gaussian Fit to Data Histogram')
    plt.savefig(f"./Plots/{variable}/{subfolder}/gaussian_fit_{current_poi}.png")
    plt.close()
    
trimming_value_left = mu_to_largest_sigma - z*largest_sigma
trimming_value_right = mu_to_largest_sigma + z*largest_sigma

print("Trimming values: ", trimming_value_left, trimming_value_right)

if trimming_value_left > trimming_value_right:
    trimming_value_left, trimming_value_right = trimming_value_right, trimming_value_left


if not os.path.exists(f'pois_trimmed_{variable}.json'):
    pois = create_poiJson_trimmed(base_dir, poi_list, trimming_value_left, trimming_value_right)
    # Save the POIs to a JSON file
    with open(f'pois_trimmed_{variable}.json', 'w') as f:
        json.dump(pois, f)
else:
    # Load the POIs from the JSON file
    with open(f'pois_trimmed_{variable}.json', 'r') as f:
        pois = json.load(f)
    
unique_pairings = list(combinations(poi_list, 2))

for current_tuple in unique_pairings:
    r_1, r_2 = current_tuple
    
    plot_individual_correlation(pois[r_1], pois[r_2], r_1, r_2, np.corrcoef(pois[r_1], pois[r_2])[0,1], folder=f"Plots/{variable}")

# data = {}

# # Cut away the lowest and highest 1% of the data
# proportiontocut = 0.005
# for i, current_poi in enumerate(poi_list):
#     # data[current_poi] = stats.trimboth(pois[current_poi], proportiontocut=proportiontocut)
#     data[current_poi] = stats.trim1(pois[current_poi], proportiontocut=proportiontocut, tail="left")
#     print(f"POI: {current_poi}. Cut away {100 - 100*(len(data[current_poi]) / len(pois[current_poi]))}% of the data with {len(pois[current_poi])} entries.")
#     print(f"minimum: {min(data[current_poi])}")
#     print(f"maximum: {max(data[current_poi])}")

produce_LLPlots(pois, poi_list, combineLL_dir, folder=f"Plots/{variable}/{subfolder}", print_first_order=False, with_crossingMethod=True)
