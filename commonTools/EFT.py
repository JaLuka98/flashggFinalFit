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

class SMEFT_chb(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        self.modelBuilder.doVar("A_tot[-0.11774443348228512]")
        self.modelBuilder.doVar("B_tot[1.0212057849486498]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-40.149]")
        self.modelBuilder.doVar("B_decay[402.985]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[-0.00013943281575603525]")
        self.modelBuilder.doVar("B_0p0_15p0[0.0030141284716450694]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.001257690587480867]")
        self.modelBuilder.doVar("B_15p0_30p0[0.0018250016396488611]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.0010902759744111658]")
        self.modelBuilder.doVar("B_30p0_45p0[0.0015747508622578263]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[-0.00261847466154589]")
        self.modelBuilder.doVar("B_45p0_80p0[0.008069436095019826]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[-0.00042630709408068157]")
        self.modelBuilder.doVar("B_80p0_120p0[0.001989051324013865]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[-0.005120367533110182]")
        self.modelBuilder.doVar("B_120p0_200p0[0.005428217597565095]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.0015202124596857551]")
        self.modelBuilder.doVar("B_200p0_350p0[0.0032789818030076363]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.00018290558877253935]")
        self.modelBuilder.doVar("B_350p0_10000p0[0.0016192620215518673]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
        self.modelBuilder.factory_("expr::ggh_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chb[0,-0.01,0.0]")
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

        self.modelBuilder.doVar("A_tot[-0.025550148767896373]")
        self.modelBuilder.doVar("B_tot[0.1851187104182335]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[-13.0861]")
        self.modelBuilder.doVar("B_decay[42.8117]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.014318283317785632]")
        self.modelBuilder.doVar("B_0p0_15p0[0.006597608217699898]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.021429526545201662]")
        self.modelBuilder.doVar("B_15p0_30p0[0.01342091412405342]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.009657934836802976]")
        self.modelBuilder.doVar("B_30p0_45p0[0.005880153739643602]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.039847418438965276]")
        self.modelBuilder.doVar("B_45p0_80p0[0.041333366875400436]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.01770998976787197]")
        self.modelBuilder.doVar("B_80p0_120p0[0.00911133215124185]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.11375881835093729]")
        self.modelBuilder.doVar("B_120p0_200p0[0.3112391122753195]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.026372349184869272]")
        self.modelBuilder.doVar("B_200p0_350p0[0.013395007265575534]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.010586612786973985]")
        self.modelBuilder.doVar("B_350p0_10000p0[0.005811129739601167]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
        self.modelBuilder.factory_("expr::ggh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chw[0,-0.04,0.04]")
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

        self.modelBuilder.doVar("A_tot[0.025344581352730065]")
        self.modelBuilder.doVar("B_tot[0.3827505596435743]")
        self.modelBuilder.out.var("A_tot").setConstant(True)
        self.modelBuilder.out.var("B_tot").setConstant(True)

        self.modelBuilder.doVar("A_decay[22.3044]")
        self.modelBuilder.doVar("B_decay[124.372]")
        self.modelBuilder.out.var("A_decay").setConstant(True)
        self.modelBuilder.out.var("B_decay").setConstant(True)

        self.modelBuilder.doVar("A_0p0_15p0[0.005233334006389932]")
        self.modelBuilder.doVar("B_0p0_15p0[0.0016877501814499057]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True)
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.0031463808699535036]")
        self.modelBuilder.doVar("B_15p0_30p0[0.0021590959838748373]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True)
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.003934972068642826]")
        self.modelBuilder.doVar("B_30p0_45p0[0.001662440949474954]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True)
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)

        self.modelBuilder.doVar("A_45p0_80p0[0.0035907837865876277]")
        self.modelBuilder.doVar("B_45p0_80p0[0.006493308927387802]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True)
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.007495465360567925]")
        self.modelBuilder.doVar("B_80p0_120p0[0.001836857777421259]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True)
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.01594851463047807]")
        self.modelBuilder.doVar("B_120p0_200p0[0.023567281699061467]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True)
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.007597191467110918]")
        self.modelBuilder.doVar("B_200p0_350p0[0.002621484701213461]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True)
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.002824946319268347]")
        self.modelBuilder.doVar("B_350p0_10000p0[0.0008053832530384278]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True)
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_0p0_15p0, B_0p0_15p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_15p0_30p0, B_15p0_30p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_30p0_45p0, B_30p0_45p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_45p0_80p0, B_45p0_80p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_80p0_120p0, B_80p0_120p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_120p0_200p0, B_120p0_200p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
        self.modelBuilder.factory_("expr::ggh_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::tth_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vbf_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")
        self.modelBuilder.factory_("expr::vh_scaling_chwb_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * ((1 + @3*@0 + @4*@0*@0) / (1 + @5*@0 + @6*@0*@0))\", chwb, A_200p0_350p0, B_200p0_350p0, A_decay, B_decay, A_tot, B_tot)")

        self.modelBuilder.doVar("chwb[0,-0.02,0.02]")
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

smeft_chg = SMEFT_chg()
smeft_chb = SMEFT_chb()
smeft_chw = SMEFT_chw()
smeft_chwb = SMEFT_chwb()

