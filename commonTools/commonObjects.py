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

def CreateVariableParameters(gen_variable, reco_variable, bins, year, BMW):
    paramStr = [f"r_{gen_variable}_{bin}=1" for bin in bins]
    paramStrNoOne = [f"r_{gen_variable}_{bin}" for bin in bins]
    catsStr = [f"RECO_{reco_variable}_{bin}" for bin in bins]
    catsStrWithBMW = [f"RECO_{reco_variable}_{bin}_{bmw}" for bin in bins for bmw in BMW]

    if "_" in year:
        years = year.split("_")
    else:
        years = [year]

    pdfIndeces = [
        f"pdfindex_RECO_{reco_variable}_{bin}_{bmw}_{yr}_{sqrts__}"
        for bin in bins for bmw in BMW for yr in years
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
    "NJ_pt30_absEta2p5",
    "PTJ0",
    "PTJ0_pt30_absEta2p5",
    "YJ0",
    "AbsPhiHJ0",
    "AbsYHJ0"
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
    "NJ_pt30_absEta2p5": [
        (80, "NJ_pt30_absEta2p5_0p0_1p0_in"),
        (81, "NJ_pt30_absEta2p5_1p0_2p0_in"),
        (82, "NJ_pt30_absEta2p5_2p0_3p0_in"),
        (83, "NJ_pt30_absEta2p5_3p0_100p0_in"),
        (84, "NJ_pt30_absEta2p5_0p0_100p0_out")
    ],
    "PTJ0": [
        (40, "PTJ0_0p0_30p0_in"),
        (41, "PTJ0_30p0_75p0_in"),
        (42, "PTJ0_75p0_120p0_in"),
        (43, "PTJ0_120p0_200p0_in"),
        (44, "PTJ0_200p0_10000p0_in"),
        (45, "PTJ0_0p0_10000p0_out")
    ],
    "PTJ0_pt30_absEta2p5": [
        (90, "PTJ0_pt30_absEta2p5_0p0_30p0_in"),
        (91, "PTJ0_pt30_absEta2p5_30p0_75p0_in"),
        (92, "PTJ0_pt30_absEta2p5_75p0_120p0_in"),
        (93, "PTJ0_pt30_absEta2p5_120p0_200p0_in"),
        (94, "PTJ0_pt30_absEta2p5_200p0_10000p0_in"),
        (95, "PTJ0_pt30_absEta2p5_0p0_10000p0_out")
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
    "CosThetaStarCS": [
        (1000, "CosThetaStarCS_0p0_0p07_in"),
        (1001, "CosThetaStarCS_0p07_0p15_in"),
        (1002, "CosThetaStarCS_0p15_0p22_in"),
        (1003, "CosThetaStarCS_0p22_0p35_in"),
        (1004, "CosThetaStarCS_0p35_0p45_in"),
        (1005, "CosThetaStarCS_0p45_0p55_in"),
        (1006, "CosThetaStarCS_0p55_0p75_in"),
        (1007, "CosThetaStarCS_0p0_0p75_out")
    ],
    "ThetaEtaStar": [
        (1010, "ThetaEtaStar_0p0_0p05_in"),
        (1011, "ThetaEtaStar_0p05_0p1_in"),
        (1012, "ThetaEtaStar_0p1_0p2_in"),
        (1013, "ThetaEtaStar_0p2_0p3_in"),
        (1014, "ThetaEtaStar_0p3_0p4_in"),
        (1015, "ThetaEtaStar_0p4_0p5_in"),
        (1016, "ThetaEtaStar_0p5_0p7_in"),
        (1017, "ThetaEtaStar_0p0_0p7_out")
    ],
    "NBJet": [
        (1020, "NBJet_0p0_1p0_in"),
        (1021, "NBJet_1p0_2p0_in"),
        (1022, "NBJet_2p0_100p0_in"),
        (1023, "NBJet_0p0_100p0_out")
    ],
    "YJ0": [
        (1100, "YJ0_0p0_0p3_in"),
        (1101, "YJ0_0p3_0p6_in"),
        (1102, "YJ0_0p6_0p9_in"),
        (1103, "YJ0_0p9_1p2_in"),
        (1104, "YJ0_1p2_1p6_in"),
        (1105, "YJ0_1p6_2p0_in"),
        (1106, "YJ0_2p0_2p5_in"),
        (1107, "YJ0_0p0_2p5_out")
    ],
    "DPhiHJ0": [
        (1110, "DPhiHJ0_0p0_2p0_in"),
        (1111, "DPhiHJ0_2p0_2p6_in"),
        (1112, "DPhiHJ0_2p6_2p85_in"),
        (1113, "DPhiHJ0_2p85_3p0_in"),
        (1114, "DPhiHJ0_3p0_3p07_in"),
        (1115, "DPhiHJ0_3p07_3p1416_in"),
        (1116, "DPhiHJ0_0p0_3p1416_out")
    ],
    "DYHJ0": [
        (1120, "DYHJ0_0p0_0p3_in"),
        (1121, "DYHJ0_0p3_0p6_in"),
        (1122, "DYHJ0_0p6_1p0_in"),
        (1123, "DYHJ0_1p0_1p4_in"),
        (1124, "DYHJ0_1p4_1p9_in"),
        (1125, "DYHJ0_1p9_2p5_in"),
        (1126, "DYHJ0_2p5_100p0_in"),
        (1127, "DYHJ0_0p0_100p0_out")
    ],
    "TauJC": [
        (1130, "TauJC_0p0_15p0_in"),
        (1131, "TauJC_15p0_20p0_in"),
        (1132, "TauJC_20p0_30p0_in"),
        (1133, "TauJC_30p0_50p0_in"),
        (1134, "TauJC_50p0_80p0_in"),
        (1135, "TauJC_80p0_10000p0_in"),
        (1136, "TauJC_0p0_10000p0_out")
    ],
    "PTJ1": [
        (1200, "PTJ1_30p0_40p0_in"),
        (1201, "PTJ1_40p0_65p0_in"),
        (1202, "PTJ1_65p0_90p0_in"),
        (1203, "PTJ1_90p0_150p0_in"),
        (1204, "PTJ1_150p0_10000p0_in"),
        (1208, "PTJ1_30p0_10000p0_out")
    ],
    "YJ1": [
        (1210, "YJ1_0p0_0p6_in"),
        (1211, "YJ1_0p6_1p2_in"),
        (1212, "YJ1_1p2_1p8_in"),
        (1213, "YJ1_1p8_3p5_in"),
        (1214, "YJ1_3p5_5p0_in"),
        (1215, "YJ1_0p0_5p0_out")
    ],
    "DPhiJ0J1": [
        (50, "DPhiJ0J1_m3p1416_m2p0944_in"),
        (51, "DPhiJ0J1_m2p0944_m1p0472_in"),
        (52, "DPhiJ0J1_m1p0472_0p0_in"),
        (53, "DPhiJ0J1_0p0_1p0472_in"),
        (54, "DPhiJ0J1_1p0472_2p0944_in"),
        (55, "DPhiJ0J1_2p0944_3p1416_in"),
        (56, "DPhiJ0J1_m3p1416_3p1416_out")
    ],
    "DPhiHJ0J1": [
        (1230, "DPhiHJ0J1_0p0_2p0_in"),
        (1231, "DPhiHJ0J1_2p0_2p7_in"),
        (1232, "DPhiHJ0J1_2p7_2p95_in"),
        (1233, "DPhiHJ0J1_2p95_3p07_in"),
        (1234, "DPhiHJ0J1_3p07_3p1416_in"),
        (1235, "DPhiHJ0J1_0p0_3p1416_out")
    ],
    "DEtaJ0J1H": [
        (1240, "DEtaJ0J1H_0p0_0p2_in"),
        (1241, "DEtaJ0J1H_0p2_0p5_in"),
        (1242, "DEtaJ0J1H_0p5_0p85_in"),
        (1243, "DEtaJ0J1H_0p85_1p2_in"),
        (1244, "DEtaJ0J1H_1p2_1p7_in"),
        (1245, "DEtaJ0J1H_1p7_100p0_in"),
        (1246, "DEtaJ0J1H_0p0_100p0_out")
    ],
    "MassJ0J1": [
        (1250, "MassJ0J1_0p0_75p0_in"),
        (1251, "MassJ0J1_75p0_120p0_in"),
        (1252, "MassJ0J1_120p0_180p0_in"),
        (1253, "MassJ0J1_180p0_300p0_in"),
        (1254, "MassJ0J1_300p0_500p0_in"),
        (1255, "MassJ0J1_500p0_1000p0_in"),
        (1256, "MassJ0J1_1000p0_10000p0_in"),
        (1257, "MassJ0J1_0p0_10000p0_out")
    ],
    "EtaJ0J1": [
        (1260, "EtaJ0J1_0p0_0p7_in"),
        (1261, "EtaJ0J1_0p7_1p6_in"),
        (1262, "EtaJ0J1_1p6_3p0_in"),
        (1263, "EtaJ0J1_3p0_5p0_in"),
        (1264, "EtaJ0J1_5p0_100p0_in"),
        (1265, "EtaJ0J1_0p0_100p0_out")
    ],
    "PTHvDPhiJ0J1": [
        (4501, "PTHvDPhiJ0J1_0p0_15p0_mPi_m23Pi_in"),
        (4502, "PTHvDPhiJ0J1_0p0_15p0_m23Pi_m13Pi_in"),
        (4503, "PTHvDPhiJ0J1_0p0_15p0_m13Pi_0p0_in"),
        (4504, "PTHvDPhiJ0J1_0p0_15p0_0p0_13Pi_in"),
        (4505, "PTHvDPhiJ0J1_0p0_15p0_13Pi_23Pi_in"),
        (4506, "PTHvDPhiJ0J1_0p0_15p0_23Pi_Pi_in"),

        (4507, "PTHvDPhiJ0J1_15p0_30p0_mPi_m23Pi_in"),
        (4508, "PTHvDPhiJ0J1_15p0_30p0_m23Pi_m13Pi_in"),
        (4509, "PTHvDPhiJ0J1_15p0_30p0_m13Pi_0p0_in"),
        (4510, "PTHvDPhiJ0J1_15p0_30p0_0p0_13Pi_in"),
        (4511, "PTHvDPhiJ0J1_15p0_30p0_13Pi_23Pi_in"),
        (4512, "PTHvDPhiJ0J1_15p0_30p0_23Pi_Pi_in"),

        (4513, "PTHvDPhiJ0J1_30p0_45p0_mPi_m23Pi_in"),
        (4514, "PTHvDPhiJ0J1_30p0_45p0_m23Pi_m13Pi_in"),
        (4515, "PTHvDPhiJ0J1_30p0_45p0_m13Pi_0p0_in"),
        (4516, "PTHvDPhiJ0J1_30p0_45p0_0p0_13Pi_in"),
        (4517, "PTHvDPhiJ0J1_30p0_45p0_13Pi_23Pi_in"),
        (4518, "PTHvDPhiJ0J1_30p0_45p0_23Pi_Pi_in"),

        (4519, "PTHvDPhiJ0J1_45p0_80p0_mPi_m23Pi_in"),
        (4520, "PTHvDPhiJ0J1_45p0_80p0_m23Pi_m13Pi_in"),
        (4521, "PTHvDPhiJ0J1_45p0_80p0_m13Pi_0p0_in"),
        (4522, "PTHvDPhiJ0J1_45p0_80p0_0p0_13Pi_in"),
        (4523, "PTHvDPhiJ0J1_45p0_80p0_13Pi_23Pi_in"),
        (4524, "PTHvDPhiJ0J1_45p0_80p0_23Pi_Pi_in"),

        (4525, "PTHvDPhiJ0J1_80p0_120p0_mPi_m23Pi_in"),
        (4526, "PTHvDPhiJ0J1_80p0_120p0_m23Pi_m13Pi_in"),
        (4527, "PTHvDPhiJ0J1_80p0_120p0_m13Pi_0p7_in"),
        (4528, "PTHvDPhiJ0J1_80p0_120p0_0p7_13Pi_in"),
        (4529, "PTHvDPhiJ0J1_80p0_120p0_13Pi_23Pi_in"),
        (4530, "PTHvDPhiJ0J1_80p0_120p0_23Pi_Pi_in"),

        (4531, "PTHvDPhiJ0J1_120p0_200p0_mPi_m23Pi_in"),
        (4532, "PTHvDPhiJ0J1_120p0_200p0_m23Pi_m13Pi_in"),
        (4533, "PTHvDPhiJ0J1_120p0_200p0_m13Pi_0p7_in"),
        (4534, "PTHvDPhiJ0J1_120p0_200p0_0p7_13Pi_in"),
        (4535, "PTHvDPhiJ0J1_120p0_200p0_13Pi_23Pi_in"),
        (4536, "PTHvDPhiJ0J1_120p0_200p0_23Pi_Pi_in"),

        (4537, "PTHvDPhiJ0J1_200p0_350p0_mPi_m23Pi_in"),
        (4538, "PTHvDPhiJ0J1_200p0_350p0_m23Pi_m13Pi_in"),
        (4539, "PTHvDPhiJ0J1_200p0_350p0_m13Pi_0p7_in"),
        (4540, "PTHvDPhiJ0J1_200p0_350p0_0p7_13Pi_in"),
        (4541, "PTHvDPhiJ0J1_200p0_350p0_13Pi_23Pi_in"),
        (4542, "PTHvDPhiJ0J1_200p0_350p0_23Pi_Pi_in"),

        (4543, "PTHvDPhiJ0J1_350p0_10000p0_mPi_m23Pi_in"),
        (4544, "PTHvDPhiJ0J1_350p0_10000p0_m23Pi_m13Pi_in"),
        (4545, "PTHvDPhiJ0J1_350p0_10000p0_m13Pi_0p7_in"),
        (4546, "PTHvDPhiJ0J1_350p0_10000p0_0p7_13Pi_in"),
        (4547, "PTHvDPhiJ0J1_350p0_10000p0_13Pi_23Pi_in"),
        (4548, "PTHvDPhiJ0J1_350p0_10000p0_23Pi_Pi_in"),

        (4549, "PTHvDPhiJ0J1_0p0_10000p0_m4p0_4p0_out"),
    ],
    "PTHvRapidity":[
        (4601, "PTHvRapidity_0p0_40p0_0p0_0p5_in"),
        (4602, "PTHvRapidity_40p0_80p0_0p0_0p5_in"),
        (4603, "PTHvRapidity_80p0_150p0_0p0_0p5_in"),
        (4604, "PTHvRapidity_150p0_10000p0_0p0_0p5_in"),

        (4611, "PTHvRapidity_0p0_45p0_0p5_1p0_in"),
        (4612, "PTHvRapidity_45p0_120p0_0p5_1p0_in"),
        (4613, "PTHvRapidity_120p0_10000p0_0p5_1p0_in"),

        (4621, "PTHvRapidity_0p0_45p0_1p0_2p5_in"),
        (4622, "PTHvRapidity_45p0_120p0_1p0_2p5_in"),
        (4623, "PTHvRapidity_120p0_10000p0_1p0_2p5_in"),

        (4631, "PTHvRapidity_0p0_10000p0_0p0_2p5_out")
    ],
}

#BMW == Best Medium Worst
BMW = ['cat0', 'cat1', 'cat2']

combineVariableDict = {
    "2022": {
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2022", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2022", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022", BMW=BMW),
        "NJ_pt30_absEta2p5": CreateVariableParameters(gen_variable="NJ_pt30_absEta2p5", reco_variable="NJ_pt30_absEta2p5", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022", BMW=BMW),
        "PTJ0_pt30_absEta2p5": CreateVariableParameters(gen_variable="PTJ0_pt30_absEta2p5", reco_variable="PTJ0_pt30_absEta2p5", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022", BMW=BMW),
        #"PTHvsDPhiJ0J1": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022", BMW=BMW)
    },
    "2023":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2023", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2023", BMW=BMW),
        "NJ_pt30_absEta2p5": CreateVariableParameters(gen_variable="NJ_pt30_absEta2p5", reco_variable="NJ_pt30_absEta2p5", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2023", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2023", BMW=BMW),
        "PTJ0_pt30_absEta2p5": CreateVariableParameters(gen_variable="PTJ0_pt30_absEta2p5", reco_variable="PTJ0_pt30_absEta2p5", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2023", BMW=BMW)
    },
    "2223":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2223", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2223", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2223", BMW=BMW),
        "NJ_pt30_absEta2p5": CreateVariableParameters(gen_variable="NJ_pt30_absEta2p5", reco_variable="NJ_pt30_absEta2p5", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2223", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2223", BMW=BMW),
        "PTJ0_pt30_absEta2p5": CreateVariableParameters(gen_variable="PTJ0_pt30_absEta2p5", reco_variable="PTJ0_pt30_absEta2p5", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2223", BMW=BMW)
    },
    "2024":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2024", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2024", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2024", BMW=BMW),
        "NJ_pt30_absEta2p5": CreateVariableParameters(gen_variable="NJ_pt30_absEta2p5", reco_variable="NJ_pt30_absEta2p5", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2024", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2024", BMW=BMW),
        "PTJ0_pt30_absEta2p5": CreateVariableParameters(gen_variable="PTJ0_pt30_absEta2p5", reco_variable="PTJ0_pt30_absEta2p5", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2024", BMW=BMW)
    },
    "2022_2023":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2022_2023", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2022_2023", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022_2023", BMW=BMW),
        "NJ_pt30_absEta2p5": CreateVariableParameters(gen_variable="NJ_pt30_absEta2p5", reco_variable="NJ_pt30_absEta2p5", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022_2023", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022_2023", BMW=BMW),
        "PTJ0_pt30_absEta2p5": CreateVariableParameters(gen_variable="PTJ0_pt30_absEta2p5", reco_variable="PTJ0_pt30_absEta2p5", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022_2023", BMW=BMW)
    },
    "2022_2023_2024":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2022_2023_2024", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2022_2023_2024", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022_2023_2024", BMW=BMW),
        "NJ_pt30_absEta2p5": CreateVariableParameters(gen_variable="NJ_pt30_absEta2p5", reco_variable="NJ_pt30_absEta2p5", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2022_2023_2024", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022_2023_2024", BMW=BMW),
        "PTJ0_pt30_absEta2p5": CreateVariableParameters(gen_variable="PTJ0_pt30_absEta2p5", reco_variable="PTJ0_pt30_absEta2p5", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022_2023_2024", BMW=BMW)
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
