import law
import luigi
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
    output_dir = law.Parameter(default = '', description="Path to the output directory")
    variable = law.Parameter(default='', description="Variable to be used for output folder naming")
    year = law.Parameter(default='2022', description="Year")
    is_unblinded = law.Parameter(default=False, description="Flag that signifies if spectrum is created for the unblinded results.")

    batch_flavor = law.Parameter(default="slurm", description="Special treatment for PSI Slurm batch system")
    batch_system = law.Parameter(default="slurm", description="Batch system to use")

    # htcondor_job_kwargs_submit = {"spool": True}  
    
    use_existing_scans = luigi.BoolParameter(default=False, description="Plot existing merged scans without requiring fit tasks")
    channel_label = law.Parameter(default='', description="Channel label for this individual spectrum")

    def requires(self):
        if self.use_existing_scans:
            return {}

        
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
            if convert_boolean_string(self.is_unblinded):
                output = [os.path.join(output_dir, 'Combine', fitFolderName, 'spectra.pdf')]
                output += [os.path.join(output_dir, 'Combine', fitFolderName, 'spectra.png')]
            else:
                output = [os.path.join(output_dir, 'Combine', fitFolderName, 'spectra_blinded.pdf')]
                output += [os.path.join(output_dir, 'Combine', fitFolderName, 'spectra_blinded.png')]
            
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
            cat_list = combineVariableDict[f'{self.year}'][f'{self.variable}']['paramStrNoOne'] #has to be in the correct order
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
                    main_scan_syst = BuildScan(cat, [os.path.join(output_dir, 'Combine', fitFolderName, 'dataFit', f'higgsCombineDataPostFitScanFit_{cat}.MultiDimFit.mH125.38.root')], yvals, y_cut)
                    main_scan_stat = BuildScan(cat, [os.path.join(output_dir, 'Combine', fitFolderName, 'dataFit', f'higgsCombineDataPostFitScanStat_{cat}.MultiDimFit.mH125.38.root')], yvals, y_cut)
                    
                    pvalue_path = os.path.join(output_dir, 'Combine', fitFolderName, 'pvalue.txt')
                    
                    with open(pvalue_path, 'r') as file:
                        pvalue = file.readline()
                    
                else:
                    best, up, down, _, _ = _scan_interval(os.path.join(output_dir, 'Combine', fitFolderName, 'asimov', f'higgsCombineAsimovPostFitScanFit_{cat}.root'), cat)
                    main_scan_syst = {'val': (best, up, -down)}
                    best, up, down, _, _ = _scan_interval(os.path.join(output_dir, 'Combine', fitFolderName, 'asimov', f'higgsCombineAsimovPostFitScanStat_{cat}.root'), cat)
                    main_scan_stat = {'val': (best, up, -down)}
                    
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
        
            
        current_config = config['spectra']

        xs = {}

        # List of variables to import
        vars = ['fidXS', 'fidXS_scale_up', 'fidXS_scale_dn', 'fidXS_pdf_up', 'fidXS_pdf_dn', 'fidXS_alpha_up', 'fidXS_alpha_dn', 'Boundaries']
        
        # Dynamically import the required module for ggH cross-section
        ggh_xs = __import__(current_config['ggh_xs'], globals(), locals(), vars)
        bins = ggh_xs.Boundaries
        bins_plot = np.array(bins)
        if 'underflow' in current_config:
            bins_plot[0] = current_config['underflow']
        if "overflow" in current_config.keys(): bins_plot[-1] = current_config['overflow']
        
        # Calculate bin centers and widths
        bins_c = (bins_plot[1:]+bins_plot[:-1])*0.5
        bin_w = np.array([bins_plot[k+1]-bins_plot[k] for k in range(len(bins)-1)])
        xs['ggh'] = np.array(ggh_xs.fidXS)
        ggh_xs_norm = xs['ggh'] / bin_w

        # Dynamically import the required module for xH cross-section
        # xh_xs = __import__(current_config['xh_xs'], globals(), locals(), vars)
        # xh_xs_norm = np.array(xh_xs.fidXS) / bin_w

        # Dynamically import the required module for VBF, VH, and ttH cross-section
        vbf_xs = __import__(current_config['vbf_xs'], globals(), locals(), vars)
        xs['vbf'] = np.array(vbf_xs.fidXS)
        vbf_xs_norm = xs['vbf'] / bin_w

        vh_xs = __import__(current_config['vh_xs'], globals(), locals(), vars)
        xs['vh'] = np.array(vh_xs.fidXS)
        vh_xs_norm = xs['vh'] / bin_w

        tth_xs = __import__(current_config['tth_xs'], globals(), locals(), vars)
        xs['tth'] = np.array(tth_xs.fidXS)
        tth_xs_norm = xs['tth'] / bin_w

        # Dynamically import the required module for ggH POWHEG cross-section
        ggh_powheg_xs = __import__(current_config['ggh_powheg_xs'], globals(), locals(), vars)
        ggh_powheg_xs_norm = np.array(ggh_powheg_xs.fidXS) / bin_w

        # Dynamically import the required module for ggH MadGraph (w/o NNLOPS reweighting) cross-section
        ggh_no_nnlops_xs = __import__(current_config['ggh_no_nnlops_xs'], globals(), locals(), vars)
        ggh_no_nnlops_xs_norm = np.array(ggh_no_nnlops_xs.fidXS) / bin_w
        
        if current_config['underflow_bin_normalized'] == True:
            ggh_xs_norm[0] = ggh_xs_norm[0] * bin_w[0]
            vbf_xs_norm[0] = vbf_xs_norm[0] * bin_w[0]
            vh_xs_norm[0] = vh_xs_norm[0] * bin_w[0]
            tth_xs_norm[0] = tth_xs_norm[0] * bin_w[0]
            ggh_powheg_xs_norm[0] = ggh_powheg_xs_norm[0] * bin_w[0]
            ggh_no_nnlops_xs_norm[0] = ggh_no_nnlops_xs_norm[0] * bin_w[0]
        
        xh_xs_norm = vbf_xs_norm + vh_xs_norm + tth_xs_norm

        # Theoretical uncertainty
        sources_up = ["fidXS_scale_up", "fidXS_pdf_up", "fidXS_alpha_up"]

        ## [[fidXS_scale_up unc per bin], [fidXS_pdf_up unc per bin], [fidXS_alpha_up unc per bin]]
        ggh_up = [abs(np.array(getattr(ggh_xs, source)) - np.array(ggh_xs.fidXS)) for source in sources_up]
        ggh_powheg_up = [abs(np.array(getattr(ggh_powheg_xs, source)) - np.array(ggh_powheg_xs.fidXS)) for source in sources_up]
        ggh_no_nnlops_up = [abs(np.array(getattr(ggh_no_nnlops_xs, source)) - np.array(ggh_no_nnlops_xs.fidXS)) for source in sources_up]
        vbf_up = [abs(np.array(getattr(vbf_xs, source)) - np.array(vbf_xs.fidXS)) for source in sources_up]
        vh_up = [abs(np.array(getattr(vh_xs, source)) - np.array(vh_xs.fidXS)) for source in sources_up]
        tth_up = [abs(np.array(getattr(tth_xs, source)) - np.array(tth_xs.fidXS)) for source in sources_up]

        sources_dn = ["fidXS_scale_dn", "fidXS_pdf_dn", "fidXS_alpha_dn"]
        
        ggh_dn = [abs(np.array(getattr(ggh_xs, source)) - np.array(ggh_xs.fidXS)) for source in sources_dn]
        ggh_powheg_dn = [abs(np.array(getattr(ggh_powheg_xs, source)) - np.array(ggh_powheg_xs.fidXS)) for source in sources_dn]
        ggh_no_nnlops_dn = [abs(np.array(getattr(ggh_no_nnlops_xs, source)) - np.array(ggh_no_nnlops_xs.fidXS)) for source in sources_dn]
        vbf_dn = [abs(np.array(getattr(vbf_xs, source)) - np.array(vbf_xs.fidXS)) for source in sources_dn]
        vh_dn = [abs(np.array(getattr(vh_xs, source)) - np.array(vh_xs.fidXS)) for source in sources_dn]
        tth_dn = [abs(np.array(getattr(tth_xs, source)) - np.array(tth_xs.fidXS)) for source in sources_dn]
        
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
            bin_w[0] = 15
            bin_w[-1] = 100
            
        # Compute expected cross-section and uncertainties
        exp_xs = np.array(exp_xs_list) * (ggh_xs_norm + xh_xs_norm)
        err_up = np.array(err_up_list) * (ggh_xs_norm + xh_xs_norm)
        err_down = np.array(err_down_list) * (ggh_xs_norm + xh_xs_norm)

        stat_up = np.array(stat_up_list) * (ggh_xs_norm + xh_xs_norm)
        stat_down = np.array(stat_down_list) * (ggh_xs_norm + xh_xs_norm)
        
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
        hep.cms.label(cms_label, data=convert_boolean_string(self.is_unblinded), lumi=intLumi, fontsize=20, com=13.6)

        # Plot theoretical predictions and experimental data
        plt.stairs((ggh_xs_norm+xh_xs_norm), bins_plot, linewidth=2, label='ggH (MadGraph5_aMC@NLO + NNLOPS + Pythia) + xH', color='tab:blue')
        plt.stairs((ggh_no_nnlops_xs_norm+xh_xs_norm), bins_plot, linewidth=2, label='ggH (MadGraph5_aMC@NLO + Pythia) + xH', color='tab:purple')
        plt.stairs((ggh_powheg_xs_norm+xh_xs_norm), bins_plot, linewidth=2, label='ggH (POWHEG + Pythia) + xH', color='brown')
        plt.stairs(xh_xs_norm, bins_plot, linewidth=2, color='green')
        plt.stairs(xh_xs_norm, bins_plot, linewidth=2, label='xH = ttH + VH + VBF (MadGraph5_aMC@NLO + Pythia)', alpha=0.2, color='green', fill=True)
        
        if current_config['last_bin_center'] > 0:
            bins_c[-1] = current_config['last_bin_center']
            
        if current_config['first_bin_center'] > 0:
            bins_c[0] = current_config['first_bin_center']
        else:
            bins_c[0] = 0
        
        plt.rcParams['hatch.linewidth'] = 2
        for center, value, err_low, err_high, width in zip(bins_c, ggh_xs_norm+xh_xs_norm, unc_th_dn, unc_th_up, bin_w):
            plt.gca().add_patch(plt.Rectangle((center - width/4, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:blue', hatch='///'))
        # POWHEG
        for center, value, err_low, err_high, width in zip(bins_c, ggh_powheg_xs_norm+xh_xs_norm, unc_th_powheg_dn, unc_th_powheg_up, bin_w):
            plt.gca().add_patch(plt.Rectangle((center + width/10, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='brown', hatch='////'))
        # Madgraph w/o NNLOPS
        for center, value, err_low, err_high, width in zip(bins_c, ggh_no_nnlops_xs_norm+xh_xs_norm, unc_th_no_nnlops_dn, unc_th_no_nnlops_up, bin_w):
            plt.gca().add_patch(plt.Rectangle((center + width/3.6, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:purple', hatch='////'))
            
        # Default font sizes
        fontsize = 14
        title_fontsize = 14
            
        if 'frame1' in plotting_config:
            frameOneSettings = plotting_config['frame1']
            
            if 'custom_xtick_labels' in frameOneSettings:
                custom_xtick_labels = frameOneSettings["custom_xtick_labels"]
                custom_xticks = frameOneSettings["custom_xticks"]
                
                frame1.set_xticks(custom_xticks)
            
            if "axvline" in frameOneSettings:
                axvline_params = frameOneSettings["axvline"]
                plt.axvline(**axvline_params)
                
            if "figtext" in frameOneSettings:
                figtext_params = frameOneSettings["figtext"]
                plt.figtext(
                    figtext_params["x"],
                    figtext_params["y"],
                    figtext_params['text'],
                    horizontalalignment=figtext_params["horizontalalignment"],
                    rotation=figtext_params["rotation"],
                    fontsize=figtext_params["fontsize"]
                )
            # Apply ylabel if defined
            if "ylabel" in frameOneSettings:
                ylabel_params = frameOneSettings["ylabel"]
                plt.ylabel(ylabel_params["text"], fontsize=ylabel_params["fontsize"])
            
            # Apply ylim if defined
            if "ylim" in frameOneSettings:
                ylim_params = frameOneSettings["ylim"]
                plt.ylim(**ylim_params)
            
            # Override font sizes if specified in the config
            fontsize = frameOneSettings.get("fontsize", fontsize)
            title_fontsize = frameOneSettings.get("title_fontsize", title_fontsize)
        
        plt.errorbar(bins_c, exp_xs , yerr=[err_down,err_up], marker = 'o', linestyle = 'None', color = 'k', linewidth = 2, ms=5, capsize=4, label=(r'Data (stat $\oplus$ sys unc.)' if convert_boolean_string(self.is_unblinded) else 'Expected (Asimov)') + (' '+self.channel_label if self.channel_label else ''))
        plt.errorbar(bins_c, exp_xs , yerr=[sys_down,sys_up], marker = 'None', linestyle = 'None', color = 'red', linewidth = 6, ms=5, capsize=4, label='Systematic uncertainty')
        
        if current_config['plot_log']:
            plt.yscale('log')
            
        ylabel_config = plotting_config.get('frame1', {}).get('ylabel', {})
        plt.ylabel(ylabel_config.get('text', r'$\Delta\sigma_{\text{fid}} / \Delta ' + current_config["variable"] + r'$ ' + current_config["y_unit"]), fontsize=ylabel_config.get('fontsize', 20))
        
        if "y_lim_top" in current_config.keys(): plt.ylim(top=current_config["y_lim_top"])
        plt.xlim(current_config['x_lim'])

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
    
        legend_location = current_config.get('legend_location', 'upper right')
        
        plt.legend(fontsize=fontsize, title='p-value (MadGraph NNLOPS) = '+ str(pvalue), alignment='left', loc= legend_location, title_fontsize=title_fontsize)
        frame1.set_xticklabels([])

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

        plt.hlines(1, 0,500, color='tab:blue')

        for center, value, err_low, err_high, width in zip(bins_c, ratio_madgraph, ratio_unc_up, ratio_unc_dn, bin_w):
            plt.gca().add_patch(plt.Rectangle((center - width/4, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:blue', hatch='/////')) #/2
        # POWHEG
        for center, value, err_low, err_high, width in zip(bins_c, ratio_powheg, ratio_unc_powheg_dn, ratio_unc_powheg_up, bin_w):
            plt.gca().add_patch(plt.Rectangle((center + width/10, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='brown', hatch='/////'))
        # Madgraph w/o NNLOPS
        for center, value, err_low, err_high, width in zip(bins_c, ratio_no_nnlops, ratio_unc_no_nnlops_dn, ratio_unc_no_nnlops_up, bin_w):
            plt.gca().add_patch(plt.Rectangle((center + width/3.6, value - err_low), width/8, err_low + err_high, fill=False, lw=0, color='tab:purple', hatch='////'))
        
        plt.stairs(ratio_powheg, bins_plot, linewidth=2, color='brown')
        plt.stairs(ratio_no_nnlops, bins_plot, linewidth=2, color='tab:purple')
        
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
                    frame2.text(
                        label["position"][0],
                        label["position"][1],
                        label["text"],
                        rotation=label["rotation"],
                        fontsize=label["fontsize"],
                        transform=frame2.transAxes if label.get("coords") == "axes" else frame2.transData,
                    )

            # Apply axvline if defined
            if "axvline" in frameTwoSettings:
                axvline_params = frameTwoSettings["axvline"]
                plt.axvline(**axvline_params)
        
        for b in bins_plot:
            plt.axvline(x=b, color='gray', ls='dashed', lw=1, alpha=0.5)
        
        plt.ylabel('Data / Prediction' if convert_boolean_string(self.is_unblinded) else 'Expected / Prediction', fontsize=20) #Not MC, since NNLOPS is based on a calculation

        plt.xlabel(r'$' + current_config["variable"] + r'$ ' + current_config["x_unit"], fontsize=20)
        tick_config = plotting_config.get("frame2", {})
        plt.xticks(fontsize=tick_config.get("xtick_fontsize", 20))
        if "xtick_rotation" in tick_config:
            plt.setp(frame2.get_xticklabels(), rotation=tick_config["xtick_rotation"], ha="right" if tick_config["xtick_rotation"] else "center")
        plt.yticks(fontsize=20)

        plt.xlim(current_config['x_lim'])
        plt.ylim(current_config['y_lim'])
        
        if convert_boolean_string(self.is_unblinded):
            plt.savefig(os.path.join(output_dir, 'Combine', fitFolderName, 'spectra.pdf'), bbox_inches='tight', dpi=120)
            plt.savefig(os.path.join(output_dir, 'Combine', fitFolderName, 'spectra.png'), bbox_inches='tight', dpi=120)
        else:
            plt.savefig(os.path.join(output_dir, 'Combine', fitFolderName, 'spectra_blinded.pdf'), bbox_inches='tight', dpi=120)
            plt.savefig(os.path.join(output_dir, 'Combine', fitFolderName, 'spectra_blinded.png'), bbox_inches='tight', dpi=120)


def _scan_interval(scan_path, poi, yvals=(1.,), y_cut=7., failed_fit_tolerance=-0.5):
    """Best fit and 68% CL interval of a 1D likelihood scan.

    Returns (bestfit, err_up, err_down, open_up, open_down) with positive errors. The best fit is taken
    from combine's best-fit entries (quantileExpected == -1); grid points with 2*deltaNLL below
    `failed_fit_tolerance` are failed minimisations and are dropped (with a warning). If a 2dNLL=1
    crossing lies outside the scanned range, that error reaches the scan edge and the flag is set.
    """
    if not os.path.exists(scan_path) or not plot.TFileIsGood(scan_path):
        raise RuntimeError(f"Missing or corrupt scan file: {scan_path}")
    root_file = ROOT.TFile.Open(scan_path)
    limit = root_file.Get("limit")
    if not limit:
        raise RuntimeError(f"No limit tree in scan file: {scan_path}")

    bestfit = None
    points = {}
    failed = []
    for entry in limit:
        x, y = getattr(entry, poi), 2. * entry.deltaNLL
        if abs(entry.quantileExpected + 1.) < 1e-6:
            bestfit = x
            continue
        if entry.quantileExpected < -1.5:
            continue
        if y < failed_fit_tolerance:
            failed.append((round(x, 4), round(y, 3)))
            continue
        if y <= y_cut:
            points[x] = min(y, points.get(x, float("inf")))
    root_file.Close()
    if failed:
        print(f"[WARNING] {scan_path}: dropped {len(failed)} failed scan point(s) of {poi} (r, 2*deltaNLL): {failed}")
    if bestfit is None:
        bestfit = min(points, key=points.get)
        print(f"[WARNING] {scan_path}: no best-fit entry, using the lowest scan point {poi} = {bestfit:.4f}")
    points[bestfit] = 0.
    if len(points) <= 1:
        raise RuntimeError(f"Scan of {poi} in {scan_path} has fewer than two valid points")

    xs = sorted(points)
    graph = ROOT.TGraph(len(xs))
    for i, x in enumerate(xs):
        graph.SetPoint(i, x, points[x])
    x_min, x_max = xs[0], xs[-1]

    spline = ROOT.TSpline3(f"spline_{poi}", graph)
    func_method = partial(lambda s, x, p: s.Eval(x[0]), spline)
    func = ROOT.TF1(f"splinefn_{poi}_{abs(hash(scan_path))}", func_method, x_min, x_max, 1)
    func._method = func_method  # keep the python callable alive for ROOT
    crossings = plot.FindCrossingsWithSpline(graph, func, yvals[0])

    lo, hi = x_min, x_max
    open_up = open_down = True
    for cr in crossings:
        if cr["lo"] <= bestfit <= cr["hi"]:
            lo, hi = cr["lo"], cr["hi"]
            open_down, open_up = not cr["valid_lo"], not cr["valid_hi"]
    return bestfit, hi - bestfit, bestfit - lo, open_up, open_down


def _load_prediction_module(name):
    """Load a fidXS prediction module by name, providing numpy as `np` to it.

    Some generated fidXS files contain np.float64(...) literals without importing numpy.
    """
    import importlib.util
    import types
    spec = importlib.util.find_spec(name)
    if spec is None or spec.origin is None:
        raise ImportError(f"Prediction module {name} not found on PYTHONPATH")
    module = types.ModuleType(name)
    module.np = np
    with open(spec.origin) as f:
        exec(compile(f.read(), spec.origin, "exec"), module.__dict__)
    return module


class CreateCombinedDiffSpectra(law.Task):
    """Differential spectrum comparing the precision of Hgg-only, H4l-only and Hgg+H4l fits.

    The three fits are ordinary FinalFits outputs of the same variable/year, living in different
    output directories (e.g. built from the combined card and its --ic channel splits). Each fit
    provides r_<bin> scans (with systematics and stat-only); the spectrum shows r x prediction per
    bin, the combination with its systematic component, and the ratio to the prediction.

    Directories and labels come from the `combined_spectra` block of config/<year>_<variable>.yml
    and can be overridden on the command line, e.g.
      law run CreateCombinedDiffSpectra --variable rapidity --year 2022_2023_2024 \
          --hgg-output-dir <dir> --hzz-output-dir <dir> --comb-output-dir <dir>
    """
    variable = law.Parameter(description="Differential variable, e.g. rapidity")
    year = law.Parameter(default='2022_2023_2024', description="Year label of the fits")
    hgg_output_dir = law.Parameter(default='', description="Output directory of the Hgg-only fit")
    hzz_output_dir = law.Parameter(default='', description="Output directory of the H4l-only fit")
    comb_output_dir = law.Parameter(default='', description="Output directory of the Hgg+H4l fit")
    is_unblinded = law.Parameter(default=False, description="Use the data fits instead of the Asimov fits")
    use_existing_scans = luigi.BoolParameter(default=False, description="Only read the merged scans already present in the "
                                           "output directories (e.g. copied from elsewhere) instead of requiring the fit tasks")

    batch_flavor = law.Parameter(default="htcondor", description="Special treatment for PSI Slurm batch system")
    batch_system = law.Parameter(default="htcondor", description="Batch system to use for the required fits")

    channels = ("hgg", "hzz", "comb")

    def _config(self):
        config_path = os.path.join(os.environ["ANALYSIS_PATH"], "config", f"{self.year}_{self.variable}.yml")
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def _output_dirs(self):
        config = self._config()
        block = config.get("combined_spectra", {})
        dirs = {
            "hgg": self.hgg_output_dir or block.get("hgg_output_dir", ""),
            "hzz": self.hzz_output_dir or block.get("hzz_output_dir", ""),
            "comb": self.comb_output_dir or block.get("comb_output_dir", config["outputFolder"]),
        }
        missing = [ch for ch, d in dirs.items() if not d]
        if missing:
            raise ValueError(f"No output directory given for {missing}: set --{missing[0]}-output-dir or combined_spectra in the config")
        return {ch: os.path.normpath(d) for ch, d in dirs.items()}

    def requires(self):
        tasks = {}
        if self.use_existing_scans:
            return tasks
        for channel, output_dir in self._output_dirs().items():
            common = dict(variable=self.variable, output_dir=output_dir, year=self.year, batch_flavor=self.batch_flavor, version=self.variable, workflow=self.batch_system)
            if convert_boolean_string(self.is_unblinded):
                tasks[channel] = CreateUnblindedFit(**common)
            else:
                tasks[channel] = CreateAsimovFit(**common)
        return tasks

    def output(self):
        fit_folder = os.path.join(self._output_dirs()["comb"], 'Combine', f'runFits_{self.variable}')
        name = "combined_spectra" if convert_boolean_string(self.is_unblinded) else "combined_spectra_blinded"
        return {
            "pdf": law.LocalFileTarget(os.path.join(fit_folder, f"{name}.pdf")),
            "png": law.LocalFileTarget(os.path.join(fit_folder, f"{name}.png")),
            "json": law.LocalFileTarget(os.path.join(fit_folder, f"{name}.json")),
        }

    def _scan_path(self, output_dir, kind, poi):
        fit_folder = os.path.join(output_dir, 'Combine', f'runFits_{self.variable}')
        if convert_boolean_string(self.is_unblinded):
            return os.path.join(fit_folder, 'dataFit', f'higgsCombineDataPostFitScan{kind}_{poi}.MultiDimFit.mH{COMBINE_MH}.root')
        return os.path.join(fit_folder, 'asimov', f'higgsCombineAsimovPostFitScan{kind}_{poi}.root')

    def run(self):
        config = self._config()
        block = config.get("combined_spectra", {})
        # combined_spectra.spectra_overrides updates individual `spectra` settings for this plot only
        spectra_cfg = {**config['spectra'], **block.get("spectra_overrides", {})}
        output_dirs = self._output_dirs()
        # combined_spectra.poi_names overrides the POI names (same bin order), e.g. when the scans use
        # r_PTJ0_m10000p0_30p0 instead of r_PTJ0_0p0_30p0
        pois = block.get("poi_names", combineVariableDict[f'{self.year}'][f'{self.variable}']['paramStrNoOne'])

        # ---- measured signal strengths per channel ----
        results = {}
        for channel, output_dir in output_dirs.items():
            results[channel] = {"r": [], "tot_up": [], "tot_dn": [], "stat_up": [], "stat_dn": [], "open_up": [], "open_dn": []}
            for poi in pois:
                r, up, dn, open_up, open_dn = _scan_interval(self._scan_path(output_dir, "Fit", poi), poi)
                _, s_up, s_dn, _, _ = _scan_interval(self._scan_path(output_dir, "Stat", poi), poi)
                res = results[channel]
                res["r"].append(r)
                res["tot_up"].append(up)
                res["tot_dn"].append(dn)
                res["stat_up"].append(s_up)
                res["stat_dn"].append(s_dn)
                res["open_up"].append(open_up)
                res["open_dn"].append(open_dn)
                if open_up or open_dn:
                    print(f"[{channel}] {poi}: 68% CL interval not closed within the scan range (up: {open_up}, down: {open_dn})")
        for res in results.values():
            for key in res:
                res[key] = np.array(res[key])
            res["syst_up"] = np.sqrt(np.clip(res["tot_up"]**2 - res["stat_up"]**2, 0., None))
            res["syst_dn"] = np.sqrt(np.clip(res["tot_dn"]**2 - res["stat_dn"]**2, 0., None))

        # ---- prediction: ggH (NNLOPS) + xH, theory band as in CreateDiffSpectra ----
        # combined_spectra.<mode>_xs overrides spectra.<mode>_xs, e.g. to use total (not fiducial) cross sections
        modules = {key: _load_prediction_module(block.get(f'{key}_xs', spectra_cfg[f'{key}_xs'])) for key in ("ggh", "vbf", "vh", "tth")}
        bins = np.array(modules["ggh"].Boundaries, dtype=float)
        bins_plot = bins.copy()
        if 'underflow' in spectra_cfg:
            bins_plot[0] = spectra_cfg['underflow']
        if block.get("overflow_width_as_previous", False):
            # rightmost bin is an overflow bin: its width is taken equal to the last but one bin
            bins_plot[-1] = bins_plot[-2] + (bins_plot[-2] - bins_plot[-3])
        elif "overflow" in spectra_cfg:
            bins_plot[-1] = spectra_cfg['overflow']
        bin_w = bins_plot[1:] - bins_plot[:-1]
        norm_w = bin_w.copy()
        if spectra_cfg.get('underflow_bin_normalized', False):
            norm_w[0] = 1.

        total = sum(np.array(m.fidXS) for m in modules.values())
        th_up = np.zeros_like(total)
        th_dn = np.zeros_like(total)
        for up_name, dn_name in (("fidXS_scale_up", "fidXS_scale_dn"), ("fidXS_pdf_up", "fidXS_pdf_dn"), ("fidXS_alpha_up", "fidXS_alpha_dn")):
            # each source is fully correlated across production modes: linear sum, then quadrature
            th_up += sum(abs(np.array(getattr(m, up_name)) - np.array(m.fidXS)) for m in modules.values())**2
            th_dn += sum(abs(np.array(getattr(m, dn_name)) - np.array(m.fidXS)) for m in modules.values())**2
        br_unc = block.get("br_uncertainty", 0.02)
        th_up = np.sqrt(th_up + (br_unc * total)**2)
        th_dn = np.sqrt(th_dn + (br_unc * total)**2)

        scale = float(block.get("prediction_scale", 1.))
        prediction = scale * total / norm_w
        pred_up = scale * th_up / norm_w
        pred_dn = scale * th_dn / norm_w

        # ---- plotting ----
        # Same plotting config as CreateDiffSpectra: Plots/Spectra/config/<year>_<variable>.yml
        # (lumi, frame1/frame2 settings) together with the `spectra` block of the main config
        # (variable, units, x_lim, y_lim, plot_log). Optional extras used here:
        #   equal_width_bins: draw every bin with the same width (ticks stay in physical units)
        #   frame1.legend_location, frame2.ylim, frame2.xtick_fontsize, frame2.ytick_fontsize, frame2.xtick_rotation
        plotting_config_path = os.path.join(os.environ["ANALYSIS_PATH"], "Plots", "Spectra", "config", f"{self.year}_{self.variable}.yml")
        plotting_config = {}
        if os.path.exists(plotting_config_path):
            with open(plotting_config_path, 'r') as file:
                plotting_config = yaml.safe_load(file) or {}
        else:
            print(f"No plotting config {plotting_config_path}, using defaults")
        frame1_cfg = plotting_config.get("frame1", {})
        frame2_cfg = plotting_config.get("frame2", {})
        is_data = convert_boolean_string(self.is_unblinded)

        bins_c = 0.5 * (bins_plot[1:] + bins_plot[:-1])
        if spectra_cfg.get('first_bin_center', 0) > 0:
            bins_c[0] = spectra_cfg['first_bin_center']
        if spectra_cfg.get('last_bin_center', 0) > 0:
            bins_c[-1] = spectra_cfg['last_bin_center']

        if plotting_config.get("equal_width_bins", False):
            to_x = lambda v: np.interp(v, bins_plot, np.arange(len(bins_plot), dtype=float))
        else:
            to_x = lambda v: np.asarray(v, dtype=float)
        edges_x = to_x(bins_plot)
        widths_x = edges_x[1:] - edges_x[:-1]
        centers_x = to_x(bins_c)

        style = {
            "comb": dict(label=block.get("comb_label", r"Combination"), color="k", marker="o", offset=0.0),
            "hgg": dict(label=block.get("hgg_label", r"H$\rightarrow\gamma\gamma$"), color="tab:red", marker="^", offset=0.25),
            "hzz": dict(label=block.get("hzz_label", r"H$\rightarrow$ZZ"), color="tab:blue", marker="v", offset=-0.25),
        }

        fig = plt.figure(figsize=(10, 10), dpi=120)
        top = fig.add_axes((.1, .35, .8, .6))
        ratio = fig.add_axes((.1, .08, .8, .23), sharex=top)

        if spectra_cfg.get('no_preliminary', False):
            cms_label = ""
        elif spectra_cfg.get('private_work', False):
            cms_label = "Private Work"
        else:
            cms_label = "Preliminary"
        if "lumi" in plotting_config:
            lumi = plotting_config["lumi"]
        else:
            lumi = sum(lumiMap[y] for y in str(self.year).split("_"))
        # data=True avoids the "Simulation" tag for Asimov results; expected fits are marked in the legend title
        hep.cms.label(cms_label, data=True, lumi=lumi, com=13.6, fontsize=20, ax=top)

        plt.rcParams['hatch.linewidth'] = 2
        for ax, pred_vals, band_up, band_dn in ((top, prediction, pred_up, pred_dn), (ratio, np.ones_like(prediction), pred_up / prediction, pred_dn / prediction)):
            ax.stairs(pred_vals, edges_x, color="darkgray", linewidth=1.5, label=block.get("prediction_label", "aMC@NLO NNLOPS + xH") if ax is top else None)
            for x0, width, value, band_hi, band_lo in zip(edges_x[:-1], widths_x, pred_vals, band_up, band_dn):
                ax.add_patch(plt.Rectangle((x0, value - band_lo), width, band_lo + band_hi, fill=False, lw=0, color="gray", hatch="///"))
            for edge in edges_x:
                ax.axvline(edge, color="lightgray", lw=0.8, zorder=0)

        for channel in ("hzz", "hgg", "comb"):
            res, st = results[channel], style[channel]
            x = centers_x + st["offset"] * widths_x * 0.5
            for ax, factor in ((top, prediction), (ratio, np.ones_like(prediction))):
                ax.errorbar(x, res["r"] * factor, yerr=[res["tot_dn"] * factor, res["tot_up"] * factor],
                            marker=st["marker"], color=st["color"], linestyle="None", ms=7, capsize=3, linewidth=1.8,
                            label=st["label"] if ax is top else None, zorder=3)
                if channel == "comb":
                    for i, (xi, ri, s_up, s_dn, width, f) in enumerate(zip(x, res["r"], res["syst_up"], res["syst_dn"], widths_x, factor)):
                        ax.add_patch(plt.Rectangle((xi - 0.06 * width, (ri - s_dn) * f), 0.12 * width, (s_dn + s_up) * f,
                                                   color="gray", alpha=0.6, lw=0, zorder=2,
                                                   label=block.get("comb_syst_label", "Combination, Syst. unc.") if (ax is top and i == 0) else None))

        # ---- upper panel ----
        variable_tex = spectra_cfg["variable"]
        if "ylabel" in frame1_cfg:
            top.set_ylabel(frame1_cfg["ylabel"]["text"], fontsize=frame1_cfg["ylabel"].get("fontsize", 20))
        else:
            top.set_ylabel(r'$\Delta\sigma_{\text{fid}} / \Delta ' + variable_tex + r'$ ' + spectra_cfg["y_unit"], fontsize=20)
        if spectra_cfg.get("plot_log", 0):
            top.set_yscale("log")
        if "ylim" in frame1_cfg:
            top.set_ylim(**frame1_cfg["ylim"])
        if "y_lim_top" in spectra_cfg:
            top.set_ylim(top=spectra_cfg["y_lim_top"])
        if "axvline" in frame1_cfg:
            params = dict(frame1_cfg["axvline"])
            params["x"] = float(to_x(params["x"]))
            top.axvline(**params)
        if "figtext" in frame1_cfg:
            ft = frame1_cfg["figtext"]
            fig.text(ft["x"], ft["y"], ft["text"], horizontalalignment=ft["horizontalalignment"], rotation=ft["rotation"], fontsize=ft["fontsize"])
        top.tick_params(axis="y", labelsize=20)

        handles, labels = top.get_legend_handles_labels()
        order = [block.get(k, d) for k, d in (("prediction_label", "aMC@NLO NNLOPS + xH"), ("comb_label", "Combination"),
                                               ("comb_syst_label", "Combination, Syst. unc."), ("hgg_label", r"H$\rightarrow\gamma\gamma$"),
                                               ("hzz_label", r"H$\rightarrow$ZZ"))]
        ordered = [(handles[labels.index(l)], l) for l in order if l in labels]
        legend_title = None if is_data else block.get("expected_title", "Expected (Asimov)")
        top.legend(*zip(*ordered), fontsize=frame1_cfg.get("fontsize", 14), title=legend_title, title_fontsize=frame1_cfg.get("title_fontsize", 14),
                   loc=frame1_cfg.get("legend_location", block.get("legend_location", "lower left")), frameon=True)
        plt.setp(top.get_xticklabels(), visible=False)

        # ---- ratio panel ----
        ratio.set_ylabel("Ratio to prediction", fontsize=16)
        ratio.set_xlim(*to_x(spectra_cfg["x_lim"]))
        ratio.set_ylim(*frame2_cfg.get("ylim", spectra_cfg["y_lim"]))
        ratio.set_xlabel(r'$' + variable_tex + r'$ ' + spectra_cfg["x_unit"], fontsize=20)
        if "xticks" in frame2_cfg:
            ratio.set_xticks(to_x(frame2_cfg["xticks"]))
        elif plotting_config.get("equal_width_bins", False):
            ratio.set_xticks(edges_x)
            ratio.set_xticklabels([f"{b:g}" for b in bins_plot])
        if "xtick_labels" in frame2_cfg:
            ratio.set_xticklabels(frame2_cfg["xtick_labels"])
        if "xtick_rotation" in frame2_cfg:
            plt.setp(ratio.get_xticklabels(), rotation=frame2_cfg["xtick_rotation"], ha="right" if frame2_cfg["xtick_rotation"] else "center")
        if "yticks" in frame2_cfg and "ytick_labels" in frame2_cfg:
            key = "is_data" if is_data else "not_data"
            ratio.set_yticks(frame2_cfg["yticks"].get(key, []))
            ratio.set_yticklabels(frame2_cfg["ytick_labels"].get(key, []))
        for label in frame2_cfg.get("additional_labels", {}).get("is_data" if is_data else "not_data", []):
            ratio.text(label["position"][0], label["position"][1], label["text"], rotation=label["rotation"], fontsize=label["fontsize"])
        if "axvline" in frame2_cfg:
            params = dict(frame2_cfg["axvline"])
            params["x"] = float(to_x(params["x"]))
            ratio.axvline(**params)
        ratio.tick_params(axis="x", labelsize=frame2_cfg.get("xtick_fontsize", 20))
        ratio.tick_params(axis="y", labelsize=frame2_cfg.get("ytick_fontsize", 20))
        ratio.minorticks_off() if plotting_config.get("equal_width_bins", False) else None
        ratio.grid(axis="y", ls=":", color="lightgray")

        outputs = self.output()
        outputs["pdf"].parent.touch()
        fig.savefig(outputs["pdf"].path, bbox_inches='tight')
        fig.savefig(outputs["png"].path, bbox_inches='tight', dpi=120)
        plt.close(fig)

        summary = {
            "pois": list(pois),
            "bins": bins.tolist(),
            "prediction": prediction.tolist(),
            "prediction_scale": scale,
            "output_dirs": output_dirs,
            "fits": {ch: {k: v.tolist() for k, v in res.items()} for ch, res in results.items()},
        }
        outputs["json"].dump(summary, indent=1, formatter="json")

        print(f"{'POI':22s}" + "".join(f"{ch:>22s}" for ch in ("hgg", "hzz", "comb")))
        for i, poi in enumerate(pois):
            row = "".join(f"   {results[ch]['r'][i]:.2f} +{results[ch]['tot_up'][i]:.3f}/-{results[ch]['tot_dn'][i]:.3f}" for ch in ("hgg", "hzz", "comb"))
            print(f"{poi:22s}{row}")
