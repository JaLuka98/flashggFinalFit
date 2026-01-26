# Python script to hold replacement model mapping for different analyses
from collections import OrderedDict as od

try:
    from commonTools.commonObjects import PTH_BINS
except ImportError:
    PTH_BINS = [
        "0p0_5p0",
        "5p0_10p0",
        "10p0_15p0",
        "15p0_20p0",
        "20p0_25p0",
        "25p0_30p0",
        "30p0_35p0",
        "35p0_45p0",
        "45p0_60p0",
        "60p0_80p0",
        "80p0_100p0",
        "100p0_120p0",
        "120p0_140p0",
        "140p0_170p0",
        "170p0_200p0",
        "200p0_250p0",
        "250p0_350p0",
        "350p0_450p0",
        "450p0_10000p0",
    ]

try:
    from commonTools.commonObjects import RAPIDITY_BINS as _RAPIDITY_BINS
except ImportError:
    _RAPIDITY_BINS = [
        "0p0_0p15",
        "0p15_0p3",
        "0p3_0p45",
        "0p45_0p6",
        "0p6_0p75",
        "0p75_0p9",
        "0p9_1p2",
        "1p2_1p6",
        "1p6_2p0",
        "2p0_2p5",
    ]

# Add analyses to globalReplacementMap. See "STXS" as an example
globalReplacementMap = od()

# Example analysis which with cats Untagged_Tag0,VBF_Tag0
globalReplacementMap['example'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['example']['procWV'] = "GG2H"
globalReplacementMap['example']['catWV'] = "Untagged_Tag0"
# For RIGHT VERTEX SCENARIO:
#  * default you should add is diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
globalReplacementMap['example']['procRVMap'] = od()
globalReplacementMap["example"]["procRVMap"]["Untagged_Tag0"] = "GG2H"
globalReplacementMap["example"]["procRVMap"]["VBF_Tag0"] = "VBF"
# Replacement category for RV fit
globalReplacementMap["example"]["catRVMap"] = od()
globalReplacementMap["example"]["catRVMap"]["Untagged_Tag0"] = "Untagged_Tag0"
globalReplacementMap["example"]["catRVMap"]["VBF_Tag0"] = "VBF_Tag0"

# Tutorial analysis
globalReplacementMap['tutorial'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['tutorial']['procWV'] = "GG2H"
globalReplacementMap['tutorial']['catWV'] = "EBEB_highR9highR9"
# For RIGHT VERTEX SCENARIO
#  * default mapping is to use diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
globalReplacementMap['tutorial']['procRVMap'] = od()
globalReplacementMap["tutorial"]["procRVMap"]["EBEB_highR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEB_highR9lowR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEB_lowR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEE_highR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEE_highR9lowR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EBEE_lowR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEB_highR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEB_highR9lowR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEB_lowR9highR9"] = "GG2H"
globalReplacementMap["tutorial"]["procRVMap"]["EEEE_incl"] = "GG2H"
globalReplacementMap['tutorial']['catRVMap'] = od()
globalReplacementMap["tutorial"]["catRVMap"]["EBEB_highR9highR9"] = "EBEB_highR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEB_highR9lowR9"] = "EBEB_highR9lowR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEB_lowR9highR9"] = "EBEB_lowR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEE_highR9highR9"] = "EBEE_highR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEE_highR9lowR9"] = "EBEE_highR9lowR9"
globalReplacementMap["tutorial"]["catRVMap"]["EBEE_lowR9highR9"] = "EBEE_lowR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEB_highR9highR9"] = "EEEB_highR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEB_highR9lowR9"] = "EEEB_highR9lowR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEB_lowR9highR9"] = "EEEB_lowR9highR9"
globalReplacementMap["tutorial"]["catRVMap"]["EEEE_incl"] = "EEEE_incl"


# STXS analysis
globalReplacementMap['STXS'] = od()
# For WRONG VERTEX SCENARIO:
#  * single proc x cat for wrong vertex since for dZ > 1cm shape independent of proc x cat
#  * use proc x cat with highest number of WV events
globalReplacementMap['STXS']['procWV'] = "GG2H_0J_PTH_GT10"
globalReplacementMap['STXS']['catWV'] = "RECO_0J_PTH_GT10_Tag1"
# For RIGHT VERTEX SCENARIO:
#  * default mapping is to use diagonal process from given category 
#  * if few events in diagonal process then may need to change the category aswell (see catRVMap)
#  * map must contain entry for all cats being processed (for replacement proc and cat)
globalReplacementMap['STXS']['procRVMap'] = od()
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_0_10_Tag0"] = "GG2H_0J_PTH_0_10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_0_10_Tag1"] = "GG2H_0J_PTH_0_10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_0_10_Tag2"] = "GG2H_0J_PTH_0_10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_GT10_Tag0"] = "GG2H_0J_PTH_GT10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_GT10_Tag1"] = "GG2H_0J_PTH_GT10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_0J_PTH_GT10_Tag2"] = "GG2H_0J_PTH_GT10"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_0_60_Tag0"] = "GG2H_1J_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_0_60_Tag1"] = "GG2H_1J_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_0_60_Tag2"] = "GG2H_1J_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_120_200_Tag0"] = "GG2H_1J_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_120_200_Tag1"] = "GG2H_1J_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_120_200_Tag2"] = "GG2H_1J_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_60_120_Tag0"] = "GG2H_1J_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_60_120_Tag1"] = "GG2H_1J_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_1J_PTH_60_120_Tag2"] = "GG2H_1J_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_0_60_Tag0"] = "GG2H_GE2J_MJJ_0_350_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_0_60_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_0_60_Tag2"] = "GG2H_GE2J_MJJ_0_350_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_120_200_Tag0"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_120_200_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_120_200_Tag2"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_60_120_Tag0"] = "GG2H_GE2J_MJJ_0_350_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_60_120_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_GE2J_PTH_60_120_Tag2"] = "GG2H_GE2J_MJJ_0_350_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_200_300_Tag0"] = "GG2H_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_200_300_Tag1"] = "GG2H_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_300_450_Tag0"] = "GG2H_PTH_300_450"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_300_450_Tag1"] = "GG2H_PTH_300_450"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_450_650_Tag0"] = "GG2H_PTH_450_650"
globalReplacementMap["STXS"]["procRVMap"]["RECO_PTH_GT650_Tag0"] = "GG2H_PTH_GT650"
globalReplacementMap["STXS"]["procRVMap"]["RECO_THQ_LEP"] = "THQ"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag0"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag1"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag2"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag3"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag0"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag1"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag2"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag3"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag0"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag1"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag2"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag0"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag1"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag2"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag3"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag0"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag1"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag2"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag0"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag1"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag2"] = "TTH_PTH_0_60"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag0"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag1"] = "TTH_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag0"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag1"] = "TTH_PTH_200_300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag0"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag1"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag2"] = "TTH_PTH_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_TTH_LEP_PTH_GT300_Tag0"] = "TTH_PTH_GT300"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFLIKEGGH_Tag0"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFLIKEGGH_Tag1"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_BSM_Tag0"] = "VBF_GE2J_MJJ_GT350_PTH_GT200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_BSM_Tag1"] = "VBF_GE2J_MJJ_GT350_PTH_GT200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0"] = "VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1"] = "VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag0"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag1"] = "VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag0"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag1"] = "GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_VHHAD_Tag0"] = "WH2HQQ_GE2J_MJJ_60_120"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VBFTOPO_VHHAD_Tag1"] = "GG2H_GE2J_MJJ_0_350_PTH_120_200"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VH_MET_Tag0"] = "QQ2HLL_PTV_150_250_0J"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VH_MET_Tag1"] = "QQ2HLL_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_VH_MET_Tag2"] = "QQ2HLL_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_0_75_Tag0"] = "QQ2HLNU_PTV_0_75"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_0_75_Tag1"] = "QQ2HLNU_PTV_0_75"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_75_150_Tag0"] = "QQ2HLNU_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_75_150_Tag1"] = "QQ2HLNU_PTV_75_150"
globalReplacementMap["STXS"]["procRVMap"]["RECO_WH_LEP_PTV_GT150_Tag0"] = "QQ2HLNU_PTV_150_250_0J"
globalReplacementMap["STXS"]["procRVMap"]["RECO_ZH_LEP_Tag0"] = "QQ2HLL_PTV_0_75"
globalReplacementMap["STXS"]["procRVMap"]["RECO_ZH_LEP_Tag1"] = "QQ2HLL_PTV_0_75"
# Replacement category for RV fit
globalReplacementMap["STXS"]["catRVMap"] = od()
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_0_10_Tag0"] = "RECO_0J_PTH_0_10_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_0_10_Tag1"] = "RECO_0J_PTH_0_10_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_0_10_Tag2"] = "RECO_0J_PTH_0_10_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_GT10_Tag0"] = "RECO_0J_PTH_GT10_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_GT10_Tag1"] = "RECO_0J_PTH_GT10_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_0J_PTH_GT10_Tag2"] = "RECO_0J_PTH_GT10_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_0_60_Tag0"] = "RECO_1J_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_0_60_Tag1"] = "RECO_1J_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_0_60_Tag2"] = "RECO_1J_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_120_200_Tag0"] = "RECO_1J_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_120_200_Tag1"] = "RECO_1J_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_120_200_Tag2"] = "RECO_1J_PTH_120_200_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_60_120_Tag0"] = "RECO_1J_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_60_120_Tag1"] = "RECO_1J_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_1J_PTH_60_120_Tag2"] = "RECO_1J_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_0_60_Tag0"] = "RECO_GE2J_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_0_60_Tag1"] = "RECO_GE2J_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_0_60_Tag2"] = "RECO_GE2J_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_120_200_Tag0"] = "RECO_GE2J_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_120_200_Tag1"] = "RECO_GE2J_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_120_200_Tag2"] = "RECO_GE2J_PTH_120_200_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_60_120_Tag0"] = "RECO_GE2J_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_60_120_Tag1"] = "RECO_GE2J_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_GE2J_PTH_60_120_Tag2"] = "RECO_GE2J_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_200_300_Tag0"] = "RECO_PTH_200_300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_200_300_Tag1"] = "RECO_PTH_200_300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_300_450_Tag0"] = "RECO_PTH_300_450_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_300_450_Tag1"] = "RECO_PTH_300_450_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_450_650_Tag0"] = "RECO_PTH_450_650_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_PTH_GT650_Tag0"] = "RECO_PTH_GT650_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_THQ_LEP"] = "RECO_THQ_LEP"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag0"] = "RECO_TTH_HAD_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag1"] = "RECO_TTH_HAD_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag2"] = "RECO_TTH_HAD_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_0_60_Tag3"] = "RECO_TTH_HAD_PTH_0_60_Tag3"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag0"] = "RECO_TTH_HAD_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag1"] = "RECO_TTH_HAD_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag2"] = "RECO_TTH_HAD_PTH_120_200_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_120_200_Tag3"] = "RECO_TTH_HAD_PTH_120_200_Tag3"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag0"] = "RECO_TTH_HAD_PTH_200_300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag1"] = "RECO_TTH_HAD_PTH_200_300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_200_300_Tag2"] = "RECO_TTH_HAD_PTH_200_300_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag0"] = "RECO_TTH_HAD_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag1"] = "RECO_TTH_HAD_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag2"] = "RECO_TTH_HAD_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_60_120_Tag3"] = "RECO_TTH_HAD_PTH_60_120_Tag3"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag0"] = "RECO_TTH_HAD_PTH_GT300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag1"] = "RECO_TTH_HAD_PTH_GT300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_HAD_PTH_GT300_Tag2"] = "RECO_TTH_HAD_PTH_GT300_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag0"] = "RECO_TTH_LEP_PTH_0_60_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag1"] = "RECO_TTH_LEP_PTH_0_60_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_0_60_Tag2"] = "RECO_TTH_LEP_PTH_0_60_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag0"] = "RECO_TTH_LEP_PTH_120_200_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_120_200_Tag1"] = "RECO_TTH_LEP_PTH_120_200_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag0"] = "RECO_TTH_LEP_PTH_200_300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_200_300_Tag1"] = "RECO_TTH_LEP_PTH_200_300_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag0"] = "RECO_TTH_LEP_PTH_60_120_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag1"] = "RECO_TTH_LEP_PTH_60_120_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_60_120_Tag2"] = "RECO_TTH_LEP_PTH_60_120_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_TTH_LEP_PTH_GT300_Tag0"] = "RECO_TTH_LEP_PTH_GT300_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFLIKEGGH_Tag0"] = "RECO_VBFLIKEGGH_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFLIKEGGH_Tag1"] = "RECO_VBFLIKEGGH_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_BSM_Tag0"] = "RECO_VBFTOPO_BSM_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_BSM_Tag1"] = "RECO_VBFTOPO_BSM_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0"] = "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1"] = "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0"] = "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1"] = "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag0"] = "RECO_VBFTOPO_JET3_HIGHMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_HIGHMJJ_Tag1"] = "RECO_VBFTOPO_JET3_HIGHMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag0"] = "RECO_VBFTOPO_JET3_LOWMJJ_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_JET3_LOWMJJ_Tag1"] = "RECO_VBFTOPO_JET3_LOWMJJ_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_VHHAD_Tag0"] = "RECO_VBFTOPO_VHHAD_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VBFTOPO_VHHAD_Tag1"] = "RECO_VBFTOPO_VHHAD_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VH_MET_Tag0"] = "RECO_VH_MET_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VH_MET_Tag1"] = "RECO_VH_MET_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_VH_MET_Tag2"] = "RECO_VH_MET_Tag2"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_0_75_Tag0"] = "RECO_WH_LEP_PTV_0_75_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_0_75_Tag1"] = "RECO_WH_LEP_PTV_0_75_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_75_150_Tag0"] = "RECO_WH_LEP_PTV_75_150_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_75_150_Tag1"] = "RECO_WH_LEP_PTV_75_150_Tag1"
globalReplacementMap["STXS"]["catRVMap"]["RECO_WH_LEP_PTV_GT150_Tag0"] = "RECO_WH_LEP_PTV_GT150_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_ZH_LEP_Tag0"] = "RECO_ZH_LEP_Tag0"
globalReplacementMap["STXS"]["catRVMap"]["RECO_ZH_LEP_Tag1"] = "RECO_ZH_LEP_Tag1"

###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################
# Run 3 Fiducial XS analysis: use 13.6 TeV cross sections and branching fraction

globalReplacementMap["Run3FidXSAnalysis"] = od()
# Wrong vertex stuff
globalReplacementMap["Run3FidXSAnalysis"]['procWV'] = "GG2H"
globalReplacementMap["Run3FidXSAnalysis"]['catWV'] = "cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysis"]['procRVMap'] = od()
globalReplacementMap["Run3FidXSAnalysis"]["procRVMap"]["cat0"] = "GG2H"
globalReplacementMap["Run3FidXSAnalysis"]["procRVMap"]["cat0"] = "VBF"
globalReplacementMap["Run3FidXSAnalysis"]["procRVMap"]["cat0"] = "VH"
globalReplacementMap["Run3FidXSAnalysis"]["procRVMap"]["cat0"] = "TTH"
# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysis"]["catRVMap"] = od()
globalReplacementMap["Run3FidXSAnalysis"]["catRVMap"]["GG2H"] = "GG2H"
globalReplacementMap["Run3FidXSAnalysis"]["catRVMap"]["VBF"]  = "VBF"
globalReplacementMap["Run3FidXSAnalysis"]["catRVMap"]["VH"]   = "VH"
globalReplacementMap["Run3FidXSAnalysis"]["catRVMap"]["TTH"]  = "TTH"


# WITH in/out splitting
globalReplacementMap["Run3FidXSAnalysisInclusive"] = od()
# Wrong vertex stuff
globalReplacementMap["Run3FidXSAnalysisInclusive"]['procWV'] = "ggh_in"
globalReplacementMap["Run3FidXSAnalysisInclusive"]['catWV'] = "cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisInclusive"]['procRVMap'] = od()
# With nico convention (ggh instead of GG2H)
globalReplacementMap["Run3FidXSAnalysisInclusive"]["procRVMap"]["cat0"] = "ggh_in"
globalReplacementMap["Run3FidXSAnalysisInclusive"]["procRVMap"]["cat1"] = "ggh_in"
globalReplacementMap["Run3FidXSAnalysisInclusive"]["procRVMap"]["cat2"] = "ggh_in"
# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisInclusive"]["catRVMap"] = od()
globalReplacementMap["Run3FidXSAnalysisInclusive"]["catRVMap"]["cat0"] = "cat0"
globalReplacementMap["Run3FidXSAnalysisInclusive"]["catRVMap"]["cat1"]  = "cat1"
globalReplacementMap["Run3FidXSAnalysisInclusive"]["catRVMap"]["cat2"]   = "cat2"


# Differential PT
globalReplacementMap["Run3FidXSAnalysisPTH"] = od()
_PTH_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_PTH_FIRST_BIN = PTH_BINS[0]
_PTH_SECOND_BIN = PTH_BINS[1] if len(PTH_BINS) > 1 else PTH_BINS[0]
_PTH_WV_BIN = "45p0_60p0"
# Wrong vertex reference
globalReplacementMap["Run3FidXSAnalysisPTH"]['procWV'] = f"ggh_PTH_{_PTH_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisPTH"]['catWV'] = f"RECO_PTH_{_PTH_WV_BIN}_cat2"

# Replacement processes for RV
globalReplacementMap["Run3FidXSAnalysisPTH"]['procRVMap'] = od()
for _bin in PTH_BINS:
    for _cat in _PTH_RECO_CATS:
        _target_bin = _PTH_SECOND_BIN if (_bin == _PTH_FIRST_BIN and _cat == 'cat0') else _bin
        reco_key = f"RECO_PTH_{_bin}_{_cat}"
        proc_value = f"ggh_PTH_{_target_bin}_in"
        globalReplacementMap["Run3FidXSAnalysisPTH"]["procRVMap"][reco_key] = proc_value

# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisPTH"]["catRVMap"] = od()
for _bin in PTH_BINS:
    for _cat in _PTH_RECO_CATS:
        _target_bin = _PTH_SECOND_BIN if (_bin == _PTH_FIRST_BIN and _cat == 'cat0') else _bin
        reco_key = f"RECO_PTH_{_bin}_{_cat}"
        target_value = f"RECO_PTH_{_target_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisPTH"]["catRVMap"][reco_key] = target_value



# Differential Y (Rapidity)
globalReplacementMap["Run3FidXSAnalysisYH"] = od()
_RAPIDITY_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_RAPIDITY_WV_BIN = "0p45_0p6"
globalReplacementMap["Run3FidXSAnalysisYH"]['procWV'] = f"ggh_YH_{_RAPIDITY_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisYH"]['catWV'] = f"RECO_rapidity_{_RAPIDITY_WV_BIN}_cat2"
globalReplacementMap["Run3FidXSAnalysisYH"]['procRVMap'] = od()
for _bin in _RAPIDITY_BINS:
    for _cat in _RAPIDITY_RECO_CATS:
        reco_key = f"RECO_rapidity_{_bin}_{_cat}"
        proc_value = f"ggh_YH_{_bin}_in"
        globalReplacementMap["Run3FidXSAnalysisYH"]["procRVMap"][reco_key] = proc_value

globalReplacementMap["Run3FidXSAnalysisYH"]["catRVMap"] = od()
for _bin in _RAPIDITY_BINS:
    for _cat in _RAPIDITY_RECO_CATS:
        reco_key = f"RECO_rapidity_{_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisYH"]["catRVMap"][reco_key] = reco_key

# Differential NJ (Number of Jets)
globalReplacementMap["Run3FidXSAnalysisNJ"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisNJ"]['procWV'] = "ggh_NJ_1p0_2p0_in"
globalReplacementMap["Run3FidXSAnalysisNJ"]['catWV'] = "RECO_NJ_2p0_3p0_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisNJ"]['procRVMap'] = od()
for _bin in ["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_4p0", "4p0_100p0"]:
    for _cat in ["cat0", "cat1", "cat2"]:
        reco_key = f"RECO_NJ_{_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisNJ"]["procRVMap"][reco_key] = f"ggh_NJ_{_bin}_in"


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisNJ"]["catRVMap"] = od()
globalReplacementMap["Run3FidXSAnalysisNJ"]["catRVMap"] = od()
for _bin in ["0p0_1p0", "1p0_2p0", "2p0_3p0", "3p0_4p0", "4p0_100p0"]:
    for _cat in ["cat0", "cat1", "cat2"]:
        reco_key = f"RECO_NJ_{_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisNJ"]["catRVMap"][reco_key] = reco_key

# Differential PTJ0 (PT of the leading jet)
globalReplacementMap["Run3FidXSAnalysisPTJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisPTJ0"]['procWV'] = "ggh_PTJ0_75p0_95p0_in"
globalReplacementMap["Run3FidXSAnalysisPTJ0"]['catWV'] = "RECO_PTJ0_75p0_95p0_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisPTJ0"]['procRVMap'] = od()
for bin_name in [
    "0p0_30p0",
    "30p0_40p0",
    "40p0_55p0",
    "55p0_75p0",
    "75p0_95p0",
    "95p0_120p0",
    "120p0_150p0",
    "150p0_200p0",
    "200p0_10000p0",
]:
    for cat in ['cat0', 'cat1', 'cat2']:
        reco_key = f"RECO_PTJ0_{bin_name}_{cat}"
        proc_val = f"ggh_PTJ0_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisPTJ0"]["procRVMap"][reco_key] = proc_val

# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisPTJ0"]["catRVMap"] = od()
for bin_name in [
    "0p0_30p0",
    "30p0_40p0",
    "40p0_55p0",
    "55p0_75p0",
    "75p0_95p0",
    "95p0_120p0",
    "120p0_150p0",
    "150p0_200p0",
    "200p0_10000p0",
]:
    for cat in ['cat0', 'cat1', 'cat2']:
        reco_key = f"RECO_PTJ0_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisPTJ0"]["catRVMap"][reco_key] = reco_key

# Differential YJ0 (Rapidity of the leading jet)
globalReplacementMap["Run3FidXSAnalysisYJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisYJ0"]['procWV'] = "ggh_YJ0_0p0_0p5_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]['catWV'] = "RECO_first_jet_eta_0p5_1p2_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisYJ0"]['procRVMap'] = od()
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_0p0_0p5_cat0"] = "ggh_YJ0_0p0_0p5_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_0p0_0p5_cat1"] = "ggh_YJ0_0p0_0p5_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_0p0_0p5_cat2"] = "ggh_YJ0_0p0_0p5_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_0p5_1p2_cat0"] = "ggh_YJ0_0p5_1p2_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_0p5_1p2_cat1"] = "ggh_YJ0_0p5_1p2_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_0p5_1p2_cat2"] = "ggh_YJ0_0p5_1p2_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_1p2_2p0_cat0"] = "ggh_YJ0_1p2_2p0_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_1p2_2p0_cat1"] = "ggh_YJ0_1p2_2p0_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_1p2_2p0_cat2"] = "ggh_YJ0_1p2_2p0_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_2p0_2p5_cat0"] = "ggh_YJ0_2p0_2p5_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_2p0_2p5_cat1"] = "ggh_YJ0_2p0_2p5_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_2p0_2p5_cat2"] = "ggh_YJ0_2p0_2p5_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_NJ0_cat0"] = "ggh_YJ0_NJ0_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_NJ0_cat1"] = "ggh_YJ0_NJ0_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"]["RECO_first_jet_eta_NJ0_cat2"] = "ggh_YJ0_NJ0_in"


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"] = od()
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_0p0_0p5_cat0"] = "RECO_first_jet_eta_0p0_0p5_cat0"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_0p0_0p5_cat1"] = "RECO_first_jet_eta_0p0_0p5_cat1"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_0p0_0p5_cat2"] = "RECO_first_jet_eta_0p0_0p5_cat2"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_0p5_1p2_cat0"] = "RECO_first_jet_eta_0p5_1p2_cat0"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_0p5_1p2_cat1"] = "RECO_first_jet_eta_0p5_1p2_cat1"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_0p5_1p2_cat2"] = "RECO_first_jet_eta_0p5_1p2_cat2"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_1p2_2p0_cat0"] = "RECO_first_jet_eta_1p2_2p0_cat0"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_1p2_2p0_cat1"] = "RECO_first_jet_eta_1p2_2p0_cat1"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_1p2_2p0_cat2"] = "RECO_first_jet_eta_1p2_2p0_cat2"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_2p0_2p5_cat0"] = "RECO_first_jet_eta_2p0_2p5_cat0"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_2p0_2p5_cat1"] = "RECO_first_jet_eta_2p0_2p5_cat1"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_2p0_2p5_cat2"] = "RECO_first_jet_eta_2p0_2p5_cat2"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_NJ0_cat0"] = "RECO_first_jet_eta_NJ0_cat0"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_NJ0_cat1"] = "RECO_first_jet_eta_NJ0_cat1"
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"]["RECO_first_jet_eta_NJ0_cat2"] = "RECO_first_jet_eta_NJ0_cat2"


# Differential AbsPhiHJ0 
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]['procWV'] = "ggh_AbsPhiHJ0_0p0_2p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]['catWV'] = "RECO_AbsPhiHJ0_0p0_2p6_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]['procRVMap'] = od()
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_0p0_2p6_cat0"] = "ggh_AbsPhiHJ0_0p0_2p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_0p0_2p6_cat1"] = "ggh_AbsPhiHJ0_0p0_2p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_0p0_2p6_cat2"] = "ggh_AbsPhiHJ0_0p0_2p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_2p6_2p9_cat0"] = "ggh_AbsPhiHJ0_2p6_2p9_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_2p6_2p9_cat1"] = "ggh_AbsPhiHJ0_2p6_2p9_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_2p6_2p9_cat2"] = "ggh_AbsPhiHJ0_2p6_2p9_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_2p9_3p03_cat0"] = "ggh_AbsPhiHJ0_2p9_3p03_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_2p9_3p03_cat1"] = "ggh_AbsPhiHJ0_2p9_3p03_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_2p9_3p03_cat2"] = "ggh_AbsPhiHJ0_2p9_3p03_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_3p03_3p1415926_cat0"] = "ggh_AbsPhiHJ0_3p03_3p1415926_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_3p03_3p1415926_cat1"] = "ggh_AbsPhiHJ0_3p03_3p1415926_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_3p03_3p1415926_cat2"] = "ggh_AbsPhiHJ0_3p03_3p1415926_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_NJ_cat0"] = "ggh_AbsPhiHJ0_NJ_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_NJ_cat1"] = "ggh_AbsPhiHJ0_NJ_in"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["procRVMap"]["RECO_AbsPhiHJ0_NJ_cat2"] = "ggh_AbsPhiHJ0_NJ_in"

# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"] = od()
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_0p0_2p6_cat0"] = "RECO_AbsPhiHJ0_0p0_2p6_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_0p0_2p6_cat1"] = "RECO_AbsPhiHJ0_0p0_2p6_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_0p0_2p6_cat2"] = "RECO_AbsPhiHJ0_0p0_2p6_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_2p6_2p9_cat0"] = "RECO_AbsPhiHJ0_2p6_2p9_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_2p6_2p9_cat1"] = "RECO_AbsPhiHJ0_2p6_2p9_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_2p6_2p9_cat2"] = "RECO_AbsPhiHJ0_2p6_2p9_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_2p9_3p03_cat0"] = "RECO_AbsPhiHJ0_2p9_3p03_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_2p9_3p03_cat1"] = "RECO_AbsPhiHJ0_2p9_3p03_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_2p9_3p03_cat2"] = "RECO_AbsPhiHJ0_2p9_3p03_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_3p03_3p1415926_cat0"] = "RECO_AbsPhiHJ0_3p03_3p1415926_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_3p03_3p1415926_cat1"] = "RECO_AbsPhiHJ0_3p03_3p1415926_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_3p03_3p1415926_cat2"] = "RECO_AbsPhiHJ0_3p03_3p1415926_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_NJ_cat0"] = "RECO_AbsPhiHJ0_NJ_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_NJ_cat1"] = "RECO_AbsPhiHJ0_NJ_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsPhiJ0"]["catRVMap"]["RECO_AbsPhiHJ0_NJ_cat2"] = "RECO_AbsPhiHJ0_NJ_cat2"

# Differential AbsYHJ0 
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]['procWV'] = "ggh_AbsYHJ0_0p0_0p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]['catWV'] = "RECO_AbsYHJ0_NJ0_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]['procRVMap'] = od()
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_0p0_0p6_cat0"] = "ggh_AbsYHJ0_0p0_0p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_0p0_0p6_cat1"] = "ggh_AbsYHJ0_0p0_0p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_0p0_0p6_cat2"] = "ggh_AbsYHJ0_0p0_0p6_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_0p6_1p2_cat0"] = "ggh_AbsYHJ0_0p6_1p2_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_0p6_1p2_cat1"] = "ggh_AbsYHJ0_0p6_1p2_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_0p6_1p2_cat2"] = "ggh_AbsYHJ0_0p6_1p2_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_1p2_1p9_cat0"] = "ggh_AbsYHJ0_1p2_1p9_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_1p2_1p9_cat1"] = "ggh_AbsYHJ0_1p2_1p9_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_1p2_1p9_cat2"] = "ggh_AbsYHJ0_1p2_1p9_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_1p9_100p0_cat0"] = "ggh_AbsYHJ0_1p9_100p0_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_1p9_100p0_cat1"] = "ggh_AbsYHJ0_1p9_100p0_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_1p9_100p0_cat2"] = "ggh_AbsYHJ0_1p9_100p0_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_NJ0_cat0"] = "ggh_AbsYHJ0_NJ0_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_NJ0_cat1"] = "ggh_AbsYHJ0_NJ0_in"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["procRVMap"]["RECO_AbsYHJ0_NJ0_cat2"] = "ggh_AbsYHJ0_NJ0_in"


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"] = od()
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_0p0_0p6_cat0"] = "RECO_AbsYHJ0_0p0_0p6_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_0p0_0p6_cat1"] = "RECO_AbsYHJ0_0p0_0p6_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_0p0_0p6_cat2"] = "RECO_AbsYHJ0_0p0_0p6_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_0p6_1p2_cat0"] = "RECO_AbsYHJ0_0p6_1p2_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_0p6_1p2_cat1"] = "RECO_AbsYHJ0_0p6_1p2_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_0p6_1p2_cat2"] = "RECO_AbsYHJ0_0p6_1p2_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_1p2_1p9_cat0"] = "RECO_AbsYHJ0_1p2_1p9_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_1p2_1p9_cat1"] = "RECO_AbsYHJ0_1p2_1p9_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_1p2_1p9_cat2"] = "RECO_AbsYHJ0_1p2_1p9_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_1p9_100p0_cat0"] = "RECO_AbsYHJ0_1p9_100p0_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_1p9_100p0_cat1"] = "RECO_AbsYHJ0_1p9_100p0_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_1p9_100p0_cat2"] = "RECO_AbsYHJ0_1p9_100p0_cat2"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_NJ0_cat0"] = "RECO_AbsYHJ0_NJ0_cat0"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_NJ0_cat1"] = "RECO_AbsYHJ0_NJ0_cat1"
globalReplacementMap["Run3FidXSAnalysisAbsYHJ0"]["catRVMap"]["RECO_AbsYHJ0_NJ0_cat2"] = "RECO_AbsYHJ0_NJ0_cat2"
