from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import csv
import json
import os

# Physics models for BSM limits on enhanced light-quark Higgs couplings.
#
# Differential signal strength parametrisation:
#   mu(kappa_q) = (1 + (bsm_xs/sm_xs) * kappa_q^2) / (1 + 0.58 * kappa_q^2)
#
# Numerator: total rate scaling from enhanced ggH production via quark loop.
# Denominator: total Higgs width increase from enhanced H->qq decay.
#
# For the differential models, bsm_xs/sm_xs is read from the local prediction
# files in this directory. The BSM prediction is converted from pb/GeV to
# fb/GeV, and the SM fiducial cross section in each bin is divided by the bin
# width to obtain fb/GeV before forming the ratio.
#
# The shape-only differential model profiles one common free signal-rate factor:
#   mu_i(kappa_q) = BR_hgg * (1 + A_i*kappa_q^2)
# The global width/branching-ratio denominator from the rate model is omitted,
# because that inclusive rate effect is intentionally absorbed by BR_hgg.
#
# Constants used by the inclusive model (update here if better values become available):
#   sm_xs  = 70.0 fb  (SM inclusive fiducial ggH cross section)
#   bsm_xs = 10.0 fb  (BSM contribution to production per unit kappa_q^2)
#   B_width = 0.58    (coefficient of kappa_q^2 in total width scaling)

SM_XS   = 70.0
BSM_XS  = 4.0
B_WIDTH = 0.58

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

LIGHT_QUARKS_DIR = os.path.dirname(os.path.abspath(__file__))
SM_PREDICTION_JSON = os.path.join(LIGHT_QUARKS_DIR, "run3_with_HIG_19_016_Binning.json")
BSM_PREDICTION_CSVS = {
    "ssH": os.path.join(LIGHT_QUARKS_DIR, "ssH_13p6TeV_PTH_HIG19016-aafidR3.csv"),
    "uuH": os.path.join(LIGHT_QUARKS_DIR, "uuH_13p6TeV_PTH_HIG19016-aafidR3.csv"),
    "ddH": os.path.join(LIGHT_QUARKS_DIR, "ddH_13p6TeV_PTH_HIG19016-aafidR3.csv"),
}
BSM_LAST_BIN_SCALE = {
    "ssH": 100.0,
    "uuH": 100.0,
    "ddH": 100.0,
}


def load_pth_predictions(bsm_label):
    if bsm_label not in BSM_PREDICTION_CSVS:
        raise RuntimeError("Unknown BSM prediction label: %s" % bsm_label)

    with open(SM_PREDICTION_JSON) as fin:
        sm_payload = json.load(fin)["total"]

    sm_edges = sm_payload["bins"]
    sm_fid_xs = sm_payload["fidXS"]
    if len(sm_edges) != len(sm_fid_xs) + 1:
        raise RuntimeError("SM prediction JSON has inconsistent bins/fidXS lengths")

    bsm_rows = []
    with open(BSM_PREDICTION_CSVS[bsm_label]) as fin:
        reader = csv.DictReader(
            (line for line in fin if not line.startswith("#")),
            fieldnames=["bin_lo", "bin_hi", "value", "error"],
        )
        for row in reader:
            bsm_rows.append(row)

    if len(sm_fid_xs) != len(PTH_BINS) or len(bsm_rows) != len(PTH_BINS):
        raise RuntimeError(
            "Prediction inputs do not match PTH bin count: model=%d, SM=%d, %s=%d" %
            (len(PTH_BINS), len(sm_fid_xs), bsm_label, len(bsm_rows))
        )

    predictions = {}
    for idx, pth_bin in enumerate(PTH_BINS):
        sm_width = float(sm_edges[idx + 1]) - float(sm_edges[idx])
        sm_xs_per_gev = float(sm_fid_xs[idx]) / sm_width

        # BSM files are in pb/GeV. Convert to fb/GeV before forming bsm/sm.
        # The final BSM overflow bin is provided in a wider source bin and is
        # rescaled to the analysis overflow bin by this dedicated factor.
        bsm_xs_per_gev = float(bsm_rows[idx]["value"]) * 1e3
        bsm_err_per_gev = float(bsm_rows[idx]["error"]) * 1e3
        if idx == len(PTH_BINS) - 1:
            bsm_xs_per_gev *= BSM_LAST_BIN_SCALE[bsm_label]
            bsm_err_per_gev *= BSM_LAST_BIN_SCALE[bsm_label]

        predictions[pth_bin] = {
            "sm_fid_xs": float(sm_fid_xs[idx]),
            "sm_xs_per_gev": sm_xs_per_gev,
            "bsm_xs_per_gev": bsm_xs_per_gev,
            "bsm_err_per_gev": bsm_err_per_gev,
            "bsm_over_sm": bsm_xs_per_gev / sm_xs_per_gev,
            "sm_bin_lo": float(sm_edges[idx]),
            "sm_bin_hi": float(sm_edges[idx + 1]),
            "bsm_bin_lo": float(bsm_rows[idx]["bin_lo"]),
            "bsm_bin_hi": float(bsm_rows[idx]["bin_hi"]),
        }

    return predictions


PTH_PREDICTIONS = dict(
    (bsm_label, load_pth_predictions(bsm_label)) for bsm_label in BSM_PREDICTION_CSVS
)
PTH_BSM_OVER_SM = {}
for bsm_label, predictions in PTH_PREDICTIONS.items():
    PTH_BSM_OVER_SM[bsm_label] = dict(
        (pth_bin, predictions[pth_bin]["bsm_over_sm"]) for pth_bin in PTH_BINS
    )


class LightQuarksInclusive(PhysicsModel):

    def doParametersOfInterest(self):
        A = BSM_XS / SM_XS  # = 0.142857...

        self.modelBuilder.doVar("kappa_q[0,0,3]")

        self.modelBuilder.doVar("A_prod[%.8f]" % A)
        self.modelBuilder.out.var("A_prod").setConstant(True)

        self.modelBuilder.doVar("B_width[%.8f]" % B_WIDTH)
        self.modelBuilder.out.var("B_width").setConstant(True)

        # mu(kappa_q) = (1 + A*kappa_q^2) / (1 + B*kappa_q^2)
        self.modelBuilder.factory_(
            'expr::mu_kappa_q("(1 + @0*@1*@1)/(1 + @2*@1*@1)", A_prod, kappa_q, B_width)'
        )

        self.modelBuilder.doSet("POI", "kappa_q")

    def getYieldScale(self, bin, process):
        if "bkg" in process:
            return 1
        print("Scaling process %s/%s by mu_kappa_q" % (bin, process))
        return "mu_kappa_q"


class LightQuarksDifferential(PhysicsModel):

    def __init__(self, bsm_label="ssH", poi_name="kappa_q"):
        PhysicsModel.__init__(self)
        self.bsm_label = bsm_label
        self.poi_name = poi_name

    def doParametersOfInterest(self):
        self.modelBuilder.doVar("%s[0,-3,3]" % self.poi_name)

        self.modelBuilder.doVar("B_width[%.8f]" % B_WIDTH)
        self.modelBuilder.out.var("B_width").setConstant(True)

        for pth_bin in PTH_BINS:
            a_name = "A_prod_%s_PTH_%s" % (self.bsm_label, pth_bin)
            mu_name = "mu_%s_%s_PTH_%s" % (self.poi_name, self.bsm_label, pth_bin)

            self.modelBuilder.doVar("%s[%.8f]" % (a_name, PTH_BSM_OVER_SM[self.bsm_label][pth_bin]))
            self.modelBuilder.out.var(a_name).setConstant(True)

            self.modelBuilder.factory_(
                'expr::%s("(1 + @0*@1*@1)/(1 + @2*@1*@1)", %s, %s, B_width)' %
                (mu_name, a_name, self.poi_name)
            )

        self.modelBuilder.doSet("POI", self.poi_name)

    def getYieldScale(self, bin, process):
        if "bkg" in process or process == "data_obs":
            return 1

        for pth_bin in PTH_BINS:
            if "_PTH_%s_in_" % pth_bin in process:
                scale = "mu_%s_%s_PTH_%s" % (self.poi_name, self.bsm_label, pth_bin)
                print("Scaling process %s/%s by %s" % (bin, process, scale))
                return scale

        return 1


class LightQuarksDifferentialShapeOnly(PhysicsModel):

    def __init__(self, bsm_label="ssH", poi_name="kappa_q"):
        PhysicsModel.__init__(self)
        self.bsm_label = bsm_label
        self.poi_name = poi_name

    def doParametersOfInterest(self):
        self.modelBuilder.doVar("%s[0,-3,3]" % self.poi_name)

        self.modelBuilder.doVar("BR_hgg[1,0,10]")
        self.modelBuilder.out.var("BR_hgg").setAttribute("flatParam")

        for pth_bin in PTH_BINS:
            a_name = "A_prod_%s_PTH_%s" % (self.bsm_label, pth_bin)
            mu_name = "mu_%s_%s_shape_only_PTH_%s" % (self.poi_name, self.bsm_label, pth_bin)

            self.modelBuilder.doVar("%s[%.8f]" % (a_name, PTH_BSM_OVER_SM[self.bsm_label][pth_bin]))
            self.modelBuilder.out.var(a_name).setConstant(True)

            self.modelBuilder.factory_(
                'expr::%s("@0*(1 + @1*@2*@2)", BR_hgg, %s, %s)' %
                (mu_name, a_name, self.poi_name)
            )

        self.modelBuilder.doSet("POI", self.poi_name)

    def getYieldScale(self, bin, process):
        if "bkg" in process or process == "data_obs":
            return 1

        for pth_bin in PTH_BINS:
            if "_PTH_%s_in_" % pth_bin in process:
                scale = "mu_%s_%s_shape_only_PTH_%s" % (self.poi_name, self.bsm_label, pth_bin)
                print("Scaling process %s/%s by %s" % (bin, process, scale))
                return scale

        return 1


light_quarks_inclusive = LightQuarksInclusive()
light_quarks_differential = LightQuarksDifferential("ssH", "kappa_q")
light_quarks_differential_shape_only = LightQuarksDifferentialShapeOnly("ssH", "kappa_q")
light_quarks_differential_uuH = LightQuarksDifferential("uuH", "kappa_u")
light_quarks_differential_uuH_shape_only = LightQuarksDifferentialShapeOnly("uuH", "kappa_u")
light_quarks_differential_ddH = LightQuarksDifferential("ddH", "kappa_d")
light_quarks_differential_ddH_shape_only = LightQuarksDifferentialShapeOnly("ddH", "kappa_d")
