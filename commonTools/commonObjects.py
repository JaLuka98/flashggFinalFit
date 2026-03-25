import os
import copy

# Paths and directory
cmsswbase__ = os.environ['CMSSW_BASE']
if 'ANALYSIS_PATH' in os.environ:
    cwd__ = os.environ['ANALYSIS_PATH']
else:
    cwd__ = os.environ['CMSSW_BASE']+"/src/flashggFinalFit"
swd__ = "%s/Signal"%cwd__
bwd__ = "%s/Background"%cwd__
dwd__ = "%s/Datacard"%cwd__
fwd__ = "%s/Combine"%cwd__
pwd__ = "%s/Plots"%cwd__
twd__ = "%s/Trees2WS"%cwd__

# Centre of mass energy string
sqrts__ = "13TeV"

# Luminosity map in fb^-1
lumiMap = {
    '2016':36.33, 
    '2017':41.48, 
    '2018':59.83, 
    'combined':137.65, 
    'merged':137.65,
    '2022preEE':7.9804,
    '2223preEE':7.9804,
    '2022postEE':26.6717,
    '2223postEE':26.6717,
    '2022': 34.6521,
    '2023preBPix': 18.063,
    '2223preBPix': 18.063,
    '2023postBPix': 9.693,
    '2223postBPix': 9.693,
    '2023': 27.756,
    '2223': 62.4081,
    '2024': 109.0,
    '2024all': 109.0,
    'Run3': 171.4081
}

def CreateVariableParameters(gen_variable, reco_variable, bins, year, BMW, reco_bins=None):
    """
    Create bookkeeping strings for differential measurements.

    By default, it assumes the bin labels are identical between gen/POI naming and reco category naming.
    When the reco category label differs from the POI label (e.g. NJ0 -> m1000p0_0p0), pass reco_bins.
    """
    if reco_bins is None:
        reco_bins = bins
    if len(reco_bins) != len(bins):
        raise ValueError(
            f"reco_bins length ({len(reco_bins)}) must match bins length ({len(bins)}) "
            f"for variable {gen_variable}"
        )

    paramStr = [f"r_{gen_variable}_{bin}=1" for bin in bins]
    paramStrNoOne = [f"r_{gen_variable}_{bin}" for bin in bins]
    catsStr = [f"RECO_{reco_variable}_{reco_bin}" for reco_bin in reco_bins]
    catsStrWithBMW = [f"RECO_{reco_variable}_{reco_bin}_{bmw}" for reco_bin in reco_bins for bmw in BMW]

    if "_" in year:
        years = year.split("_")
    else:
        years = [year]

    pdfIndeces = [
        f"pdfindex_RECO_{reco_variable}_{reco_bin}_{bmw}_{yr}_{sqrts__}"
        for reco_bin in reco_bins for bmw in BMW for yr in years
    ]

    poi_to_reco_bin = {poi_bin: reco_bin for poi_bin, reco_bin in zip(bins, reco_bins)}

    VariableDict = {
        "paramStr": paramStr,
        "paramStrNoOne": paramStrNoOne,
        "catsStr": catsStr,
        "catsStrWithBMW": catsStrWithBMW,
        "pdfIndeces": pdfIndeces,
        "poiToRecoBin": poi_to_reco_bin,
    }
    
    return VariableDict


# If using ReReco samples then switch to lumiMap below (missing data in 2018 EGamma data set)
#lumiMap = {'2016':36.33, '2017':41.48, '2018':59.35, 'combined':137.17, 'merged':137.17}
lumiScaleFactor = 1000. # Converting from pb to fb
# Reference for 2022: https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#DATA_AN2

# Constants
BR_W_lnu = 3.*10.86*0.01
BR_Z_ll = 3*3.3658*0.01
BR_Z_nunu = 20.00*0.01
BR_Z_qq = 69.91*0.01
BR_W_qq = 67.41*0.01

# List of years
years_to_process = ['2016','2017','2018','2022preEE','2022postEE','2023preBPix','2023postBPix', '2024']
# Production modes and decay channel: for extract XS from combine
productionModes = ['ggH','qqH','ttH','tHq','tHW','ggZH', 'WH','ZH','bbH']
decayMode = 'hgg'

# flashgg input WS objects
inputWSName__ = "tagsDumper/cms_hgg_13TeV"
inputHiggsDNAAllData__ = "DiphotonTree"
inputNuisanceExtMap = {'scales':'','scalesCorr':'','smears':''}
# Signal output WS objects
outputWSName__ = "wsig"
outputWSObjectTitle__ = "hggpdfsmrel"
outputWSNuisanceTitle__ = "CMS_hgg_nuisance"
#outputNuisanceExtMap = {'scales':'%sscale'%sqrts__,'scalesCorr':'%sscaleCorr'%sqrts__,'smears':'%ssmear'%sqrts__,'scalesGlobal':'%sscale'%sqrts__}
outputNuisanceExtMap = {'scales':'','scalesCorr':'','smears':'','scalesGlobal':''}
# Bkg output WS objects
bkgWSName__ = "multipdf"

# Define an array of input masses
input_masses = [120, 125, 130]

# Define an array of production modes and corresponding process strings
# JLS 23th Jan 2025, also adding 2G naming conventions
production_modes = [
    ("ggh", "GluGluHtoGG"),
    ("ggh", "GluGluHto2G"),
    ("vbf", "VBFHtoGG"),
    ("vbf", "VBFHto2G"),
    ("vh", "VHtoGG"),
    ("vh", "VHto2G"),
    ("tth", "ttHtoGG"),
    ("tth", "ttHto2G"),
    ("bbh", "bbHtoGG"),
    ("bbh", "bbHto2G")
]

# Getting production XS from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap, for 125.38 @ 13.6 TeV
production_XS = {
    "GluGluHtoGG": 51.96,
    "GluGluHto2G": 51.96,
    "VBFHtoGG": 4.067,
    "VBFHto2G": 4.067,
    "VHtoGG": 2.3781,
    "VHto2G": 2.3781,
    "ttHtoGG": 0.5638,
    "ttHto2G": 0.5638,
    "bbHtoGG": 0.49,
    "bbHto2G": 0.49,
}

short_production_modes = ["ggh", "vbf", "vh", "tth", "bbh"]

eft_variables = ["chg", "chb", "chw", "chwb", "chbox", "chd", "chl3", "cll1", "ctbre", "cthre", "ctwre"]

allErasMap = {
    '2022': ["preEE", "postEE"],
    '2023': ["preBPix", "postBPix"],
    '2223': ["preEE", "postEE", "preBPix", "postBPix"],
    # 2024 does not have eras
    'Run3': ["preEE", "postEE", "preBPix", "postBPix"],
}

conversionTable_ = {
    "GluGluHtoGG": "ggh",
    "GluGluHto2G": "ggh",
    "ttHtoGG": "tth",
    "ttHto2G": "tth",
    "bbHtoGG": "bbh",
    "bbHto2G": "bbh",
    "VBFHtoGG": "vbf",
    "VBFHto2G": "vbf",
    "VHtoGG": "vh",
    "VHto2G": "vh",
    }

# List of all jet-related variables. Variables listed here will get the CMS_scale_j and CMS_res_j uncertainty in the datacard step.
jetVariables = [
    "NJ",
    "PTJ0",
    "PTJ1",
    "YJ0",
    "AbsPhiHJ0",
    "AbsYHJ0",
    "MassJ0J1",
    "DYHJ0",
]

differentialProcTable_ = {
    "PTH": [
        (10, "PTH_0p0_15p0_in"),
        (11, "PTH_15p0_30p0_in"),
        (12, "PTH_30p0_45p0_in"),
        (13, "PTH_45p0_80p0_in"),
        (14, "PTH_80p0_120p0_in"),
        (15, "PTH_120p0_200p0_in"),
        (16, "PTH_200p0_350p0_in"),
        (17, "PTH_350p0_10000p0_in"),
        (18, "PTH_0p0_10000p0_out")
    ],
    "rapidity": [
        (20, "YH_0p0_0p15_in"),
        (21, "YH_0p15_0p3_in"),
        (22, "YH_0p3_0p6_in"),
        (23, "YH_0p6_0p9_in"),
        (24, "YH_0p9_2p5_in"),
        (25, "YH_0p0_2p5_out")
    ],
    "NJ": [
        (30, "NJ_0p0_1p0_in"),
        (31, "NJ_1p0_2p0_in"),
        (32, "NJ_2p0_3p0_in"),
        (33, "NJ_3p0_100p0_in"),
        (34, "NJ_0p0_100p0_out")
    ],
    "PTJ0": [
        (40, "PTJ0_0p0_30p0_in"),
        (41, "PTJ0_30p0_75p0_in"),
        (42, "PTJ0_75p0_120p0_in"),
        (43, "PTJ0_120p0_200p0_in"),
        (44, "PTJ0_200p0_10000p0_in"),
        (45, "PTJ0_0p0_10000p0_out")
    ],
    "PTJ1": [
        (50, "PTJ1_NJLE1_in"),
        (51, "PTJ1_30p0_40p0_in"),
        (52, "PTJ1_40p0_65p0_in"),
        (53, "PTJ1_65p0_90p0_in"),
        (54, "PTJ1_90p0_150p0_in"),
        (55, "PTJ1_150p0_10000p0_in"),
        (56, "PTJ1_incl_out"),
    ],
    "CosThetaStarCS": [
        (46, "CosThetaStarCS_0p0_0p07_in"),
        (47, "CosThetaStarCS_0p07_0p15_in"),
        (48, "CosThetaStarCS_0p15_0p22_in"),
        (49, "CosThetaStarCS_0p22_0p35_in"),
        (50, "CosThetaStarCS_0p35_0p45_in"),
        (51, "CosThetaStarCS_0p45_0p55_in"),
        (52, "CosThetaStarCS_0p55_0p75_in"),
        (53, "CosThetaStarCS_0p75_1p0_in"),
        (54, "CosThetaStarCS_0p0_1p0_out"),
    ],
    "YJ0": [
        (50, "YJ0_NJ0_in"),
        (51, "YJ0_0p0_0p3_in"),
        (52, "YJ0_0p3_0p6_in"),
        (53, "YJ0_0p6_0p9_in"),
        (54, "YJ0_0p9_1p2_in"),
        (55, "YJ0_1p2_1p6_in"),
        (56, "YJ0_1p6_2p0_in"),
        (57, "YJ0_2p0_2p5_in"),
        (58, "YJ0_2p5_5p0_in"),
        (59, "YJ0_incl_out"),
    ],
    "DYHJ0": [
        (50, "DYHJ0_NJ0_in"),
        (51, "DYHJ0_0p0_0p3_in"),
        (52, "DYHJ0_0p3_0p6_in"),
        (53, "DYHJ0_0p6_1p0_in"),
        (54, "DYHJ0_1p0_1p4_in"),
        (55, "DYHJ0_1p4_1p9_in"),
        (56, "DYHJ0_1p9_2p5_in"),
        (57, "DYHJ0_2p5_5p0_in"),
        (58, "DYHJ0_incl_out"),
    ],
    "AbsPhiHJ0": [
        (60, "AbsPhiHJ0_0p0_2p6_in"),
        (61, "AbsPhiHJ0_2p6_2p9_in"),
        (62, "AbsPhiHJ0_2p9_3p03_in"),
        (63, "AbsPhiHJ0_3p03_3p1415926_in"),
        (64, "AbsPhiHJ0_NJ_in"),
        (65, "AbsPhiHJ0_0p0_Pi_out")
    ],
    "AbsYHJ0": [
        (70, "AbsYHJ0_0p0_0p6_in"),
        (71, "AbsYHJ0_0p6_1p2_in"),
        (72, "AbsYHJ0_1p2_1p9_in"),
        (73, "AbsYHJ0_1p9_100p0_in"),
        (74, "AbsYHJ0_NJ0_in"),
        (75, "AbsYHJ0_0p0_100p0_out")
    ],
    "MassJ0J1": [
        (70, "MassJ0J1_NJLE1_in"),
        (71, "MassJ0J1_0p0_75p0_in"),
        (72, "MassJ0J1_75p0_120p0_in"),
        (73, "MassJ0J1_120p0_180p0_in"),
        (74, "MassJ0J1_180p0_300p0_in"),
        (75, "MassJ0J1_300p0_500p0_in"),
        (76, "MassJ0J1_500p0_1000p0_in"),
        (77, "MassJ0J1_1000p0_10000p0_in"),
        (78, "MassJ0J1_incl_out"),
    ]
}

#BMW == Best Medium Worst
BMW = ['cat0', 'cat1', 'cat2']

combineVariableDict = {
    "2022": {
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2022", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2022", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022", BMW=BMW),
        "PTJ1": CreateVariableParameters(gen_variable="PTJ1", reco_variable="PTJ1", bins=["NJLE1", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], reco_bins=["0p0_30p0", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], year="2022", BMW=BMW),
        "CosThetaStarCS": CreateVariableParameters(gen_variable="CosThetaStarCS", reco_variable="CosThetaStarCS", bins=["0p0_0p07", "0p07_0p15", "0p15_0p22", "0p22_0p35", "0p35_0p45", "0p45_0p55", "0p55_0p75", "0p75_1p0"], year="2022", BMW=BMW),
        "YJ0": CreateVariableParameters(gen_variable="YJ0", reco_variable="YJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], reco_bins=["m1000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], year="2022", BMW=BMW),
        "MassJ0J1": CreateVariableParameters(gen_variable="MassJ0J1", reco_variable="MassJ0J1", bins=["NJLE1", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], reco_bins=["m1000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], year="2022", BMW=BMW),
        "DYHJ0": CreateVariableParameters(gen_variable="DYHJ0", reco_variable="DYHJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], reco_bins=["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], year="2022", BMW=BMW),
        #"PTHvsDPhiJ0J1": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022", BMW=BMW)
    },
    "2023":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2023", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2023", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2023", BMW=BMW),
        "PTJ1": CreateVariableParameters(gen_variable="PTJ1", reco_variable="PTJ1", bins=["NJLE1", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], reco_bins=["0p0_30p0", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], year="2023", BMW=BMW),
        "CosThetaStarCS": CreateVariableParameters(gen_variable="CosThetaStarCS", reco_variable="CosThetaStarCS", bins=["0p0_0p07", "0p07_0p15", "0p15_0p22", "0p22_0p35", "0p35_0p45", "0p45_0p55", "0p55_0p75", "0p75_1p0"], year="2023", BMW=BMW),
        "YJ0": CreateVariableParameters(gen_variable="YJ0", reco_variable="YJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], reco_bins=["m1000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], year="2023", BMW=BMW),
        "MassJ0J1": CreateVariableParameters(gen_variable="MassJ0J1", reco_variable="MassJ0J1", bins=["NJLE1", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], reco_bins=["m1000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], year="2023", BMW=BMW),
        "DYHJ0": CreateVariableParameters(gen_variable="DYHJ0", reco_variable="DYHJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], reco_bins=["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], year="2023", BMW=BMW),
    },
    "2223":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2223", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2223", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2223", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2223", BMW=BMW),
        "PTJ1": CreateVariableParameters(gen_variable="PTJ1", reco_variable="PTJ1", bins=["NJLE1", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], reco_bins=["0p0_30p0", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], year="2223", BMW=BMW),
        "CosThetaStarCS": CreateVariableParameters(gen_variable="CosThetaStarCS", reco_variable="CosThetaStarCS", bins=["0p0_0p07", "0p07_0p15", "0p15_0p22", "0p22_0p35", "0p35_0p45", "0p45_0p55", "0p55_0p75", "0p75_1p0"], year="2223", BMW=BMW),
        "YJ0": CreateVariableParameters(gen_variable="YJ0", reco_variable="YJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], reco_bins=["m1000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], year="2223", BMW=BMW),
        "MassJ0J1": CreateVariableParameters(gen_variable="MassJ0J1", reco_variable="MassJ0J1", bins=["NJLE1", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], reco_bins=["m1000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], year="2223", BMW=BMW),
        "DYHJ0": CreateVariableParameters(gen_variable="DYHJ0", reco_variable="DYHJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], reco_bins=["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], year="2223", BMW=BMW),
    },
    "2024":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2024", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2024", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2024", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2024", BMW=BMW),
        "PTJ1": CreateVariableParameters(gen_variable="PTJ1", reco_variable="PTJ1", bins=["NJLE1", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], reco_bins=["0p0_30p0", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], year="2024", BMW=BMW),
        "CosThetaStarCS": CreateVariableParameters(gen_variable="CosThetaStarCS", reco_variable="CosThetaStarCS", bins=["0p0_0p07", "0p07_0p15", "0p15_0p22", "0p22_0p35", "0p35_0p45", "0p45_0p55", "0p55_0p75", "0p75_1p0"], year="2024", BMW=BMW),
        "YJ0": CreateVariableParameters(gen_variable="YJ0", reco_variable="YJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], reco_bins=["m1000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], year="2024", BMW=BMW),
        "MassJ0J1": CreateVariableParameters(gen_variable="MassJ0J1", reco_variable="MassJ0J1", bins=["NJLE1", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], reco_bins=["m1000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], year="2024", BMW=BMW),
        "DYHJ0": CreateVariableParameters(gen_variable="DYHJ0", reco_variable="DYHJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], reco_bins=["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], year="2024", BMW=BMW),
    },
    "2022_2023":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2022_2023", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2022_2023", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022_2023", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022_2023", BMW=BMW),
        "PTJ1": CreateVariableParameters(gen_variable="PTJ1", reco_variable="PTJ1", bins=["NJLE1", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], reco_bins=["0p0_30p0", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], year="2022_2023", BMW=BMW),
        "CosThetaStarCS": CreateVariableParameters(gen_variable="CosThetaStarCS", reco_variable="CosThetaStarCS", bins=["0p0_0p07", "0p07_0p15", "0p15_0p22", "0p22_0p35", "0p35_0p45", "0p45_0p55", "0p55_0p75", "0p75_1p0"], year="2022_2023", BMW=BMW),
        "YJ0": CreateVariableParameters(gen_variable="YJ0", reco_variable="YJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], reco_bins=["m1000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], year="2022_2023", BMW=BMW),
        "MassJ0J1": CreateVariableParameters(gen_variable="MassJ0J1", reco_variable="MassJ0J1", bins=["NJLE1", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], reco_bins=["m1000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], year="2022_2023", BMW=BMW),
        "DYHJ0": CreateVariableParameters(gen_variable="DYHJ0", reco_variable="DYHJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], reco_bins=["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], year="2022_2023", BMW=BMW),
    },
    "2022_2023_2024":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2022_2023_2024", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2022_2023_2024", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022_2023_2024", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022_2023_2024", BMW=BMW),
        "PTJ1": CreateVariableParameters(gen_variable="PTJ1", reco_variable="PTJ1", bins=["NJLE1", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], reco_bins=["0p0_30p0", "30p0_40p0", "40p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"], year="2022_2023_2024", BMW=BMW),
        "CosThetaStarCS": CreateVariableParameters(gen_variable="CosThetaStarCS", reco_variable="CosThetaStarCS", bins=["0p0_0p07", "0p07_0p15", "0p15_0p22", "0p22_0p35", "0p35_0p45", "0p45_0p55", "0p55_0p75", "0p75_1p0"], year="2022_2023_2024", BMW=BMW),
        "YJ0": CreateVariableParameters(gen_variable="YJ0", reco_variable="YJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], reco_bins=["m1000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5", "2p5_5p0"], year="2022_2023_2024", BMW=BMW),
        "MassJ0J1": CreateVariableParameters(gen_variable="MassJ0J1", reco_variable="MassJ0J1", bins=["NJLE1", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], reco_bins=["m1000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"], year="2022_2023_2024", BMW=BMW),
        "DYHJ0": CreateVariableParameters(gen_variable="DYHJ0", reco_variable="DYHJ0", bins=["NJ0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], reco_bins=["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_5p0"], year="2022_2023_2024", BMW=BMW),
    },
}


def _register_combined_year(name, year_list):
    """
    Build a combined entry in combineVariableDict by reusing the parameter
    definitions from the first year and concatenating the pdf index lists across
    all requested years.
    """
    if name in combineVariableDict:
        return

    missing_years = [year for year in year_list if year not in combineVariableDict]
    if missing_years:
        raise KeyError(f"Cannot build combined year '{name}' without definitions for: {', '.join(missing_years)}")

    template_year = year_list[0]
    combined_entry = {}
    template_variables = combineVariableDict[template_year].keys()

    for variable in template_variables:
        combined_payload = copy.deepcopy(combineVariableDict[template_year][variable])
        combined_payload["pdfIndeces"] = []
        for year in year_list:
            year_payload = combineVariableDict[year][variable]
            combined_payload["pdfIndeces"].extend(year_payload["pdfIndeces"])
        combined_entry[variable] = combined_payload

    combineVariableDict[name] = combined_entry


_combined_year_map = {
    "2022_2023": ["2022", "2023"],
    "2022_2023_2024": ["2022", "2023", "2024"],
}

for combined_name, year_sequence in _combined_year_map.items():
    _register_combined_year(combined_name, year_sequence)
