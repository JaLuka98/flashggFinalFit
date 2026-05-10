# Python script to hold replacement model mapping for different analyses
from collections import OrderedDict as od
from commonObjects import *

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

PTH_BINS = variableBins["PTH"]

globalReplacementMap["Run3FidXSAnalysisPTH"] = od()
_PTH_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_PTH_FIRST_BIN = PTH_BINS[0]
_PTH_SECOND_BIN = PTH_BINS[1] if len(PTH_BINS) > 1 else PTH_BINS[0]
_PTH_WV_BIN = "35p0_45p0"
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
_RAPIDITY_BINS = variableBins["rapidity"]

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

globalReplacementMap["Run3FidXSAnalysisYH"]["catRVMap"]["RECO_rapidity_1p2_1p6_cat0"] = "RECO_rapidity_1p2_1p6_cat2"
globalReplacementMap["Run3FidXSAnalysisYH"]["catRVMap"]["RECO_rapidity_1p6_2p0_cat0"] = "RECO_rapidity_1p6_2p0_cat2"


# Differential NJ (Number of Jets)
_NJ_BINS = variableBins["NJ"]

globalReplacementMap["Run3FidXSAnalysisNJ"] = od()
_NJ_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_NJ_WV_BIN = "1p0_2p0"
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisNJ"]['procWV'] = f"ggh_NJ_{_NJ_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisNJ"]['catWV'] = f"RECO_NJ_{_NJ_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisNJ"]['procRVMap'] = od()
for _bin in _NJ_BINS:
    for _cat in _NJ_RECO_CATS:
        reco_key = f"RECO_NJ_{_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisNJ"]["procRVMap"][reco_key] = f"ggh_NJ_{_bin}_in"
        
# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisNJ"]["catRVMap"] = od()
for _bin in _NJ_BINS:
    for _cat in _NJ_RECO_CATS:
        reco_key = f"RECO_NJ_{_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisNJ"]["catRVMap"][reco_key] = reco_key

# Differential PTJ0 (PT of the leading jet)

_PTJ0_BINS = variableBins["PTJ0"]
_PTJ0_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_PTJ0_WV_BIN = "75p0_95p0"

globalReplacementMap["Run3FidXSAnalysisPTJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisPTJ0"]['procWV'] = f"ggh_PTJ0_{_PTJ0_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisPTJ0"]['catWV'] = f"RECO_PTJ0_{_PTJ0_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisPTJ0"]['procRVMap'] = od()
for bin_name in _PTJ0_BINS:
    for cat in _PTJ0_RECO_CATS:
        reco_key = f"RECO_PTJ0_{bin_name}_{cat}"
        proc_val = f"ggh_PTJ0_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisPTJ0"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisPTJ0"]["catRVMap"] = od()
for bin_name in _PTJ0_BINS:
    for cat in _PTJ0_RECO_CATS:
        reco_key = f"RECO_PTJ0_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisPTJ0"]["catRVMap"][reco_key] = reco_key


# Differential DPhiJ0J1
_DPhiJ0J1_BINS = variableBins["DPhiJ0J1"]

globalReplacementMap["Run3FidXSAnalysisDPhiJ0J1"] = od()
_DPhiJ0J1_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_DPhiJ0J1_WV_BIN = "m2p0944_m1p0472"
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisDPhiJ0J1"]['procWV'] = f"ggh_DPhiJ0J1_{_DPhiJ0J1_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisDPhiJ0J1"]['catWV'] = f"RECO_DPhiJ0J1_{_DPhiJ0J1_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisDPhiJ0J1"]['procRVMap'] = od()
for _bin in _DPhiJ0J1_BINS:
    for _cat in _DPhiJ0J1_RECO_CATS:
        reco_key = f"RECO_DPhiJ0J1_{_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisDPhiJ0J1"]["procRVMap"][reco_key] = f"ggh_DPhiJ0J1_{_bin}_in"
        
# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisDPhiJ0J1"]["catRVMap"] = od()
for _bin in _DPhiJ0J1_BINS:
    for _cat in _DPhiJ0J1_RECO_CATS:
        reco_key = f"RECO_DPhiJ0J1_{_bin}_{_cat}"
        globalReplacementMap["Run3FidXSAnalysisDPhiJ0J1"]["catRVMap"][reco_key] = reco_key

# Differential NBJet
_NBJET_BINS = variableBins["NBJet"]
_NBJET_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_NBJET_WV_BIN = "0p0_1p0"

globalReplacementMap["Run3FidXSAnalysisNBJet"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisNBJet"]['procWV'] = f"ggh_NBJet_{_NBJET_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisNBJet"]['catWV'] = f"RECO_NBJet_{_NBJET_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisNBJet"]['procRVMap'] = od()
for bin_name in _NBJET_BINS:
    for cat in _NBJET_RECO_CATS:
        reco_key = f"RECO_NBJet_{bin_name}_{cat}"
        proc_val = f"ggh_NBJet_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisNBJet"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisNBJet"]["catRVMap"] = od()
for bin_name in _NBJET_BINS:
    for cat in _NBJET_RECO_CATS:
        reco_key = f"RECO_NBJet_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisNBJet"]["catRVMap"][reco_key] = reco_key

# Differential DYHJ0
_DYHJ0_BINS = variableBins["DYHJ0"]
_DYHJ0_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_DYHJ0_WV_BIN = "0p3_0p6"

globalReplacementMap["Run3FidXSAnalysisDYHJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisDYHJ0"]['procWV'] = f"ggh_DYHJ0_{_DYHJ0_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisDYHJ0"]['catWV'] = f"RECO_DYHJ0_{_DYHJ0_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisDYHJ0"]['procRVMap'] = od()
for bin_name in _DYHJ0_BINS:
    for cat in _DYHJ0_RECO_CATS:
        reco_key = f"RECO_DYHJ0_{bin_name}_{cat}"
        proc_val = f"ggh_DYHJ0_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisDYHJ0"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisDYHJ0"]["catRVMap"] = od()
for bin_name in _DYHJ0_BINS:
    for cat in _DYHJ0_RECO_CATS:
        reco_key = f"RECO_DYHJ0_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisDYHJ0"]["catRVMap"][reco_key] = reco_key


# Differential TauJC
_TauJC_BINS = variableBins["TauJC"]
_TauJC_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_TauJC_WV_BIN = "0p0_15p0"

globalReplacementMap["Run3FidXSAnalysisTauJC"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisTauJC"]['procWV'] = f"ggh_TauJC_{_TauJC_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisTauJC"]['catWV'] = f"RECO_TauJC_{_TauJC_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisTauJC"]['procRVMap'] = od()
for bin_name in _TauJC_BINS:
    for cat in _TauJC_RECO_CATS:
        reco_key = f"RECO_TauJC_{bin_name}_{cat}"
        proc_val = f"ggh_TauJC_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisTauJC"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisTauJC"]["catRVMap"] = od()
for bin_name in _TauJC_BINS:
    for cat in _TauJC_RECO_CATS:
        reco_key = f"RECO_TauJC_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisTauJC"]["catRVMap"][reco_key] = reco_key


# Differential PTJ1
_PTJ1_BINS = variableBins["PTJ1"]
_PTJ1_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_PTJ1_WV_BIN = "45p0_65p0"

globalReplacementMap["Run3FidXSAnalysisPTJ1"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisPTJ1"]['procWV'] = f"ggh_PTJ1_{_PTJ1_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisPTJ1"]['catWV'] = f"RECO_PTJ1_{_PTJ1_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisPTJ1"]['procRVMap'] = od()
for bin_name in _PTJ1_BINS:
    for cat in _PTJ1_RECO_CATS:
        reco_key = f"RECO_PTJ1_{bin_name}_{cat}"
        proc_val = f"ggh_PTJ1_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisPTJ1"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisPTJ1"]["catRVMap"] = od()
for bin_name in _PTJ1_BINS:
    for cat in _PTJ1_RECO_CATS:
        reco_key = f"RECO_PTJ1_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisPTJ1"]["catRVMap"][reco_key] = reco_key



# Differential YJ1
_YJ1_BINS = variableBins["YJ1"]
_YJ1_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_YJ1_WV_BIN = "0p0_0p6"

globalReplacementMap["Run3FidXSAnalysisYJ1"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisYJ1"]['procWV'] = f"ggh_YJ1_{_YJ1_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisYJ1"]['catWV'] = f"RECO_YJ1_{_YJ1_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisYJ1"]['procRVMap'] = od()
for bin_name in _YJ1_BINS:
    for cat in _YJ1_RECO_CATS:
        reco_key = f"RECO_YJ1_{bin_name}_{cat}"
        proc_val = f"ggh_YJ1_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisYJ1"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisYJ1"]["catRVMap"] = od()
for bin_name in _YJ1_BINS:
    for cat in _YJ1_RECO_CATS:
        reco_key = f"RECO_YJ1_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisYJ1"]["catRVMap"][reco_key] = reco_key


# Differential CosThetaStarCS
_CosThetaStarCS_BINS = variableBins["CosThetaStarCS"]
_CosThetaStarCS_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_CosThetaStarCS_WV_BIN = "0p15_0p22"

globalReplacementMap["Run3FidXSAnalysisCosThetaStarCS"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisCosThetaStarCS"]['procWV'] = f"ggh_CosThetaStarCS_{_CosThetaStarCS_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisCosThetaStarCS"]['catWV'] = f"RECO_CosThetaStarCS_{_CosThetaStarCS_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisCosThetaStarCS"]['procRVMap'] = od()
for bin_name in _CosThetaStarCS_BINS:
    for cat in _CosThetaStarCS_RECO_CATS:
        reco_key = f"RECO_CosThetaStarCS_{bin_name}_{cat}"
        proc_val = f"ggh_CosThetaStarCS_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisCosThetaStarCS"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisCosThetaStarCS"]["catRVMap"] = od()
for bin_name in _CosThetaStarCS_BINS:
    for cat in _CosThetaStarCS_RECO_CATS:
        reco_key = f"RECO_CosThetaStarCS_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisCosThetaStarCS"]["catRVMap"][reco_key] = reco_key


# Differential PhiEtaStar
_PhiEtaStar_BINS = variableBins["PhiEtaStar"]
_PhiEtaStar_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_PhiEtaStar_WV_BIN = "0p2_0p3"

globalReplacementMap["Run3FidXSAnalysisPhiEtaStar"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisPhiEtaStar"]['procWV'] = f"ggh_PhiEtaStar_{_PhiEtaStar_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisPhiEtaStar"]['catWV'] = f"RECO_PhiEtaStar_{_PhiEtaStar_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisPhiEtaStar"]['procRVMap'] = od()
for bin_name in _PhiEtaStar_BINS:
    for cat in _PhiEtaStar_RECO_CATS:
        reco_key = f"RECO_PhiEtaStar_{bin_name}_{cat}"
        proc_val = f"ggh_PhiEtaStar_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisPhiEtaStar"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisPhiEtaStar"]["catRVMap"] = od()
for bin_name in _PhiEtaStar_BINS:
    for cat in _PhiEtaStar_RECO_CATS:
        reco_key = f"RECO_PhiEtaStar_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisPhiEtaStar"]["catRVMap"][reco_key] = reco_key


# Differential DPhiHJ0
_DPhiHJ0_BINS = variableBins["DPhiHJ0"]
_DPhiHJ0_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_DPhiHJ0_WV_BIN = "0p0_2p0"

globalReplacementMap["Run3FidXSAnalysisDPhiHJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0"]['procWV'] = f"ggh_DPhiHJ0_{_DPhiHJ0_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0"]['catWV'] = f"RECO_DPhiHJ0_{_DPhiHJ0_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0"]['procRVMap'] = od()
for bin_name in _DPhiHJ0_BINS:
    for cat in _DPhiHJ0_RECO_CATS:
        reco_key = f"RECO_DPhiHJ0_{bin_name}_{cat}"
        proc_val = f"ggh_DPhiHJ0_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisDPhiHJ0"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0"]["catRVMap"] = od()
for bin_name in _DPhiHJ0_BINS:
    for cat in _DPhiHJ0_RECO_CATS:
        reco_key = f"RECO_DPhiHJ0_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisDPhiHJ0"]["catRVMap"][reco_key] = reco_key


# Differential YJ0
_YJ0_BINS = variableBins["YJ0"]
_YJ0_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_YJ0_WV_BIN = "0p3_0p6"

globalReplacementMap["Run3FidXSAnalysisYJ0"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisYJ0"]['procWV'] = f"ggh_YJ0_{_YJ0_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisYJ0"]['catWV'] = f"RECO_YJ0_{_YJ0_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisYJ0"]['procRVMap'] = od()
for bin_name in _YJ0_BINS:
    for cat in _YJ0_RECO_CATS:
        reco_key = f"RECO_YJ0_{bin_name}_{cat}"
        proc_val = f"ggh_YJ0_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisYJ0"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"] = od()
for bin_name in _YJ0_BINS:
    for cat in _YJ0_RECO_CATS:
        reco_key = f"RECO_YJ0_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisYJ0"]["catRVMap"][reco_key] = reco_key


# Differential DPhiHJ0J1
_DPhiHJ0J1_BINS = variableBins["DPhiHJ0J1"]
_DPhiHJ0J1_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_DPhiHJ0J1_WV_BIN = "0p0_2p0"

globalReplacementMap["Run3FidXSAnalysisDPhiHJ0J1"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0J1"]['procWV'] = f"ggh_DPhiHJ0J1_{_DPhiHJ0J1_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0J1"]['catWV'] = f"RECO_DPhiHJ0J1_{_DPhiHJ0J1_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0J1"]['procRVMap'] = od()
for bin_name in _DPhiHJ0J1_BINS:
    for cat in _DPhiHJ0J1_RECO_CATS:
        reco_key = f"RECO_DPhiHJ0J1_{bin_name}_{cat}"
        proc_val = f"ggh_DPhiHJ0J1_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisDPhiHJ0J1"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisDPhiHJ0J1"]["catRVMap"] = od()
for bin_name in _DPhiHJ0J1_BINS:
    for cat in _DPhiHJ0J1_RECO_CATS:
        reco_key = f"RECO_DPhiHJ0J1_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisDPhiHJ0J1"]["catRVMap"][reco_key] = reco_key


# Differential DEtaJ0J1H
_DEtaJ0J1H_BINS = variableBins["DEtaJ0J1H"]
_DEtaJ0J1H_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_DEtaJ0J1H_WV_BIN = "0p2_0p5"

globalReplacementMap["Run3FidXSAnalysisDEtaJ0J1H"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisDEtaJ0J1H"]['procWV'] = f"ggh_DEtaJ0J1H_{_DEtaJ0J1H_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisDEtaJ0J1H"]['catWV'] = f"RECO_DEtaJ0J1H_{_DEtaJ0J1H_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisDEtaJ0J1H"]['procRVMap'] = od()
for bin_name in _DEtaJ0J1H_BINS:
    for cat in _DEtaJ0J1H_RECO_CATS:
        reco_key = f"RECO_DEtaJ0J1H_{bin_name}_{cat}"
        proc_val = f"ggh_DEtaJ0J1H_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisDEtaJ0J1H"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisDEtaJ0J1H"]["catRVMap"] = od()
for bin_name in _DEtaJ0J1H_BINS:
    for cat in _DEtaJ0J1H_RECO_CATS:
        reco_key = f"RECO_DEtaJ0J1H_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisDEtaJ0J1H"]["catRVMap"][reco_key] = reco_key


# Differential MassJ0J1
_MassJ0J1_BINS = variableBins["MassJ0J1"]
_MassJ0J1_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_MassJ0J1_WV_BIN = "160p0_300p0"

globalReplacementMap["Run3FidXSAnalysisMassJ0J1"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisMassJ0J1"]['procWV'] = f"ggh_MassJ0J1_{_MassJ0J1_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisMassJ0J1"]['catWV'] = f"RECO_MassJ0J1_{_MassJ0J1_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisMassJ0J1"]['procRVMap'] = od()
for bin_name in _MassJ0J1_BINS:
    for cat in _MassJ0J1_RECO_CATS:
        reco_key = f"RECO_MassJ0J1_{bin_name}_{cat}"
        proc_val = f"ggh_MassJ0J1_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisMassJ0J1"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisMassJ0J1"]["catRVMap"] = od()
for bin_name in _MassJ0J1_BINS:
    for cat in _MassJ0J1_RECO_CATS:
        reco_key = f"RECO_MassJ0J1_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisMassJ0J1"]["catRVMap"][reco_key] = reco_key


# Differential EtaJ0J1
_EtaJ0J1_BINS = variableBins["EtaJ0J1"]
_EtaJ0J1_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_EtaJ0J1_WV_BIN = "0p0_0p7"

globalReplacementMap["Run3FidXSAnalysisEtaJ0J1"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisEtaJ0J1"]['procWV'] = f"ggh_EtaJ0J1_{_EtaJ0J1_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisEtaJ0J1"]['catWV'] = f"RECO_EtaJ0J1_{_EtaJ0J1_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisEtaJ0J1"]['procRVMap'] = od()
for bin_name in _EtaJ0J1_BINS:
    for cat in _EtaJ0J1_RECO_CATS:
        reco_key = f"RECO_EtaJ0J1_{bin_name}_{cat}"
        proc_val = f"ggh_EtaJ0J1_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisEtaJ0J1"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisEtaJ0J1"]["catRVMap"] = od()
for bin_name in _EtaJ0J1_BINS:
    for cat in _EtaJ0J1_RECO_CATS:
        reco_key = f"RECO_EtaJ0J1_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisEtaJ0J1"]["catRVMap"][reco_key] = reco_key



# Differential PTHvsDPhiJ0J1
_PTHvsDPhiJ0J1_BINS = variableBins["PTHvsDPhiJ0J1"]
_PTHvsDPhiJ0J1_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_PTHvsDPhiJ0J1_WV_BIN = "0p0_35p0_1p5708_3p1416"

globalReplacementMap["Run3FidXSAnalysisPTHvsDPhiJ0J1"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisPTHvsDPhiJ0J1"]['procWV'] = f"ggh_PTHvsDPhiJ0J1_{_PTHvsDPhiJ0J1_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisPTHvsDPhiJ0J1"]['catWV'] = f"RECO_PTHvsDPhiJ0J1_{_PTHvsDPhiJ0J1_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisPTHvsDPhiJ0J1"]['procRVMap'] = od()
for bin_name in _PTHvsDPhiJ0J1_BINS:
    for cat in _PTHvsDPhiJ0J1_RECO_CATS:
        reco_key = f"RECO_PTHvsDPhiJ0J1_{bin_name}_{cat}"
        proc_val = f"ggh_PTHvsDPhiJ0J1_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisPTHvsDPhiJ0J1"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisPTHvsDPhiJ0J1"]["catRVMap"] = od()
for bin_name in _PTHvsDPhiJ0J1_BINS:
    for cat in _PTHvsDPhiJ0J1_RECO_CATS:
        reco_key = f"RECO_PTHvsDPhiJ0J1_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisPTHvsDPhiJ0J1"]["catRVMap"][reco_key] = reco_key



# Differential PTHvYH
_PTHvYH_BINS = variableBins["PTHvYH"]
_PTHvYH_RECO_CATS = ['cat0', 'cat1', 'cat2', 'catMerged']
_PTHvYH_WV_BIN = "0p0_50p0_0p4_0p65"

globalReplacementMap["Run3FidXSAnalysisPTHvYH"] = od()
# Wrong vertex stuff, which process should be considered?
globalReplacementMap["Run3FidXSAnalysisPTHvYH"]['procWV'] = f"ggh_PTHvYH_{_PTHvYH_WV_BIN}_in"
globalReplacementMap["Run3FidXSAnalysisPTHvYH"]['catWV'] = f"RECO_PTHvYH_{_PTHvYH_WV_BIN}_cat2"
# Relacement processes for RV
globalReplacementMap["Run3FidXSAnalysisPTHvYH"]['procRVMap'] = od()
for bin_name in _PTHvYH_BINS:
    for cat in _PTHvYH_RECO_CATS:
        reco_key = f"RECO_PTHvYH_{bin_name}_{cat}"
        proc_val = f"ggh_PTHvYH_{bin_name}_in"
        globalReplacementMap["Run3FidXSAnalysisPTHvYH"]["procRVMap"][reco_key] = proc_val


# Replacement categories for RV
globalReplacementMap["Run3FidXSAnalysisPTHvYH"]["catRVMap"] = od()
for bin_name in _PTHvYH_BINS:
    for cat in _PTHvYH_RECO_CATS:
        reco_key = f"RECO_PTHvYH_{bin_name}_{cat}"
        globalReplacementMap["Run3FidXSAnalysisPTHvYH"]["catRVMap"][reco_key] = reco_key