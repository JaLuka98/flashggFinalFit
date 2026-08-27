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
    '2022preEE': 7.99,
    '2223preEE': 7.99,
    '2022postEE': 26.68,
    '2223postEE': 26.68,
    '2022': 34.67,
    '2023preBPix': 17.96,
    '2223preBPix': 17.96,
    '2023postBPix': 9.68,
    '2223postBPix': 9.68,
    '2023': 27.64,
    '2223': 62.31,
    '2024': 109.82,
    '2024all': 109.82,
    'Run3': 172.13,
    '2022_2023_2024': 172.13,
    '222324': 172.13,
}

def CreateVariableParameters(gen_variable, reco_variable, bins, year, BMW, reco_bins=None):
    if reco_bins is None:
        reco_bins = bins

    paramStr = [f"r_{gen_variable}_{bin}=1" for bin in bins]
    paramStrNoOne = [f"r_{gen_variable}_{bin}" for bin in bins]
    catsStr = [f"RECO_{reco_variable}_{bin}" for bin in reco_bins]
    catsStrWithBMW = [f"RECO_{reco_variable}_{bin}_{bmw}" for bin in reco_bins for bmw in BMW]

    if "_" in year:
        years = year.split("_")
    else:
        years = [year]

    pdfIndeces = [
        f"pdfindex_RECO_{reco_variable}_{bin}_{bmw}_{yr}_{sqrts__}"
        for bin in reco_bins for bmw in BMW for yr in years
    ]

    VariableDict = {
        "paramStr": paramStr,
        "paramStrNoOne": paramStrNoOne,
        "catsStr": catsStr,
        "catsStrWithBMW": catsStrWithBMW,
        "pdfIndeces": pdfIndeces,
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
    ("bbh", "bbHto2G"),
    ("uuH", "uuHToGG"),
    ("ddH", "ddHToGG"),
    ("ssH", "ssHToGG")
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
    "bbHtoGG": 0.52218,
    "bbHto2G": 0.52218,
    "uuHToGG": 1.0,
    "ddHToGG": 1.0,
    "ssHToGG": 1.0,
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
    "uuH": "uuH",
    "ddH": "ddH",
    "ssH": "ssH",
    }

# List of all jet-related variables. Variables listed here will get the CMS_scale_j and CMS_res_j uncertainty in the datacard step.
jetVariables = [
    "NJ",
    "PTJ0",
    "YJ0",
    "NBJet",
    "DYHJ0",
    "TauJC",
    "PTJ1",
    "YJ1",
    "DPhiHJ0",
    "DPhiJ0J1",
    "DPhiHJ0J1",
    "DEtaJ0J1H",
    "MassJ0J1",
    "EtaJ0J1",
    "PTHvsNJ",
]

differentialProcTable_ = {
    "PTH": [
        (10, "PTH_0p0_5p0_in"),
        (11, "PTH_5p0_10p0_in"),
        (12, "PTH_10p0_15p0_in"),
        (13, "PTH_15p0_20p0_in"),
        (14, "PTH_20p0_25p0_in"),
        (15, "PTH_25p0_30p0_in"),
        (16, "PTH_30p0_35p0_in"),
        (17, "PTH_35p0_45p0_in"),
        (18, "PTH_45p0_60p0_in"),
        (19, "PTH_60p0_80p0_in"),
        (110, "PTH_80p0_100p0_in"),
        (111, "PTH_100p0_120p0_in"),
        (112, "PTH_120p0_140p0_in"),
        (113, "PTH_140p0_170p0_in"),
        (114, "PTH_170p0_200p0_in"),
        (115, "PTH_200p0_250p0_in"),
        (116, "PTH_250p0_350p0_in"),
        (117, "PTH_350p0_450p0_in"),
        (118, "PTH_450p0_10000p0_in"),
        (119, "PTH_0p0_10000p0_out")
    ],
    "rapidity": [
        (20, "YH_0p0_0p15_in"),
        (21, "YH_0p15_0p3_in"),
        (22, "YH_0p3_0p45_in"),
        (23, "YH_0p45_0p6_in"),
        (24, "YH_0p6_0p75_in"),
        (25, "YH_0p75_0p9_in"),
        (26, "YH_0p9_1p2_in"),
        (27, "YH_1p2_1p6_in"),
        (28, "YH_1p6_2p0_in"),
        (29, "YH_2p0_2p5_in"),
        (120, "YH_0p0_2p5_out")
    ],
    "NJ": [
        (30, "NJ_0p0_1p0_in"),
        (31, "NJ_1p0_2p0_in"),
        (32, "NJ_2p0_3p0_in"),
        (33, "NJ_3p0_4p0_in"),
        (34, "NJ_4p0_100p0_in"),
        (35, "NJ_0p0_100p0_out")
    ],
    "PTJ0": [
        (40, "PTJ0_m10000p0_30p0_in"),
        (41, "PTJ0_30p0_40p0_in"),
        (42, "PTJ0_40p0_55p0_in"),
        (43, "PTJ0_55p0_75p0_in"),
        (44, "PTJ0_75p0_95p0_in"),
        (45, "PTJ0_95p0_120p0_in"),
        (46, "PTJ0_120p0_150p0_in"),
        (47, "PTJ0_150p0_200p0_in"),
        (48, "PTJ0_200p0_10000p0_in"),
        (49, "PTJ0_0p0_10000p0_out")
    ],
    "CosThetaStarCS": [
        (1000, "CosThetaStarCS_0p0_0p07_in"),
        (1001, "CosThetaStarCS_0p07_0p15_in"),
        (1002, "CosThetaStarCS_0p15_0p22_in"),
        (1003, "CosThetaStarCS_0p22_0p35_in"),
        (1004, "CosThetaStarCS_0p35_0p45_in"),
        (1005, "CosThetaStarCS_0p45_0p55_in"),
        (1006, "CosThetaStarCS_0p55_0p75_in"),
        (1007, "CosThetaStarCS_0p75_1p0_in"),
        (1008, "CosThetaStarCS_0p0_1p0_out")
    ],
    "PhiEtaStar": [
        (1010, "PhiEtaStar_0p0_0p05_in"),
        (1011, "PhiEtaStar_0p05_0p1_in"),
        (1012, "PhiEtaStar_0p1_0p2_in"),
        (1013, "PhiEtaStar_0p2_0p3_in"),
        (1014, "PhiEtaStar_0p3_0p4_in"),
        (1015, "PhiEtaStar_0p4_0p5_in"),
        (1016, "PhiEtaStar_0p5_0p7_in"),
        (1017, "PhiEtaStar_0p7_1p0_in"),
        (1018, "PhiEtaStar_1p0_1p5_in"),
        (1019, "PhiEtaStar_1p5_2p5_in"),
        (1020, "PhiEtaStar_2p5_4p0_in"),
        (1021, "PhiEtaStar_4p0_100p0_in"),
        (1022, "PhiEtaStar_0p0_4p0_out")
    ],
    "NBJet": [
        (1270, "NBJet_0p0_1p0_in"),
        (1271, "NBJet_1p0_2p0_in"),
        (1272, "NBJet_2p0_100p0_in"),
        (1273, "NBJet_0p0_100p0_out")
    ],
    "YJ0": [
        (1100, "YJ0_m10000p0_0p0_in"),
        (1101, "YJ0_0p0_0p3_in"),
        (1102, "YJ0_0p3_0p6_in"),
        (1103, "YJ0_0p6_0p9_in"),
        (1104, "YJ0_0p9_1p2_in"),
        (1105, "YJ0_1p2_1p6_in"),
        (1106, "YJ0_1p6_2p0_in"),
        (1107, "YJ0_2p0_2p5_in"),
        (1108, "YJ0_0p0_2p5_out")
    ],
    "DPhiHJ0": [
        (1110, "DPhiHJ0_m10000p0_0p0_in"),
        (1111, "DPhiHJ0_0p0_2p0_in"),
        (1112, "DPhiHJ0_2p0_2p6_in"),
        (1113, "DPhiHJ0_2p6_2p85_in"),
        (1114, "DPhiHJ0_2p85_3p0_in"),
        (1115, "DPhiHJ0_3p0_3p07_in"),
        (1116, "DPhiHJ0_3p07_3p1416_in"),
        (1117, "DPhiHJ0_0p0_3p1416_out")
    ],
    "DYHJ0": [
        (1120, "DYHJ0_m10000p0_0p0_in"),
        (1121, "DYHJ0_0p0_0p3_in"),
        (1122, "DYHJ0_0p3_0p6_in"),
        (1123, "DYHJ0_0p6_1p0_in"),
        (1124, "DYHJ0_1p0_1p4_in"),
        (1125, "DYHJ0_1p4_1p9_in"),
        (1126, "DYHJ0_1p9_2p5_in"),
        (1127, "DYHJ0_2p5_100p0_in"),
        (1128, "DYHJ0_0p0_100p0_out")
    ],
    "TauJC": [
        (1130, "TauJC_m10000p0_0p0_in"),
        (1131, "TauJC_0p0_15p0_in"),
        (1132, "TauJC_15p0_20p0_in"),
        (1133, "TauJC_20p0_30p0_in"),
        (1134, "TauJC_30p0_50p0_in"),
        (1135, "TauJC_50p0_80p0_in"),
        (1136, "TauJC_80p0_10000p0_in"),
        (1137, "TauJC_0p0_10000p0_out")
    ],
    "PTJ1": [
        (50, "PTJ1_m10000p0_30p0_in"),
        (51, "PTJ1_30p0_45p0_in"),
        (52, "PTJ1_45p0_65p0_in"),
        (53, "PTJ1_65p0_90p0_in"),
        (54, "PTJ1_90p0_150p0_in"),
        (55, "PTJ1_150p0_10000p0_in"),
        (56, "PTJ1_m10000p0_10000p0_out")
    ],
    "YJ1": [
        (1210, "YJ1_m10000p0_0p0_in"),
        (1211, "YJ1_0p0_0p6_in"),
        (1212, "YJ1_0p6_1p2_in"),
        (1213, "YJ1_1p2_1p8_in"),
        (1214, "YJ1_1p8_2p5_in"),
        (1215, "YJ1_2p5_3p5_in"),
        (1216, "YJ1_3p5_5p0_in"),
        (1217, "YJ1_0p0_5p0_out")
    ],
    "DPhiJ0J1": [
        (50, "DPhiJ0J1_m10000p0_m3p1416_in"),
        (51, "DPhiJ0J1_m3p1416_m2p0944_in"),
        (52, "DPhiJ0J1_m2p0944_m1p0472_in"),
        (53, "DPhiJ0J1_m1p0472_0p0_in"),
        (54, "DPhiJ0J1_0p0_1p0472_in"),
        (55, "DPhiJ0J1_1p0472_2p0944_in"),
        (56, "DPhiJ0J1_2p0944_3p1416_in"),
        (57, "DPhiJ0J1_m3p1416_3p1416_out")
    ],
    "DPhiHJ0J1": [
        (1230, "DPhiHJ0J1_m10000p0_0p0_in"),
        (1231, "DPhiHJ0J1_0p0_2p0_in"),
        (1232, "DPhiHJ0J1_2p0_2p7_in"),
        (1233, "DPhiHJ0J1_2p7_2p95_in"),
        (1234, "DPhiHJ0J1_2p95_3p07_in"),
        (1235, "DPhiHJ0J1_3p07_3p1416_in"),
        (1236, "DPhiHJ0J1_0p0_3p1416_out")
    ],
    "DEtaJ0J1H": [
        (1240, "DEtaJ0J1H_m10000p0_0p0_in"),
        (1241, "DEtaJ0J1H_0p0_0p2_in"),
        (1242, "DEtaJ0J1H_0p2_0p5_in"),
        (1243, "DEtaJ0J1H_0p5_0p85_in"),
        (1244, "DEtaJ0J1H_0p85_1p2_in"),
        (1245, "DEtaJ0J1H_1p2_1p7_in"),
        (1246, "DEtaJ0J1H_1p7_100p0_in"),
        (1247, "DEtaJ0J1H_0p0_100p0_out")
    ],
    "MassJ0J1": [
        (70, "MassJ0J1_m10000p0_0p0_in"),
        (71, "MassJ0J1_0p0_75p0_in"),
        (72, "MassJ0J1_75p0_120p0_in"),
        (73, "MassJ0J1_120p0_180p0_in"),
        (74, "MassJ0J1_180p0_300p0_in"),
        (75, "MassJ0J1_300p0_500p0_in"),
        (76, "MassJ0J1_500p0_1000p0_in"),
        (77, "MassJ0J1_1000p0_10000p0_in"),
        (78, "MassJ0J1_m10000p0_10000p0_out")
    ],
    "EtaJ0J1": [
        (1260, "EtaJ0J1_m10000p0_0p0_in"),
        (1261, "EtaJ0J1_0p0_0p7_in"),
        (1262, "EtaJ0J1_0p7_1p6_in"),
        (1263, "EtaJ0J1_1p6_3p0_in"),
        (1264, "EtaJ0J1_3p0_5p0_in"),
        (1265, "EtaJ0J1_5p0_100p0_in"),
        (1266, "EtaJ0J1_0p0_100p0_out")
    ],
    "PTHvDPhiJ0J1": [
        (4501, "PTHvDPhiJ0J1_0p0_35p0_m3p1416_m1p5708_in"),
        (4502, "PTHvDPhiJ0J1_0p0_35p0_m1p5708_0p0_in"),
        (4503, "PTHvDPhiJ0J1_0p0_35p0_0p0_1p5708_in"),
        (4504, "PTHvDPhiJ0J1_0p0_35p0_1p5708_3p1416_in"),
        (4505, "PTHvDPhiJ0J1_35p0_80p0_m3p1416_m1p5708_in"),
        (4506, "PTHvDPhiJ0J1_35p0_80p0_m1p5708_0p0_in"),
        (4507, "PTHvDPhiJ0J1_35p0_80p0_0p0_1p5708_in"),
        (4508, "PTHvDPhiJ0J1_35p0_80p0_1p5708_3p1416_in"),
        (4509, "PTHvDPhiJ0J1_80p0_150p0_m3p1416_m1p5708_in"),
        (4510, "PTHvDPhiJ0J1_80p0_150p0_m1p5708_0p0_in"),
        (4511, "PTHvDPhiJ0J1_80p0_150p0_0p0_1p5708_in"),
        (4512, "PTHvDPhiJ0J1_80p0_150p0_1p5708_3p1416_in"),
        (4513, "PTHvDPhiJ0J1_150p0_300p0_m3p1416_m1p5708_in"),
        (4514, "PTHvDPhiJ0J1_150p0_300p0_m1p5708_0p0_in"),
        (4515, "PTHvDPhiJ0J1_150p0_300p0_0p0_1p5708_in"),
        (4516, "PTHvDPhiJ0J1_150p0_300p0_1p5708_3p1416_in"),
        (4517, "PTHvDPhiJ0J1_300p0_10000p0_m3p1416_m1p5708_in"),
        (4518, "PTHvDPhiJ0J1_300p0_10000p0_m1p5708_0p0_in"),
        (4519, "PTHvDPhiJ0J1_300p0_10000p0_0p0_1p5708_in"),
        (4520, "PTHvDPhiJ0J1_300p0_10000p0_1p5708_3p1416_in"),
        (4533, "PTHvDPhiJ0J1_0p0_10000p0_m4p0_4p0_out"),
    ],
    "PTHvYH":[
        (4601, "PTHvYH_0p0_50p0_0p0_0p2_in"),
        (4602, "PTHvYH_0p0_50p0_0p2_0p4_in"),
        (4603, "PTHvYH_0p0_50p0_0p4_0p65_in"),
        (4604, "PTHvYH_0p0_50p0_0p65_0p9_in"),
        (4605, "PTHvYH_0p0_50p0_0p9_1p2_in"),
        (4606, "PTHvYH_0p0_50p0_1p2_2p5_in"),
        (4607, "PTHvYH_50p0_105p0_0p0_0p5_in"),
        (4608, "PTHvYH_50p0_105p0_0p5_1p15_in"),
        (4609, "PTHvYH_50p0_105p0_1p15_2p5_in"),
        (4610, "PTHvYH_105p0_10000p0_0p0_0p45_in"),
        (4611, "PTHvYH_105p0_10000p0_0p45_1p0_in"),
        (4612, "PTHvYH_105p0_10000p0_1p0_2p5_in"),
        (4631, "PTHvYH_0p0_10000p0_0p0_2p5_out")
    ],
    "PTHvsNJ": [
        (46001, "PTHvsNJ_NJ0_PTH_0p0_5p0_in"),
        (46002, "PTHvsNJ_NJ0_PTH_5p0_10p0_in"),
        (46003, "PTHvsNJ_NJ0_PTH_10p0_15p0_in"),
        (46004, "PTHvsNJ_NJ0_PTH_15p0_20p0_in"),
        (46005, "PTHvsNJ_NJ0_PTH_20p0_25p0_in"),
        (46006, "PTHvsNJ_NJ0_PTH_25p0_30p0_in"),
        (46007, "PTHvsNJ_NJ0_PTH_30p0_35p0_in"),
        (46008, "PTHvsNJ_NJ0_PTH_35p0_45p0_in"),
        (46009, "PTHvsNJ_NJ0_PTH_45p0_60p0_in"),
        (46010, "PTHvsNJ_NJ0_PTH_60p0_10000p0_in"),
        (46011, "PTHvsNJ_NJ1_PTH_0p0_30p0_in"),
        (46012, "PTHvsNJ_NJ1_PTH_30p0_60p0_in"),
        (46013, "PTHvsNJ_NJ1_PTH_60p0_100p0_in"),
        (46014, "PTHvsNJ_NJ1_PTH_100p0_170p0_in"),
        (46015, "PTHvsNJ_NJ1_PTH_170p0_10000p0_in"),
        (46016, "PTHvsNJ_NJ2p_PTH_0p0_100p0_in"),
        (46017, "PTHvsNJ_NJ2p_PTH_100p0_170p0_in"),
        (46018, "PTHvsNJ_NJ2p_PTH_170p0_250p0_in"),
        (46019, "PTHvsNJ_NJ2p_PTH_250p0_350p0_in"),
        (46020, "PTHvsNJ_NJ2p_PTH_350p0_10000p0_in"),
        (46021, "PTHvsNJ_NJ0p_PTH_0p0_10000p0_out"),
    ],
}

#BMW == Best Medium Worst
BMW = ['cat0', 'cat1', 'cat2']

# Variable bins
variableBins = {
    "PTH": ["0p0_5p0","5p0_10p0","10p0_15p0","15p0_20p0","20p0_25p0","25p0_30p0","30p0_35p0","35p0_45p0","45p0_60p0","60p0_80p0","80p0_100p0","100p0_120p0","120p0_140p0","140p0_170p0","170p0_200p0","200p0_250p0","250p0_350p0","350p0_450p0","450p0_10000p0"],
    "NJ": ["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_4p0", "4p0_100p0"],
    "rapidity": ["0p0_0p15", "0p15_0p3", "0p3_0p45", "0p45_0p6", "0p6_0p75", "0p75_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5"],
    "PTJ0": ["m10000p0_30p0", "30p0_40p0", "40p0_55p0", "55p0_75p0", "75p0_95p0", "95p0_120p0", "120p0_150p0", "150p0_200p0", "200p0_10000p0"],
    "DPhiJ0J1": ["m10000p0_m3p1416", "m3p1416_m2p0944", "m2p0944_m1p0472", "m1p0472_0p0", "0p0_1p0472", "1p0472_2p0944", "2p0944_3p1416"],
    "PTHvsDPhiJ0J1": ["0p0_35p0_m3p1416_m1p5708", "0p0_35p0_m1p5708_0p0", "0p0_35p0_0p0_1p5708", "0p0_35p0_1p5708_3p1416", "35p0_80p0_m3p1416_m1p5708", "35p0_80p0_m1p5708_0p0", "35p0_80p0_0p0_1p5708", "35p0_80p0_1p5708_3p1416", "80p0_150p0_m3p1416_m1p5708", "80p0_150p0_m1p5708_0p0", "80p0_150p0_0p0_1p5708", "80p0_150p0_1p5708_3p1416", "150p0_300p0_m3p1416_m1p5708", "150p0_300p0_m1p5708_0p0", "150p0_300p0_0p0_1p5708", "150p0_300p0_1p5708_3p1416", "300p0_10000p0_m3p1416_m1p5708", "300p0_10000p0_m1p5708_0p0", "300p0_10000p0_0p0_1p5708", "300p0_10000p0_1p5708_3p1416"],
    "NBJet": ["0p0_1p0", "1p0_2p0", "2p0_100p0"],
    "DYHJ0": ["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_1p0", "1p0_1p4", "1p4_1p9", "1p9_2p5", "2p5_100p0"],
    "TauJC": ["m10000p0_0p0", "0p0_15p0", "15p0_20p0", "20p0_30p0", "30p0_50p0", "50p0_80p0", "80p0_10000p0"],
    "PTJ1": ["m10000p0_30p0", "30p0_45p0", "45p0_65p0", "65p0_90p0", "90p0_150p0", "150p0_10000p0"],
    "YJ1": ["m10000p0_0p0", "0p0_0p6", "0p6_1p2", "1p2_1p8", "1p8_2p5", "2p5_3p5", "3p5_5p0"],
    "CosThetaStarCS": ["0p0_0p07", "0p07_0p15", "0p15_0p22", "0p22_0p35", "0p35_0p45", "0p45_0p55", "0p55_0p75", "0p75_1p0"],
    "PhiEtaStar": ["0p0_0p05", "0p05_0p1", "0p1_0p2", "0p2_0p3", "0p3_0p4", "0p4_0p5", "0p5_0p7", "0p7_1p0", "1p0_1p5", "1p5_2p5", "2p5_4p0", "4p0_100p0"],
    "DPhiHJ0": ["m10000p0_0p0", "0p0_2p0", "2p0_2p6", "2p6_2p85", "2p85_3p0", "3p0_3p07", "3p07_3p1416"],
    "YJ0": ["m10000p0_0p0", "0p0_0p3", "0p3_0p6", "0p6_0p9", "0p9_1p2", "1p2_1p6", "1p6_2p0", "2p0_2p5"],
    "DPhiHJ0J1": ["m10000p0_0p0", "0p0_2p0", "2p0_2p7", "2p7_2p95", "2p95_3p07", "3p07_3p1416"],
    "DEtaJ0J1H": ["m10000p0_0p0", "0p0_0p2", "0p2_0p5", "0p5_0p85", "0p85_1p2", "1p2_1p7", "1p7_100p0"],
    "MassJ0J1": ["m10000p0_0p0", "0p0_75p0", "75p0_120p0", "120p0_180p0", "180p0_300p0", "300p0_500p0", "500p0_1000p0", "1000p0_10000p0"],
    "EtaJ0J1": ["m10000p0_0p0", "0p0_0p7", "0p7_1p6", "1p6_3p0", "3p0_5p0", "5p0_100p0"],
    "PTHvYH": ["0p0_50p0_0p0_0p2", "0p0_50p0_0p2_0p4", "0p0_50p0_0p4_0p65", "0p0_50p0_0p65_0p9", "0p0_50p0_0p9_1p2", "0p0_50p0_1p2_2p5", "50p0_105p0_0p0_0p5", "50p0_105p0_0p5_1p15", "50p0_105p0_1p15_2p5", "105p0_10000p0_0p0_0p45", "105p0_10000p0_0p45_1p0", "105p0_10000p0_1p0_2p5"],
    "PTHvsNJ": [
        "NJ0_PTH_0p0_5p0",
        "NJ0_PTH_5p0_10p0",
        "NJ0_PTH_10p0_15p0",
        "NJ0_PTH_15p0_20p0",
        "NJ0_PTH_20p0_25p0",
        "NJ0_PTH_25p0_30p0",
        "NJ0_PTH_30p0_35p0",
        "NJ0_PTH_35p0_45p0",
        "NJ0_PTH_45p0_60p0",
        "NJ0_PTH_60p0_10000p0",
        "NJ1_PTH_0p0_30p0",
        "NJ1_PTH_30p0_60p0",
        "NJ1_PTH_60p0_100p0",
        "NJ1_PTH_100p0_170p0",
        "NJ1_PTH_170p0_10000p0",
        "NJ2p_PTH_0p0_100p0",
        "NJ2p_PTH_100p0_170p0",
        "NJ2p_PTH_170p0_250p0",
        "NJ2p_PTH_250p0_350p0",
        "NJ2p_PTH_350p0_10000p0",
    ],
}

recoVariableBins = {
    variable: bins[:] for variable, bins in variableBins.items()
}
recoVariableBins["YJ0"] = [
    "m10000p0_0p0",
    "0p0_0p3",
    "0p3_0p6",
    "0p6_0p9",
    "0p9_1p2",
    "1p2_1p6",
    "1p6_2p0",
    "2p0_2p5",
]
recoVariableBins["YJ1"] = [
    "m10000p0_0p0",
    "0p0_0p6",
    "0p6_1p2",
    "1p2_1p8",
    "1p8_2p5",
    "2p5_3p5",
    "3p5_4p7",
]
recoVariableBins["PTHvsNJ"] = [
    "NJ0p0_PTH0p0_5p0",
    "NJ0p0_PTH5p0_10p0",
    "NJ0p0_PTH10p0_15p0",
    "NJ0p0_PTH15p0_20p0",
    "NJ0p0_PTH20p0_25p0",
    "NJ0p0_PTH25p0_30p0",
    "NJ0p0_PTH30p0_35p0",
    "NJ0p0_PTH35p0_45p0",
    "NJ0p0_PTH45p0_60p0",
    "NJ0p0_PTH60p0_10000p0",
    "NJ1p0_PTH0p0_30p0",
    "NJ1p0_PTH30p0_60p0",
    "NJ1p0_PTH60p0_100p0",
    "NJ1p0_PTH100p0_170p0",
    "NJ1p0_PTH170p0_10000p0",
    "NJ2p0_PTH0p0_100p0",
    "NJ2p0_PTH100p0_170p0",
    "NJ2p0_PTH170p0_250p0",
    "NJ2p0_PTH250p0_350p0",
    "NJ2p0_PTH350p0_10000p0",
]

differentialProcTable_["PTH_lightquarks"] = differentialProcTable_["PTH"]
variableBins["PTH_lightquarks"] = variableBins["PTH"]
recoVariableBins["PTH_lightquarks"] = recoVariableBins["PTH"]

differentialProcTable_["rapidity_lightquarks"] = differentialProcTable_["rapidity"]
variableBins["rapidity_lightquarks"] = variableBins["rapidity"]
recoVariableBins["rapidity_lightquarks"] = recoVariableBins["rapidity"]

def combineVariableDict(variable, year):
    if variable == "inclusive_lightquarks":
        return {
            "paramStr": ["r=1"],
            "paramStrNoOne": ["r"],
            "catsStr": [],
            "catsStrWithBMW": [],
            "pdfIndeces": [],
        }

    # Split the years if it's a combined year, otherwise just use the single year
    year_list = year.split('_') if '_' in year else [year]
    template_year = year_list[0]
    if len(year_list) > 1:
        # Add the pdfIndices from all the years together for the combined year
        combined_pdf_indices = []
        gen_variable = "YH" if variable in ["rapidity", "rapidity_lightquarks"] else variable
        reco_variable = "rapidity" if variable == "rapidity_lightquarks" else variable
        combined_payload = CreateVariableParameters(gen_variable=gen_variable, reco_variable=reco_variable, bins=variableBins[variable], reco_bins=recoVariableBins[variable], year=template_year, BMW=BMW)
        for y in year_list:
            year_payload = combineVariableDict(variable, y)
            combined_pdf_indices.extend(year_payload["pdfIndeces"])
        combined_payload["pdfIndeces"] = combined_pdf_indices
        return combined_payload
    else:
        gen_variable = "YH" if variable in ["rapidity", "rapidity_lightquarks"] else variable
        reco_variable = "rapidity" if variable == "rapidity_lightquarks" else variable
        return CreateVariableParameters(gen_variable=gen_variable, reco_variable=reco_variable, bins=variableBins[variable], reco_bins=recoVariableBins[variable], year=template_year, BMW=BMW)
