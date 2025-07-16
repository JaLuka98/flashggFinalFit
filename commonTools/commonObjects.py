import os

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

# Luminosity map in fb^-1: for using UL 2018
lumiMap = {
    '2016':36.33, 
    '2017':41.48, 
    '2018':59.83, 
    'combined':137.65, 
    'merged':137.65,
    '2022preEE':8.00,
    '2022postEE':26.70,
    '2022': 34.7,
    '2023preBPix': 17.8,
    '2023postBPix': 9.5,
    '2023': 27.3
}

def CreateVariableParameters(gen_variable, reco_variable, bins, year, BMW, procs=None, eft_variable=None, individual=False):
    paramStr = [f"r_{gen_variable}_{bin}=1" for bin in bins]
    paramStrNoOne = [f"r_{gen_variable}_{bin}" for bin in bins]
    catsStr = [f"RECO_{reco_variable}_{bin}" for bin in bins]
    catsStrWithBMW = [f"RECO_{reco_variable}_{bin}_{bmw}" for bin in bins for bmw in BMW]
    pdfIndeces = [f"pdfindex_RECO_{reco_variable}_{bin}_{bmw}_{year}_{sqrts__}" for bin in bins for bmw in BMW]

    VariableDict = {
        "paramStr": paramStr,
        "paramStrNoOne": paramStrNoOne,
        "catsStr": catsStr,
        "catsStrWithBMW": catsStrWithBMW,
        "pdfIndeces": pdfIndeces,
    }

    if (procs is not None) and (eft_variable is not None):
        # eftParamStr = [f"{proc}_scaling_{eft_variable}_{bin}=0" for proc in procs for bin in bins]
        # eftParamStrNoZero = [f"{proc}_scaling_{eft_variable}_{bin}" for proc in procs for bin in bins]
        
        if individual:
            # Individual bins
            eftParamStr = [f"{eft_variable}_{bin}=0" for bin in bins]
            eftParamStrNoZero = [f"{eft_variable}_{bin}" for bin in bins]
        else:
            # Inclusive fit
            eftParamStr = [f"{eft_variable}=0"]
            eftParamStrNoZero = [f"{eft_variable}"]
        VariableDict["eftParamStr"] = eftParamStr
        VariableDict["eftParamStrNoZero"] = eftParamStrNoZero
    
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
years_to_process = ['2016','2017','2018','2022preEE','2022postEE','2022preBPix','2022postBPix']
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
]

short_production_modes = ["ggh", "vbf", "vh", "tth"]

eft_variables = ["chg", "chb", "chw", "chwb", "chbox", "chd", "chl3", "cll1", "ctbre", "cthre", "ctwre"]

# Define an array of eras
# JLS 22th of Jan 2025: This syntax looks pretty criminal and should be improved at some point
TwentyTwentyTwoEras = ["preEE", "postEE"]
TwentyTwentyThreeEras = ["preBPix", "postBPix"]


allErasMap = {
    '2022': TwentyTwentyTwoEras,
    '2023': TwentyTwentyThreeEras
}

conversionTable_ = {
    "GluGluHtoGG": "ggh",
    "GluGluHto2G": "ggh",
    "ttHtoGG": "tth",
    "ttHto2G": "tth",
    "VBFHtoGG": "vbf",
    "VBFHto2G": "vbf",
    "VHtoGG": "vh",
    "VHto2G": "vh",
    }

# List of all jet-related variables. Variables listed here will get the CMS_scale_j and CMS_res_j uncertainty in the datacard step.
jetVariables = [
    "Njets2p5",
    "ptJ0",
    "YJ0",
    "AbsPhiHJ0",
    "AbsYHJ0",
    "PTHvsDPhiJ0J1"
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
    "Njets2p5": [
        (30, "NJ_0p0_1p0_in"),
        (31, "NJ_1p0_2p0_in"),
        (32, "NJ_2p0_3p0_in"),
        (33, "NJ_3p0_100p0_in"),
        (34, "NJ_0p0_100p0_out")
    ],
    "ptJ0": [
        (40, "PTJ0_0p0_30p0_in"),
        (41, "PTJ0_30p0_75p0_in"),
        (42, "PTJ0_75p0_120p0_in"),
        (43, "PTJ0_120p0_200p0_in"),
        (44, "PTJ0_200p0_10000p0_in"),
        (45, "PTJ0_0p0_10000p0_out")
    ],
    "YJ0": [
        (50, "YJ0_0p0_0p5_in"),
        (51, "YJ0_0p5_1p2_in"),
        (52, "YJ0_1p2_2p0_in"),
        (53, "YJ0_2p0_2p5_in"),
        (54, "YJ0_NJ0_in"),
        (55, "YJ0_0p0_2p5_out")
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
    "PTHvsDPhiJ0J1": [
        (4501, "PTHvsDPhiJ0J1_0p0_15p0_mPi_m23Pi_in"),
        (4502, "PTHvsDPhiJ0J1_0p0_15p0_m23Pi_m13Pi_in"),
        (4503, "PTHvsDPhiJ0J1_0p0_15p0_m13Pi_0p0_in"),
        (4504, "PTHvsDPhiJ0J1_0p0_15p0_0p0_13Pi_in"),
        (4505, "PTHvsDPhiJ0J1_0p0_15p0_13Pi_23Pi_in"),
        (4506, "PTHvsDPhiJ0J1_0p0_15p0_23Pi_Pi_in"),

        (4506, "PTHvsDPhiJ0J1_15p0_30p0_mPi_m23Pi_in"),
        (4507, "PTHvsDPhiJ0J1_15p0_30p0_m23Pi_m13Pi_in"),
        (4508, "PTHvsDPhiJ0J1_15p0_30p0_m13Pi_0p0_in"),
        (4509, "PTHvsDPhiJ0J1_15p0_30p0_0p0_13Pi_in"),
        (4510, "PTHvsDPhiJ0J1_15p0_30p0_13Pi_23Pi_in"),
        (4511, "PTHvsDPhiJ0J1_15p0_30p0_23Pi_Pi_in"),

        (4512, "PTHvsDPhiJ0J1_30p0_45p0_mPi_m23Pi_in"),
        (4513, "PTHvsDPhiJ0J1_30p0_45p0_m23Pi_m13Pi_in"),
        (4514, "PTHvsDPhiJ0J1_30p0_45p0_m13Pi_0p0_in"),
        (4515, "PTHvsDPhiJ0J1_30p0_45p0_0p0_13Pi_in"),
        (4516, "PTHvsDPhiJ0J1_30p0_45p0_13Pi_23Pi_in"),
        (4517, "PTHvsDPhiJ0J1_30p0_45p0_23Pi_Pi_in"),

        (4518, "PTHvsDPhiJ0J1_45p0_80p0_mPi_m23Pi_in"),
        (4519, "PTHvsDPhiJ0J1_45p0_80p0_m23Pi_m13Pi_in"),
        (4520, "PTHvsDPhiJ0J1_45p0_80p0_m13Pi_0p0_in"),
        (4521, "PTHvsDPhiJ0J1_45p0_80p0_0p0_13Pi_in"),
        (4522, "PTHvsDPhiJ0J1_45p0_80p0_13Pi_23Pi_in"),
        (4523, "PTHvsDPhiJ0J1_45p0_80p0_23Pi_Pi_in"),

        (4524, "PTHvsDPhiJ0J1_80p0_120p0_mPi_m23Pi_in"),
        (4525, "PTHvsDPhiJ0J1_80p0_120p0_m23Pi_m13Pi_in"),
        (4526, "PTHvsDPhiJ0J1_80p0_120p0_m13Pi_0p0_in"),
        (4527, "PTHvsDPhiJ0J1_80p0_120p0_0p0_13Pi_in"),
        (4528, "PTHvsDPhiJ0J1_80p0_120p0_13Pi_23Pi_in"),
        (4529, "PTHvsDPhiJ0J1_80p0_120p0_23Pi_Pi_in"),

        (4530, "PTHvsDPhiJ0J1_120p0_200p0_mPi_m23Pi_in"),
        (4531, "PTHvsDPhiJ0J1_120p0_200p0_m23Pi_m13Pi_in"),
        (4532, "PTHvsDPhiJ0J1_120p0_200p0_m13Pi_0p0_in"),
        (4533, "PTHvsDPhiJ0J1_120p0_200p0_0p0_13Pi_in"),
        (4534, "PTHvsDPhiJ0J1_120p0_200p0_13Pi_23Pi_in"),
        (4535, "PTHvsDPhiJ0J1_120p0_200p0_23Pi_Pi_in"),

        (4536, "PTHvsDPhiJ0J1_200p0_350p0_mPi_m23Pi_in"),
        (4537, "PTHvsDPhiJ0J1_200p0_350p0_m23Pi_m13Pi_in"),
        (4538, "PTHvsDPhiJ0J1_200p0_350p0_m13Pi_0p0_in"),
        (4539, "PTHvsDPhiJ0J1_200p0_350p0_0p0_13Pi_in"),
        (4540, "PTHvsDPhiJ0J1_200p0_350p0_13Pi_23Pi_in"),
        (4541, "PTHvsDPhiJ0J1_200p0_350p0_23Pi_Pi_in"),

        (4542, "PTHvsDPhiJ0J1_350p0_10000p0_mPi_m23Pi_in"),
        (4543, "PTHvsDPhiJ0J1_350p0_10000p0_m23Pi_m13Pi_in"),
        (4544, "PTHvsDPhiJ0J1_350p0_10000p0_m13Pi_0p0_in"),
        (4545, "PTHvsDPhiJ0J1_350p0_10000p0_0p0_13Pi_in"),
        (4546, "PTHvsDPhiJ0J1_350p0_10000p0_13Pi_23Pi_in"),
        (4547, "PTHvsDPhiJ0J1_350p0_10000p0_23Pi_Pi_in"),

        (4548, "PTHvsDPhiJ0J1_0p0_10000p0_m4p0_4p0_out")
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
        "PTHvsDPhiJ0J1": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2022", BMW=BMW)
    },
    "2023":{
        "PTH": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW),
        "rapidity": CreateVariableParameters(gen_variable="YH", reco_variable="rapidity", bins=["0p0_0p15", "0p15_0p3", "0p3_0p6", "0p6_0p9", "0p9_2p5"], year="2023", BMW=BMW),
        "NJ": CreateVariableParameters(gen_variable="NJ", reco_variable="NJ", bins=["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_100p0"], year="2023", BMW=BMW),
        "PTJ0": CreateVariableParameters(gen_variable="PTJ0", reco_variable="PTJ0", bins=["0p0_30p0", "30p0_75p0", "75p0_120p0", "120p0_200p0", "200p0_10000p0"], year="2023", BMW=BMW),
        "chg": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chg"),
        "chw": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chw"),
        "chb": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chb"),
        "chwb": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chwb"),
        "chbox": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chbox"),
        "chd": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chd"),
        "chl3": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chl3"),
        "cll1": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="cll1"),
        "ctbre": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="ctbre"),
        "cthre": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="cthre"),
        "ctwre": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="ctwre"),
        "chg_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chg", individual=True),
        "chw_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chw", individual=True),
        "chb_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chb", individual=True),
        "chwb_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chwb", individual=True),
        "chbox_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chbox", individual=True),
        "chd_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chd", individual=True),
        "chl3_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="chl3", individual=True),
        "cll1_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="cll1", individual=True),
        "ctbre_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="ctbre", individual=True),
        "cthre_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="cthre", individual=True),
        "ctwre_individual": CreateVariableParameters(gen_variable="PTH", reco_variable="PTH", bins=["0p0_15p0","15p0_30p0","30p0_45p0","45p0_80p0","80p0_120p0","120p0_200p0","200p0_350p0","350p0_10000p0"], year="2023", BMW=BMW, procs=short_production_modes, eft_variable="ctwre", individual=True),
    }
}