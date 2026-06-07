### Examples of command line
# python fiducial_xsec_calculator.py PATH_TO_FOLDER_WITH_ParticleLevelProcessor_OUTPUT --process all --bin '|0|0.15|0.3|0.6|0.9|2.5|' --era all --obs YH
## Without NNLOPS reweighing
# python fiducial_xsec_calculator.py /work/atarabin/HiggsDNA/prod/particleLevel/ --process ggH --bin '|0|1|2|3|100|' --era all --obs NJ --weight "genWeight"
## POWHEG
# python fiducial_xsec_calculator.py /work/atarabin/HiggsDNA/prod/particleLevel/ --process ggH --bin '|0|15|30|45|80|120|200|350|1000|' --era all --powheg
## For inclusive XS
# python fiducial_xsec_calculator.py /work/atarabin/HiggsDNA/prod/particleLevel/ --process all --bin '|0|500|' --era all
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import awkward as ak
import numpy as np
from pathlib import Path
from scipy import interpolate

"""Compute fiducial cross sections from particle-level HiggsDNA parquet outputs."""


def safe_divide(num, den):
    """Return num/den, guarding against division by zero."""
    return 0.0 if den == 0 else num / den


def evaluate_value_at_mass(values, mass_points, no_interpolation, target_mass=125.07):
    """
    Evaluate a quantity defined at discrete mass points at a desired target mass.
    If interpolation is disabled, the 125 GeV value is returned.
    """
    if not values:
        return 0.0
    if no_interpolation:
        key = "125" if "125" in values else mass_points[0]
        return values[key]
    mass_value_pairs = sorted((float(m), values[m]) for m in mass_points)
    masses, points = zip(*mass_value_pairs)
    order = min(2, len(masses) - 1)
    if order < 1:
        return points[0]
    spline = interpolate.splrep(masses, points, k=order)
    return float(interpolate.splev(target_mass, spline))


def compute_fid_xsec(in_frac, mass_points, xs_value, BR, no_interpolation, target_mass=125.07):
    """
    Compute the fiducial cross section for a given observable.

    Parameters:
      in_frac (dict): Dictionary of in-fiducial fractions keyed by mass point.
      mass_points (list): List of mass points (as strings) provided via the command line.
      xs_value (float): Cross section value from the XS map for the process.
      BR (float): Branching ratio.
      no_interpolation (bool): Flag to disable interpolation when only mass point 125 is provided.
      target_mass (float): The mass at which to evaluate the spline (default 125.07).
    
    Returns:
      float: The computed fiducial cross section.
    """
    value = evaluate_value_at_mass(in_frac, mass_points, no_interpolation, target_mass=target_mass)
    return value * xs_value * 1000 * BR


# Map modern era labels to the legacy folder suffixes used in older production campaigns.
legacy_era_map = {
    '2022preEE': 'preEE',
    '2022postEE': 'postEE',
    '2023preBPix': 'preBPix',
    '2023postBPix': 'postBPix',
}


def resolve_era_labels(path_folder, eras):
    """
    Resolve the on-disk era suffix for each requested era.

    Newer campaigns store directories with labels like ``2022preEE`` while older
    campaigns may only use the era part, e.g. ``preEE``. This helper inspects
    the input directory once and returns the suffix that should be used for each
    requested era when constructing sample paths.
    """
    available_dirs = {entry.name for entry in path_folder.iterdir() if entry.is_dir()}
    resolved_eras = {}
    for era in eras:
        legacy_era = legacy_era_map.get(era, era)
        has_year_prefixed = any(name.endswith(f'_{era}') for name in available_dirs)
        has_legacy = legacy_era != era and any(name.endswith(f'_{legacy_era}') for name in available_dirs)
        if has_year_prefixed:
            resolved_eras[era] = era
        elif has_legacy:
            resolved_eras[era] = legacy_era
            print(
                f"INFO: No directories found with era suffix '{era}' in {path_folder}. "
                f"Falling back to legacy suffix '{legacy_era}'."
            )
        else:
            resolved_eras[era] = era
    return resolved_eras


def get_available_directory_names(path_folder):
    """Return the set of directory names available in the particle-level folder."""
    return {entry.name for entry in path_folder.iterdir() if entry.is_dir()}


def infer_year_from_era(era):
    """Infer the data-taking year from an era label when possible."""
    if era == 'all':
        return None
    for year in available_years:
        if era == year or era.startswith(year):
            return year
    return None



available_processes = ['ggH', 'VBFH', 'VH', 'ttH', 'all', 'xH']
available_mass_points = ['120', '125', '130']
available_fid_selections = ['fiducialGeometricFlag', 'fiducialClassicalFlag']
available_years = ['2022', '2023', '2024']
available_eras = ['2022preEE', '2022postEE', '2023preBPix', '2023postBPix', '2024', 'all']
available_year_choices = available_years + ['all']

# Command-line interface definition.
parser = argparse.ArgumentParser(description = "Calculate the inclusive fiducial cross section of pp->H(yy)+X process(es) based on processed samples without detector-level selections. ")
parser.add_argument('path', type = str, help = "Path to the top-level folder containing the different directories. Please only run this on the output of the ParticleLevelProcessor.")
parser.add_argument('--process', type = str, choices = available_processes, default = 'ggH', help = "Please specify the process(es) for which you want to calculate the inclusive fiducial xsec.")
parser.add_argument('--mass-points', nargs='+', choices = available_mass_points, default = available_mass_points, help = "Please specify the mass points to run over. If only one single mass point of 125 is specified: No interpolation is performed.")
parser.add_argument('--fid-selection', type = str, choices = available_fid_selections, default = 'fiducialGeometricFlag', help = "Please specify the fiducial selection flag to use.")
parser.add_argument('--year', nargs='+', choices = available_year_choices, default = ['2022'], help = "Please specify one or more years to process, or 'all' to process every available year.")
parser.add_argument('--era', type = str, choices = available_eras, default = '2022postEE', help = "Please specify the era(s) that you want to run over. If you specify 'all', an inverse variance weighting is performed across the selected years.")
parser.add_argument('--bin', type = str, default = '|0|5000|', help = "Bin boundaries of the differential XS. The default")
parser.add_argument('--obs', type = str, default = 'GenPTH', help = "Name of the differential observable.")
parser.add_argument('--weight', type = str, default = 'weight', help = "Weight to use.")
parser.add_argument('--powheg', action="store_true", help="To process powheg sample.")
parser.add_argument('--per-process-output', action="store_true", help="Also store the fiducial cross sections and acceptances for each process separately.")
parser.add_argument('--workers', type = int, default = 2, help = "Number of local worker threads used to process independent samples.")
parser.add_argument('--obs2', type=str, default=None, help="Name of the second observable for 2D binning (e.g. GenNJ).")
parser.add_argument('--2d-slices', dest='slices_2d', type=str, default=None,
                    help="2D slice definitions as 'nj_lo:nj_hi:pth0,pth1,...|nj_lo:nj_hi:pth0,pth1,...'. "
                         "Each '|'-separated segment encodes one NJ slice with its PTH bin edges.")

args = parser.parse_args()


def parse_2d_slices(slices_str):
    """
    Parse a compact 2D slice string into a list of (nj_lo, nj_hi, pth_lo, pth_hi) tuples.

    Format: 'nj_lo:nj_hi:pth0,pth1,pth2,...|nj_lo:nj_hi:pth0,pth1,...'
    Each '|'-separated segment is one NJ slice; the PTH values are bin *edges*.
    """
    bins_2d = []
    for segment in slices_str.split('|'):
        parts = segment.split(':')
        nj_lo, nj_hi = float(parts[0]), float(parts[1])
        pth_edges = [float(x) for x in parts[2].split(',')]
        for i in range(len(pth_edges) - 1):
            bins_2d.append((nj_lo, nj_hi, pth_edges[i], pth_edges[i + 1]))
    return bins_2d


bins_2d = parse_2d_slices(args.slices_2d) if args.slices_2d is not None else None
obs2_name = args.obs2  # None in 1D mode


# When only one mass point is requested, only the 125 GeV sample is allowed and
# no interpolation is needed later on.
if len(args.mass_points) == 1:
    if args.mass_points[0] != '125':
        parser.error("When specifying a single mass point, only '125' is allowed.")
    no_interpolation = True
else:
    no_interpolation = False

if args.workers < 1:
    parser.error("--workers must be at least 1.")

if 'all' in args.year and len(args.year) != 1:
    parser.error("--year accepts either 'all' or one or more concrete years, not both.")

if args.fid_selection == 'fiducialGeometricFlag':
    print('INFO: Using the geometric fiducial flag for the selection.')
elif args.fid_selection == 'fiducialClassicalFlag':
    print('INFO: Using the classical fiducial flag for the selection.')

# Convert simple CLI inputs into the arrays used by the main loop.
path_folder = Path(args.path)
if args.process == 'all':
    processes = [p for p in available_processes if p not in ('all', 'xH')]
elif args.process == 'xH':
    processes = ['VBFH', 'VH', 'ttH']
else:
    processes = [args.process]
inferred_year = infer_year_from_era(args.era)
requested_years = list(available_years) if args.year == ['all'] else args.year
if inferred_year is not None:
    if requested_years != [inferred_year]:
        print(f"INFO: Inferring year {inferred_year} from era {args.era}.")
    selected_years = [inferred_year]
else:
    selected_years = requested_years
# Expand the requested eras. `all` now means all concrete eras across the selected years.
if args.era == 'all':
    eras = [e for year in selected_years for e in available_eras if e != 'all' and e.startswith(year)]
else:
    eras = [args.era] if inferred_year is not None else []
resolved_era_labels = resolve_era_labels(path_folder, eras)
available_directory_names = get_available_directory_names(path_folder)

# Parse the differential observable binning from the CLI string.
obs_bins = [float(num) for num in args.bin.strip("|").split("|")]

# Reference cross sections, in picobarn.
# 13p6 values correspond to 125.07 GeV and are used for the final fiducial
# cross section normalisation after the acceptance extraction.
XS_map = {'13':   {'ggH': 48.58, 'VBFH': 3.782, 'VH': 2.2569, 'ttH': 0.5071},
         '13p6': {'ggH': 51.96, 'VBFH': 4.067, 'VH': 2.3781, 'ttH': 0.5638},
         '14':   {'ggH': 54.67, 'VBFH': 4.278, 'VH': 2.4991, 'ttH': 0.6137},}

XS_map_scale_up = {'13':   {},
                   '13p6': {'ggH': 53.98644, 'VBFH': 4.087335, 'VH': 2.3376723, 'ttH': 0.597628},
                   '14':   {},}

XS_map_scale_dn = {'13':   {},
                   '13p6': {'ggH': 49.93356, 'VBFH': 4.054799, 'VH': 2.4185277, 'ttH': 0.5113666},
                   '14':   {},}

XS_map_pdf_up = {'13':   {},
                   '13p6': {'ggH': 52.94724, 'VBFH': 4.152407, 'VH': 2.4137715, 'ttH': 0.580714},
                   '14':   {},}

XS_map_pdf_dn = {'13':   {},
                   '13p6': {'ggH': 50.97276, 'VBFH': 3.981593, 'VH': 2.3424285, 'ttH': 0.546886},
                   '14':   {},}

XS_map_alphaS_up = {'13':   {},
                   '13p6': {'ggH': 53.31096, 'VBFH': 4.087335, 'VH': 2.3995029, 'ttH': 0.575076},
                   '14':   {},}

XS_map_alphaS_dn = {'13':   {},
                    '13p6': {'ggH': 50.60904, 'VBFH': 4.046665, 'VH': 2.3566971, 'ttH': 0.552524},
                    '14':   {},}


def combine_acceptances(process_acceptances):
    """
    Combine per-process acceptances into a single inclusive acceptance.

    The weighting uses the nominal 13.6 TeV production cross sections so that
    the inclusive acceptance is consistent with the final inclusive fiducial
    cross section obtained by summing over processes.
    """
    total_sigma = 0.0
    weighted_sum = 0.0
    for process, acc in process_acceptances.items():
        sigma = XS_map['13p6'].get(process, 0.0)
        total_sigma += sigma
        weighted_sum += sigma * acc
    return safe_divide(weighted_sum, total_sigma)


# Mapping between the analysis-level process labels and the folder naming
# convention used by the particle-level production.
processMap = {'2022': 
                {'ggH':  'GluGluHtoGG',
                 'VBFH': 'VBFHtoGG',
                 'VH':   'VHtoGG',
                 'ttH':   'ttHtoGG'},
              '2023':
                {'ggH':  'GluGluHtoGG',
                 'VBFH': 'VBFHto2G',
                 'VH':   'VHto2G',
                 'ttH':   'ttHtoGG'},
              '2024':
                {'ggH':  'GluGluHtoGG',
                 'VBFH': 'VBFHto2G',
                 'VH':   'VHto2G',
                 'ttH':   'ttHtoGG'}
            }

# Physics constants and systematic weight bookkeeping.
BR = 0.2270/100 # SM value for mH close to 125: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
mass_points = args.mass_points # The fiducial acceptance is interpolated to 125.07 GeV unless only mH=125 is requested.
# For POWHEG only the 125 GeV sample is available, so all requested mass points
# are redirected to the same input directory.
mass_powheg = {120:125, 125:125, 130:125}
scale_weight_indices = [0, 1, 3, 5, 7, 8]
pdf_weight_indices = list(range(1, 101))
alpha_weight_map = {'alpha_up': 101, 'alpha_dn': 102}
alpha_keys = list(alpha_weight_map.keys())
scale_weight_fields = [f'LHEScaleWeight_{idx}' for idx in scale_weight_indices]
pdf_weight_fields = [f'LHEPdfWeight_{idx}' for idx in pdf_weight_indices]
alpha_weight_fields = {key: f'LHEPdfWeight_{idx}' for key, idx in alpha_weight_map.items()}


def build_parquet_columns(args, obs2_name=None):
    """
    Return the minimal set of parquet columns needed for one run.

    The speed-critical part of the script is parquet I/O. Restricting the read
    to the observable, selection flag, nominal weight, and the requested
    systematic weights avoids loading unrelated kinematic columns.
    """
    columns = {args.fid_selection, args.obs, args.weight}
    if obs2_name is not None:
        columns.add(obs2_name)
    columns.update(scale_weight_fields)
    columns.update(pdf_weight_fields)
    columns.update(alpha_weight_fields.values())
    return sorted(columns)


def initialize_mass_accumulator(n_bins):
    """
    Create the accumulator used for one process/mass combination.

    The script now processes each sample once and fills all bins in one pass.
    These arrays store the running denominators and numerators for the nominal
    acceptance and all supported systematic variations.
    """
    return {
        'nom_den': 0.0,
        'nom_num': np.zeros(n_bins),
        'scale_den': np.zeros(len(scale_weight_indices)),
        'scale_num': np.zeros((len(scale_weight_indices), n_bins)),
        'pdf_den': np.zeros(len(pdf_weight_indices)),
        'pdf_num': np.zeros((len(pdf_weight_indices), n_bins)),
        'alpha_den': np.zeros(len(alpha_keys)),
        'alpha_num': np.zeros((len(alpha_keys), n_bins)),
    }


def merge_accumulators(target, source):
    """
    Merge one sample-local accumulator into the process/mass accumulator.

    Thread workers build their own independent accumulators. The main thread
    combines them afterwards to keep the reduction deterministic and avoid any
    shared-state mutation from multiple threads.
    """
    target['nom_den'] += source['nom_den']
    target['nom_num'] += source['nom_num']
    target['scale_den'] += source['scale_den']
    target['scale_num'] += source['scale_num']
    target['pdf_den'] += source['pdf_den']
    target['pdf_num'] += source['pdf_num']
    target['alpha_den'] += source['alpha_den']
    target['alpha_num'] += source['alpha_num']


def get_process_name_candidates(year, process):
    """
    Return acceptable directory-name prefixes for one logical process.

    Some productions use ``...toGG`` while others use ``...to2G`` for the same
    process. The first candidate keeps the nominal year-based preference from
    ``processMap`` and the remaining candidates act as fallbacks.
    """
    preferred_name = processMap[year][process]
    candidates = [preferred_name]
    if "toGG" in preferred_name:
        candidates.append(preferred_name.replace("toGG", "to2G"))
    if "to2G" in preferred_name:
        candidates.append(preferred_name.replace("to2G", "toGG"))
    return list(dict.fromkeys(candidates))


def build_process_path(path_folder, year, process, mass, resolved_era, args, available_dir_names):
    """
    Construct the parquet directory path for a given process, mass, and era.

    Besides the preferred process label from ``processMap``, this helper also
    accepts ``GG``/``2G`` naming aliases when probing the input directory.
    """
    if args.powheg:
        return path_folder / f"{processMap[year][process]}_M-{mass_powheg[int(mass)]}_powheg"

    for process_name in get_process_name_candidates(year, process):
        directory_name = f"{process_name}_M-{mass}_{resolved_era}"
        if directory_name in available_dir_names:
            return path_folder / directory_name

    raise FileNotFoundError(
        f"Could not find a sample directory for process={process}, mass={mass}, era={resolved_era}. "
        f"Tried prefixes: {get_process_name_candidates(year, process)}"
    )


def build_bin_masks(fid_flag, observable, obs_bins):
    """
    Build one fiducial mask per observable bin for the current sample.

    If the binning contains any negative edge (e.g. MassJ0J1 sentinel bin
    [-1000, 0)), the signed observable is used for every bin. This prevents
    double-counting: without this, abs(-999)=999 would leak into positive bins
    such as [500, 1000). When all edges are non-negative, abs(observable) is
    used so that symmetric distributions fold correctly.
    """
    eff_observable = observable if any(e < 0 for e in obs_bins) else abs(observable)
    bin_masks = []
    for b in range(len(obs_bins) - 1):
        mask = fid_flag & (eff_observable >= obs_bins[b]) & (eff_observable < obs_bins[b + 1])
        bin_masks.append(mask)
    return bin_masks


def build_2d_bin_masks(fid_flag, obs_pth, obs_nj, bins_2d):
    """
    Build one fiducial mask per (NJ slice, PTH bin) pair for 2D binning.

    Each element of bins_2d is a (nj_lo, nj_hi, pth_lo, pth_hi) tuple.
    NJ uses strict integer equality logic: nj_lo <= GenNJ < nj_hi.
    """
    return [
        fid_flag & (obs_nj >= nj_lo) & (obs_nj < nj_hi) & (obs_pth >= pth_lo) & (obs_pth < pth_hi)
        for nj_lo, nj_hi, pth_lo, pth_hi in bins_2d
    ]


def accumulate_sample(accumulator, arr, args, obs_bins, bins_2d=None, obs2_name=None):
    """
    Fold one loaded parquet sample into the running accumulators.

    All bin masks are built once from the in-memory sample and then reused for
    the nominal, scale, PDF, and alphaS weighted sums. This is the core speedup
    compared with the old bin-by-bin reload pattern.
    """
    weights = arr[args.weight]
    fid_flag = arr[args.fid_selection] == True
    if bins_2d is not None:
        obs_pth = arr[args.obs]
        obs_nj  = arr[obs2_name]
        bin_masks = build_2d_bin_masks(fid_flag, obs_pth, obs_nj, bins_2d)
    else:
        observable = arr[args.obs]
        bin_masks = build_bin_masks(fid_flag, observable, obs_bins)
    masked_weights = [weights[mask] for mask in bin_masks]

    accumulator['nom_den'] += float(ak.sum(weights))
    for b, weight_slice in enumerate(masked_weights):
        accumulator['nom_num'][b] += float(ak.sum(weight_slice))

    for i, field in enumerate(scale_weight_fields):
        scale_weight = arr[field]
        accumulator['scale_den'][i] += float(ak.sum(weights * scale_weight))
        for b, mask in enumerate(bin_masks):
            accumulator['scale_num'][i, b] += float(ak.sum(masked_weights[b] * scale_weight[mask]))

    for i, field in enumerate(pdf_weight_fields):
        pdf_weight = arr[field]
        accumulator['pdf_den'][i] += float(ak.sum(weights * pdf_weight))
        for b, mask in enumerate(bin_masks):
            accumulator['pdf_num'][i, b] += float(ak.sum(masked_weights[b] * pdf_weight[mask]))

    for i, key in enumerate(alpha_keys):
        alpha_weight = arr[alpha_weight_fields[key]]
        accumulator['alpha_den'][i] += float(ak.sum(weights * alpha_weight))
        for b, mask in enumerate(bin_masks):
            accumulator['alpha_num'][i, b] += float(ak.sum(masked_weights[b] * alpha_weight[mask]))


def compute_sample_contribution(process, mass, era, resolved_era, path_folder, sample_year, args, obs_bins, n_bins, parquet_columns, available_dir_names, bins_2d=None, obs2_name=None):
    """
    Load one sample and compute its full contribution to all observable bins.

    This is the unit of work submitted to the thread pool. Each worker returns
    a fresh accumulator for one (process, mass, era) combination, which is then
    merged in the main thread.
    """
    process_string = build_process_path(path_folder, sample_year, process, mass, resolved_era, args, available_dir_names)
    arr = ak.from_parquet(str(process_string), columns=parquet_columns)
    accumulator = initialize_mass_accumulator(n_bins)
    accumulate_sample(accumulator, arr, args, obs_bins, bins_2d=bins_2d, obs2_name=obs2_name)
    return process, mass, era, accumulator


def finalize_mass_acceptances(accumulator):
    """
    Convert raw accumulated sums into per-bin acceptances.

    The output contains one acceptance array per uncertainty prescription for a
    single process/mass combination. Interpolation across Higgs mass points is
    performed later, once all requested masses have been processed.
    """
    nominal = np.array([safe_divide(num, accumulator['nom_den']) for num in accumulator['nom_num']])

    scale_acceptances = np.array([
        [safe_divide(num, accumulator['scale_den'][i]) for num in accumulator['scale_num'][i]]
        for i in range(len(scale_weight_indices))
    ])
    pdf_acceptances = np.array([
        [safe_divide(num, accumulator['pdf_den'][i]) for num in accumulator['pdf_num'][i]]
        for i in range(len(pdf_weight_indices))
    ])
    alpha_acceptances = np.array([
        [safe_divide(num, accumulator['alpha_den'][i]) for num in accumulator['alpha_num'][i]]
        for i in range(len(alpha_keys))
    ])

    pdf_uncertainty = np.sqrt(np.sum(np.square(pdf_acceptances - nominal), axis=0))
    return {
        'nom': nominal,
        'scale_up': np.max(scale_acceptances, axis=0) if len(scale_acceptances) else nominal,
        'scale_dn': np.min(scale_acceptances, axis=0) if len(scale_acceptances) else nominal,
        'pdf_up': nominal + pdf_uncertainty,
        'pdf_dn': nominal - pdf_uncertainty,
        'alpha_up': alpha_acceptances[0] if len(alpha_acceptances) else nominal,
        'alpha_dn': alpha_acceptances[1] if len(alpha_acceptances) > 1 else nominal,
    }


def interpolate_acceptances_per_bin(mass_acceptances, acceptance_key, mass_points, no_interpolation, n_bins):
    """
    Interpolate one acceptance type across Higgs mass points, bin by bin.

    For each observable bin, the acceptance values at the available mass points
    are evaluated at 125.07 GeV using the same spline logic as in the original
    implementation.
    """
    interpolated = np.zeros(n_bins)
    for b in range(n_bins):
        values = {mass: mass_acceptances[mass][acceptance_key][b] for mass in mass_points}
        interpolated[b] = evaluate_value_at_mass(values, mass_points, no_interpolation)
    return interpolated

# Containers for the final per-bin outputs written to stdout and the output file.
fid_xsecs_per_bin = {}
fid_xsecs_per_bin_scale_up = {}
fid_xsecs_per_bin_scale_dn = {}
fid_xsecs_per_bin_pdf_up = {}
fid_xsecs_per_bin_pdf_dn = {}
fid_xsecs_per_bin_alpha_up = {}
fid_xsecs_per_bin_alpha_dn = {}
acc_per_bin = {}
acc_per_bin_scale_up = {}
acc_per_bin_scale_dn = {}
acc_per_bin_pdf_up = {}
acc_per_bin_pdf_dn = {}
acc_per_bin_alpha_up = {}
acc_per_bin_alpha_dn = {}
n_bins = len(bins_2d) if bins_2d is not None else len(obs_bins) - 1
parquet_columns = build_parquet_columns(args, obs2_name=obs2_name)
mass_accumulators = {
    process: {mass: initialize_mass_accumulator(n_bins) for mass in mass_points}
    for process in processes
}

# Main reduction step:
# build one task per independent sample and process those tasks in a local
# thread pool. Each task loads its parquet directory once and fills all bins.
sample_tasks = []
for process in processes:
    print(f'INFO: Now extracting fraction of in-fiducial events for process {process} ...')
    for mass in mass_points:
        print(f'INFO: Scheduling sample tasks for mass {mass}...')
        for era in eras:
            sample_year = infer_year_from_era(era)
            if sample_year is None:
                parser.error(f"Could not infer a year from era '{era}'.")
            sample_tasks.append((process, mass, era, sample_year, resolved_era_labels[era]))

with ThreadPoolExecutor(max_workers=args.workers) as executor:
    futures = {
        executor.submit(
            compute_sample_contribution,
            process,
            mass,
            era,
            resolved_era,
            path_folder,
            sample_year,
            args,
            obs_bins,
            n_bins,
            parquet_columns,
            available_directory_names,
            bins_2d,
            obs2_name,
        ): (process, mass, era)
        for process, mass, era, sample_year, resolved_era in sample_tasks
    }

    for future in as_completed(futures):
        process, mass, era = futures[future]
        try:
            _, _, _, sample_accumulator = future.result()
        except Exception as exc:
            raise RuntimeError(
                f"Failed to process sample for process={process}, mass={mass}, era={era}"
            ) from exc
        merge_accumulators(mass_accumulators[process][mass], sample_accumulator)
        print(f"INFO: Finished sample for process {process}, mass {mass}, and era {era}.")

# Turn the raw sums into acceptances for each process/mass combination.
mass_acceptances = {
    process: {mass: finalize_mass_acceptances(mass_accumulators[process][mass]) for mass in mass_points}
    for process in processes
}

# Interpolate the mass-dependent acceptances to 125.07 GeV for each bin.
acceptance_keys = ['nom', 'scale_up', 'scale_dn', 'pdf_up', 'pdf_dn', 'alpha_up', 'alpha_dn']
process_acceptance_arrays = {process: {} for process in processes}
for process in processes:
    for acceptance_key in acceptance_keys:
        process_acceptance_arrays[process][acceptance_key] = interpolate_acceptances_per_bin(
            mass_acceptances[process],
            acceptance_key,
            args.mass_points,
            no_interpolation,
            n_bins,
        )

# Convert acceptances into fiducial cross section arrays using the fixed theory
# normalisation maps defined above.
process_fid_xsec_arrays = {process: {} for process in processes}
for process in processes:
    process_fid_xsec_arrays[process]['fidXS'] = process_acceptance_arrays[process]['nom'] * XS_map['13p6'][process] * 1000 * BR
    process_fid_xsec_arrays[process]['fidXS_scale_up'] = process_acceptance_arrays[process]['scale_up'] * XS_map_scale_up['13p6'][process] * 1000 * BR
    process_fid_xsec_arrays[process]['fidXS_scale_dn'] = process_acceptance_arrays[process]['scale_dn'] * XS_map_scale_dn['13p6'][process] * 1000 * BR
    process_fid_xsec_arrays[process]['fidXS_pdf_up'] = process_acceptance_arrays[process]['pdf_up'] * XS_map_pdf_up['13p6'][process] * 1000 * BR
    process_fid_xsec_arrays[process]['fidXS_pdf_dn'] = process_acceptance_arrays[process]['pdf_dn'] * XS_map_pdf_dn['13p6'][process] * 1000 * BR
    process_fid_xsec_arrays[process]['fidXS_alpha_up'] = process_acceptance_arrays[process]['alpha_up'] * XS_map_alphaS_up['13p6'][process] * 1000 * BR
    process_fid_xsec_arrays[process]['fidXS_alpha_dn'] = process_acceptance_arrays[process]['alpha_dn'] * XS_map_alphaS_dn['13p6'][process] * 1000 * BR

if args.per_process_output:
    fid_keys = ['fidXS', 'fidXS_scale_up', 'fidXS_scale_dn', 'fidXS_pdf_up', 'fidXS_pdf_dn', 'fidXS_alpha_up', 'fidXS_alpha_dn']
    acc_key_map = {
        'Acc': 'nom',
        'Acc_scale_up': 'scale_up',
        'Acc_scale_dn': 'scale_dn',
        'Acc_pdf_up': 'pdf_up',
        'Acc_pdf_dn': 'pdf_dn',
        'Acc_alpha_up': 'alpha_up',
        'Acc_alpha_dn': 'alpha_dn',
    }
    per_process_fid_xsecs = {
        key: {process: process_fid_xsec_arrays[process][key].tolist() for process in processes}
        for key in fid_keys
    }
    per_process_acc = {
        key: {process: process_acceptance_arrays[process][acc_key_map[key]].tolist() for process in processes}
        for key in acc_key_map
    }
else:
    per_process_fid_xsecs = {}
    per_process_acc = {}

# Human-readable label per bin used in print statements below.
if bins_2d is not None:
    bin_labels = [f"NJ∈[{nj_lo},{nj_hi}), PTH∈[{pth_lo},{pth_hi})" for nj_lo, nj_hi, pth_lo, pth_hi in bins_2d]
else:
    bin_labels = [f"[{obs_bins[b]},{obs_bins[b+1]}]" for b in range(n_bins)]

# Report and store the final per-bin inclusive outputs.
for b in range(n_bins):
    fid_xsecs_per_bin_process = {process: process_fid_xsec_arrays[process]['fidXS'][b] for process in processes}
    fid_xsecs_per_bin_process_scale_up = {process: process_fid_xsec_arrays[process]['fidXS_scale_up'][b] for process in processes}
    fid_xsecs_per_bin_process_scale_dn = {process: process_fid_xsec_arrays[process]['fidXS_scale_dn'][b] for process in processes}
    fid_xsecs_per_bin_process_pdf_up = {process: process_fid_xsec_arrays[process]['fidXS_pdf_up'][b] for process in processes}
    fid_xsecs_per_bin_process_pdf_dn = {process: process_fid_xsec_arrays[process]['fidXS_pdf_dn'][b] for process in processes}
    fid_xsecs_per_bin_process_alpha_up = {process: process_fid_xsec_arrays[process]['fidXS_alpha_up'][b] for process in processes}
    fid_xsecs_per_bin_process_alpha_dn = {process: process_fid_xsec_arrays[process]['fidXS_alpha_dn'][b] for process in processes}

    acc_per_bin_process = {process: process_acceptance_arrays[process]['nom'][b] for process in processes}
    acc_per_bin_process_scale_up = {process: process_acceptance_arrays[process]['scale_up'][b] for process in processes}
    acc_per_bin_process_scale_dn = {process: process_acceptance_arrays[process]['scale_dn'][b] for process in processes}
    acc_per_bin_process_pdf_up = {process: process_acceptance_arrays[process]['pdf_up'][b] for process in processes}
    acc_per_bin_process_pdf_dn = {process: process_acceptance_arrays[process]['pdf_dn'][b] for process in processes}
    acc_per_bin_process_alpha_up = {process: process_acceptance_arrays[process]['alpha_up'][b] for process in processes}
    acc_per_bin_process_alpha_dn = {process: process_acceptance_arrays[process]['alpha_dn'][b] for process in processes}

    fid_xsecs_per_bin[b] = np.sum(np.asarray([fid_xsecs_per_bin_process[process] for process in processes]))
    print(f"The fiducial cross section for {args.obs} in {bin_labels[b]} is: {fid_xsecs_per_bin[b]} fb")

    fid_xsecs_per_bin_scale_up[b] = np.sum(np.asarray([fid_xsecs_per_bin_process_scale_up[process] for process in processes]))
    print(f"The fiducial cross section (scale_up) for {args.obs} in {bin_labels[b]} is: {fid_xsecs_per_bin_scale_up[b]} fb")

    fid_xsecs_per_bin_scale_dn[b] = np.sum(np.asarray([fid_xsecs_per_bin_process_scale_dn[process] for process in processes]))
    print(f"The fiducial cross section (scale_dn) for {args.obs} in {bin_labels[b]} is: {fid_xsecs_per_bin_scale_dn[b]} fb")

    fid_xsecs_per_bin_pdf_up[b] = np.sum(np.asarray([fid_xsecs_per_bin_process_pdf_up[process] for process in processes]))
    print(f"The fiducial cross section (pdf_up) for {args.obs} in {bin_labels[b]} is: {fid_xsecs_per_bin_pdf_up[b]} fb")

    fid_xsecs_per_bin_pdf_dn[b] = np.sum(np.asarray([fid_xsecs_per_bin_process_pdf_dn[process] for process in processes]))
    print(f"The fiducial cross section (pdf_dn) for {args.obs} in {bin_labels[b]} is: {fid_xsecs_per_bin_pdf_dn[b]} fb")

    fid_xsecs_per_bin_alpha_up[b] = np.sum(np.asarray([fid_xsecs_per_bin_process_alpha_up[process] for process in processes]))
    print(f"The fiducial cross section (alpha_up) for {args.obs} in {bin_labels[b]} is: {fid_xsecs_per_bin_alpha_up[b]} fb")

    fid_xsecs_per_bin_alpha_dn[b] = np.sum(np.asarray([fid_xsecs_per_bin_process_alpha_dn[process] for process in processes]))
    print(f"The fiducial cross section (alpha_dn) for {args.obs} in {bin_labels[b]} is: {fid_xsecs_per_bin_alpha_dn[b]} fb")

    acc_per_bin[b] = combine_acceptances(acc_per_bin_process)
    print(f"The acceptance for {args.obs} in {bin_labels[b]} at 125.07 GeV is: {acc_per_bin[b]}")

    acc_per_bin_scale_up[b] = combine_acceptances(acc_per_bin_process_scale_up)
    print(f"The acceptance (scale_up) for {args.obs} in {bin_labels[b]} at 125.07 GeV is: {acc_per_bin_scale_up[b]}")

    acc_per_bin_scale_dn[b] = combine_acceptances(acc_per_bin_process_scale_dn)
    print(f"The acceptance (scale_dn) for {args.obs} in {bin_labels[b]} at 125.07 GeV is: {acc_per_bin_scale_dn[b]}")

    acc_per_bin_pdf_up[b] = combine_acceptances(acc_per_bin_process_pdf_up)
    print(f"The acceptance (pdf_up) for {args.obs} in {bin_labels[b]} at 125.07 GeV is: {acc_per_bin_pdf_up[b]}")

    acc_per_bin_pdf_dn[b] = combine_acceptances(acc_per_bin_process_pdf_dn)
    print(f"The acceptance (pdf_dn) for {args.obs} in {bin_labels[b]} at 125.07 GeV is: {acc_per_bin_pdf_dn[b]}")

    acc_per_bin_alpha_up[b] = combine_acceptances(acc_per_bin_process_alpha_up)
    print(f"The acceptance (alpha_up) for {args.obs} in {bin_labels[b]} at 125.07 GeV is: {acc_per_bin_alpha_up[b]}")

    acc_per_bin_alpha_dn[b] = combine_acceptances(acc_per_bin_process_alpha_dn)
    print(f"The acceptance (alpha_dn) for {args.obs} in {bin_labels[b]} at 125.07 GeV is: {acc_per_bin_alpha_dn[b]}")


# Sum the bin-wise values to obtain the inclusive fiducial cross sections.
final_fid_xsec = np.sum(np.asarray([fid_xsecs_per_bin[b] for b in range(len(obs_bins)-1)]))
print(f"The inclusive fiducial cross section is given by: {final_fid_xsec} fb")

final_fid_xsec_scale_up = np.sum(np.asarray([fid_xsecs_per_bin_scale_up[b] for b in range(len(obs_bins)-1)]))
print(f"The inclusive fiducial cross section (scale up) is given by: {final_fid_xsec_scale_up} fb")

final_fid_xsec_scale_dn = np.sum(np.asarray([fid_xsecs_per_bin_scale_dn[b] for b in range(len(obs_bins)-1)]))
print(f"The inclusive fiducial cross section (scale dn) is given by: {final_fid_xsec_scale_dn} fb")

final_fid_xsec_pdf_up = np.sum(np.asarray([fid_xsecs_per_bin_pdf_up[b] for b in range(len(obs_bins)-1)]))
print(f"The inclusive fiducial cross section (pdf_up) is given by: {final_fid_xsec_pdf_up} fb")

final_fid_xsec_pdf_dn = np.sum(np.asarray([fid_xsecs_per_bin_pdf_dn[b] for b in range(len(obs_bins)-1)]))
print(f"The inclusive fiducial cross section (pdf_dn) is given by: {final_fid_xsec_pdf_dn} fb")

final_fid_xsec_alpha_up = np.sum(np.asarray([fid_xsecs_per_bin_alpha_up[b] for b in range(len(obs_bins)-1)]))
print(f"The inclusive fiducial cross section (alpha_up) is given by: {final_fid_xsec_alpha_up} fb")

final_fid_xsec_alpha_dn = np.sum(np.asarray([fid_xsecs_per_bin_alpha_dn[b] for b in range(len(obs_bins)-1)]))
print(f"The inclusive fiducial cross section (alpha_dn) is given by: {final_fid_xsec_alpha_dn} fb")

if bins_2d is not None:
    output_obs = f"{args.obs[3:] if args.obs.startswith('Gen') else args.obs}vs{obs2_name[3:] if obs2_name.startswith('Gen') else obs2_name}"
else:
    output_obs = args.obs
    if output_obs.startswith("Gen"):
        output_obs = output_obs[3:]

output = 'fidXS_'+output_obs+'_'+args.process
if args.powheg: output += '_powheg'
if args.weight != "weight": output += '_'+args.weight

def _fl(d):
    """Convert dict values to plain Python floats for clean output."""
    return [float(v) for v in d.values()]

# Write a compact Python file that can be imported directly by downstream plots.
with open(output+'.py', 'w') as f:
        f.write('Boundaries = '+str(list(bins_2d) if bins_2d is not None else obs_bins)+' \n')
        f.write('fidXS = '+str(_fl(fid_xsecs_per_bin))+' \n')
        f.write('fidXS_scale_up = '+str(_fl(fid_xsecs_per_bin_scale_up))+' \n')
        f.write('fidXS_scale_dn = '+str(_fl(fid_xsecs_per_bin_scale_dn))+' \n')
        f.write('fidXS_pdf_up = '+str(_fl(fid_xsecs_per_bin_pdf_up))+' \n')
        f.write('fidXS_pdf_dn = '+str(_fl(fid_xsecs_per_bin_pdf_dn))+' \n')
        f.write('fidXS_alpha_up = '+str(_fl(fid_xsecs_per_bin_alpha_up))+' \n')
        f.write('fidXS_alpha_dn = '+str(_fl(fid_xsecs_per_bin_alpha_dn))+' \n')
        f.write('Acc = '+str(_fl(acc_per_bin))+' \n')
        f.write('Acc_scale_up = '+str(_fl(acc_per_bin_scale_up))+' \n')
        f.write('Acc_scale_dn = '+str(_fl(acc_per_bin_scale_dn))+' \n')
        f.write('Acc_pdf_up = '+str(_fl(acc_per_bin_pdf_up))+' \n')
        f.write('Acc_pdf_dn = '+str(_fl(acc_per_bin_pdf_dn))+' \n')
        f.write('Acc_alpha_up = '+str(_fl(acc_per_bin_alpha_up))+' \n')
        f.write('Acc_alpha_dn = '+str(_fl(acc_per_bin_alpha_dn))+' \n')
        if args.per_process_output:
            for process in processes:
                f.write(f'fidXS_{process} = {per_process_fid_xsecs["fidXS"][process]} \n')
                f.write(f'fidXS_scale_up_{process} = {per_process_fid_xsecs["fidXS_scale_up"][process]} \n')
                f.write(f'fidXS_scale_dn_{process} = {per_process_fid_xsecs["fidXS_scale_dn"][process]} \n')
                f.write(f'fidXS_pdf_up_{process} = {per_process_fid_xsecs["fidXS_pdf_up"][process]} \n')
                f.write(f'fidXS_pdf_dn_{process} = {per_process_fid_xsecs["fidXS_pdf_dn"][process]} \n')
                f.write(f'fidXS_alpha_up_{process} = {per_process_fid_xsecs["fidXS_alpha_up"][process]} \n')
                f.write(f'fidXS_alpha_dn_{process} = {per_process_fid_xsecs["fidXS_alpha_dn"][process]} \n')
                f.write(f'Acc_{process} = {per_process_acc["Acc"][process]} \n')
                f.write(f'Acc_scale_up_{process} = {per_process_acc["Acc_scale_up"][process]} \n')
                f.write(f'Acc_scale_dn_{process} = {per_process_acc["Acc_scale_dn"][process]} \n')
                f.write(f'Acc_pdf_up_{process} = {per_process_acc["Acc_pdf_up"][process]} \n')
                f.write(f'Acc_pdf_dn_{process} = {per_process_acc["Acc_pdf_dn"][process]} \n')
                f.write(f'Acc_alpha_up_{process} = {per_process_acc["Acc_alpha_up"][process]} \n')
                f.write(f'Acc_alpha_dn_{process} = {per_process_acc["Acc_alpha_dn"][process]} \n')
