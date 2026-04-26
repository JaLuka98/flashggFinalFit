from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

# The values contained in this file correspond to parametrization 1 of v2.

class SMEFT_chg(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        self.modelBuilder.doVar("A_tot[3.2321440588070733]")
        self.modelBuilder.doVar("B_tot[36.08012882940807]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[0.000]")
        self.modelBuilder.doVar("B_decay[0.000]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[36.1549119811163]")
        self.modelBuilder.doVar("B_0p0_15p0[358.50849793875545]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[39.3193063219607]")
        self.modelBuilder.doVar("B_15p0_30p0[423.66635645843076]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[36.67866663971999]")
        self.modelBuilder.doVar("B_30p0_45p0[364.7504217917983]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[40.75844283333928]")
        self.modelBuilder.doVar("B_45p0_80p0[488.621471552114]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[34.52011616353232]")
        self.modelBuilder.doVar("B_80p0_120p0[344.2811404553864]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[11.71296235826623]")
        self.modelBuilder.doVar("B_120p0_200p0[253.5236415605519]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[32.53110866567134]")
        self.modelBuilder.doVar("B_200p0_350p0[327.3260641502254]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[38.139215360822796]")
        self.modelBuilder.doVar("B_350p0_10000p0[392.1679145359597]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
        self.modelBuilder.factory_("expr::ggh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chg[0,-0.025,0.025]")
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


smeft_chg = SMEFT_chg()
