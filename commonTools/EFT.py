from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel


class SMEFT_chg_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        self.modelBuilder.doVar("A_tot[3.232]")
        self.modelBuilder.doVar("B_tot[36.080]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[0.000]")
        self.modelBuilder.doVar("B_decay[0.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[15.080]")
        self.modelBuilder.doVar("B_0p0_15p0[172.550]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[14.897]")
        self.modelBuilder.doVar("B_15p0_30p0[170.786]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[14.673]")
        self.modelBuilder.doVar("B_30p0_45p0[169.875]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[14.337]")
        self.modelBuilder.doVar("B_45p0_80p0[166.016]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[13.712]")
        self.modelBuilder.doVar("B_80p0_120p0[158.921]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[13.570]")
        self.modelBuilder.doVar("B_120p0_200p0[158.153]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[14.238]")
        self.modelBuilder.doVar("B_200p0_350p0[185.317]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[18.776]")
        self.modelBuilder.doVar("B_350p0_10000p0[351.115]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chg_0p0_15p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg_15p0_30p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg_30p0_45p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg_45p0_80p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg_80p0_120p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg_120p0_200p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg_200p0_350p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg_350p0_10000p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chg_0p0_15p0", "chg_15p0_30p0", "chg_30p0_45p0", "chg_45p0_80p0", "chg_80p0_120p0", "chg_120p0_200p0", "chg_200p0_350p0", "chg_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chg_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chg_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chg_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chg_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chg_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chg_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chg_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chg_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chg_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chg_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chg_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chg_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chg_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chg_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chg_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chg_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chg_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chg_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chg_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chg_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chg_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chg_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chg_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chg_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chg_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chg_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chg_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chg_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chg_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chg_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chg_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chg_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chb_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[-11.774]")
        self.modelBuilder.doVar("B_tot[10212.058]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-4014.900]")
        self.modelBuilder.doVar("B_decay[4029850.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.009]")
        self.modelBuilder.doVar("B_0p0_15p0[1.730]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.018]")
        self.modelBuilder.doVar("B_15p0_30p0[4.128]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.046]")
        self.modelBuilder.doVar("B_30p0_45p0[6.781]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.092]")
        self.modelBuilder.doVar("B_45p0_80p0[6.979]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.164]")
        self.modelBuilder.doVar("B_80p0_120p0[14.523]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.206]")
        self.modelBuilder.doVar("B_120p0_200p0[17.360]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.113]")
        self.modelBuilder.doVar("B_200p0_350p0[24.630]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.268]")
        self.modelBuilder.doVar("B_350p0_10000p0[84.513]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chb_0p0_15p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb_15p0_30p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb_30p0_45p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb_45p0_80p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb_80p0_120p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb_120p0_200p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb_200p0_350p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb_350p0_10000p0[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chb_0p0_15p0", "chb_15p0_30p0", "chb_30p0_45p0", "chb_45p0_80p0", "chb_80p0_120p0", "chb_120p0_200p0", "chb_200p0_350p0", "chb_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chb_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chb_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chb_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chb_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chb_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chb_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chb_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chb_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chb_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chb_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chb_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chb_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chb_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chb_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chb_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chb_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chb_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chb_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chb_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chb_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chb_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chb_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chb_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chb_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chb_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chb_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chb_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chb_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chb_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chb_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chb_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chb_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chw_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 10.000

        self.modelBuilder.doVar("A_tot[-0.256]")
        self.modelBuilder.doVar("B_tot[18.512]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-130.861]")
        self.modelBuilder.doVar("B_decay[4281.170]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.015]")
        self.modelBuilder.doVar("B_0p0_15p0[0.072]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.035]")
        self.modelBuilder.doVar("B_15p0_30p0[0.118]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.071]")
        self.modelBuilder.doVar("B_30p0_45p0[0.236]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.134]")
        self.modelBuilder.doVar("B_45p0_80p0[0.506]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.251]")
        self.modelBuilder.doVar("B_80p0_120p0[1.114]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.314]")
        self.modelBuilder.doVar("B_120p0_200p0[1.869]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.409]")
        self.modelBuilder.doVar("B_200p0_350p0[4.368]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.458]")
        self.modelBuilder.doVar("B_350p0_10000p0[11.918]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chw_0p0_15p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw_15p0_30p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw_30p0_45p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw_45p0_80p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw_80p0_120p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw_120p0_200p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw_200p0_350p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw_350p0_10000p0[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chw_0p0_15p0", "chw_15p0_30p0", "chw_30p0_45p0", "chw_45p0_80p0", "chw_80p0_120p0", "chw_120p0_200p0", "chw_200p0_350p0", "chw_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chw_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chw_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chw_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chw_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chw_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chw_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chw_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chw_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chw_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chw_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chw_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chw_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chw_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chw_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chw_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chw_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chw_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chw_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chw_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chw_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chw_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chw_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chw_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chw_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chw_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chw_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chw_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chw_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chw_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chw_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chw_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chw_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chwb_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[2.534]")
        self.modelBuilder.doVar("B_tot[3827.506]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[2230.440]")
        self.modelBuilder.doVar("B_decay[1243720.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.048]")
        self.modelBuilder.doVar("B_0p0_15p0[1.359]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.129]")
        self.modelBuilder.doVar("B_15p0_30p0[2.911]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.232]")
        self.modelBuilder.doVar("B_30p0_45p0[4.878]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.428]")
        self.modelBuilder.doVar("B_45p0_80p0[7.838]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.697]")
        self.modelBuilder.doVar("B_80p0_120p0[15.509]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.770]")
        self.modelBuilder.doVar("B_120p0_200p0[21.844]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.694]")
        self.modelBuilder.doVar("B_200p0_350p0[35.438]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.748]")
        self.modelBuilder.doVar("B_350p0_10000p0[97.423]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chwb_0p0_15p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb_15p0_30p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb_30p0_45p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb_45p0_80p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb_80p0_120p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb_120p0_200p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb_200p0_350p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb_350p0_10000p0[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chwb_0p0_15p0", "chwb_15p0_30p0", "chwb_30p0_45p0", "chwb_45p0_80p0", "chwb_80p0_120p0", "chwb_120p0_200p0", "chwb_200p0_350p0", "chwb_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chwb_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chwb_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chwb_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chwb_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chwb_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chwb_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chwb_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chwb_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chwb_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chwb_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chwb_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chwb_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chwb_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chwb_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chwb_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chwb_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chwb_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chwb_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chwb_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chwb_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chwb_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chwb_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chwb_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chwb_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chwb_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chwb_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chwb_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chwb_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chwb_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chwb_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chwb_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chwb_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chbox_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 10.000

        self.modelBuilder.doVar("A_tot[1.111]")
        self.modelBuilder.doVar("B_tot[0.337]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[1.212]")
        self.modelBuilder.doVar("B_decay[0.367]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[1.212]")
        self.modelBuilder.doVar("B_0p0_15p0[0.370]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[1.212]")
        self.modelBuilder.doVar("B_15p0_30p0[0.370]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[1.212]")
        self.modelBuilder.doVar("B_30p0_45p0[0.371]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[1.212]")
        self.modelBuilder.doVar("B_45p0_80p0[0.370]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[1.212]")
        self.modelBuilder.doVar("B_80p0_120p0[0.370]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[1.212]")
        self.modelBuilder.doVar("B_120p0_200p0[0.371]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[1.212]")
        self.modelBuilder.doVar("B_200p0_350p0[0.369]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[1.212]")
        self.modelBuilder.doVar("B_350p0_10000p0[0.366]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chbox_0p0_15p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox_15p0_30p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox_30p0_45p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox_45p0_80p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox_80p0_120p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox_120p0_200p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox_200p0_350p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox_350p0_10000p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chbox_0p0_15p0", "chbox_15p0_30p0", "chbox_30p0_45p0", "chbox_45p0_80p0", "chbox_80p0_120p0", "chbox_120p0_200p0", "chbox_200p0_350p0", "chbox_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chbox_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chbox_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chbox_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chbox_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chbox_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chbox_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chbox_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chbox_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chbox_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chbox_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chbox_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chbox_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chbox_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chbox_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chbox_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chbox_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chbox_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chbox_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chbox_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chbox_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chbox_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chbox_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chbox_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chbox_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chbox_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chbox_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chbox_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chbox_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chbox_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chbox_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chbox_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chbox_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chd_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[-0.055]")
        self.modelBuilder.doVar("B_tot[0.605]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-24.164]")
        self.modelBuilder.doVar("B_decay[145.979]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-0.014]")
        self.modelBuilder.doVar("B_0p0_15p0[44.619]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-0.031]")
        self.modelBuilder.doVar("B_15p0_30p0[6.151]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-0.046]")
        self.modelBuilder.doVar("B_30p0_45p0[10.679]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-0.098]")
        self.modelBuilder.doVar("B_45p0_80p0[20.489]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-0.237]")
        self.modelBuilder.doVar("B_80p0_120p0[83.994]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-0.394]")
        self.modelBuilder.doVar("B_120p0_200p0[194.699]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-0.340]")
        self.modelBuilder.doVar("B_200p0_350p0[361.402]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-1.179]")
        self.modelBuilder.doVar("B_350p0_10000p0[5823.196]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chd_0p0_15p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd_15p0_30p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd_30p0_45p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd_45p0_80p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd_80p0_120p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd_120p0_200p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd_200p0_350p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd_350p0_10000p0[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chd_0p0_15p0", "chd_15p0_30p0", "chd_30p0_45p0", "chd_45p0_80p0", "chd_80p0_120p0", "chd_120p0_200p0", "chd_200p0_350p0", "chd_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chd_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chd_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chd_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chd_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chd_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chd_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chd_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chd_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chd_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chd_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chd_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chd_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chd_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chd_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chd_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chd_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chd_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chd_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chd_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chd_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chd_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chd_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chd_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chd_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chd_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chd_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chd_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chd_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chd_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chd_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chd_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chd_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chl3_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 10.000

        self.modelBuilder.doVar("A_tot[-1.415]")
        self.modelBuilder.doVar("B_tot[0.676]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-3.638]")
        self.modelBuilder.doVar("B_decay[3.308]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-1.223]")
        self.modelBuilder.doVar("B_0p0_15p0[0.385]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-1.239]")
        self.modelBuilder.doVar("B_15p0_30p0[0.401]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-1.264]")
        self.modelBuilder.doVar("B_30p0_45p0[0.432]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-1.315]")
        self.modelBuilder.doVar("B_45p0_80p0[0.471]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-1.390]")
        self.modelBuilder.doVar("B_80p0_120p0[0.574]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-1.408]")
        self.modelBuilder.doVar("B_120p0_200p0[0.594]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-1.383]")
        self.modelBuilder.doVar("B_200p0_350p0[0.557]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-1.374]")
        self.modelBuilder.doVar("B_350p0_10000p0[0.237]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chl3_0p0_15p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3_15p0_30p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3_30p0_45p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3_45p0_80p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3_80p0_120p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3_120p0_200p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3_200p0_350p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3_350p0_10000p0[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chl3_0p0_15p0", "chl3_15p0_30p0", "chl3_30p0_45p0", "chl3_45p0_80p0", "chl3_80p0_120p0", "chl3_120p0_200p0", "chl3_200p0_350p0", "chl3_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chl3_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chl3_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chl3_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chl3_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chl3_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chl3_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chl3_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chl3_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chl3_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chl3_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chl3_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chl3_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chl3_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chl3_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chl3_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chl3_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chl3_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chl3_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chl3_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chl3_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chl3_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chl3_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chl3_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chl3_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chl3_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chl3_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chl3_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chl3_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chl3_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chl3_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chl3_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chl3_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_cll1_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[7.135]")
        self.modelBuilder.doVar("B_tot[17.993]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[18.188]")
        self.modelBuilder.doVar("B_decay[82.698]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[6.116]")
        self.modelBuilder.doVar("B_0p0_15p0[9.376]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[6.199]")
        self.modelBuilder.doVar("B_15p0_30p0[9.681]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[6.339]")
        self.modelBuilder.doVar("B_30p0_45p0[10.609]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[6.580]")
        self.modelBuilder.doVar("B_45p0_80p0[10.301]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[6.996]")
        self.modelBuilder.doVar("B_80p0_120p0[14.169]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[7.081]")
        self.modelBuilder.doVar("B_120p0_200p0[14.572]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[6.938]")
        self.modelBuilder.doVar("B_200p0_350p0[12.975]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[6.670]")
        self.modelBuilder.doVar("B_350p0_10000p0[-1.710]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("cll1_0p0_15p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1_15p0_30p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1_30p0_45p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1_45p0_80p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1_80p0_120p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1_120p0_200p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1_200p0_350p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1_350p0_10000p0[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["cll1_0p0_15p0", "cll1_15p0_30p0", "cll1_30p0_45p0", "cll1_45p0_80p0", "cll1_80p0_120p0", "cll1_120p0_200p0", "cll1_200p0_350p0", "cll1_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_cll1_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_cll1_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_cll1_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_cll1_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_cll1_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_cll1_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_cll1_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_cll1_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_cll1_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_cll1_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_cll1_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_cll1_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_cll1_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_cll1_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_cll1_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_cll1_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_cll1_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_cll1_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_cll1_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_cll1_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_cll1_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_cll1_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_cll1_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_cll1_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_cll1_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_cll1_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_cll1_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_cll1_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_cll1_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_cll1_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_cll1_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_cll1_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_ctbre_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 1000.000

        self.modelBuilder.doVar("A_tot[-4.747]")
        self.modelBuilder.doVar("B_tot[2637.037]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-2150.720]")
        self.modelBuilder.doVar("B_decay[1156400.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-0.004]")
        self.modelBuilder.doVar("B_0p0_15p0[11.453]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-0.003]")
        self.modelBuilder.doVar("B_15p0_30p0[3.489]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-0.006]")
        self.modelBuilder.doVar("B_30p0_45p0[8.879]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-0.013]")
        self.modelBuilder.doVar("B_45p0_80p0[24.243]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-0.036]")
        self.modelBuilder.doVar("B_80p0_120p0[52.588]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-0.074]")
        self.modelBuilder.doVar("B_120p0_200p0[130.159]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-0.167]")
        self.modelBuilder.doVar("B_200p0_350p0[376.836]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-0.484]")
        self.modelBuilder.doVar("B_350p0_10000p0[2022.820]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("ctbre_0p0_15p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre_15p0_30p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre_30p0_45p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre_45p0_80p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre_80p0_120p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre_120p0_200p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre_200p0_350p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre_350p0_10000p0[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["ctbre_0p0_15p0", "ctbre_15p0_30p0", "ctbre_30p0_45p0", "ctbre_45p0_80p0", "ctbre_80p0_120p0", "ctbre_120p0_200p0", "ctbre_200p0_350p0", "ctbre_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_ctbre_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_ctbre_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_ctbre_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_ctbre_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_ctbre_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_ctbre_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_ctbre_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_ctbre_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_ctbre_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_ctbre_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_ctbre_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_ctbre_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_ctbre_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_ctbre_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_ctbre_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_ctbre_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_ctbre_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_ctbre_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_ctbre_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_ctbre_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_ctbre_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_ctbre_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_ctbre_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_ctbre_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_ctbre_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_ctbre_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_ctbre_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_ctbre_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_ctbre_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_ctbre_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_ctbre_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_ctbre_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_cthre_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[0.009]")
        self.modelBuilder.doVar("B_tot[0.007]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[3.447]")
        self.modelBuilder.doVar("B_decay[2.970]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-12.040]")
        self.modelBuilder.doVar("B_0p0_15p0[36.734]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-11.900]")
        self.modelBuilder.doVar("B_15p0_30p0[36.388]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-11.744]")
        self.modelBuilder.doVar("B_30p0_45p0[35.927]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-11.494]")
        self.modelBuilder.doVar("B_45p0_80p0[35.302]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-11.103]")
        self.modelBuilder.doVar("B_80p0_120p0[34.314]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-11.034]")
        self.modelBuilder.doVar("B_120p0_200p0[34.209]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-11.189]")
        self.modelBuilder.doVar("B_200p0_350p0[35.230]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-11.304]")
        self.modelBuilder.doVar("B_350p0_10000p0[36.237]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("cthre_0p0_15p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre_15p0_30p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre_30p0_45p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre_45p0_80p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre_80p0_120p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre_120p0_200p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre_200p0_350p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre_350p0_10000p0[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["cthre_0p0_15p0", "cthre_15p0_30p0", "cthre_30p0_45p0", "cthre_45p0_80p0", "cthre_80p0_120p0", "cthre_120p0_200p0", "cthre_200p0_350p0", "cthre_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_cthre_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_cthre_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_cthre_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_cthre_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_cthre_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_cthre_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_cthre_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_cthre_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_cthre_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_cthre_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_cthre_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_cthre_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_cthre_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_cthre_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_cthre_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_cthre_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_cthre_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_cthre_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_cthre_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_cthre_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_cthre_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_cthre_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_cthre_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_cthre_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_cthre_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_cthre_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_cthre_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_cthre_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_cthre_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_cthre_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_cthre_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_cthre_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_ctwre_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[-0.372]")
        self.modelBuilder.doVar("B_tot[9.499]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-115.159]")
        self.modelBuilder.doVar("B_decay[3315.370]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-0.008]")
        self.modelBuilder.doVar("B_0p0_15p0[3.168]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-0.008]")
        self.modelBuilder.doVar("B_15p0_30p0[0.532]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-0.018]")
        self.modelBuilder.doVar("B_30p0_45p0[1.729]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-0.047]")
        self.modelBuilder.doVar("B_45p0_80p0[3.530]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-0.143]")
        self.modelBuilder.doVar("B_80p0_120p0[15.738]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-0.234]")
        self.modelBuilder.doVar("B_120p0_200p0[124.324]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-0.531]")
        self.modelBuilder.doVar("B_200p0_350p0[95.980]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-1.311]")
        self.modelBuilder.doVar("B_350p0_10000p0[716.012]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("ctwre_0p0_15p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_0p0_15p0, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre_15p0_30p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_15p0_30p0, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre_30p0_45p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_30p0_45p0, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre_45p0_80p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_45p0_80p0, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre_80p0_120p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_80p0_120p0, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre_120p0_200p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_120p0_200p0, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre_200p0_350p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_200p0_350p0, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre_350p0_10000p0[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["ctwre_0p0_15p0", "ctwre_15p0_30p0", "ctwre_30p0_45p0", "ctwre_45p0_80p0", "ctwre_80p0_120p0", "ctwre_120p0_200p0", "ctwre_200p0_350p0", "ctwre_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_ctwre_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_ctwre_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_ctwre_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_ctwre_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_ctwre_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_ctwre_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_ctwre_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_ctwre_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_ctwre_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_ctwre_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_ctwre_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_ctwre_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_ctwre_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_ctwre_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_ctwre_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_ctwre_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_ctwre_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_ctwre_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_ctwre_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_ctwre_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_ctwre_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_ctwre_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_ctwre_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_ctwre_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_ctwre_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_ctwre_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_ctwre_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_ctwre_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_ctwre_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_ctwre_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_ctwre_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_ctwre_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chg(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        self.modelBuilder.doVar("A_tot[3.232]")
        self.modelBuilder.doVar("B_tot[36.080]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[0.000]")
        self.modelBuilder.doVar("B_decay[0.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[15.080]")
        self.modelBuilder.doVar("B_0p0_15p0[172.550]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[14.897]")
        self.modelBuilder.doVar("B_15p0_30p0[170.786]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[14.673]")
        self.modelBuilder.doVar("B_30p0_45p0[169.875]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[14.337]")
        self.modelBuilder.doVar("B_45p0_80p0[166.016]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[13.712]")
        self.modelBuilder.doVar("B_80p0_120p0[158.921]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[13.570]")
        self.modelBuilder.doVar("B_120p0_200p0[158.153]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[14.238]")
        self.modelBuilder.doVar("B_200p0_350p0[185.317]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[18.776]")
        self.modelBuilder.doVar("B_350p0_10000p0[351.115]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chg"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chg_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chg_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chg_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chg_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chg_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chg_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chg_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chg_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chg_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chg_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chg_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chg_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chg_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chg_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chg_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chg_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chg_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chg_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chg_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chg_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chg_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chg_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chg_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chg_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chg_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chg_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chg_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chg_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chg_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chg_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chg_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chg_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chb(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[-11.774]")
        self.modelBuilder.doVar("B_tot[10212.058]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-4014.900]")
        self.modelBuilder.doVar("B_decay[4029850.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.009]")
        self.modelBuilder.doVar("B_0p0_15p0[1.730]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.018]")
        self.modelBuilder.doVar("B_15p0_30p0[4.128]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.046]")
        self.modelBuilder.doVar("B_30p0_45p0[6.781]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.092]")
        self.modelBuilder.doVar("B_45p0_80p0[6.979]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.164]")
        self.modelBuilder.doVar("B_80p0_120p0[14.523]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.206]")
        self.modelBuilder.doVar("B_120p0_200p0[17.360]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.113]")
        self.modelBuilder.doVar("B_200p0_350p0[24.630]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.268]")
        self.modelBuilder.doVar("B_350p0_10000p0[84.513]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.0005,0.0015]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chb"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chb_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chb_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chb_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chb_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chb_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chb_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chb_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chb_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chb_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chb_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chb_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chb_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chb_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chb_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chb_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chb_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chb_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chb_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chb_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chb_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chb_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chb_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chb_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chb_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chb_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chb_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chb_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chb_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chb_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chb_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chb_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chb_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chw(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 10.000

        self.modelBuilder.doVar("A_tot[-0.256]")
        self.modelBuilder.doVar("B_tot[18.512]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-130.861]")
        self.modelBuilder.doVar("B_decay[4281.170]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.015]")
        self.modelBuilder.doVar("B_0p0_15p0[0.072]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.035]")
        self.modelBuilder.doVar("B_15p0_30p0[0.118]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.071]")
        self.modelBuilder.doVar("B_30p0_45p0[0.236]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.134]")
        self.modelBuilder.doVar("B_45p0_80p0[0.506]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.251]")
        self.modelBuilder.doVar("B_80p0_120p0[1.114]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.314]")
        self.modelBuilder.doVar("B_120p0_200p0[1.869]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.409]")
        self.modelBuilder.doVar("B_200p0_350p0[4.368]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.458]")
        self.modelBuilder.doVar("B_350p0_10000p0[11.918]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.05,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chw"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chw_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chw_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chw_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chw_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chw_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chw_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chw_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chw_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chw_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chw_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chw_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chw_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chw_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chw_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chw_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chw_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chw_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chw_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chw_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chw_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chw_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chw_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chw_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chw_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chw_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chw_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chw_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chw_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chw_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chw_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chw_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chw_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chwb(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[2.534]")
        self.modelBuilder.doVar("B_tot[3827.506]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[2230.440]")
        self.modelBuilder.doVar("B_decay[1243720.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.048]")
        self.modelBuilder.doVar("B_0p0_15p0[1.359]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.129]")
        self.modelBuilder.doVar("B_15p0_30p0[2.911]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.232]")
        self.modelBuilder.doVar("B_30p0_45p0[4.878]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.428]")
        self.modelBuilder.doVar("B_45p0_80p0[7.838]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.697]")
        self.modelBuilder.doVar("B_80p0_120p0[15.509]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.770]")
        self.modelBuilder.doVar("B_120p0_200p0[21.844]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.694]")
        self.modelBuilder.doVar("B_200p0_350p0[35.438]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.748]")
        self.modelBuilder.doVar("B_350p0_10000p0[97.423]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.003,0.002]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chwb"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chwb_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chwb_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chwb_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chwb_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chwb_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chwb_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chwb_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chwb_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chwb_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chwb_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chwb_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chwb_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chwb_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chwb_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chwb_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chwb_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chwb_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chwb_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chwb_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chwb_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chwb_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chwb_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chwb_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chwb_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chwb_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chwb_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chwb_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chwb_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chwb_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chwb_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chwb_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chwb_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chbox(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 10.000

        self.modelBuilder.doVar("A_tot[1.111]")
        self.modelBuilder.doVar("B_tot[0.337]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[1.212]")
        self.modelBuilder.doVar("B_decay[0.367]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[1.212]")
        self.modelBuilder.doVar("B_0p0_15p0[0.370]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[1.212]")
        self.modelBuilder.doVar("B_15p0_30p0[0.370]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[1.212]")
        self.modelBuilder.doVar("B_30p0_45p0[0.371]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[1.212]")
        self.modelBuilder.doVar("B_45p0_80p0[0.370]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[1.212]")
        self.modelBuilder.doVar("B_80p0_120p0[0.370]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[1.212]")
        self.modelBuilder.doVar("B_120p0_200p0[0.371]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[1.212]")
        self.modelBuilder.doVar("B_200p0_350p0[0.369]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[1.212]")
        self.modelBuilder.doVar("B_350p0_10000p0[0.366]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chbox[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chbox_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chbox, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chbox"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chbox_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chbox_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chbox_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chbox_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chbox_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chbox_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chbox_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chbox_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chbox_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chbox_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chbox_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chbox_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chbox_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chbox_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chbox_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chbox_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chbox_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chbox_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chbox_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chbox_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chbox_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chbox_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chbox_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chbox_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chbox_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chbox_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chbox_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chbox_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chbox_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chbox_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chbox_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chbox_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chd(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[-0.055]")
        self.modelBuilder.doVar("B_tot[0.605]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-24.164]")
        self.modelBuilder.doVar("B_decay[145.979]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-0.014]")
        self.modelBuilder.doVar("B_0p0_15p0[44.619]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-0.031]")
        self.modelBuilder.doVar("B_15p0_30p0[6.151]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-0.046]")
        self.modelBuilder.doVar("B_30p0_45p0[10.679]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-0.098]")
        self.modelBuilder.doVar("B_45p0_80p0[20.489]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-0.237]")
        self.modelBuilder.doVar("B_80p0_120p0[83.994]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-0.394]")
        self.modelBuilder.doVar("B_120p0_200p0[194.699]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-0.340]")
        self.modelBuilder.doVar("B_200p0_350p0[361.402]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-1.179]")
        self.modelBuilder.doVar("B_350p0_10000p0[5823.196]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chd[0,-0.2,0.2]")
        self.modelBuilder.factory_("expr::ggh_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chd_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chd, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chd"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chd_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chd_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chd_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chd_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chd_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chd_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chd_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chd_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chd_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chd_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chd_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chd_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chd_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chd_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chd_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chd_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chd_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chd_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chd_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chd_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chd_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chd_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chd_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chd_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chd_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chd_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chd_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chd_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chd_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chd_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chd_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chd_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_chl3(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 10.000

        self.modelBuilder.doVar("A_tot[-1.415]")
        self.modelBuilder.doVar("B_tot[0.676]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-3.638]")
        self.modelBuilder.doVar("B_decay[3.308]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-1.223]")
        self.modelBuilder.doVar("B_0p0_15p0[0.385]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-1.239]")
        self.modelBuilder.doVar("B_15p0_30p0[0.401]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-1.264]")
        self.modelBuilder.doVar("B_30p0_45p0[0.432]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-1.315]")
        self.modelBuilder.doVar("B_45p0_80p0[0.471]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-1.390]")
        self.modelBuilder.doVar("B_80p0_120p0[0.574]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-1.408]")
        self.modelBuilder.doVar("B_120p0_200p0[0.594]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-1.383]")
        self.modelBuilder.doVar("B_200p0_350p0[0.557]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-1.374]")
        self.modelBuilder.doVar("B_350p0_10000p0[0.237]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chl3[0,-1,1]")
        self.modelBuilder.factory_("expr::ggh_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chl3_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chl3, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chl3"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_chl3_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_chl3_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_chl3_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_chl3_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_chl3_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_chl3_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_chl3_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_chl3_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_chl3_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_chl3_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_chl3_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_chl3_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_chl3_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_chl3_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_chl3_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_chl3_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_chl3_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_chl3_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_chl3_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_chl3_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_chl3_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_chl3_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_chl3_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_chl3_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_chl3_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_chl3_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_chl3_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_chl3_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_chl3_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_chl3_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_chl3_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_chl3_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_cll1(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[7.135]")
        self.modelBuilder.doVar("B_tot[17.993]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[18.188]")
        self.modelBuilder.doVar("B_decay[82.698]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[6.116]")
        self.modelBuilder.doVar("B_0p0_15p0[9.376]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[6.199]")
        self.modelBuilder.doVar("B_15p0_30p0[9.681]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[6.339]")
        self.modelBuilder.doVar("B_30p0_45p0[10.609]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[6.580]")
        self.modelBuilder.doVar("B_45p0_80p0[10.301]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[6.996]")
        self.modelBuilder.doVar("B_80p0_120p0[14.169]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[7.081]")
        self.modelBuilder.doVar("B_120p0_200p0[14.572]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[6.938]")
        self.modelBuilder.doVar("B_200p0_350p0[12.975]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[6.670]")
        self.modelBuilder.doVar("B_350p0_10000p0[-1.710]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cll1[0,-0.7,0.1]")
        self.modelBuilder.factory_("expr::ggh_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cll1_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cll1, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["cll1"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_cll1_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_cll1_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_cll1_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_cll1_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_cll1_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_cll1_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_cll1_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_cll1_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_cll1_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_cll1_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_cll1_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_cll1_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_cll1_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_cll1_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_cll1_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_cll1_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_cll1_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_cll1_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_cll1_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_cll1_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_cll1_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_cll1_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_cll1_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_cll1_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_cll1_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_cll1_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_cll1_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_cll1_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_cll1_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_cll1_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_cll1_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_cll1_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_ctbre(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 1000.000

        self.modelBuilder.doVar("A_tot[-4.747]")
        self.modelBuilder.doVar("B_tot[2637.037]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-2150.720]")
        self.modelBuilder.doVar("B_decay[1156400.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-0.004]")
        self.modelBuilder.doVar("B_0p0_15p0[11.453]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-0.003]")
        self.modelBuilder.doVar("B_15p0_30p0[3.489]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-0.006]")
        self.modelBuilder.doVar("B_30p0_45p0[8.879]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-0.013]")
        self.modelBuilder.doVar("B_45p0_80p0[24.243]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-0.036]")
        self.modelBuilder.doVar("B_80p0_120p0[52.588]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-0.074]")
        self.modelBuilder.doVar("B_120p0_200p0[130.159]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-0.167]")
        self.modelBuilder.doVar("B_200p0_350p0[376.836]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-0.484]")
        self.modelBuilder.doVar("B_350p0_10000p0[2022.820]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctbre[0,-0.001,0.003]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctbre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctbre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["ctbre"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_ctbre_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_ctbre_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_ctbre_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_ctbre_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_ctbre_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_ctbre_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_ctbre_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_ctbre_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_ctbre_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_ctbre_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_ctbre_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_ctbre_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_ctbre_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_ctbre_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_ctbre_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_ctbre_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_ctbre_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_ctbre_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_ctbre_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_ctbre_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_ctbre_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_ctbre_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_ctbre_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_ctbre_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_ctbre_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_ctbre_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_ctbre_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_ctbre_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_ctbre_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_ctbre_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_ctbre_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_ctbre_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_cthre(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[0.009]")
        self.modelBuilder.doVar("B_tot[0.007]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[3.447]")
        self.modelBuilder.doVar("B_decay[2.970]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-12.040]")
        self.modelBuilder.doVar("B_0p0_15p0[36.734]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-11.900]")
        self.modelBuilder.doVar("B_15p0_30p0[36.388]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-11.744]")
        self.modelBuilder.doVar("B_30p0_45p0[35.927]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-11.494]")
        self.modelBuilder.doVar("B_45p0_80p0[35.302]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-11.103]")
        self.modelBuilder.doVar("B_80p0_120p0[34.314]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-11.034]")
        self.modelBuilder.doVar("B_120p0_200p0[34.209]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-11.189]")
        self.modelBuilder.doVar("B_200p0_350p0[35.230]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-11.304]")
        self.modelBuilder.doVar("B_350p0_10000p0[36.237]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("cthre[0,-0.8,0.4]")
        self.modelBuilder.factory_("expr::ggh_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_cthre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", cthre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["cthre"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_cthre_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_cthre_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_cthre_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_cthre_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_cthre_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_cthre_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_cthre_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_cthre_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_cthre_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_cthre_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_cthre_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_cthre_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_cthre_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_cthre_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_cthre_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_cthre_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_cthre_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_cthre_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_cthre_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_cthre_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_cthre_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_cthre_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_cthre_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_cthre_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_cthre_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_cthre_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_cthre_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_cthre_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_cthre_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_cthre_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_cthre_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_cthre_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

class SMEFT_ctwre(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # Scaled by factor 100.000

        self.modelBuilder.doVar("A_tot[-0.372]")
        self.modelBuilder.doVar("B_tot[9.499]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-115.159]")
        self.modelBuilder.doVar("B_decay[3315.370]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-0.008]")
        self.modelBuilder.doVar("B_0p0_15p0[3.168]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[-0.008]")
        self.modelBuilder.doVar("B_15p0_30p0[0.532]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[-0.018]")
        self.modelBuilder.doVar("B_30p0_45p0[1.729]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-0.047]")
        self.modelBuilder.doVar("B_45p0_80p0[3.530]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-0.143]")
        self.modelBuilder.doVar("B_80p0_120p0[15.738]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-0.234]")
        self.modelBuilder.doVar("B_120p0_200p0[124.324]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[-0.531]")
        self.modelBuilder.doVar("B_200p0_350p0[95.980]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[-1.311]")
        self.modelBuilder.doVar("B_350p0_10000p0[716.012]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("ctwre[0,-0.03,0.05]")
        self.modelBuilder.factory_("expr::ggh_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_ctwre_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", ctwre, A_350p0_10000p0, B_350p0_10000p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["ctwre"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)

        if 'ggh_PTH_0p0_15p0_in' in process: poi = 'ggh_scaling_ctwre_0p0_15p0'
        elif 'tth_PTH_0p0_15p0_in' in process: poi = 'tth_scaling_ctwre_0p0_15p0'
        elif 'vbf_PTH_0p0_15p0_in' in process: poi = 'vbf_scaling_ctwre_0p0_15p0'
        elif 'vh_PTH_0p0_15p0_in' in process: poi = 'vh_scaling_ctwre_0p0_15p0'

        elif 'ggh_PTH_15p0_30p0_in' in process: poi = 'ggh_scaling_ctwre_15p0_30p0'
        elif 'tth_PTH_15p0_30p0_in' in process: poi = 'tth_scaling_ctwre_15p0_30p0'
        elif 'vbf_PTH_15p0_30p0_in' in process: poi = 'vbf_scaling_ctwre_15p0_30p0'
        elif 'vh_PTH_15p0_30p0_in' in process: poi = 'vh_scaling_ctwre_15p0_30p0'

        elif 'ggh_PTH_30p0_45p0_in' in process: poi = 'ggh_scaling_ctwre_30p0_45p0'
        elif 'tth_PTH_30p0_45p0_in' in process: poi = 'tth_scaling_ctwre_30p0_45p0'
        elif 'vbf_PTH_30p0_45p0_in' in process: poi = 'vbf_scaling_ctwre_30p0_45p0'
        elif 'vh_PTH_30p0_45p0_in' in process: poi = 'vh_scaling_ctwre_30p0_45p0'

        elif 'ggh_PTH_45p0_80p0_in' in process: poi = 'ggh_scaling_ctwre_45p0_80p0'
        elif 'tth_PTH_45p0_80p0_in' in process: poi = 'tth_scaling_ctwre_45p0_80p0'
        elif 'vbf_PTH_45p0_80p0_in' in process: poi = 'vbf_scaling_ctwre_45p0_80p0'
        elif 'vh_PTH_45p0_80p0_in' in process: poi = 'vh_scaling_ctwre_45p0_80p0'

        elif 'ggh_PTH_80p0_120p0_in' in process: poi = 'ggh_scaling_ctwre_80p0_120p0'
        elif 'tth_PTH_80p0_120p0_in' in process: poi = 'tth_scaling_ctwre_80p0_120p0'
        elif 'vbf_PTH_80p0_120p0_in' in process: poi = 'vbf_scaling_ctwre_80p0_120p0'
        elif 'vh_PTH_80p0_120p0_in' in process: poi = 'vh_scaling_ctwre_80p0_120p0'

        elif 'ggh_PTH_120p0_200p0_in' in process: poi = 'ggh_scaling_ctwre_120p0_200p0'
        elif 'tth_PTH_120p0_200p0_in' in process: poi = 'tth_scaling_ctwre_120p0_200p0'
        elif 'vbf_PTH_120p0_200p0_in' in process: poi = 'vbf_scaling_ctwre_120p0_200p0'
        elif 'vh_PTH_120p0_200p0_in' in process: poi = 'vh_scaling_ctwre_120p0_200p0'

        elif 'ggh_PTH_200p0_350p0_in' in process: poi = 'ggh_scaling_ctwre_200p0_350p0'
        elif 'tth_PTH_200p0_350p0_in' in process: poi = 'tth_scaling_ctwre_200p0_350p0'
        elif 'vbf_PTH_200p0_350p0_in' in process: poi = 'vbf_scaling_ctwre_200p0_350p0'
        elif 'vh_PTH_200p0_350p0_in' in process: poi = 'vh_scaling_ctwre_200p0_350p0'

        elif 'ggh_PTH_350p0_10000p0_in' in process: poi = 'ggh_scaling_ctwre_350p0_10000p0'
        elif 'tth_PTH_350p0_10000p0_in' in process: poi = 'tth_scaling_ctwre_350p0_10000p0'
        elif 'vbf_PTH_350p0_10000p0_in' in process: poi = 'vbf_scaling_ctwre_350p0_10000p0'
        elif 'vh_PTH_350p0_10000p0_in' in process: poi = 'vh_scaling_ctwre_350p0_10000p0'

        else: poi = 1

        print('Will scale ', string, ' by ', poi)

        return poi

smeft_chg = SMEFT_chg()
smeft_chg_individual = SMEFT_chg_individual_bins()
smeft_chb = SMEFT_chb()
smeft_chb_individual = SMEFT_chb_individual_bins()
smeft_chw = SMEFT_chw()
smeft_chw_individual = SMEFT_chw_individual_bins()
smeft_chwb = SMEFT_chwb()
smeft_chwb_individual = SMEFT_chwb_individual_bins()
smeft_chbox = SMEFT_chbox()
smeft_chbox_individual = SMEFT_chbox_individual_bins()
smeft_chd = SMEFT_chd()
smeft_chd_individual = SMEFT_chd_individual_bins()
smeft_chl3 = SMEFT_chl3()
smeft_chl3_individual = SMEFT_chl3_individual_bins()
smeft_cll1 = SMEFT_cll1()
smeft_cll1_individual = SMEFT_cll1_individual_bins()
smeft_ctbre = SMEFT_ctbre()
smeft_ctbre_individual = SMEFT_ctbre_individual_bins()
smeft_cthre = SMEFT_cthre()
smeft_cthre_individual = SMEFT_cthre_individual_bins()
smeft_ctwre = SMEFT_ctwre()
smeft_ctwre_individual = SMEFT_ctwre_individual_bins()
