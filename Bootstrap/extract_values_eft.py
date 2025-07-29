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

# from scipy.stats import gaussian_kde
# from scipy.optimize import minimize_scalar

def gaus(x, amp, mu, sigma):
    return amp * np.exp(-(x - mu)**2 / (2 * sigma**2))

# Importing translation dictionary
translationFilePath = "/work/niharrin/t35/CMSSW_14_1_0_pre4/src/flashggFinalFit/Bootstrap/translation.json"
with open(translationFilePath) as translationFile:
    translation = json.load(translationFile)


poi_to_eft2obs_namingConvention = {
    "r_PTH_0p0_15p0": "0.0",
    "r_PTH_15p0_30p0": "15.0",
    "r_PTH_30p0_45p0": "30.0",
    "r_PTH_45p0_80p0": "45.0",
    "r_PTH_80p0_120p0": "80.0",
    "r_PTH_120p0_200p0": "120.0",
    "r_PTH_200p0_350p0": "200.0",
    "r_PTH_350p0_10000p0": "350.0"
}

# Importing the Run 2 EFT parametrization from Massi
decayFilePath = "/work/niharrin/tests/eft_fitter/functions/extract_EFT2Obs/mgalli/decay.json"
productionFilePath = "/work/niharrin/tests/eft_fitter/functions/extract_EFT2Obs/mgalli/run3_binning_massi_param.json"

with open(decayFilePath) as decayFile:
    decay = json.load(decayFile)
with open(productionFilePath) as productionFile:
    production = json.load(productionFile)

# Importing scaling file
scalingFilePath = "/work/niharrin/tests/eft_fitter/functions/extract_EFT2Obs/mgalli/scaling.json"
with open(scalingFilePath) as scalingFile:
    scaling_dict = json.load(scalingFile)

# Importing ranging file
rangingFilePath = "/work/niharrin/tests/eft_fitter/functions/extract_EFT2Obs/mgalli/ranges.json"
with open(rangingFilePath) as rangingFile:
    range_dict = json.load(rangingFile)

# Changing the plotting ranges for some EFT variables

range_dict["chb"] = [-0.001, 0.002]
range_dict["chwb"] = [-0.003, 0.001]
range_dict["ctbre"] = [-0.001, 0.003]
range_dict["cthre"] = [-1, 0.5]
range_dict["ctwre"] = [-0.025, 0.05]


def produce_bf_combine(poi_list_, combineLL_dir_):
    bf_combine = []
    for current_poi in poi_list_:

        with uproot.open(os.path.join(combineLL_dir_, f"higgsCombinefirstStep_{current_poi}.MultiDimFit.mH125.38.root")) as file:
            # Get the TGraphs - note that uproot reads them as pairs of arrays
            tree = file[f"limit;1"]
            # Extract minimum value
            bf_combine.append(tree[current_poi].array(library="np")[0])
    return bf_combine

def coefficients(_m1, _m2ii, _m3):
    # Eq 2.9: coefficient c
    c = -np.sign(_m3) * np.sqrt(2*_m2ii) * np.cos( (4*np.pi/3) + (1/3)*np.arctan( np.sqrt(8*_m2ii**3/_m3**2 - 1) ) )

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

def WCToMu(wc, _current_poi, _eft_variable):
    # Note, only valid for 1D parameter space, i.e. only one POI is considered
    # eft_variable is something like "chg". Note: It MUST be in the EFT2Obs naming convention
    # current_poi is something like "r_PTH_0p0_15p0". It will be converted to the EFT2Obs naming convention
    
    eft_scaling = scaling_dict.get(_eft_variable, 1.0)

    current_poi_eft2obsConvention = poi_to_eft2obs_namingConvention[_current_poi]

    # Extract the A's and B's from production and decay where applicable
    A_prod = production.get(current_poi_eft2obsConvention, {}).get(f"A_{_eft_variable}", 0)
    B_prod = production.get(current_poi_eft2obsConvention, {}).get(f"B_{_eft_variable}_2", 0)

    A_decay = decay.get("gamgam", {}).get(f"A_{_eft_variable}", 0)
    B_decay = decay.get("gamgam", {}).get(f"B_{_eft_variable}_2", 0)

    A_tot = decay.get("tot", {}).get(f"A_{_eft_variable}", 0)
    B_tot = decay.get("tot", {}).get(f"B_{_eft_variable}_2", 0)

    if eft_scaling != 1.0:
        A_prod *= eft_scaling
        B_prod *= eft_scaling**2

        A_decay *= eft_scaling
        B_decay *= eft_scaling**2

        A_tot *= eft_scaling
        B_tot *= eft_scaling**2

    # Calculate mu := mu_prod * mu_decay
    mu_prod = 1 + A_prod*wc + B_prod*wc**2
    mu_decay = (1 + A_decay*wc + B_decay*wc**2) / (1 + A_tot*wc + B_tot*wc**2)

    return mu_prod * mu_decay

def chi_vector(wc_exp, mu_obs, _a, _b, _c, _current_poi, _eft_variable):
    # mu_obs is the observed value of mu and should not be translated, or is it?
    if _c == 0:
        chi_exp = (WCToMu(wc_exp, _current_poi, _eft_variable) - _a) / _b
        chi_obs = (mu_obs - _a) / _b
    else:
        chi_exp = (np.sqrt(_b**2 - 4*(_a-WCToMu(wc_exp, _current_poi, _eft_variable))*_c) - _b) / (2*_c)
        chi_obs = (np.sqrt(_b**2 - 4*(_a-mu_obs)*_c) - _b) / (2*_c)
    
    chi_diff = (chi_obs - chi_exp) # Chi_Obs is very small compared to chi_exp
    return chi_diff

def chi(wc, pois_, poi_list_, rho_, eft_variable_, abc_values=None, first_order=False, bf_combine_=None):
    chi_vector_ = []

    if first_order:
        if bf_combine_ is None:
            print("Provide bf_combine")
            exit(1)
        for i, current_poi in enumerate(poi_list_):
            chi_vector_.append([(bf_combine_[i] - WCToMu(wc[i], current_poi, eft_variable_))])

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

            chi_vector_.append([chi_vector(wc[i], mean, a, b, c, current_poi, eft_variable_)])
    
    chi_vector_ = np.array(chi_vector_).flatten()

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

def extract_covariance_matrix(root_file_path, poi_list_):
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
    df_filtered = df_covariance.loc[poi_list_, poi_list_]

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
    plt.close()

def plot_covariance_matrix(rho_, poi_list_, folder="", title="Covariance Matrix", output_name="covariance_matrix.png"):
    # rho is here a matrix
    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)

    plt.style.use(hep.style.CMS)
    _, ax = plt.subplots(figsize=(10, 6))

    labels = [translation[poi] for poi in poi_list_]

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

def produce_rho(pois_, poi_list_, subfolder_, plot_r_distribution=True):

    # Covariance matrix
    cov_matrix = np.cov([pois_[current_poi] for current_poi in poi_list_])

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

        a, b, c = coefficients(mean, cov_matrix[i,i], third_moment)
    
        if plot_r_distribution:
            plt.figure()
            if current_poi == "r_PTH_350p0_10000p0":
                plt.hist(r, bins=50, edgecolor='black', range=(-2, 5)) # range=(-1, 3)
            else:
                plt.hist(r, bins=50, edgecolor='black')
            # plt.title('Distribution of the third moment')
            plt.title('Distribution of r')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.grid(True)
            rho_plot_path = f"./Plots/{variable}/{subfolder_}"
            if (not os.path.exists(rho_plot_path)) & (rho_plot_path!=""):
                os.makedirs(rho_plot_path)
            plt.savefig(f"{rho_plot_path}/{current_poi}.png")
            plt.close()

        abc_values[current_poi] = [a, b, c]

        # Print results
        print(f"Current POI: {current_poi}")    

        rho_II = compute_rho_ij(abc_values[current_poi][2], abc_values[current_poi][2], abc_values[current_poi][1], abc_values[current_poi][1], cov_matrix[i,i])

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
    std_devs = np.sqrt(np.diag(cov_matrix))  # Standard deviations
    outer_std_dev = np.outer(std_devs, std_devs)

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        corr_matrix = np.divide(cov_matrix, outer_std_dev)
        corr_matrix[outer_std_dev == 0] = 0  # Handle zeros in outer product

    return corr_matrix

def produce_and_minimize_chi_crossingMethod(pois_, poi_list_, combineLL_dir_, eft_variable_, inclusive_=False):
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
        print("XS crossings", find_crossings(x0_points, y0_points))
        if len(find_crossings(x0_points, y0_points)) != 2:
            print(f"Warning: Expected two crossings for {current_poi}, found {len(find_crossings(x0_points, y0_points))}. Using the last two crossings.")
            crossing_minus, crossing_plus = find_crossings(x0_points, y0_points)[-2:]  # Use the last two crossings
        else:
            crossing_minus, crossing_plus = find_crossings(x0_points, y0_points)
        sigma_plus = crossing_plus - z_hat
        sigma_minus = z_hat - crossing_minus

        a, b, c = coefficients_crossingMethod(z_hat, sigma_minus, sigma_plus)
        
        abc_values_crossingMethod[current_poi] = [a, b, c]

    if len(cov_matrix) == 1:
        rho_crossingMethod = np.array([[1.]])  # If only one POI, correlation is 1
    else:
        rho_crossingMethod = covariance_to_correlation(np.array(cov_matrix))
    
    x0 = np.array([0. for i in range(len(poi_list_))])
    res = minimize(chi, x0, args=(pois_, poi_list_, rho_crossingMethod, eft_variable_, abc_values_crossingMethod), bounds=[(range_dict[eft_variable_][0], range_dict[eft_variable_][1]) for _ in poi_list_])
    
    if not res.success:
        print(f"WARNING: Minimization did not succeed. Message: {res.message}")
    
    # Get optimal values from minimization
    optimal_values = res.x
    
    x0_ranges = []
    chi_x0_scans = []

    for i, current_poi in enumerate(poi_list_):
        print(f"{current_poi}: {optimal_values[i]:.3f}")

        # Create a grid of points

        x0_range = np.linspace(range_dict[eft_variable_][0], range_dict[eft_variable_][1], 200)

        optimal_values_copy = optimal_values.copy()

        chi_x0_scan = []
        for x0 in x0_range:
            for j in range(len(poi_list_)):
                if j!=i:
                    if inclusive_:
                        optimal_values_copy[j] = x0
                    else:
                        optimal_values_copy[j] = optimal_values[j]
                if j == i:
                    optimal_values_copy[j] = x0

            chi_x0_scan.append(float(chi(optimal_values_copy, pois_, poi_list_, rho_crossingMethod, eft_variable_, abc_values_crossingMethod, first_order=False)))

        chi_x0_scan = np.array(chi_x0_scan)

        x0_ranges.append(x0_range)
        chi_x0_scans.append(chi_x0_scan)

    return x0_ranges, chi_x0_scans, optimal_values

def produce_and_minimize_chi(pois_, poi_list_, eft_variable_, subfolder_, path_to_hesse_, first_order=False, bf_combine_=None, inclusive_=False, plot_r_distribution=True):

    cov_matrix = np.cov([pois_[r] for r in poi_list_])   

    if first_order:
        rho = extract_covariance_matrix(path_to_hesse_, poi_list_)

        x0 = np.array([0. for i in range(len(poi_list_))])
        abc_values = None

        res = minimize(chi, x0, args=(pois_, poi_list_, rho, eft_variable_, abc_values, first_order, bf_combine_), bounds=[(range_dict[eft_variable_][0], range_dict[eft_variable_][1]) for _ in poi_list_])
    
        if not res.success:
            print(f"WARNING: Minimization did not succeed. Message: {res.message}")

        print("res.x for first order", res.x)

    else:
        print("cov_matrix", cov_matrix)
        rho, abc_values = produce_rho(pois_, poi_list_, subfolder_, plot_r_distribution=plot_r_distribution)

        x0 = np.array([0. for i in range(len(poi_list_))])
        res = minimize(chi, x0, args=(pois_, poi_list_, rho, eft_variable_, abc_values, first_order), bounds=[(range_dict[eft_variable_][0], range_dict[eft_variable_][1]) for _ in poi_list_])
    
        if not res.success:
            print(f"WARNING: Minimization did not succeed. Message: {res.message}")

    # Get optimal values from minimization
    optimal_values = res.x
    
    print("Optimal values: ", optimal_values)
    
    x0_ranges = []
    chi_x0_scans = []
    
    # Per bin extraction of the XS / WC
    for i, current_poi in enumerate(poi_list_):
        print(f"{current_poi}: {optimal_values[i]:.3f}")

        # Create a grid of points
        x0_range = np.linspace(range_dict[eft_variable_][0], range_dict[eft_variable_][1], 200)  # Adjust range as needed

        optimal_values_copy = optimal_values.copy()

        chi_x0_scan = []
        for x0 in x0_range:
            for j in range(len(poi_list_)):
                if j!=i:
                    if inclusive_:
                        optimal_values_copy[j] = x0
                    else:
                        optimal_values_copy[j] = optimal_values[j]
                    # optimal_values_copy[j] = x0
                if j == i:
                    optimal_values_copy[j] = x0
            if first_order:
                chi_x0_scan.append(float(chi(optimal_values_copy, pois_, poi_list_, rho, eft_variable_, abc_values, first_order=True, bf_combine_=bf_combine_)))
            else:
                chi_x0_scan.append(float(chi(optimal_values_copy, pois_, poi_list_, rho, eft_variable_, abc_values, first_order=False)))

        chi_x0_scan = np.array(chi_x0_scan)

        x0_ranges.append(x0_range)
        chi_x0_scans.append(chi_x0_scan)

    return x0_ranges, chi_x0_scans, optimal_values

def produce_LLPlots(pois_, poi_list_, combineLL_dir_, eft_variable_, combineLL_eftDir_, path_to_hesse_, folder="", subfolder_="", print_first_order=False, bf_combine_=None, with_crossingMethod=False, inclusive_=False, plot_r_distribution=True):

    x0_ranges, chi_x0_scans, optimal_values = produce_and_minimize_chi(pois_, poi_list_, eft_variable_, subfolder_, path_to_hesse_, bf_combine_=bf_combine_, inclusive_=inclusive_, plot_r_distribution=plot_r_distribution)

    if print_first_order:
        x0_ranges_fo, chi_x0_scans_fo, optimal_values_fo = produce_and_minimize_chi(pois_, poi_list_, eft_variable_, subfolder_, path_to_hesse_, first_order=True, bf_combine_=bf_combine_, inclusive_=inclusive_, plot_r_distribution=plot_r_distribution)

    if with_crossingMethod:
        x0_ranges_cm, chi_x0_scans_cm, optimal_values_cm = produce_and_minimize_chi_crossingMethod(pois_, poi_list_, combineLL_dir_, eft_variable_, inclusive_=inclusive_)

    if (not os.path.exists(folder)) & (folder!=""):
        os.makedirs(folder)

    cov_matrix = np.cov([pois_[r] for r in poi_list_])

    for i, current_poi in enumerate(poi_list_):
        if inclusive_ and i > 0:
            continue

        # Check if condition is satisfied
        mean = np.mean(pois_[current_poi])
        variance = cov_matrix[i,i]
        third_moment = np.mean((pois_[current_poi] - mean)**3)

        condition = (8*variance**3 >= third_moment**2)
        print(f"Condition for {current_poi}: {condition}")
        print(f"8*variance**3 / third_moment**2 for {current_poi}: {(8*variance**3) / (third_moment**2)}\n")

        if not condition:
            print(f"Skipping {current_poi} as condition is not satisfied")
            continue

        # Create plots
        plt.style.use(hep.style.CMS)
        _, ax1 = plt.subplots(1, 1, figsize=(12, 8))
        hep.cms.label('Preliminary', data=False, lumi=27.3, com=13.6)

        # Plot x0 scan
        ax1.plot(x0_ranges[i], chi_x0_scans[i], label='Simplified likelihood', color="green")
        ax1.axvline(optimal_values[i], color='red', linestyle='--', label=f'Minimum: {optimal_values[i]:.3f}')
        if print_first_order:
            ax1.plot(x0_ranges_fo[i], chi_x0_scans_fo[i], label='Gaussian likelihood', color="teal")

        if with_crossingMethod:
            ax1.plot(x0_ranges_cm[i], chi_x0_scans_cm[i], label='Crossing Method', color="darkmagenta")
        eft_variable_bin = f"{eft_variable_}_{'_'.join(current_poi.split('_')[-2:])}"
        # with uproot.open(f"/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_06_12/intermediateRun3/finalfits/PTH/Combine/runFits_chg/eft_asimov/scans/scan_{current_poi}.root") as file:
        if inclusive_:
            combine_file_path = os.path.join(combineLL_eftDir_, "scans", f"scan_{eft_variable_}.root")
        else:
            combine_file_path = os.path.join(combineLL_eftDir_, "scans", f"scan_{eft_variable_bin}.root")
        with uproot.open(combine_file_path) as file:
        # with uproot.open("/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_06_12/intermediateRun3/finalfits/PTH/Combine/runFits_chg_v1/eft_asimov/scans/scan_chg.root") as file:
            # Get the TGraphs - note that uproot reads them as pairs of arrays
            # graph = file[f"scan_{current_poi};1"]  # Replace with your TGraph name
            if inclusive_:
                graph = file[f"scan_{eft_variable_};1"]
            else:
                graph = file[f"scan_{eft_variable_bin};1"]  # Replace with your TGraph name
            # graph = file[f"scan_chg;1"]  # Replace with your TGraph name
            # Extract x and y values
            x0_points = graph.member("fX")  # Gets x values
            y0_points = graph.member("fY")  # Gets y values

        with uproot.open(os.path.join(combineLL_dir_, f"higgsCombinefirstStep_{current_poi}.MultiDimFit.mH125.38.root")) as file:
            # Get the TGraphs - note that uproot reads them as pairs of arrays
            tree = file[f"limit;1"]
            # Extract minimum value
            optimal_values_combine = tree[current_poi].array(library="np")[0]

        ax1.plot(x0_points, y0_points, 'r--', label='Full likelihood', color="black")

        print(f"SL Minimum and Crossings: {optimal_values[i]:.3f}, {find_crossings(x0_ranges[i], chi_x0_scans[i])}") 
        if print_first_order:
            print(f"Hesse Minimum and Crossings: {optimal_values_fo[i]:.3f}, {find_crossings(x0_ranges_fo[i], chi_x0_scans_fo[i])}") 
        print(f"Combine Minimum and Crossings: {optimal_values_combine}, {find_crossings(x0_points, y0_points)}")
        if inclusive_:
            ax1.set_xlabel(f"{translation[f'{eft_variable_}']}")
        else:
            ax1.set_xlabel(f"{translation[f'{eft_variable_bin}']}")
        ax1.set_ylabel('2ΔNLL')
        ax1.grid(True)
        ax1.legend()

        # ax1.set_ylim(0, 4)
        ax1.set_ylim(0, 10)
        ax1.set_xlim(range_dict[eft_variable_][0], range_dict[eft_variable_][1])

        plt.tight_layout()
        if inclusive_:
            plt.savefig(os.path.join(folder, f"chi_scan_{eft_variable_}.pdf"))
            plt.savefig(os.path.join(folder, f"chi_scan_{eft_variable_}.png"))
        else:
            plt.savefig(os.path.join(folder, f"chi_scan_{eft_variable_bin}.pdf"))
            plt.savefig(os.path.join(folder, f"chi_scan_{eft_variable_bin}.png"))

    # rho, _ = produce_rho(pois_, poi_list_, subfolder_, plot_r_distribution=plot_r_distribution)
    # plot_covariance_matrix(rho, poi_list_, folder=folder, title="Covariance Matrix (Simplified Likelihood)", output_name="covariance_matrix_sl.png")

    # covariance_df = extract_covariance_matrix(path_to_hesse_, poi_list_)
    # plot_covariance_matrix(covariance_df, poi_list_, folder=folder, title="Covariance Matrix (Hessian)", output_name="covariance_matrix_hesse.png")

def pois_untrimmed(toyDir_, poi_list_):
    pois = {}

    for current_poi in poi_list_:

        pois[current_poi] = []

    for i in range(len(glob.glob(os.path.join(toyDir_, "toy_*")))):

        if i%100==0:
            print(f"Processing fit_{i}")

        try:
            current_root_files = uproot.open(f"{toyDir_}/toy_{i}/higgsCombinefirstStep.MultiDimFit.mH125.38.root")
        except:
            print(f"Skipping fit_{i}: Required scan files not found")
            continue

        for j, current_poi in enumerate(poi_list_):

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

def pois_trimmed(toyDir_, poi_list_, trimming_value_left_, trimming_value_right_):
    pois = {}

    for current_poi in poi_list_:

        pois[current_poi] = []

    for i in range(len(glob.glob(os.path.join(toyDir_, "toy_*")))):

        if i%100==0:
            print(f"Processing fit_{i}")

        try:
            current_root_files = uproot.open(f"{toyDir_}/toy_{i}/higgsCombinefirstStep.MultiDimFit.mH125.38.root")
        except:
            print(f"Skipping fit_{i}: Required scan files not found")
            continue

        kill_event = False

        # First loop to check if there are outliers (outliers are events smaller than -4 and bigger than 4)
        for j, current_poi in enumerate(poi_list_):
            try: 
                current_tree = current_root_files["limit"]
            except:
                print(f"Skipping fit_{i}: Tree 'limit' not found in ROOT file")
                continue

            current_limit_values = current_tree[current_poi].array()

            try:
                if (current_limit_values[0] > trimming_value_right_) or (current_limit_values[0] < trimming_value_left_):
                    kill_event = True
                    break
            except:
                if j == 0:
                    print("Empty ROOT file for bootstrap: ", i)
                continue

        if kill_event:
            print(f"Skipping fit_{i} with {current_limit_values}: Outlier found")
            continue

        for j, current_poi in enumerate(poi_list_):

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

def create_json_untrimmed(variable_, toyDir_, poi_list_):
    # Loop through all fit directories (fit_0, fit_1, etc.)
    if not os.path.exists(f'pois_untrimmed_{variable_}.json'):
        pois = pois_untrimmed(toyDir_, poi_list_)
        # Save the POIs to a JSON file
        with open(f'pois_untrimmed_{variable_}.json', 'w') as f:
            json.dump(pois, f)
    else:
        # Load the POIs from the JSON file
        with open(f'pois_untrimmed_{variable_}.json', 'r') as f:
            pois = json.load(f)

    return pois

def create_json_trimmed(variable_, toyDir_, pois_untrimmed_, poi_list_, subfolder_):

    # Now we have to fit a gaussian core to all the categories to get the values where we cut. z is the number of standard deviations we want to cut away
    trimming_value_left = 0
    trimming_value_right = 0
    largest_sigma = 0
    mu_to_largest_sigma = 0
    z = 4
    for i, current_poi in enumerate(poi_list_):
        r = np.array(pois_untrimmed_[current_poi])
        mean = np.mean(r)
        s = np.std(r)

        counts, bin_edges = np.histogram(r, bins=50, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        popt, _ = curve_fit(gaus, bin_centers, counts, p0=[1, mean, s])
        amp_fit, mu_fit, sigma_fit = popt

        if i == 0:
            largest_sigma = sigma_fit
            mu_to_largest_sigma = mu_fit
        else:
            if (sigma_fit > largest_sigma):
                largest_sigma = sigma_fit
                mu_to_largest_sigma = mu_fit

        if (not os.path.exists(f"./Plots/{variable_}/{subfolder_}")) & (f"./Plots/{variable_}/{subfolder_}"!=""):
            os.makedirs(f"./Plots/{variable_}/{subfolder_}")

        plt.figure()
        plt.hist(r, bins=30, density=True, alpha=0.6, label='Histogram')
        plt.plot(bin_centers, gaus(bin_centers, *popt), color='red', label='Fitted Gaussian')
        plt.legend()
        plt.xlabel('Value')
        plt.ylabel('Density')
        plt.title('Gaussian Fit to Data Histogram')
        plt.savefig(f"./Plots/{variable_}/{subfolder_}/gaussian_fit_{current_poi}.png")
        plt.close()

    trimming_value_left = mu_to_largest_sigma - z*largest_sigma
    trimming_value_right = mu_to_largest_sigma + z*largest_sigma

    print("Trimming values: ", trimming_value_left, trimming_value_right)

    if trimming_value_left > trimming_value_right:
        trimming_value_left, trimming_value_right = trimming_value_right, trimming_value_left

    if not os.path.exists(f'pois_trimmed_{variable_}.json'):
        pois = pois_trimmed(toyDir_, poi_list_, trimming_value_left, trimming_value_right)
        # Save the POIs to a JSON file
        with open(f'pois_trimmed_{variable_}.json', 'w') as f:
            json.dump(pois, f)
    else:
        # Load the POIs from the JSON file
        with open(f'pois_trimmed_{variable_}.json', 'r') as f:
            pois = json.load(f)
    
    return pois

def plot_individual_correlation(pois_, poi_list_, variable_):

    unique_pairings = list(combinations(poi_list_, 2))

    for current_tuple in unique_pairings:
        r_1, r_2 = current_tuple

        plot_individual_correlation(pois_[r_1], pois_[r_2], r_1, r_2, np.corrcoef(pois_[r_1], pois_[r_2])[0,1], folder=f"Plots/{variable_}")

# data = {}

# # Cut away the lowest and highest 1% of the data
# proportiontocut = 0.005
# for i, current_poi in enumerate(poi_list_):
#     # data[current_poi] = stats.trimboth(pois[current_poi], proportiontocut=proportiontocut)
#     data[current_poi] = stats.trim1(pois[current_poi], proportiontocut=proportiontocut, tail="left")
#     print(f"POI: {current_poi}. Cut away {100 - 100*(len(data[current_poi]) / len(pois[current_poi]))}% of the data with {len(pois[current_poi])} entries.")
#     print(f"minimum: {min(data[current_poi])}")
#     print(f"maximum: {max(data[current_poi])}")

sample_dir = '/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_07_17_powheg/finalfits'
sample_dir = '/pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/2025_06_12/intermediateRun3/finalfits'

variables = ["PTH"]
eft_variables = ["chg", "chd", "chw", "chbox", "chl3", "cll1", "cthre", "ctwre", "chwb", "ctbre", "chb"]

for variable in variables:
    
    if variable == "PTH":
        poi_list = ["r_PTH_0p0_15p0", "r_PTH_15p0_30p0", "r_PTH_30p0_45p0", "r_PTH_45p0_80p0", "r_PTH_80p0_120p0", "r_PTH_120p0_200p0", "r_PTH_200p0_350p0", "r_PTH_350p0_10000p0"]
    elif variable == "NJ":
        poi_list = ["r_NJ_0p0_1p0", "r_NJ_1p0_2p0", "r_NJ_2p0_3p0", "r_NJ_3p0_100p0"]
    elif variable == "PTJ0":
        poi_list = ["r_PTJ0_0p0_30p0", "r_PTJ0_30p0_75p0", "r_PTJ0_75p0_120p0", "r_PTJ0_120p0_200p0", "r_PTJ0_200p0_10000p0"]

    # The paths
    main_dir = os.path.join(sample_dir, variable, "Combine", f"runFits_{variable}")
    path_to_hesse = os.path.join(main_dir, "hesse", 'robustHessefirstStep.root')
    toyDir = os.path.join(main_dir, "toyFit")
    combineLL_dir = os.path.join(main_dir, "asimov")
    
    # XS Toys
    pois_untrimmed = create_json_untrimmed(variable, toyDir, poi_list)
    pois = create_json_trimmed(variable, toyDir, pois_untrimmed, poi_list, subfolder_=f"SL_{variable}")

    for eft_variable in eft_variables:
        
        print("Processing EFT variable:", eft_variable)
        
        combineLL_eftDir = os.path.join(sample_dir, variable, "Combine", f"runFits_{eft_variable}_individual", "eft_asimov")
        subfolder = f"SL_{eft_variable}"
        
        bf_combine = produce_bf_combine(poi_list, combineLL_dir)

        produce_LLPlots(pois, poi_list, combineLL_dir, eft_variable, combineLL_eftDir, path_to_hesse, folder=f"Plots/{variable}/{subfolder}", subfolder_=subfolder, print_first_order=True, with_crossingMethod=True, bf_combine_=bf_combine, plot_r_distribution=False)
    
    # Change plotting ranges for inclusive plots
    range_dict["chb"] = [-0.0005, 0.0015]
    range_dict["chbox"] = [-0.6, 0.5]
    range_dict["chd"] = [-0.05, 0.05]
    range_dict["chg"] = [-0.15, 0.06]
    range_dict["chl3"] = [-0.25, 0.25]
    range_dict["chw"] = [-0.01, 0.04]
    range_dict["chwb"] = [-0.0025, 0.0005]
    range_dict["cll1"] = [-0.05, 0.05]
    range_dict["ctbre"] = [-0.0005, 0.0025]
    range_dict["cthre"] = [-0.8, 0.4]
    range_dict["ctwre"] = [-0.01, 0.04]
    
    for eft_variable in eft_variables:
        
        print("Processing EFT variable (inclusive):", eft_variable)
        
        bf_combine = produce_bf_combine(poi_list, combineLL_dir)
        
        combineLL_eftDir = os.path.join(sample_dir, variable, "Combine", f"runFits_{eft_variable}", "eft_asimov")
        subfolder = f"SL_{eft_variable}_inclusive"
        produce_LLPlots(pois, poi_list, combineLL_dir, eft_variable, combineLL_eftDir, path_to_hesse, folder=f"Plots/{variable}/{subfolder}", subfolder_=subfolder, print_first_order=True, with_crossingMethod=True, bf_combine_=bf_combine, inclusive_=True, plot_r_distribution=False)
