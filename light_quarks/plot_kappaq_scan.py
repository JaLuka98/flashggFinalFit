#!/usr/bin/env python3
"""
Plot the NLL scan from the light-quark expected limit.
Supports both old inclusive outputs with a kappa_q_sq branch and newer
outputs with a kappa_q branch.

Usage:
    python3 light_quarks/plot_kappaq_scan.py
    python3 light_quarks/plot_kappaq_scan.py --mode differential
    python3 light_quarks/plot_kappaq_scan.py --input path/to/higgsCombine.root
"""

import argparse
import glob
import os
import sys
import numpy as np

os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib-light-quarks')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

INCLUSIVE_OUTPUT_DIR = (
    '/net/data_cms3a-1/daumann/PhD/Final_fits_repo/'
    'CMSSW_14_1_0_pre4/src/flashggFinalFit/'
    'output_Zmmg_SaS_opt_bound/2024_inclusive/LightQuarks_limits_kappaq'
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FLASHGG_DIR = os.path.dirname(SCRIPT_DIR)
DIFFERENTIAL_OUTPUT_DIR = os.path.join(
    FLASHGG_DIR,
    'outputs_run2_bins_20_04_2026',
    'output_2024_PTH_htcondor_out_fiducial',
    'LightQuarks_limits_kappaq_PTH',
)

DEFAULT_FILES = {
    'inclusive': os.path.join(
        INCLUSIVE_OUTPUT_DIR,
        'higgsCombineLightQuarks_2022_expected.MultiDimFit.mH125.38.root',
    ),
    'differential': os.path.join(
        DIFFERENTIAL_OUTPUT_DIR,
        'higgsCombineLightQuarks_2024_PTH_expected.MultiDimFit.mH125.38.root',
    ),
}

DEFAULT_TITLES = {
    'inclusive': '',
    'differential': '',
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--mode',
        choices=['auto', 'inclusive', 'differential'],
        default='auto',
        help='Which default output to plot. auto prefers differential if present.',
    )
    parser.add_argument(
        '--input',
        default=None,
        help='Explicit higgsCombine ROOT file to plot.',
    )
    parser.add_argument(
        '--output-dir',
        default=None,
        help='Directory for kappaq_expected_scan.pdf/png. Defaults to input file directory.',
    )
    parser.add_argument(
        '--title',
        default=None,
        help='Override plot title.',
    )
    parser.add_argument(
        '--poi',
        choices=['auto', 'kappa_q', 'kappa_s', 'kappa_u', 'kappa_d', 'kappa_q_sq'],
        default='auto',
        help='POI branch to plot. auto tries kappa_q, kappa_s, kappa_u, kappa_d, then kappa_q_sq.',
    )
    parser.add_argument(
        '--cms-label',
        default='Internal',
        help='Text shown next to the CMS label.',
    )
    parser.add_argument(
        '--lumi',
        default=r'61.9 fb$^{-1}$ (13.6 TeV)',
        help='Luminosity label shown above the plot.',
    )
    parser.add_argument(
        '--y-max',
        type=float,
        default=8.0,
        help='Maximum y-axis value.',
    )
    parser.add_argument(
        '--y-cut',
        type=float,
        default=20.0,
        help='Remove scan points with -2 delta ln L above this value before interpolation.',
    )
    return parser.parse_args()


def choose_input(args):
    if args.input:
        return args.input, args.mode

    if args.mode == 'auto':
        for mode in ['differential', 'inclusive']:
            if os.path.exists(DEFAULT_FILES[mode]):
                return DEFAULT_FILES[mode], mode
        return DEFAULT_FILES['differential'], 'differential'

    return DEFAULT_FILES[args.mode], args.mode


args = parse_args()
FNAME, MODE = choose_input(args)
OUTPUT_DIR = args.output_dir or os.path.dirname(FNAME)
TITLE = args.title or DEFAULT_TITLES.get(MODE, DEFAULT_TITLES['differential'])

# --------------------------------------------------------------------------
# Read scan from ROOT file (uproot, no CMSSW needed)
# --------------------------------------------------------------------------
try:
    import uproot
except ImportError:
    sys.exit('ERROR: uproot not available. Run: pip install uproot')

def input_files_for_scan(path):
    if os.path.isdir(path):
        split_files = sorted(glob.glob(os.path.join(path, 'higgsCombine*.POINTS.*.root')))
        if split_files:
            return split_files
        files = sorted(glob.glob(os.path.join(path, 'higgsCombine*.root')))
        return [f for f in files if not os.path.basename(f).startswith('merged_')]

    if not os.path.exists(path):
        sys.exit('ERROR: ROOT file not found:\n  %s' % path)

    return [path]


input_files = input_files_for_scan(FNAME)
if not input_files:
    sys.exit('ERROR: no higgsCombine ROOT files found for input:\n  %s' % FNAME)

first_tree = uproot.open(input_files[0])['limit']
keys = set(first_tree.keys())

required = ['deltaNLL', 'quantileExpected']
missing = [key for key in required if key not in keys]
if missing:
    sys.exit('ERROR: missing branch(es) in %s: %s' % (input_files[0], ', '.join(missing)))

POI_LABELS = {
    'kappa_q': r'$\bar{\kappa}_{q}$',
    'kappa_s': r'$\bar{\kappa}_{s}$',
    'kappa_u': r'$\bar{\kappa}_{u}$',
    'kappa_d': r'$\bar{\kappa}_{d}$',
    'kappa_q_sq': r'$|\bar{\kappa}_{q}|$',
}
POI_ANNOTATION_LABELS = {
    'kappa_q': r'\bar{\kappa}_{q}',
    'kappa_s': r'\bar{\kappa}_{s}',
    'kappa_u': r'\bar{\kappa}_{u}',
    'kappa_d': r'\bar{\kappa}_{d}',
    'kappa_q_sq': r'|\bar{\kappa}_{q}|',
}

if args.poi == 'auto':
    x_branch = None
    for candidate in ['kappa_q', 'kappa_s', 'kappa_u', 'kappa_d', 'kappa_q_sq']:
        if candidate in keys:
            x_branch = candidate
            break
    if x_branch is None:
        sys.exit(
            'ERROR: no supported kappa branch found in %s.\nAvailable branches: %s' %
            (input_files[0], ', '.join(first_tree.keys()))
        )
elif args.poi in keys:
    x_branch = args.poi
else:
    sys.exit(
        'ERROR: requested POI branch %s not found in %s.\nAvailable branches: %s' %
        (args.poi, input_files[0], ', '.join(first_tree.keys()))
    )

if x_branch == 'kappa_q_sq':
    x_branch = 'kappa_q_sq'
    x_label = POI_LABELS[x_branch]
else:
    x_label = POI_LABELS[x_branch]

scan_chunks = []
for input_file in input_files:
    tree = uproot.open(input_file)['limit']
    arrays = tree.arrays([x_branch, 'deltaNLL', 'quantileExpected'], library='np')
    if x_branch == 'kappa_q_sq':
        kappa_q_plot = np.sqrt(np.maximum(arrays[x_branch], 0.0))
    else:
        kappa_q_plot = arrays[x_branch]
    scan_chunks.append(np.column_stack((
        kappa_q_plot,
        arrays['deltaNLL'],
        arrays['quantileExpected'],
    )))

scan = np.concatenate(scan_chunks)

print('Reading: %s' % FNAME)
if len(input_files) > 1:
    print('Using split scan files: %d' % len(input_files))
print('Using branch: %s' % x_branch)

print('=== Raw scan entries ===')
print('  %14s  %14s  %17s' % (x_branch + '_plot', 'deltaNLL', 'quantileExpected'))
for x_val, dnll_val, q_val in scan:
    print('  %14.6g  %14.6g  %17.6g' % (x_val, dnll_val, q_val))
print()

# --------------------------------------------------------------------------
# Build scan points. Combine writes a separate continuous best-fit row with
# quantileExpected = -1 in each split output. Keep that row for the annotation,
# but do not blindly add it to the interpolation if it is essentially on top of
# a grid point. Near-duplicate x values make cubic splines overshoot badly.
# --------------------------------------------------------------------------
grid_points = scan[scan[:, 2] > -0.5]
best_fit_rows = scan[scan[:, 2] <= -0.5]

scan_points = grid_points
best_fit = None
if len(best_fit_rows):
    best_fit_row = best_fit_rows[np.argmin(best_fit_rows[:, 1])]
    best_fit = best_fit_row[0]
    if len(grid_points):
        grid_x = np.sort(np.unique(grid_points[:, 0]))
        positive_spacings = np.diff(grid_x)
        positive_spacings = positive_spacings[positive_spacings > 0]
        grid_step = positive_spacings.min() if len(positive_spacings) else 1.0
        close_to_grid = np.min(np.abs(grid_x - best_fit)) < max(1e-5, 1e-4 * grid_step)
        if not close_to_grid:
            scan_points = np.vstack((scan_points, best_fit_row))
    else:
        scan_points = best_fit_rows

scan_points = scan_points[np.argsort(scan_points[:, 0])]

if len(scan_points) < 2:
    sys.exit('ERROR: need at least two scan points to plot; found %d' % len(scan_points))

kappa_arr = scan_points[:, 0]
two_dnll  = 2.0 * scan_points[:, 1]

# Keep a single point per x value, taking the lowest NLL when duplicates exist.
unique_points = {}
for x_val, y_val in zip(kappa_arr, two_dnll):
    if x_val not in unique_points or y_val < unique_points[x_val]:
        unique_points[x_val] = y_val
kappa_arr = np.array(sorted(unique_points.keys()))
two_dnll = np.array([unique_points[x_val] for x_val in kappa_arr])
two_dnll -= two_dnll.min()

keep = two_dnll <= args.y_cut
if keep.sum() >= 2:
    kappa_arr = kappa_arr[keep]
    two_dnll = two_dnll[keep]

# --------------------------------------------------------------------------
# Shape-preserving interpolation for the curve and crossings. A plain cubic
# spline can invent bumps between sparse scan points, especially when the
# likelihood is flat or symmetric around zero.
# --------------------------------------------------------------------------
kappa_fine = np.linspace(kappa_arr.min(), kappa_arr.max(), 2000)
try:
    from scipy.interpolate import PchipInterpolator
    scan_spline = PchipInterpolator(kappa_arr, two_dnll)
    dnll_fine = np.maximum(scan_spline(kappa_fine), 0)
except ImportError:
    print('WARNING: scipy not available, falling back to linear interpolation.')
    dnll_fine = np.maximum(np.interp(kappa_fine, kappa_arr, two_dnll), 0)

# --------------------------------------------------------------------------
# Find 95% and 68% CL crossings on the interpolated curve
# --------------------------------------------------------------------------
def find_crossings(x, y, level):
    crossings = []
    for i in range(len(y) - 1):
        if y[i] == level:
            crossings.append(x[i])
            continue
        if (y[i] - level) * (y[i + 1] - level) < 0:
            frac = (level - y[i]) / (y[i + 1] - y[i])
            crossings.append(x[i] + frac * (x[i + 1] - x[i]))
    if len(y) and y[-1] == level:
        crossings.append(x[-1])
    return crossings

crossings_68 = find_crossings(kappa_fine, dnll_fine, 1.00)
crossings_95 = find_crossings(kappa_fine, dnll_fine, 4.00)

print('68%% CL crossings: %s' % str(['%.3f' % c for c in crossings_68]))
print('95%% CL crossings: %s' % str(['%.3f' % c for c in crossings_95]))
if best_fit is not None:
    print('Best-fit point: %.6g' % best_fit)

def central_interval(crossings, best_fit):
    if len(crossings) < 2:
        return None
    lows = [c for c in crossings if c <= best_fit]
    highs = [c for c in crossings if c >= best_fit]
    if not lows or not highs:
        return None
    return max(lows), min(highs)

# --------------------------------------------------------------------------
# Plot
# --------------------------------------------------------------------------
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    'font.size': 16,
    'axes.linewidth': 1.2,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.major.size': 7,
    'ytick.major.size': 7,
    'xtick.minor.size': 4,
    'ytick.minor.size': 4,
})

fig, ax = plt.subplots(figsize=(7, 7))
fig.subplots_adjust(left=0.15, right=0.96, bottom=0.13, top=0.91)

ax.plot(kappa_fine, dnll_fine, color='black', linewidth=2.8,
        label='Expected')
ax.plot(kappa_arr, two_dnll, 'o', color='black', markersize=4.5, zorder=3)

for yval in [1.0, 4.0]:
    ax.axhline(yval, color='0.55', linestyle='--', linewidth=1.2, zorder=0)

for xc in crossings_68:
    ax.vlines(xc, 0, 1.0, color='0.55', linestyle='--', linewidth=1.0, zorder=0)
for xc in crossings_95:
    ax.vlines(xc, 0, 4.0, color='0.55', linestyle='--', linewidth=1.0, zorder=0)

ax.text(0.985, 1.012, args.lumi, transform=ax.transAxes,
        ha='right', va='bottom', fontsize=17)
ax.text(0.000, 1.005, 'CMS', transform=ax.transAxes,
        ha='left', va='bottom', fontsize=30, fontweight='bold')
if args.cms_label:
    ax.text(0.205, 1.006, args.cms_label, transform=ax.transAxes,
            ha='left', va='bottom', fontsize=23, style='italic')

if best_fit is None:
    best_idx = np.argmin(two_dnll)
    best_fit = kappa_arr[best_idx]
interval_68 = central_interval(crossings_68, best_fit)
interval_95 = central_interval(crossings_95, best_fit)
limit_lines = []
if interval_68 is not None:
    lo68, hi68 = interval_68
    limit_lines.append(
        r'$%s^{\mathrm{Exp.}} = %.3f^{+%.3f}_{-%.3f}$' %
        (POI_ANNOTATION_LABELS[x_branch], best_fit, hi68 - best_fit, best_fit - lo68)
    )
    limit_lines.append(r'$68\%%\,\mathrm{CL}: [%.3f,\, %.3f]$' % (lo68, hi68))
if interval_95 is not None:
    lo95, hi95 = interval_95
    limit_lines.append(r'$95\%%\,\mathrm{CL}: [%.3f,\, %.3f]$' % (lo95, hi95))
if limit_lines:
    ax.text(0.53, 0.84, '\n'.join(limit_lines), transform=ax.transAxes,
            ha='left', va='top', fontsize=14, linespacing=1.35)

ax.text(0.965, 1.0, r'$1\sigma$', transform=ax.get_yaxis_transform(),
        ha='right', va='bottom', color='0.35', fontsize=15)
ax.text(0.965, 4.0, r'$2\sigma$', transform=ax.get_yaxis_transform(),
        ha='right', va='bottom', color='0.35', fontsize=15)

ax.set_xlabel(x_label, fontsize=22)
ax.set_ylabel(r'$-2\,\Delta\ln L$', fontsize=22)
ax.tick_params(axis='both', which='major', labelsize=18)
if TITLE:
    ax.text(0.03, 0.92, TITLE, transform=ax.transAxes,
            ha='left', va='top', fontsize=12)
ax.set_xlim(kappa_arr.min(), kappa_arr.max())
ax.set_ylim(bottom=0, top=args.y_max)
ax.legend(loc='upper left', bbox_to_anchor=(0.03, 0.79),
          frameon=False, fontsize=15, handlelength=2.4)
ax.minorticks_on()

for spine in ax.spines.values():
    spine.set_linewidth(1.2)

os.makedirs(OUTPUT_DIR, exist_ok=True)
out_pdf = os.path.join(OUTPUT_DIR, 'kappaq_expected_scan.pdf')
out_png = os.path.join(OUTPUT_DIR, 'kappaq_expected_scan.png')
plt.savefig(out_pdf)
plt.savefig(out_png)
print('Saved: %s' % out_pdf)
print('Saved: %s' % out_png)
