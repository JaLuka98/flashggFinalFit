# Hold common objects used for Trees2WS scripts
from collections import OrderedDict as od

diffDict = od()

DIFFVAR_TO_VARIABLE = {
    'diffVariable_GenPTH': 'PTH',
    'diffVariable_GenYH': 'rapidity',
    'diffVariable_GenNJ': 'NJ',
    'diffVariable_GenPTJ0': 'PTJ0',
    'diffVariable_GenYJ0': 'YJ0',
    'diffVariable_GenAbsPhiHJ0': 'AbsPhiHJ0',
    'diffVariable_GenAbsYHJ0': 'AbsYHJ0',
}

_PTH_BINS = [
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
_PTH_START_ID = 10
for idx, label in enumerate(_PTH_BINS):
    diffDict[_PTH_START_ID + idx] = f"PTH_{label}_in"
diffDict[0] = "PTH_0p0_10000p0_out"

diffDict[20] = "YH_0p0_0p15_in"
diffDict[21] = "YH_0p15_0p3_in"
diffDict[22] = "YH_0p3_0p45_in"
diffDict[23] = "YH_0p45_0p6_in"
diffDict[34] = "YH_0p6_0p75_in"
diffDict[24] = "YH_0p75_0p9_in"
diffDict[36] = "YH_0p9_1p2_in"
diffDict[37] = "YH_1p2_1p6_in"
diffDict[38] = "YH_1p6_2p0_in"
diffDict[39] = "YH_2p0_2p5_in"
diffDict[25] = "YH_0p0_2p5_out"

diffDict[30] = "NJ_0p0_1p0_in"
diffDict[31] = "NJ_1p0_2p0_in"
diffDict[32] = "NJ_2p0_3p0_in"
diffDict[33] = "NJ_3p0_100p0_in"
# diffDict[33] = "NJ_3p0_4p0_in"
# diffDict[34] = "NJ_4p0_100p0_in"
diffDict[34] = "NJ_0p0_100p0_out"

diffDict[50] = "PTJ0_0p0_30p0_in"
diffDict[51] = "PTJ0_30p0_40p0_in"
diffDict[52] = "PTJ0_40p0_55p0_in"
diffDict[53] = "PTJ0_55p0_75p0_in"
diffDict[54] = "PTJ0_75p0_95p0_in"
diffDict[55] = "PTJ0_95p0_120p0_in"
diffDict[56] = "PTJ0_120p0_150p0_in"
diffDict[57] = "PTJ0_150p0_200p0_in"
diffDict[58] = "PTJ0_200p0_10000p0_in"
diffDict[59] = "PTJ0_0p0_10000p0_out"

diffDict[50] = "YJ0_0p0_0p5_in"
diffDict[51] = "YJ0_0p5_1p2_in"
diffDict[52] = "YJ0_1p2_2p0_in"
diffDict[53] = "YJ0_2p0_2p5_in"
diffDict[54] = "YJ0_NJ0_in"
diffDict[55] = "YJ0_0p0_2p5_out"

diffDict[60] = "AbsPhiHJ0_0p0_2p6_in"
diffDict[61] = "AbsPhiHJ0_2p6_2p9_in"
diffDict[62] = "AbsPhiHJ0_2p9_3p03_in"
# diffDict[63] = "AbsPhiHJ0_3p03_Pi_in"
# diffDict[64] = "AbsPhiHJ0_NJ0_in"
diffDict[63] = "AbsPhiHJ0_3p03_3p1415926_in"
diffDict[64] = "AbsPhiHJ0_NJ_in"

diffDict[65] = "AbsPhiHJ0_0p0_Pi_out"

diffDict[70] = "AbsYHJ0_0p0_0p6_in"
diffDict[71] = "AbsYHJ0_0p6_1p2_in"
diffDict[72] = "AbsYHJ0_1p2_1p9_in"
diffDict[73] = "AbsYHJ0_1p9_100p0_in"
diffDict[74] = "AbsYHJ0_NJ0_in"
diffDict[75] = "AbsYHJ0_0p0_100p0_out"
