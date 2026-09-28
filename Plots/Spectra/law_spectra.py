import law
import os, sys
import matplotlib.pyplot as plt
import ROOT
import re
import uproot
from collections import OrderedDict as od
import glob, shutil
import errno
import yaml

from functools import partial
import CombineHarvester.CombineTools.plotting as plot
from six.moves import range

import pandas
import numpy as np
import mplhep as hep

# Use CMS style from mplhep for plotting
plt.style.use(hep.style.CMS)

from commonTools import *
from commonObjects import *

from Combine.law_combine import *

from framework import Task
from framework import HTCondorWorkflow, SlurmWorkflow

HIGGS_MASS = "125.07"

# Function to safely create a directory
def safe_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def leave():
  print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ HGG TREES 2 WS (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  exit(0)
  
def convert_boolean_string(string):
    if (string == "True") or (string == "true") or (string == True):
        return True
    else:
        return False

class CreateDiffSpectra(law.Task):#(law.Task): #(Task, HTCondorWorkflow, law.LocalWorkflow):
    """Create a differential cross-section spectrum in the fiducial phase space.

    Subclasses can select another cross-section family written by the theory-input
    producer by overriding ``cross_section_prefix`` and ``spectrum_output_stem``.
    """

    phase_space = "fiducial"
    cross_section_prefix = "fidXS"
    cross_section_label = r"\text{fid}"
    spectrum_output_stem = "spectra"
    upper_panel_scale = 1.0

    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default='', description="Variable to be used for output folder naming")
    year = law.Parameter(default='2022', description="Year")
    is_unblinded = law.Parameter(default=False, description="Flag that signifies if spectrum is created for the unblinded results.")
    log_x = law.Parameter(default=False, description="Use a logarithmic x axis for the spectrum.")

    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    batch_system = law.Parameter(default="slurm", description="Batch system to use")

    # htcondor_job_kwargs_submit = {"spool": True}  

    def _spectrum_output_names(self):
        suffix = "" if convert_boolean_string(self.is_unblinded) else "_blinded"
        scale_suffix = "_logx" if convert_boolean_string(self.log_x) else ""
        stem = self.spectrum_output_stem + scale_suffix + suffix
        return [f"{stem}.pdf", f"{stem}.png"]

    def _cross_section(self, module, source=None):
        attribute = self.cross_section_prefix
        if source is not None:
            attribute += f"_{source}"
        try:
            return np.asarray(getattr(module, attribute), dtype=float)
        except AttributeError as exc:
            raise AttributeError(
                f"Theory input module '{module.__name__}' does not define "
                f"'{attribute}', required by {self.__class__.__name__}."
            ) from exc

    def _phase_space_text(self, value):
        """Adapt fiducial labels from the shared plot config for this task."""
        if self.cross_section_prefix == "fidXS" or not isinstance(value, str):
            return value
        text = (
            value.replace(r"\sigma_{\text{fid}}", r"\sigma_{\text{tot}}")
            .replace(r"\sigma_{fid}", r"\sigma_{tot}")
        )
        if self.upper_panel_scale == 1e-3:
            text = text.replace("fb", "pb")
        return text

    def _spectra_config(self, config):
        """Return common spectrum settings with the selected phase-space overrides."""
        spectra_config = config["spectra"]
        current_config = {
            key: value
            for key, value in spectra_config.items()
            if key not in ("fiducial", "total")
        }
        current_config.update(spectra_config.get(self.phase_space, {}))
        return current_config

    def _generator_dependence_uncertainty(self, current_config, number_of_bins):
        """Load the relative generator-dependence uncertainty for total measurements."""
        if self.phase_space == "fiducial":
            return np.zeros(number_of_bins, dtype=float)

        uncertainty_config = current_config.get("generator_dependence_uncertainty")
        if uncertainty_config is None:
            raise KeyError(
                "The total spectrum requires 'spectra.total."
                "generator_dependence_uncertainty' in the analysis config."
            )

        module_name = uncertainty_config["module"]
        attribute = uncertainty_config["attribute"]
        module = __import__(module_name, globals(), locals(), [attribute])
        try:
            relative_uncertainty = np.asarray(getattr(module, attribute), dtype=float)
        except AttributeError as exc:
            raise AttributeError(
                f"Generator-dependence module '{module_name}' does not define "
                f"the configured attribute '{attribute}'."
            ) from exc

        if relative_uncertainty.ndim != 1 or len(relative_uncertainty) != number_of_bins:
            raise ValueError(
                f"Generator-dependence uncertainty '{module_name}.{attribute}' has "
                f"{len(relative_uncertainty)} bins, but the spectrum has {number_of_bins}."
            )
        if not np.all(np.isfinite(relative_uncertainty)) or np.any(relative_uncertainty < 0):
            raise ValueError(
                f"Generator-dependence uncertainty '{module_name}.{attribute}' "
                "must contain finite, non-negative values."
            )

        return relative_uncertainty
    
    def requires(self):
        
        tasks = {}
        
        if self.variable == '':
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_inclusive.yml")
        else:
            configYamlPath = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")
        
        #Load central config file
        with open(configYamlPath, 'r') as file:
            config = yaml.safe_load(file)
        
        if self.output_dir == '':
            output_dir = config['outputFolder']
        else:
            output_dir = self.output_dir
            
        if convert_boolean_string(self.is_unblinded):
            hesseConfig = config["combine_hesse"]
            tasks["PValueCalculation"] = PValueCalculation(variable=self.variable, output_dir=output_dir, year=self.year, batch_flavor=self.batch_flavor, version=self.variable if self.variable != '' else 'inclusive', workflow=self.batch_system, slurm_partition=hesseConfig['batchPartition'], slurm_memory=hesseConfig['batchMemory'], slurm_max_runtime=hesseConfig['batchMaxRuntime'], htcondor_partition=hesseConfig['batchPartition'], htcondor_memory=hesseConfig['batchMemory'], htcondor_max_runtime=hesseConfig['batchMaxRuntime'])
            tasks["CreateUnblindedFit"] = CreateUnblindedFit(variable=self.variable, output_dir=output_dir, year=self.year, batch_flavor=self.batch_flavor, version=self.variable if self.variable != "" else "inclusive", workflow=self.batch_system)
        else:
            tasks["CreateAsimovFit"] = CreateAsimovFit(variable=self.variable, output_dir=output_dir, year=self.year, batch_flavor=self.batch_flavor, version=self.variable if self.variable != '' else 'inclusive', workflow=self.batch_system)
        
        return tasks
    
    def create_branch_map(self):
        # map branch indexes to ascii numbers from 97 to 122 ("a" to "z")

        branch_map = {i: current_branch for i, current_branch in enumerate([0])}
        return branch_map

    def output(self):
        # current_mode_proc_mass = self.branch_data
        
        # returns output folder
        if self.variable == '':
            input_config = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_inclusive.yml")
        else:
            input_config = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")
        
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)

        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
        
        outputFileTargets = []
        
        if self.variable == '':
            fitFolderName = f'runFits_mu_fiducial'
            output = [] 
        else:
            fitFolderName = f'runFits_{self.variable}'
            output = [
                os.path.join(output_dir, 'Combine', fitFolderName, name)
                for name in self._spectrum_output_names()
            ]
            
        for current_output in output:
            outputFileTargets.append(law.LocalFileTarget(current_output))        
        return outputFileTargets

    def run(self):
        
        # current_mode_proc_mass = self.branch_data
        
        # returns output folder
        if self.variable == '':
            input_config = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_inclusive.yml")
        else:
            input_config = os.path.join(os.environ["ANALYSIS_PATH"],"config",f"{self.year}_{self.variable}.yml")
        
        with open(input_config, 'r') as file:
            config = yaml.safe_load(file)

        if self.output_dir == '':
            output_dir = config["outputFolder"]
        else:
            output_dir = self.output_dir
        
        
        def read(scan, param, files, ycut):
            goodfiles = [f for f in files if plot.TFileIsGood(f)]
            limit = plot.MakeTChain(goodfiles, 'limit')
            graph = plot.TGraphFromTree(limit, param, '2*deltaNLL', 'quantileExpected > -1.5')
            graph.SetName(scan)
            graph.Sort()
            plot.RemoveGraphXDuplicates(graph)
            plot.RemoveGraphYAbove(graph, ycut)
            # graph.Print()
            return graph    


        def Eval(obj, x, params):
            return obj.Eval(x[0])


        def BuildScan(param, files, yvals, ycut):
            graph = read('1', param, files, ycut)
            if graph.GetN() <= 1:
                graph.Print()
                raise RuntimeError(f'Attempting to build {param} scan from TGraph with zero or one point (see above)')
            
            bestfit = None
            for i in range(graph.GetN()):
                if graph.GetY()[i] == 0.:
                    bestfit = graph.GetX()[i]
            
            spline = ROOT.TSpline3("spline3", graph)
            
            # Incrementally build the function name using a counter passed as a parameter
            func_method = partial(Eval, spline)
            func_name = f'splinefn_{param}'
            func = ROOT.TF1(func_name, func_method, graph.GetX()[0], graph.GetX()[graph.GetN() - 1], 1)
            func._method = func_method
            func.SetLineWidth(3)

            assert bestfit is not None
            crossings = {}
            cross_1sig = None
            cross_2sig = None
            other_1sig = []
            other_2sig = []
            val = None
            val_2sig = None

            # Find crossings for the 1-sigma and 2-sigma levels
            for yval in yvals:
                crossings[yval] = plot.FindCrossingsWithSpline(graph, func, yval)
                for cr in crossings[yval]:
                    cr["contains_bf"] = cr["lo"] <= bestfit and cr["hi"] >= bestfit
            
            # Process 1-sigma crossings
            for cr in crossings[yvals[0]]:
                if cr['contains_bf']:
                    val = (bestfit, cr['hi'] - bestfit, cr['lo'] - bestfit)
                    cross_1sig = cr
                else:
                    other_1sig.append(cr)
            
            # Process 2-sigma crossings
            if len(yvals) > 1:
                for cr in crossings[yvals[1]]:
                    if cr['contains_bf']:
                        val_2sig = (bestfit, cr['hi'] - bestfit, cr['lo'] - bestfit)
                        cross_2sig = cr
                    else:
                        other_2sig.append(cr)
            else:
                val_2sig = (0., 0., 0.)
                cross_2sig = cross_1sig

            return {
                "graph": graph,
                "spline": spline,
                "func": func,
                "crossings": crossings,
                "val": val,
                "val_2sig": val_2sig,
                "cross_1sig": cross_1sig,
                "cross_2sig": cross_2sig,
                "other_1sig": other_1sig,
                "other_2sig": other_2sig
            }

        # 1 sigma, 2 sigma
        yvals = [1., 4.]
        
        rounding_to_digits = 3
        # Remove points with y > y-cut
        y_cut = 7.
        
        if self.variable == '':
            # Spectra with only one POI does not make any sense
            print("Variable is not set. Please set the variable parameter to a valid value.")
            exit(1)
        else:
            cat_list = combineVariableDict(self.variable, self.year)['paramStrNoOne'] #has to be in the correct order
            fitFolderName = f'runFits_{self.variable}'
            
            oneSigmaDict = {}
            stat_up_list = []
            stat_down_list = []
            
            exp_xs_list = []
            err_up_list = []
            err_down_list = []
            for cat in cat_list:
                # oneSigmaDict[f'{cat}'] = {}
                
                if convert_boolean_string(self.is_unblinded):
                    main_scan_syst = BuildScan(cat, [os.path.join(output_dir, 'Combine', fitFolderName, 'dataFit', f'higgsCombineDataPostFitScanFit_{cat}.MultiDimFit.mH{HIGGS_MASS}.root')], yvals, y_cut)
                    main_scan_stat = BuildScan(cat, [os.path.join(output_dir, 'Combine', fitFolderName, 'dataFit', f'higgsCombineDataPostFitScanStat_{cat}.MultiDimFit.mH{HIGGS_MASS}.root')], yvals, y_cut)
                    
                    pvalue_path = os.path.join(output_dir, 'Combine', fitFolderName, 'pvalue.txt')
                    
                    with open(pvalue_path, 'r') as file:
                        pvalue = file.readline()
                    
                else:
                    main_scan_syst = BuildScan(cat, [os.path.join(output_dir, 'Combine', fitFolderName, 'asimov', f'higgsCombineAsimovPostFitScanFit_{cat}.root')], yvals, y_cut)
                    main_scan_stat = BuildScan(cat, [os.path.join(output_dir, 'Combine', fitFolderName, 'asimov', f'higgsCombineAsimovPostFitScanStat_{cat}.root')], yvals, y_cut)
                    
                    pvalue = 1
                
                stat_up_list.append(abs(round(main_scan_stat['val'][1],rounding_to_digits)))
                stat_down_list.append(abs(round(main_scan_stat['val'][2],rounding_to_digits)))
                
                exp_xs_list.append(round(main_scan_syst['val'][0],rounding_to_digits))
                err_up_list.append(abs(round(main_scan_syst['val'][1],rounding_to_digits)))
                err_down_list.append(abs(round(main_scan_syst['val'][2],rounding_to_digits)))
                
        # print(exp_xs_list)
        # print(err_up_list)
        # print(err_down_list)
        # print(stat_up_list)
        # print(stat_down_list)
        
            
        current_config = self._spectra_config(config)
        upper_panel_scale = self.upper_panel_scale
        plot_log_x = convert_boolean_string(self.log_x)
        plot_x_lim = (
            current_config.get('x_lim_log', current_config['x_lim'])
            if plot_log_x
            else current_config['x_lim']
        )
        if plot_log_x and plot_x_lim[0] <= 0:
            raise ValueError("A logarithmic x axis requires a positive lower x limit.")

        xs = {}

        # List of variables to import
        vars = [
            self.cross_section_prefix,
            f'{self.cross_section_prefix}_scale_up',
            f'{self.cross_section_prefix}_scale_dn',
            f'{self.cross_section_prefix}_pdf_up',
            f'{self.cross_section_prefix}_pdf_dn',
            f'{self.cross_section_prefix}_alpha_up',
            f'{self.cross_section_prefix}_alpha_dn',
            'Boundaries',
        ]
        
        # Dynamically import the required module for ggH cross-section
        ggh_xs = __import__(current_config['ggh_xs'], globals(), locals(), vars)
        bins = ggh_xs.Boundaries
        plot_2d_as_1d = current_config.get("plot_2d_as_1d", False)
        if plot_2d_as_1d:
            bins_plot = [0.0]
            bins_c = []
            bin_w = []
            bin_w_plot = []
            group_key = None
            group_index = -1
            overflow_edges = current_config.get("pthvsnj_overflow_edges", [])
            overflow_threshold = current_config.get("pthvsnj_overflow_threshold", 9999.0)
            panel_width = current_config.get("pthvsnj_panel_width", None)
            group_offset = 0.0
            group_scale = 1.0

            for boundary in bins:
                nj_low, nj_high, pt_low, pt_high = boundary
                current_group_key = (nj_low, nj_high)
                if current_group_key != group_key:
                    group_key = current_group_key
                    group_index += 1
                    if panel_width is not None:
                        group_offset = group_index * panel_width
                        group_scale = panel_width / overflow_edges[group_index]
                    else:
                        group_offset = bins_plot[-1] - pt_low
                        group_scale = 1.0

                pt_high_plot = pt_high
                if pt_high >= overflow_threshold and group_index < len(overflow_edges):
                    pt_high_plot = overflow_edges[group_index]

                bins_plot.append(group_offset + pt_high_plot * group_scale)
                bins_c.append(group_offset + 0.5 * (pt_low + pt_high_plot) * group_scale)
                bin_w.append(pt_high_plot - pt_low)
                bin_w_plot.append((pt_high_plot - pt_low) * group_scale)

            bins_plot = np.array(bins_plot, dtype=float)
            bins_c = np.array(bins_c, dtype=float)
            bin_w = np.array(bin_w, dtype=float)
            bin_w_plot = np.array(bin_w_plot, dtype=float)
        else:
            bins_plot = np.array(bins)
            if "overflow" in current_config.keys(): bins_plot[-1] = current_config['overflow']
            # If first_bin_center <= 0, clip the left edge of bins_plot to x_lim start
            # so the underflow bin histogram bar and its transition line are completely hidden.
            if current_config.get('first_bin_center', 1) <= 0:
                bins_plot[0] = current_config.get('x_lim', [0, 1])[0]
            
            # Calculate bin centers and widths
            bins_c = (bins_plot[1:]+bins_plot[:-1])*0.5
            bin_w = np.array([bins_plot[k+1]-bins_plot[k] for k in range(len(bins)-1)])
            bin_w_plot = bin_w.copy()
        xs['ggh'] = self._cross_section(ggh_xs)
        ggh_xs_norm = xs['ggh'] / bin_w

        # Dynamically import the required module for xH cross-section
        # xh_xs = __import__(current_config['xh_xs'], globals(), locals(), vars)
        # xh_xs_norm = np.array(xh_xs.fidXS) / bin_w

        # Dynamically import the required module for VBF, VH, and ttH cross-section
        vbf_xs = __import__(current_config['vbf_xs'], globals(), locals(), vars)
        xs['vbf'] = self._cross_section(vbf_xs)
        vbf_xs_norm = xs['vbf'] / bin_w

        vh_xs = __import__(current_config['vh_xs'], globals(), locals(), vars)
        xs['vh'] = self._cross_section(vh_xs)
        vh_xs_norm = xs['vh'] / bin_w

        tth_xs = __import__(current_config['tth_xs'], globals(), locals(), vars)
        xs['tth'] = self._cross_section(tth_xs)
        tth_xs_norm = xs['tth'] / bin_w

        # Dynamically import the required module for ggH POWHEG cross-section
        ggh_powheg_xs = __import__(current_config['ggh_powheg_xs'], globals(), locals(), vars)
        ggh_powheg_xs_norm = self._cross_section(ggh_powheg_xs) / bin_w

        # Dynamically import the required module for ggH MadGraph (w/o NNLOPS reweighting) cross-section
        ggh_no_nnlops_xs = __import__(current_config['ggh_no_nnlops_xs'], globals(), locals(), vars)
        ggh_no_nnlops_xs_norm = self._cross_section(ggh_no_nnlops_xs) / bin_w
        
        if current_config['underflow_bin_normalized'] == True:
            ggh_xs_norm[0] = ggh_xs_norm[0] * bin_w[0]
            vbf_xs_norm[0] = vbf_xs_norm[0] * bin_w[0]
            vh_xs_norm[0] = vh_xs_norm[0] * bin_w[0]
            tth_xs_norm[0] = tth_xs_norm[0] * bin_w[0]
            ggh_powheg_xs_norm[0] = ggh_powheg_xs_norm[0] * bin_w[0]
            ggh_no_nnlops_xs_norm[0] = ggh_no_nnlops_xs_norm[0] * bin_w[0]
        
        xh_xs_norm = vbf_xs_norm + vh_xs_norm + tth_xs_norm

        # Theoretical uncertainty
        sources_up = ["scale_up", "pdf_up", "alpha_up"]

        # One uncertainty array per source (scale, PDF, alpha_s) and production mode.
        ggh_up = [abs(self._cross_section(ggh_xs, source) - xs['ggh']) for source in sources_up]
        ggh_powheg_up = [abs(self._cross_section(ggh_powheg_xs, source) - self._cross_section(ggh_powheg_xs)) for source in sources_up]
        ggh_no_nnlops_up = [abs(self._cross_section(ggh_no_nnlops_xs, source) - self._cross_section(ggh_no_nnlops_xs)) for source in sources_up]
        vbf_up = [abs(self._cross_section(vbf_xs, source) - xs['vbf']) for source in sources_up]
        vh_up = [abs(self._cross_section(vh_xs, source) - xs['vh']) for source in sources_up]
        tth_up = [abs(self._cross_section(tth_xs, source) - xs['tth']) for source in sources_up]

        sources_dn = ["scale_dn", "pdf_dn", "alpha_dn"]

        ggh_dn = [abs(self._cross_section(ggh_xs, source) - xs['ggh']) for source in sources_dn]
        ggh_powheg_dn = [abs(self._cross_section(ggh_powheg_xs, source) - self._cross_section(ggh_powheg_xs)) for source in sources_dn]
        ggh_no_nnlops_dn = [abs(self._cross_section(ggh_no_nnlops_xs, source) - self._cross_section(ggh_no_nnlops_xs)) for source in sources_dn]
        vbf_dn = [abs(self._cross_section(vbf_xs, source) - xs['vbf']) for source in sources_dn]
        vh_dn = [abs(self._cross_section(vh_xs, source) - xs['vh']) for source in sources_dn]
        tth_dn = [abs(self._cross_section(tth_xs, source) - xs['tth']) for source in sources_dn]
        
        ## sum of the contributions for each production mode
        ## Linear sum as each source of uncertainty is fully correlated across the production modes
        madgraph_up = np.sum([ggh_up,vbf_up,vh_up,tth_up], axis=0)
        powheg_up = np.sum([ggh_powheg_up,vbf_up,vh_up,tth_up], axis=0)
        no_nnlops_up = np.sum([ggh_no_nnlops_up,vbf_up,vh_up,tth_up], axis=0)

        madgraph_dn = np.sum([ggh_dn,vbf_dn,vh_dn,tth_dn], axis=0)
        powheg_dn = np.sum([ggh_powheg_dn,vbf_dn,vh_dn,tth_dn], axis=0)
        no_nnlops_dn = np.sum([ggh_no_nnlops_dn,vbf_dn,vh_dn,tth_dn], axis=0)

        ## Sum in quadrature of the different sources of uncertainties + uncertainty on the BR
        unc_th_up = (np.sqrt((np.sqrt(np.sum(np.square(madgraph_up), axis=0)) / (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']))**2 + 0.02**2 ) * (xs['ggh']+xs['vbf']+xs['vh']+xs['tth'])) / bin_w
        unc_th_dn = (np.sqrt((np.sqrt(np.sum(np.square(madgraph_dn), axis=0)) / (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']))**2 + 0.02**2 ) * (xs['ggh']+xs['vbf']+xs['vh']+xs['tth'])) / bin_w

        unc_th_powheg_up = np.sqrt((np.sqrt(np.sum(np.square(powheg_up), axis=0)) / (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']))**2 + 0.02**2 ) * (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']) / bin_w
        unc_th_powheg_dn = np.sqrt((np.sqrt(np.sum(np.square(powheg_dn), axis=0)) / (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']))**2 + 0.02**2 ) * (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']) / bin_w

        unc_th_no_nnlops_up = np.sqrt((np.sqrt(np.sum(np.square(no_nnlops_up), axis=0)) / (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']))**2 + 0.02**2 ) * (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']) / bin_w
        unc_th_no_nnlops_dn = np.sqrt((np.sqrt(np.sum(np.square(no_nnlops_dn), axis=0)) / (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']))**2 + 0.02**2 ) * (xs['ggh']+xs['vbf']+xs['vh']+xs['tth']) / bin_w
        
        if current_config['underflow_bin_normalized'] == True:
            unc_th_up[0] = unc_th_up[0] * bin_w[0]
            unc_th_dn[0] = unc_th_dn[0] * bin_w[0]
            unc_th_powheg_up[0] = unc_th_powheg_up[0] * bin_w[0]
            unc_th_powheg_dn[0] = unc_th_powheg_dn[0] * bin_w[0]
            unc_th_no_nnlops_up[0] = unc_th_no_nnlops_up[0] * bin_w[0]
            unc_th_no_nnlops_dn[0] = unc_th_no_nnlops_dn[0] * bin_w[0]
            # Once the underflow/overflow values have been converted back to
            # integrated cross sections, only their visual widths need to be
            # restored.  Use the configured display-bin widths; fixed values
            # would place the uncertainty markers incorrectly for variables
            # such as MassJ0J1 (whose categorical bin spans -130..0 GeV).
            underflow_bin_width = current_config.get('underflow_bin_width', 15)
            overflow_bin_width = current_config.get('overflow_bin_width', 100)
            bin_w[0] = underflow_bin_width
            bin_w[-1] = overflow_bin_width
            bin_w_plot[0] = underflow_bin_width
            bin_w_plot[-1] = overflow_bin_width
            
        # Compute expected cross-section and uncertainties
        exp_xs = np.array(exp_xs_list) * (ggh_xs_norm + xh_xs_norm)
        err_up = np.array(err_up_list) * (ggh_xs_norm + xh_xs_norm)
        err_down = np.array(err_down_list) * (ggh_xs_norm + xh_xs_norm)

        stat_up = np.array(stat_up_list) * (ggh_xs_norm + xh_xs_norm)
        stat_down = np.array(stat_down_list) * (ggh_xs_norm + xh_xs_norm)

        # The extrapolation from the fiducial to the total phase space introduces
        # a generator dependence.  Treat it as a symmetric systematic uncertainty
        # on the measured cross section and add it in quadrature to the experimental
        # total uncertainty.  Fiducial measurements receive an all-zero contribution.
        relative_gen_unc = self._generator_dependence_uncertainty(current_config, len(exp_xs))
        gen_unc = np.abs(exp_xs) * relative_gen_unc
        err_up = np.sqrt(err_up**2 + gen_unc**2)
        err_down = np.sqrt(err_down**2 + gen_unc**2)
        
        sys_up = []
        sys_down = []
        
        for diff_up in (err_up**2 - stat_up**2):
            if diff_up >= 0:
                sys_up.append(np.sqrt(diff_up))
            else:
                print(f"(err_up**2 - stat_up**2) == {diff_up}: Setting sys_up == 0")
                sys_up.append(0)
        
        for diff_down in (err_down**2 - stat_down**2):
            if diff_down >= 0:
                sys_down.append(np.sqrt(diff_down))
            else:
                print(f"(err_down**2 - stat_down**2) == {diff_down}: Setting sys_down == 0")
                sys_down.append(0)

        # Keep the systematic uncertainties consistent with the other NumPy
        # arrays, so floating-point unit conversions (fb -> pb) work directly.
        sys_up = np.asarray(sys_up, dtype=float)
        sys_down = np.asarray(sys_down, dtype=float)
        
        # #######################################
        # ##### S T A R T   P L O T T I N G #####
        # #######################################

        plotting_config_path = os.path.join(os.environ["ANALYSIS_PATH"],"Plots", "Spectra", "config",f"{self.year}_{self.variable}.yml")
        
        with open(plotting_config_path, 'r') as file:
            plotting_config = yaml.safe_load(file)

        fig = plt.figure(figsize=(10,8), dpi=120) # (10,8)
        frame1 = fig.add_axes((.1, .35, .8, .6)) #(.1, .35, .8, .6)
        # frame1 = fig.add_axes((.1, .35, .8, .8))
        if current_config['no_preliminary']:
            cms_label = ""
        elif current_config['private_work']:
            cms_label = "Private Work"
        else:
            cms_label = "Preliminary"
        # print(args.no_preliminary, cms_label)
        # Use lumi from config if available, else build it from the individual years if something like 2022_2023 is queried
        # If that is also not the case, it is a single year, so take lumi from the map
        if "lumi" in plotting_config:
            intLumi = plotting_config["lumi"]
        else:
            year_str = str(self.year)
            if "_" in year_str:
                years = year_str.split("_")
                intLumi = sum(lumiMap[y] for y in years)
            else:
                intLumi = lumiMap[year_str]
        # hep.cms.label(cms_label, data=convert_boolean_string(self.is_unblinded), lumi=intLumi, fontsize=20, com=13.6)
        hep.cms.label(
            "Private work (CMS data/simulation)",
            exp="",
            data=True,
            lumi=intLumi,
            com=13.6,
            fontsize=20,
        )

        # Plot theoretical predictions and experimental data
        plt.stairs((ggh_xs_norm+xh_xs_norm) * upper_panel_scale, bins_plot, linewidth=2, label='ggH (MadGraph5_aMC@NLO + NNLOPS + Pythia) + xH', color='tab:blue')
        plt.stairs((ggh_no_nnlops_xs_norm+xh_xs_norm) * upper_panel_scale, bins_plot, linewidth=2, label='ggH (MadGraph5_aMC@NLO + Pythia) + xH', color='tab:purple')
        plt.stairs((ggh_powheg_xs_norm+xh_xs_norm) * upper_panel_scale, bins_plot, linewidth=2, label='ggH (POWHEG + Pythia) + xH', color='brown')
        plt.stairs(xh_xs_norm * upper_panel_scale, bins_plot, linewidth=2, color='green')
        plt.stairs(xh_xs_norm * upper_panel_scale, bins_plot, linewidth=2, label='xH = ttH + VH + VBF (MadGraph5_aMC@NLO + Pythia)', alpha=0.2, color='green', fill=True)
        
        if (not plot_2d_as_1d) and current_config['last_bin_center'] > 0:
            bins_c[-1] = current_config['last_bin_center']
            
        if plot_2d_as_1d:
            pass
        elif current_config.get('show_underflow_bin', False):
            # Display a categorical underflow bin (for example N_jets < 2 in
            # m_jj) at the configured position, analogous to the 0-jet bin in
            # the leading-jet-pT spectrum.
            bins_c[0] = current_config['first_bin_center']
        elif current_config['first_bin_center'] > 0:
            bins_c[0] = current_config['first_bin_center']
        else:
            # Push the underflow data point far off-screen (not plotted)
            bins_c[0] = current_config.get('x_lim', [0, 1])[0] - 1e6
        
        plt.rcParams['hatch.linewidth'] = 2
        for center, value, err_low, err_high, width in zip(bins_c, (ggh_xs_norm+xh_xs_norm) * upper_panel_scale, unc_th_dn * upper_panel_scale, unc_th_up * upper_panel_scale, bin_w_plot):
            plt.gca().add_patch(plt.Rectangle((center - width/4, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:blue', hatch='///'))
        # POWHEG
        for center, value, err_low, err_high, width in zip(bins_c, (ggh_powheg_xs_norm+xh_xs_norm) * upper_panel_scale, unc_th_powheg_dn * upper_panel_scale, unc_th_powheg_up * upper_panel_scale, bin_w_plot):
            plt.gca().add_patch(plt.Rectangle((center + width/10, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='brown', hatch='////'))
        # Madgraph w/o NNLOPS
        for center, value, err_low, err_high, width in zip(bins_c, (ggh_no_nnlops_xs_norm+xh_xs_norm) * upper_panel_scale, unc_th_no_nnlops_dn * upper_panel_scale, unc_th_no_nnlops_up * upper_panel_scale, bin_w_plot):
            plt.gca().add_patch(plt.Rectangle((center + width/3.6, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:purple', hatch='////'))
            
        # Default font sizes
        fontsize = 14
        title_fontsize = 14
        frameOneSettings = {}
            
        if 'frame1' in plotting_config:
            frameOneSettings = plotting_config['frame1']
            
            if 'custom_xtick_labels' in frameOneSettings:
                custom_xtick_labels = frameOneSettings["custom_xtick_labels"]
                custom_xticks = frameOneSettings["custom_xticks"]
                
                frame1.set_xticks(custom_xticks)
            
            if "axvline" in frameOneSettings:
                axvline_params = frameOneSettings["axvline"]
                if isinstance(axvline_params, list):
                    for params in axvline_params:
                        plt.axvline(**params)
                else:
                    plt.axvline(**axvline_params)
                
            # A log-x plot can use a data-aware annotation with an arrow
            # instead of the fixed overflow-bin text used by the linear plot.
            figtext_key = None if plot_log_x and "overflow_annotation_log_x" in frameOneSettings else "figtext"
            if figtext_key is not None and figtext_key in frameOneSettings:
                figtext_params = frameOneSettings[figtext_key]
                plt.figtext(
                    figtext_params["x"],
                    figtext_params["y"],
                    self._phase_space_text(figtext_params['text']),
                    horizontalalignment=figtext_params["horizontalalignment"],
                    rotation=figtext_params["rotation"],
                    fontsize=figtext_params["fontsize"]
                )
            if "additional_labels" in frameOneSettings:
                for label in frameOneSettings["additional_labels"]:
                    frame1.text(
                        label["position"][0],
                        label["position"][1] * upper_panel_scale,
                        self._phase_space_text(label["text"]),
                        rotation=label["rotation"],
                        fontsize=label["fontsize"]
                    )
            # Apply ylabel if defined
            custom_frame1_ylabel = False
            if "ylabel" in frameOneSettings:
                ylabel_params = frameOneSettings["ylabel"]
                plt.ylabel(self._phase_space_text(ylabel_params["text"]), fontsize=ylabel_params["fontsize"])
                custom_frame1_ylabel = True
            
            # Apply ylim if defined
            if "ylim" in frameOneSettings:
                ylim_params = {
                    key: value * upper_panel_scale if key in ("bottom", "top") else value
                    for key, value in frameOneSettings["ylim"].items()
                }
                plt.ylim(**ylim_params)
            
            # Override font sizes if specified in the config
            fontsize = frameOneSettings.get("fontsize", fontsize)
            title_fontsize = frameOneSettings.get("title_fontsize", title_fontsize)
        
        plt.errorbar(bins_c, exp_xs * upper_panel_scale, yerr=[err_down * upper_panel_scale, err_up * upper_panel_scale], marker = 'o', linestyle = 'None', color = 'k', linewidth = 2, ms=5, capsize=4, label=r'Data (stat $\oplus$ sys unc.)')
        plt.errorbar(bins_c, exp_xs * upper_panel_scale, yerr=[sys_down * upper_panel_scale, sys_up * upper_panel_scale], marker = 'None', linestyle = 'None', color = 'red', linewidth = 6, ms=5, capsize=4, label='Systematic uncertainty')
        
        if current_config['plot_log']:
            plt.yscale('log')

        if plot_log_x:
            frame1.set_xscale('log')

        if not locals().get("custom_frame1_ylabel", False):
            plt.ylabel(r'$\Delta\sigma_{' + self.cross_section_label + r'} / \Delta ' + current_config["variable"] + r'$ ' + self._phase_space_text(current_config["y_unit"]), fontsize=20)

        y_lim_top_key = (
            "y_lim_top_log_x"
            if plot_log_x and "y_lim_top_log_x" in current_config
            else "y_lim_top"
        )
        if y_lim_top_key in current_config:
            plt.ylim(top=current_config[y_lim_top_key])
        plt.xlim(plot_x_lim)

        if plot_log_x and "overflow_annotation_log_x" in frameOneSettings:
            annotation = frameOneSettings["overflow_annotation_log_x"]
            frame1.annotate(
                self._phase_space_text(annotation["text"]),
                # Point to the nominal MadGraph-NNLOPS prediction at the left
                # edge of the final bin, rather than to the measured marker.
                xy=(
                    bins_plot[-2],
                    (ggh_xs_norm[-1] + xh_xs_norm[-1]) * upper_panel_scale,
                ),
                xycoords="data",
                xytext=annotation["text_position"],
                textcoords="axes fraction",
                horizontalalignment=annotation.get("horizontalalignment", "center"),
                verticalalignment=annotation.get("verticalalignment", "center"),
                rotation=annotation.get("rotation", 0),
                fontsize=annotation.get("fontsize", 22),
                arrowprops=annotation.get(
                    "arrowprops",
                    {"arrowstyle": "->", "color": "black", "linewidth": 1.5},
                ),
                annotation_clip=False,
            )

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
    
        legend_location = current_config.get('legend_location', 'upper right')
        
        plt.legend(fontsize=fontsize, title='p-value (MadGraph NNLOPS) = '+ str(pvalue), alignment='left', loc= legend_location, title_fontsize=title_fontsize)
        frame1.set_xticklabels([])

        # For a categorical underflow bin, keep the automatically selected
        # numerical major ticks but remove minor ticks inside that bin.  The
        # categorical-bin centre receives a manually drawn major-sized tick,
        # matching the treatment in the ratio panel below.
        frame1_suppress_minor_xticks = frameOneSettings.get("suppress_minor_xticks")
        if frame1_suppress_minor_xticks is not None:
            frame1_xlim = frame1.get_xlim()
            suppress_low, suppress_high = frame1_suppress_minor_xticks
            automatic_minor_ticks = frame1.xaxis.get_minorticklocs()
            frame1.set_xticks(
                [
                    tick
                    for tick in automatic_minor_ticks
                    if not suppress_low < tick < suppress_high
                ],
                minor=True,
            )
            # set_xticks expands the axis when the automatic locator returned
            # an outer tick (for MassJ0J1 at about -150 GeV).  Restore the
            # configured range so the prediction starts exactly at the spine.
            frame1.set_xlim(frame1_xlim)

        for tick in frameOneSettings.get("additional_xaxis_ticks", []):
            for axis_height, tick_offset in (
                (0, plt.rcParams["xtick.major.size"]),
                (1, -plt.rcParams["xtick.major.size"]),
            ):
                frame1.annotate(
                    "",
                    xy=(tick["position"], axis_height),
                    xycoords=frame1.get_xaxis_transform(),
                    xytext=(0, tick_offset),
                    textcoords="offset points",
                    arrowprops={
                        "arrowstyle": "-",
                        "color": "black",
                        "linewidth": plt.rcParams["xtick.major.width"],
                        "shrinkA": 0,
                        "shrinkB": 0,
                    },
                    annotation_clip=False,
                )

        frame2 = fig.add_axes((.1,.05,.8,.25))

        # Plot ratio (Data/Prediction) in a separate frame
        ratio_xs = exp_xs / (ggh_xs_norm+xh_xs_norm)
        ratio_powheg = (ggh_powheg_xs_norm+xh_xs_norm) / (ggh_xs_norm+xh_xs_norm)
        ratio_no_nnlops = (ggh_no_nnlops_xs_norm+xh_xs_norm) / (ggh_xs_norm+xh_xs_norm)
        ratio_madgraph = (ggh_xs_norm+xh_xs_norm) / (ggh_xs_norm+xh_xs_norm) # Dummy, it is always 1
        ratio_err_up = err_up / (ggh_xs_norm+xh_xs_norm)
        ratio_err_down = err_down / (ggh_xs_norm+xh_xs_norm)
        ratio_sys_up = sys_up / (ggh_xs_norm+xh_xs_norm)
        ratio_sys_down = sys_down / (ggh_xs_norm+xh_xs_norm)
        ratio_unc_up = unc_th_up / (ggh_xs_norm+xh_xs_norm)
        ratio_unc_dn = unc_th_dn / (ggh_xs_norm+xh_xs_norm)
        ratio_unc_powheg_up = unc_th_powheg_up / (ggh_xs_norm+xh_xs_norm)
        ratio_unc_powheg_dn = unc_th_powheg_dn / (ggh_xs_norm+xh_xs_norm)
        ratio_unc_no_nnlops_up = unc_th_no_nnlops_up / (ggh_xs_norm+xh_xs_norm)
        ratio_unc_no_nnlops_dn = unc_th_no_nnlops_dn / (ggh_xs_norm+xh_xs_norm)

        plt.errorbar(bins_c, ratio_xs , yerr=[ratio_err_down,ratio_err_up], marker = 'o', linestyle = 'None', color = 'k', linewidth = 2, ms=5, capsize=4, label='Data (Stat + Syst)')
        plt.errorbar(bins_c, ratio_xs , yerr=[ratio_sys_down,ratio_sys_up], marker = 'None', linestyle = 'None', color = 'red', linewidth = 6, ms=5, capsize=4, label='Systematic error')

        plt.stairs(ratio_madgraph, bins_plot, linewidth=2, color='tab:blue')

        for center, value, err_low, err_high, width in zip(bins_c, ratio_madgraph, ratio_unc_up, ratio_unc_dn, bin_w_plot):
            plt.gca().add_patch(plt.Rectangle((center - width/4, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:blue', hatch='/////')) #/2
        # POWHEG
        for center, value, err_low, err_high, width in zip(bins_c, ratio_powheg, ratio_unc_powheg_dn, ratio_unc_powheg_up, bin_w_plot):
            plt.gca().add_patch(plt.Rectangle((center + width/10, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='brown', hatch='/////'))
        # Madgraph w/o NNLOPS
        for center, value, err_low, err_high, width in zip(bins_c, ratio_no_nnlops, ratio_unc_no_nnlops_dn, ratio_unc_no_nnlops_up, bin_w_plot):
            plt.gca().add_patch(plt.Rectangle((center + width/3.6, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:purple', hatch='////'))
        
        plt.stairs(ratio_powheg, bins_plot, linewidth=2, color='brown')
        plt.stairs(ratio_no_nnlops, bins_plot, linewidth=2, color='tab:purple')

        frame2_xtick_fontsize = 20
        frame2_ytick_fontsize = 20
        frame2_xlabel_fontsize = 20
        frame2_ylabel_fontsize = 20
        frame2_xtick_rotation = 0
        additional_xaxis_labels = []
        suppress_minor_xticks = None
        
        if 'frame2' in plotting_config:
            frameTwoSettings = plotting_config['frame2']
            
            # Apply xticks and xtick_labels
            if "xticks" in frameTwoSettings:
                custom_xticks = frameTwoSettings["xticks"]
                frame2.set_xticks(custom_xticks)
            if "xtick_labels" in frameTwoSettings:
                custom_xtick_labels = frameTwoSettings["xtick_labels"]
                frame2.set_xticklabels(custom_xtick_labels)

            # Apply yticks and ytick_labels depending on `is_data`
            if "yticks" in frameTwoSettings and "ytick_labels" in frameTwoSettings:
                if convert_boolean_string(self.is_unblinded):
                    custom_yticks = frameTwoSettings["yticks"].get("is_data", [])
                    custom_ytick_labels = frameTwoSettings["ytick_labels"].get("is_data", [])
                else:
                    custom_yticks = frameTwoSettings["yticks"].get("not_data", [])
                    custom_ytick_labels = frameTwoSettings["ytick_labels"].get("not_data", [])
                frame2.set_yticks(custom_yticks)
                frame2.set_yticklabels(custom_ytick_labels)

            # Apply additional labels for specific variables
            if "additional_labels" in frameTwoSettings:
                additional_labels = frameTwoSettings["additional_labels"]["is_data"] if convert_boolean_string(self.is_unblinded) else frameTwoSettings["additional_labels"]["not_data"]
                for label in additional_labels:
                    if self.phase_space == "total" and label.get("fiducial_only", False):
                        continue
                    frame2.text(
                        label["position"][0],
                        label["position"][1],
                        self._phase_space_text(label["text"]),
                        rotation=label["rotation"],
                        fontsize=label["fontsize"]
                    )

            # Apply axvline if defined
            if "axvline" in frameTwoSettings:
                axvline_params = frameTwoSettings["axvline"]
                if isinstance(axvline_params, list):
                    for params in axvline_params:
                        plt.axvline(**params)
                else:
                    plt.axvline(**axvline_params)

            frame2_xtick_fontsize = frameTwoSettings.get("xtick_fontsize", frame2_xtick_fontsize)
            frame2_ytick_fontsize = frameTwoSettings.get("ytick_fontsize", frame2_ytick_fontsize)
            frame2_xlabel_fontsize = frameTwoSettings.get("xlabel_fontsize", frame2_xlabel_fontsize)
            frame2_ylabel_fontsize = frameTwoSettings.get("ylabel_fontsize", frame2_ylabel_fontsize)
            frame2_xtick_rotation = frameTwoSettings.get("xtick_rotation", frame2_xtick_rotation)
            additional_xaxis_labels = frameTwoSettings.get("additional_xaxis_labels", [])
            suppress_minor_xticks = frameTwoSettings.get("suppress_minor_xticks")
        
        for b in bins_plot:
            plt.axvline(x=b, color='gray', ls='dashed', lw=1, alpha=0.5)
        
        plt.ylabel(r'Data / Prediction', fontsize=frame2_ylabel_fontsize) #Not MC, since NNLOPS is based on a calculation

        plt.xlabel(r'$' + current_config["variable"] + r'$ ' + current_config["x_unit"], fontsize=frame2_xlabel_fontsize)
        plt.xticks(fontsize=frame2_xtick_fontsize, rotation=frame2_xtick_rotation)
        plt.yticks(fontsize=frame2_ytick_fontsize)

        if plot_log_x:
            frame2.set_xscale('log')

        # Use exactly the same horizontal range as the main panel.  In
        # particular, this prevents the categorical underflow bin from gaining
        # an extra margin in only the ratio panel through autoscaling.
        frame2.set_xlim(frame1.get_xlim())
        plt.ylim(current_config['y_lim'])

        if suppress_minor_xticks is not None:
            frame2_xlim = frame2.get_xlim()
            suppress_low, suppress_high = suppress_minor_xticks
            automatic_minor_ticks = frame2.xaxis.get_minorticklocs()
            frame2.set_xticks(
                [
                    tick
                    for tick in automatic_minor_ticks
                    if not suppress_low < tick < suppress_high
                ],
                minor=True,
            )
            frame2.set_xlim(frame2_xlim)

        # Place categorical underflow labels independently of the tick locator,
        # preserving the automatically chosen numerical x ticks exactly.
        for label in additional_xaxis_labels:
            # Draw major-sized inward ticks at both panel edges without
            # replacing the automatic major or minor tick locators.
            for axis_height, tick_offset in (
                (0, plt.rcParams["xtick.major.size"]),
                (1, -plt.rcParams["xtick.major.size"]),
            ):
                frame2.annotate(
                    "",
                    xy=(label["position"], axis_height),
                    xycoords=frame2.get_xaxis_transform(),
                    xytext=(0, tick_offset),
                    textcoords="offset points",
                    arrowprops={
                        "arrowstyle": "-",
                        "color": "black",
                        "linewidth": plt.rcParams["xtick.major.width"],
                        "shrinkA": 0,
                        "shrinkB": 0,
                    },
                    annotation_clip=False,
                )
            frame2.annotate(
                self._phase_space_text(label["text"]),
                xy=(label["position"], 0),
                xycoords=frame2.get_xaxis_transform(),
                xytext=(label.get("x_offset", 0), label.get("y_offset", -30)),
                textcoords="offset points",
                horizontalalignment=label.get("horizontalalignment", "center"),
                verticalalignment="top",
                fontsize=label.get("fontsize", frame2_xtick_fontsize),
                annotation_clip=False,
            )

        for output_name in self._spectrum_output_names():
            plt.savefig(
                os.path.join(output_dir, 'Combine', fitFolderName, output_name),
                bbox_inches='tight',
                dpi=120,
            )


class CreateTotalDiffSpectra(CreateDiffSpectra):
    """Create differential spectra extrapolated to the total phase space."""

    phase_space = "total"
    cross_section_prefix = "totXS"
    cross_section_label = r"\text{tot}"
    spectrum_output_stem = "spectra_total"
    upper_panel_scale = 1e-3
