import uproot
import os
import glob
import matplotlib.pyplot as plt
import mplhep as hep
from scipy import stats
import numpy as np
from scipy.optimize import minimize
from scipy.stats import moment

def coefficients(_m1, _m2ii, _m3):
    # Eq 2.9: coefficient a
    c = -np.sign(_m3) * np.sqrt(2*_m2ii) * np.cos( (4*np.pi/3) + (1/3)*np.arctan( np.sqrt(8*_m2ii**3/_m3**2 - 1) ) )
    
    # Eq 2.10: coefficient b
    b = np.sqrt(_m2ii - 2*c**2)
    
    # Eq 2.11: coefficient c
    a = _m1 - c
        
    return a, b, c

def rho(_ci, _cj, _bi, _bj, _m2ij, _m2ii, _m2jj):
    rho_ii = (1/(4*_ci*_ci)) * (np.sqrt((_bi*_bi)**2 + 8*_ci*_ci*_m2ii) - _bi*_bi)
    rho_jj = (1/(4*_cj*_cj)) * (np.sqrt((_bj*_bj)**2 + 8*_cj*_cj*_m2jj) - _bj*_bj)
    rho_ij = (1/(4*_ci*_cj)) * (np.sqrt((_bi*_bj)**2 + 8*_ci*_cj*_m2ij) - _bi*_bj)

    # Create 2x2 matrix
    rho_matrix = np.array([[rho_ii, rho_ij],
                           [rho_ij, rho_jj]])  # Note: rho_ji = rho_ij (symmetric matrix)
    return rho_matrix

def chi(x, _a_high, _b_high, _c_high, _a_low, _b_low, _c_low, _rho):
    chi_high = (np.sqrt(_b_high**2 - 4*(_a_high-x[0])*_c_high) - _b_high) / (2*_c_high)
    chi_low = (np.sqrt(_b_low**2 - 4*(_a_low-x[1])*_c_low) - _b_low) / (2*_c_low)

    chi_high_meas = (np.sqrt(_b_high**2 - 4*(_a_high-1.821)*_c_high) - _b_high) / (2*_c_high)
    chi_low_meas = (np.sqrt(_b_low**2 - 4*(_a_low-0.803)*_c_low) - _b_low) / (2*_c_low)

    chi_vector = np.array([[chi_high_meas - chi_high],
                           [chi_low_meas - chi_low]])
    return chi_vector.T @ _rho @ chi_vector

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

# Define the base directory path
base_dir = "/work/niharrin/CMSSW_14_1_0_pre4/src/flashggFinalFit/output/2025_01_20_intermediateNTuples_2023/PTH_bootstrap/Combine/runFits_PTH/dataFit"

r_high_name = "r_PTH_80p0_120p0"
r_low_name = "r_PTH_120p0_200p0"

r_high = []
r_low = []

# Loop through all fit directories (fit_0, fit_1, etc.)
for i in range(len(glob.glob(os.path.join(base_dir, "bootstrap_*")))):

    # Check if both required files exist
    # high_scan_file = f"{base_dir}/bootstrap_{i}/scan_ggH_high_{i}.root"
    # low_scan_file = f"{base_dir}/bootstrap_{i}/scan_ggH_low_{i}.root"
    # if not (os.path.exists(high_scan_file) and os.path.exists(low_scan_file)):
    #     print(f"Skipping fit_{i}: Required scan files not found")
    #     continue

    # Find all MultiDimFit ROOT files in this directory
    root_files_high = uproot.open(f"{base_dir}/bootstrap_{i}/higgsCombineDataPostFitBestFit_{r_high_name}.MultiDimFit.mH125.38.root")
    root_files_low = uproot.open(f"{base_dir}/bootstrap_{i}/higgsCombineDataPostFitBestFit_{r_low_name}.MultiDimFit.mH125.38.root")

    tree_high = root_files_high["limit"]
    tree_low = root_files_low["limit"]

    limit_values_high = tree_high[r_high_name].array()
    limit_values_low = tree_low[r_low_name].array()

    if limit_values_low[0]<-4:
        print(limit_values_low[0])
        print(i)

    r_high.append(limit_values_high[0])
    r_low.append(limit_values_low[0])
    if i==1000:
        break


plt.style.use(hep.style.CMS)
plt.figure(figsize=(10, 6))
plt.scatter(r_high, r_low)
plt.xlabel(r_high_name)
plt.ylabel(r_low_name)
plt.savefig("r_high_vs_r_low.pdf", bbox_inches='tight')
plt.show()


# Convert to numpy arrays for easier computation
r_high = np.array(r_high)
r_low = np.array(r_low)

# 1. Mean values
mean_high = np.mean(r_high)
mean_low = np.mean(r_low)

# 2. Covariance matrix
cov_matrix = np.cov((r_high, r_low))

# 3. Diagonal components of the third moment
# Computing E[(X - μ)³]
third_moment_high = np.mean((r_high - mean_high)**3)
third_moment_low = np.mean((r_low - mean_low)**3)

a_high, b_high, c_high = coefficients(mean_high, cov_matrix[0,0], third_moment_high)
a_low, b_low, c_low = coefficients(mean_low, cov_matrix[1,1], third_moment_low)

rho_high_low = rho(c_high, c_low, b_high, b_low, cov_matrix[0,1], cov_matrix[0,0], cov_matrix[1,1])

x0 = np.array([1., 1.])
res = minimize(chi, x0, args=(a_high, b_high, c_high, a_low, b_low, c_low, rho_high_low))

# Get optimal values from minimization
optimal_x0, optimal_x1 = res.x

# Create a grid of points
x0_0_range = np.linspace(-10, 10, 100)  # Adjust range as needed
x0_1_range = np.linspace(-10, 10, 100)  # Adjust range as needed

# Calculate chi values for x0 scan (keeping x1 fixed at optimal value)
chi_x0_scan = np.array([float(chi(np.array([x0, optimal_x1]), 
                           a_high, b_high, c_high, 
                           a_low, b_low, c_low, 
                           rho_high_low)) for x0 in x0_0_range])
# Calculate chi values for x1 scan (keeping x0 fixed at optimal value)
chi_x1_scan = np.array([float(chi(np.array([optimal_x0, x1]), 
                           a_high, b_high, c_high, 
                           a_low, b_low, c_low, 
                           rho_high_low)) for x1 in x0_1_range])

    
# Find crossing points at for 68% interval 
crossings_x0 = find_crossings(x0_0_range, chi_x0_scan)
crossings_x1 = find_crossings(x0_1_range, chi_x1_scan)
print('crossings_x0', crossings_x0-optimal_x0)
print('crossings_x1', crossings_x1-optimal_x1)

# Create plots
plt.style.use(hep.style.CMS)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# # Plot x0 scan
# ax1.plot(x0_0_range, chi_x0_scan, label='Simplified likelihood')
# with uproot.open("scan_ggH_high.root") as file:
#     # Get the TGraphs - note that uproot reads them as pairs of arrays
#     graph = file["scan_ggH_high"]  # Replace with your TGraph name
#     # Extract x and y values
#     x0_points = graph.member("fX")  # Gets x values
#     y0_points = graph.member("fY")  # Gets y values
# ax1.plot(x0_points, y0_points, 'r--', label='Combine likelihood')
# ax1.set_xlabel('r_high')
# ax1.set_ylabel('2ΔNLL')
# ax1.grid(True)
# ax1.set_ylim(0, max(y0_points))
# ax1.axvline(optimal_x0, color='grey', linestyle='--', label=f'Minimum: {optimal_x0:.3f}')
# ax1.legend()

# # Plot x1 scan
# ax2.plot(x0_1_range, chi_x1_scan, label='Simplified likelihood')
# with uproot.open("scan_ggH_low.root") as file:
#     # Get the TGraphs - note that uproot reads them as pairs of arrays
#     graph = file["scan_ggH_low"]  # Replace with your TGraph name
#     # Extract x and y values
#     x0_points = graph.member("fX")  # Gets x values
#     y0_points = graph.member("fY")  # Gets y values
# ax2.plot(x0_points, y0_points, 'r--', label='Combine likelihood')
# ax2.set_xlabel('r_low')
# ax2.set_ylabel('2ΔNLL')
# ax2.grid(True)
# ax2.set_ylim(0, max(y0_points))
# ax2.set_xlim(min(x0_points), max(x0_points))
# ax2.axvline(optimal_x1, color='grey', linestyle='--', label=f'Minimum: {optimal_x1:.3f}')
# ax2.legend()

# plt.tight_layout()
# plt.savefig("chi_scans.pdf")
# plt.show()

# Print results
print("\nMean values:")
print(f"{r_high_name}: {mean_high:.3f}")
print(f"{r_low_name}: {mean_low:.3f}")

print("\nCovariance matrix:")
print(cov_matrix)

print("\nDiagonal components of third moment:")
print(f"{r_high_name}: {third_moment_high:.3f}")
print(f"{r_low_name}: {third_moment_low:.3f}")
