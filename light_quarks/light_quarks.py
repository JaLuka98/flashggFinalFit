from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
import csv
import json
import os

# Physics models for BSM limits on enhanced light-quark Higgs couplings.
#
# Inclusive signal strength parametrisation:
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

SM_XS   = 67.8
BSM_XS  = 5.333
B_WIDTH = 0.5824

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
INCLUSIVE_DIR = os.path.join(LIGHT_QUARKS_DIR, "inclusive")
SM_PREDICTION_JSON = os.path.join(LIGHT_QUARKS_DIR, "run3_with_HIG_19_016_Binning.json")
INCLUSIVE_BSM_CSVS = {
    "ssH": os.path.join(INCLUSIVE_DIR, "ssH_13p6TeV_total-aafidR3.csv"),
    "uuH": os.path.join(INCLUSIVE_DIR, "uuH_13p6TeV_total-aafidR2.csv"),
    "ddH": os.path.join(INCLUSIVE_DIR, "ddH_13p6TeV_total-aafidR3.csv"),
}
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


def load_inclusive_bsm_xs(bsm_label):
    if bsm_label not in INCLUSIVE_BSM_CSVS:
        raise RuntimeError("Unknown inclusive BSM prediction label: %s" % bsm_label)

    with open(INCLUSIVE_BSM_CSVS[bsm_label]) as fin:
        reader = csv.DictReader(
            (line for line in fin if not line.startswith("#")),
            fieldnames=["bin_lo", "bin_hi", "value", "error"],
        )
        rows = list(reader)

    if len(rows) != 1:
        raise RuntimeError(
            "Expected exactly one inclusive total cross-section row for %s, found %d" %
            (bsm_label, len(rows))
        )

    # Inclusive total prediction files are in pb. Convert to fb before
    # forming A = sigma_BSM / sigma_SM.
    return float(rows[0]["value"]) * 1e3


INCLUSIVE_BSM_XS = dict(
    (bsm_label, load_inclusive_bsm_xs(bsm_label)) for bsm_label in INCLUSIVE_BSM_CSVS
)
INCLUSIVE_BSM_OVER_SM = dict(
    (bsm_label, INCLUSIVE_BSM_XS[bsm_label] / SM_XS) for bsm_label in INCLUSIVE_BSM_XS
)


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

    def __init__(self, bsm_label="ssH", poi_name="kappa_q"):
        PhysicsModel.__init__(self)
        self.bsm_label = bsm_label
        self.poi_name = poi_name

    def doParametersOfInterest(self):
        A = INCLUSIVE_BSM_OVER_SM[self.bsm_label]

        self.modelBuilder.doVar("%s[0,-2,2]" % self.poi_name)

        a_name = "A_prod_%s_inclusive" % self.bsm_label
        mu_name = "mu_%s_%s_inclusive" % (self.poi_name, self.bsm_label)

        self.modelBuilder.doVar("%s[%.8f]" % (a_name, A))
        self.modelBuilder.out.var(a_name).setConstant(True)

        self.modelBuilder.doVar("B_width[%.8f]" % B_WIDTH)
        self.modelBuilder.out.var("B_width").setConstant(True)

        # Inclusive rate scaling applied to all signal processes.
        self.modelBuilder.factory_(
            'expr::%s("(1 + @0*@1*@1)/(1 + @2*@1*@1)", %s, %s, B_width)' %
            (mu_name, a_name, self.poi_name)
        )

        self.modelBuilder.doSet("POI", self.poi_name)

    def getYieldScale(self, bin, process):
        if "bkg" in process or process == "data_obs":
            return 1
        scale = "mu_%s_%s_inclusive" % (self.poi_name, self.bsm_label)
        print("Scaling process %s/%s by %s" % (bin, process, scale))
        return scale


class LightQuarksThreeFlavorInclusive(PhysicsModel):
    """Inclusive rate+BR model with kappa_s, kappa_u, and kappa_d floating.

    Signal strength:
        mu = (1 + A_ssH*ks^2 + A_uuH*ku^2 + A_ddH*kd^2)
             / (1 + B_width*(ks^2 + ku^2 + kd^2))

    Use --redefineSignalPOIs kappa_X in combine to scan one coupling while
    profiling the other two.
    """

    def doParametersOfInterest(self):
        self.modelBuilder.doVar("kappa_s[0,-2,2]")
        self.modelBuilder.doVar("kappa_u[0,-2,2]")
        self.modelBuilder.doVar("kappa_d[0,-2,2]")

        self.modelBuilder.doVar("B_width[%.8f]" % B_WIDTH)
        self.modelBuilder.out.var("B_width").setConstant(True)

        for bsm_label in ["ssH", "uuH", "ddH"]:
            a_name = "A_prod_%s_inclusive" % bsm_label
            self.modelBuilder.doVar("%s[%.8f]" % (a_name, INCLUSIVE_BSM_OVER_SM[bsm_label]))
            self.modelBuilder.out.var(a_name).setConstant(True)

        self.modelBuilder.factory_(
            'expr::mu_three_flavor_inclusive("(1 + @0*@1*@1 + @2*@3*@3 + @4*@5*@5)'
            '/(1 + @6*(@1*@1 + @3*@3 + @5*@5))",'
            ' A_prod_ssH_inclusive, kappa_s,'
            ' A_prod_uuH_inclusive, kappa_u,'
            ' A_prod_ddH_inclusive, kappa_d, B_width)'
        )

        self.modelBuilder.doSet("POI", "kappa_s,kappa_u,kappa_d")

    def getYieldScale(self, bin, process):
        if "bkg" in process or process == "data_obs":
            return 1
        print("Scaling process %s/%s by mu_three_flavor_inclusive" % (bin, process))
        return "mu_three_flavor_inclusive"


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


class LightQuarksThreeFlavorShapeOnly(PhysicsModel):
    """Shape-only model with all three light-quark couplings (kappa_u, kappa_d,
    kappa_s) floating simultaneously.

    Per-bin signal strength:
        mu_i = BR_hgg * (1 + A_ssH_i*kappa_s^2 + A_uuH_i*kappa_u^2 + A_ddH_i*kappa_d^2)

    BR_hgg is a free common normalization factor (flatParam) that absorbs the
    inclusive rate/BR uncertainty, leaving the constraint purely in the PTH shape.
    The global width denominator is intentionally omitted for the same reason as
    in LightQuarksDifferentialShapeOnly.

    Intended usage: scan one kappa while profiling the other two with
    --redefineSignalPOIs kappa_X in combineTool.py.
    """

    def doParametersOfInterest(self):
        self.modelBuilder.doVar("kappa_s[0,-3,3]")
        self.modelBuilder.doVar("kappa_u[0,-3,3]")
        self.modelBuilder.doVar("kappa_d[0,-3,3]")

        # Free global normalization: absorbs overall rate/BR uncertainty so
        # the remaining sensitivity comes purely from the PTH bin-shape.
        self.modelBuilder.doVar("BR_hgg[1,0,10]")
        self.modelBuilder.out.var("BR_hgg").setAttribute("flatParam")

        for pth_bin in PTH_BINS:
            a_s    = "A_prod_ssH_PTH_%s" % pth_bin
            a_u    = "A_prod_uuH_PTH_%s" % pth_bin
            a_d    = "A_prod_ddH_PTH_%s" % pth_bin
            mu_name = "mu_three_flavor_shape_only_PTH_%s" % pth_bin

            self.modelBuilder.doVar("%s[%.8f]" % (a_s, PTH_BSM_OVER_SM["ssH"][pth_bin]))
            self.modelBuilder.out.var(a_s).setConstant(True)
            self.modelBuilder.doVar("%s[%.8f]" % (a_u, PTH_BSM_OVER_SM["uuH"][pth_bin]))
            self.modelBuilder.out.var(a_u).setConstant(True)
            self.modelBuilder.doVar("%s[%.8f]" % (a_d, PTH_BSM_OVER_SM["ddH"][pth_bin]))
            self.modelBuilder.out.var(a_d).setConstant(True)

            # @0=BR_hgg  @1=A_s  @2=kappa_s  @3=A_u  @4=kappa_u  @5=A_d  @6=kappa_d
            self.modelBuilder.factory_(
                'expr::%s("@0*(1 + @1*@2*@2 + @3*@4*@4 + @5*@6*@6)",'
                ' BR_hgg, %s, kappa_s, %s, kappa_u, %s, kappa_d)' %
                (mu_name, a_s, a_u, a_d)
            )

        self.modelBuilder.doSet("POI", "kappa_s,kappa_u,kappa_d")

    def getYieldScale(self, bin, process):
        if "bkg" in process or process == "data_obs":
            return 1

        for pth_bin in PTH_BINS:
            if "_PTH_%s_in_" % pth_bin in process:
                scale = "mu_three_flavor_shape_only_PTH_%s" % pth_bin
                print("Scaling process %s/%s by %s" % (bin, process, scale))
                return scale

        return 1


class LightQuarksThreeFlavorDifferential(PhysicsModel):
    """Full rate+BR model with all three light-quark couplings floating.

    Per-bin signal strength:
        mu_i = (1 + A_ssH_i*kappa_s^2 + A_uuH_i*kappa_u^2 + A_ddH_i*kappa_d^2)
               / (1 + B_width*(kappa_s^2 + kappa_u^2 + kappa_d^2))

    Numerator: bin-by-bin production rate enhancement from all three quark loops.
    Denominator: total Higgs width increase from H->ss, H->uu, H->dd with the
                 same B_WIDTH coefficient used in the single-flavor models.

    Intended usage: scan one kappa while profiling the other two with
    --redefineSignalPOIs kappa_X in combineTool.py.
    """

    def doParametersOfInterest(self):
        self.modelBuilder.doVar("kappa_s[0,-3,3]")
        self.modelBuilder.doVar("kappa_u[0,-3,3]")
        self.modelBuilder.doVar("kappa_d[0,-3,3]")

        self.modelBuilder.doVar("B_width[%.8f]" % B_WIDTH)
        self.modelBuilder.out.var("B_width").setConstant(True)

        for pth_bin in PTH_BINS:
            a_s     = "A_prod_ssH_PTH_%s" % pth_bin
            a_u     = "A_prod_uuH_PTH_%s" % pth_bin
            a_d     = "A_prod_ddH_PTH_%s" % pth_bin
            mu_name = "mu_three_flavor_PTH_%s" % pth_bin

            self.modelBuilder.doVar("%s[%.8f]" % (a_s, PTH_BSM_OVER_SM["ssH"][pth_bin]))
            self.modelBuilder.out.var(a_s).setConstant(True)
            self.modelBuilder.doVar("%s[%.8f]" % (a_u, PTH_BSM_OVER_SM["uuH"][pth_bin]))
            self.modelBuilder.out.var(a_u).setConstant(True)
            self.modelBuilder.doVar("%s[%.8f]" % (a_d, PTH_BSM_OVER_SM["ddH"][pth_bin]))
            self.modelBuilder.out.var(a_d).setConstant(True)

            # @0=A_s  @1=kappa_s  @2=A_u  @3=kappa_u  @4=A_d  @5=kappa_d  @6=B_width
            self.modelBuilder.factory_(
                'expr::%s("(1 + @0*@1*@1 + @2*@3*@3 + @4*@5*@5)'
                '/(1 + @6*(@1*@1 + @3*@3 + @5*@5))",'
                ' %s, kappa_s, %s, kappa_u, %s, kappa_d, B_width)' %
                (mu_name, a_s, a_u, a_d)
            )

        self.modelBuilder.doSet("POI", "kappa_s,kappa_u,kappa_d")

    def getYieldScale(self, bin, process):
        if "bkg" in process or process == "data_obs":
            return 1

        for pth_bin in PTH_BINS:
            if "_PTH_%s_in_" % pth_bin in process:
                scale = "mu_three_flavor_PTH_%s" % pth_bin
                print("Scaling process %s/%s by %s" % (bin, process, scale))
                return scale

        return 1


light_quarks_inclusive = LightQuarksInclusive("ssH", "kappa_q")
light_quarks_inclusive_ssH = LightQuarksInclusive("ssH", "kappa_s")
light_quarks_inclusive_uuH = LightQuarksInclusive("uuH", "kappa_u")
light_quarks_inclusive_ddH = LightQuarksInclusive("ddH", "kappa_d")
light_quarks_three_flavor_inclusive = LightQuarksThreeFlavorInclusive()
light_quarks_differential = LightQuarksDifferential("ssH", "kappa_q")
light_quarks_differential_shape_only = LightQuarksDifferentialShapeOnly("ssH", "kappa_q")
light_quarks_differential_ssH = LightQuarksDifferential("ssH", "kappa_q")
light_quarks_differential_ssH_shape_only = LightQuarksDifferentialShapeOnly("ssH", "kappa_q")
light_quarks_differential_uuH = LightQuarksDifferential("uuH", "kappa_u")
light_quarks_differential_uuH_shape_only = LightQuarksDifferentialShapeOnly("uuH", "kappa_u")
light_quarks_differential_ddH = LightQuarksDifferential("ddH", "kappa_d")
light_quarks_differential_ddH_shape_only = LightQuarksDifferentialShapeOnly("ddH", "kappa_d")
light_quarks_three_flavor_shape_only = LightQuarksThreeFlavorShapeOnly()
light_quarks_three_flavor_differential = LightQuarksThreeFlavorDifferential()
