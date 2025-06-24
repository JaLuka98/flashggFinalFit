from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

class SMEFT_chg_individual_bins(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("A_0p0_15p0[15.08]")
        self.modelBuilder.doVar("B_0p0_15p0[172.55]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True) 
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[14.90]")
        self.modelBuilder.doVar("B_15p0_30p0[170.79]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True) 
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[14.67]")
        self.modelBuilder.doVar("B_30p0_45p0[169.88]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True) 
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)
        
        self.modelBuilder.doVar("A_45p0_80p0[14.34]")
        self.modelBuilder.doVar("B_45p0_80p0[166.02]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True) 
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[13.71]")
        self.modelBuilder.doVar("B_80p0_120p0[158.92]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True) 
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[13.57]")
        self.modelBuilder.doVar("B_120p0_200p0[158.15]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True) 
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[14.24]")
        self.modelBuilder.doVar("B_200p0_350p0[185.32]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True) 
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[18.78]")
        self.modelBuilder.doVar("B_350p0_10000p0[351.12]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True) 
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        # First approximation
        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg(\"1+@1*@0+@2*@0*@0\", chg, A_0p0_15p0, B_0p0_15p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg(\"1+@1*@0+@2*@0*@0\", chg, A_0p0_15p0, B_0p0_15p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg(\"1+@1*@0+@2*@0*@0\", chg, A_0p0_15p0, B_0p0_15p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg(\"1+@1*@0+@2*@0*@0\", chg, A_0p0_15p0, B_0p0_15p0)")

        self.modelBuilder.doVar("chg_15p0_30p0[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_15p0_30p0(\"1+@1*@0+@2*@0*@0\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_15p0_30p0(\"1+@1*@0+@2*@0*@0\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_15p0_30p0(\"1+@1*@0+@2*@0*@0\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_15p0_30p0(\"1+@1*@0+@2*@0*@0\", chg_15p0_30p0, A_15p0_30p0, B_15p0_30p0)")

        self.modelBuilder.doVar("chg_30p0_45p0[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_30p0_45p0(\"1+@1*@0+@2*@0*@0\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_30p0_45p0(\"1+@1*@0+@2*@0*@0\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_30p0_45p0(\"1+@1*@0+@2*@0*@0\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_30p0_45p0(\"1+@1*@0+@2*@0*@0\", chg_30p0_45p0, A_30p0_45p0, B_30p0_45p0)")

        self.modelBuilder.doVar("chg_45p0_80p0[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_45p0_80p0(\"1+@1*@0+@2*@0*@0\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_45p0_80p0(\"1+@1*@0+@2*@0*@0\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_45p0_80p0(\"1+@1*@0+@2*@0*@0\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_45p0_80p0(\"1+@1*@0+@2*@0*@0\", chg_45p0_80p0, A_45p0_80p0, B_45p0_80p0)")

        self.modelBuilder.doVar("chg_80p0_120p0[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_80p0_120p0(\"1+@1*@0+@2*@0*@0\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_80p0_120p0(\"1+@1*@0+@2*@0*@0\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_80p0_120p0(\"1+@1*@0+@2*@0*@0\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_80p0_120p0(\"1+@1*@0+@2*@0*@0\", chg_80p0_120p0, A_80p0_120p0, B_80p0_120p0)")

        self.modelBuilder.doVar("chg_120p0_200p0[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_120p0_200p0(\"1+@1*@0+@2*@0*@0\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_120p0_200p0(\"1+@1*@0+@2*@0*@0\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_120p0_200p0(\"1+@1*@0+@2*@0*@0\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_120p0_200p0(\"1+@1*@0+@2*@0*@0\", chg_120p0_200p0, A_120p0_200p0, B_120p0_200p0)")

        self.modelBuilder.doVar("chg_200p0_350p0[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_200p0_350p0(\"1+@1*@0+@2*@0*@0\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_200p0_350p0(\"1+@1*@0+@2*@0*@0\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_200p0_350p0(\"1+@1*@0+@2*@0*@0\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_200p0_350p0(\"1+@1*@0+@2*@0*@0\", chg_200p0_350p0, A_200p0_350p0, B_200p0_350p0)")

        self.modelBuilder.doVar("chg_350p0_10000p0[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_350p0_10000p0(\"1+@1*@0+@2*@0*@0\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_350p0_10000p0(\"1+@1*@0+@2*@0*@0\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_350p0_10000p0(\"1+@1*@0+@2*@0*@0\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_350p0_10000p0(\"1+@1*@0+@2*@0*@0\", chg_350p0_10000p0, A_350p0_10000p0, B_350p0_10000p0)")

        self.modelBuilder.doSet("POI", ",".join(["chg", "chg_15p0_30p0", "chg_30p0_45p0",
                                                  "chg_45p0_80p0", "chg_80p0_120p0", "chg_120p0_200p0",
                                                  "chg_200p0_350p0", "chg_350p0_10000p0"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)
        
        if "ggh_PTH_0p0_15p0_in" in process: poi = "ggh_scaling_chg"
        elif "tth_PTH_0p0_15p0_in" in process: poi = "tth_scaling_chg"
        elif "vbf_PTH_0p0_15p0_in" in process: poi = "vbf_scaling_chg"
        elif "vh_PTH_0p0_15p0_in" in process: poi = "vh_scaling_chg"

        elif "ggh_PTH_15p0_30p0_in" in process: poi = "ggh_scaling_chg_15p0_30p0"
        elif "tth_PTH_15p0_30p0_in" in process: poi = "tth_scaling_chg_15p0_30p0"
        elif "vbf_PTH_15p0_30p0_in" in process: poi = "vbf_scaling_chg_15p0_30p0"
        elif "vh_PTH_15p0_30p0_in" in process: poi = "vh_scaling_chg_15p0_30p0"

        elif "ggh_PTH_30p0_45p0_in" in process: poi = "ggh_scaling_chg_30p0_45p0"
        elif "tth_PTH_30p0_45p0_in" in process: poi = "tth_scaling_chg_30p0_45p0"
        elif "vbf_PTH_30p0_45p0_in" in process: poi = "vbf_scaling_chg_30p0_45p0"
        elif "vh_PTH_30p0_45p0_in" in process: poi = "vh_scaling_chg_30p0_45p0"

        elif "ggh_PTH_45p0_80p0_in" in process: poi = "ggh_scaling_chg_45p0_80p0"
        elif "tth_PTH_45p0_80p0_in" in process: poi = "tth_scaling_chg_45p0_80p0"
        elif "vbf_PTH_45p0_80p0_in" in process: poi = "vbf_scaling_chg_45p0_80p0"
        elif "vh_PTH_45p0_80p0_in" in process: poi = "vh_scaling_chg_45p0_80p0"

        elif "ggh_PTH_80p0_120p0_in" in process: poi = "ggh_scaling_chg_80p0_120p0"
        elif "tth_PTH_80p0_120p0_in" in process: poi = "tth_scaling_chg_80p0_120p0"
        elif "vbf_PTH_80p0_120p0_in" in process: poi = "vbf_scaling_chg_80p0_120p0"
        elif "vh_PTH_80p0_120p0_in" in process: poi = "vh_scaling_chg_80p0_120p0"

        elif "ggh_PTH_120p0_200p0_in" in process: poi = "ggh_scaling_chg_120p0_200p0"
        elif "tth_PTH_120p0_200p0_in" in process: poi = "tth_scaling_chg_120p0_200p0"
        elif "vbf_PTH_120p0_200p0_in" in process: poi = "vbf_scaling_chg_120p0_200p0"
        elif "vh_PTH_120p0_200p0_in" in process: poi = "vh_scaling_chg_120p0_200p0"

        elif "ggh_PTH_200p0_350p0_in" in process: poi = "ggh_scaling_chg_200p0_350p0"
        elif "tth_PTH_200p0_350p0_in" in process: poi = "tth_scaling_chg_200p0_350p0"
        elif "vbf_PTH_200p0_350p0_in" in process: poi = "vbf_scaling_chg_200p0_350p0"
        elif "vh_PTH_200p0_350p0_in" in process: poi = "vh_scaling_chg_200p0_350p0"

        elif "ggh_PTH_350p0_10000p0_in" in process: poi = "ggh_scaling_chg_350p0_10000p0"
        elif "tth_PTH_350p0_10000p0_in" in process: poi = "tth_scaling_chg_350p0_10000p0"
        elif "vbf_PTH_350p0_10000p0_in" in process: poi = "vbf_scaling_chg_350p0_10000p0"
        elif "vh_PTH_350p0_10000p0_in" in process: poi = "vh_scaling_chg_350p0_10000p0"

        else: poi = 1
        
        print("Will scale ", string, " by ", poi)
        
        return poi


class SMEFT_chg(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        
        self.modelBuilder.doVar("A_tot[3.232]")
        self.modelBuilder.doVar("B_tot[36.08]")
        self.modelBuilder.out.var("A_tot").setConstant(True) 
        self.modelBuilder.out.var("B_tot").setConstant(True) 

        self.modelBuilder.doVar("A_0p0_15p0[15.08]")
        self.modelBuilder.doVar("B_0p0_15p0[172.55]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True) 
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[14.90]")
        self.modelBuilder.doVar("B_15p0_30p0[170.79]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True) 
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[14.67]")
        self.modelBuilder.doVar("B_30p0_45p0[169.88]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True) 
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)
        
        self.modelBuilder.doVar("A_45p0_80p0[14.34]")
        self.modelBuilder.doVar("B_45p0_80p0[166.02]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True) 
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[13.71]")
        self.modelBuilder.doVar("B_80p0_120p0[158.92]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True) 
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[13.57]")
        self.modelBuilder.doVar("B_120p0_200p0[158.15]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True) 
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[14.24]")
        self.modelBuilder.doVar("B_200p0_350p0[185.32]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True) 
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[18.78]")
        self.modelBuilder.doVar("B_350p0_10000p0[351.12]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True) 
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        # First approximation
        self.modelBuilder.doVar("chg[0,-0.2,0.2]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chg_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chg, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chg"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)
        
        if "ggh_PTH_0p0_15p0_in" in process: poi = "ggh_scaling_chg_0p0_15p0"
        elif "tth_PTH_0p0_15p0_in" in process: poi = "tth_scaling_chg_0p0_15p0"
        elif "vbf_PTH_0p0_15p0_in" in process: poi = "vbf_scaling_chg_0p0_15p0"
        elif "vh_PTH_0p0_15p0_in" in process: poi = "vh_scaling_chg_0p0_15p0"

        elif "ggh_PTH_15p0_30p0_in" in process: poi = "ggh_scaling_chg_15p0_30p0"
        elif "tth_PTH_15p0_30p0_in" in process: poi = "tth_scaling_chg_15p0_30p0"
        elif "vbf_PTH_15p0_30p0_in" in process: poi = "vbf_scaling_chg_15p0_30p0"
        elif "vh_PTH_15p0_30p0_in" in process: poi = "vh_scaling_chg_15p0_30p0"

        elif "ggh_PTH_30p0_45p0_in" in process: poi = "ggh_scaling_chg_30p0_45p0"
        elif "tth_PTH_30p0_45p0_in" in process: poi = "tth_scaling_chg_30p0_45p0"
        elif "vbf_PTH_30p0_45p0_in" in process: poi = "vbf_scaling_chg_30p0_45p0"
        elif "vh_PTH_30p0_45p0_in" in process: poi = "vh_scaling_chg_30p0_45p0"

        elif "ggh_PTH_45p0_80p0_in" in process: poi = "ggh_scaling_chg_45p0_80p0"
        elif "tth_PTH_45p0_80p0_in" in process: poi = "tth_scaling_chg_45p0_80p0"
        elif "vbf_PTH_45p0_80p0_in" in process: poi = "vbf_scaling_chg_45p0_80p0"
        elif "vh_PTH_45p0_80p0_in" in process: poi = "vh_scaling_chg_45p0_80p0"

        elif "ggh_PTH_80p0_120p0_in" in process: poi = "ggh_scaling_chg_80p0_120p0"
        elif "tth_PTH_80p0_120p0_in" in process: poi = "tth_scaling_chg_80p0_120p0"
        elif "vbf_PTH_80p0_120p0_in" in process: poi = "vbf_scaling_chg_80p0_120p0"
        elif "vh_PTH_80p0_120p0_in" in process: poi = "vh_scaling_chg_80p0_120p0"

        elif "ggh_PTH_120p0_200p0_in" in process: poi = "ggh_scaling_chg_120p0_200p0"
        elif "tth_PTH_120p0_200p0_in" in process: poi = "tth_scaling_chg_120p0_200p0"
        elif "vbf_PTH_120p0_200p0_in" in process: poi = "vbf_scaling_chg_120p0_200p0"
        elif "vh_PTH_120p0_200p0_in" in process: poi = "vh_scaling_chg_120p0_200p0"

        elif "ggh_PTH_200p0_350p0_in" in process: poi = "ggh_scaling_chg_200p0_350p0"
        elif "tth_PTH_200p0_350p0_in" in process: poi = "tth_scaling_chg_200p0_350p0"
        elif "vbf_PTH_200p0_350p0_in" in process: poi = "vbf_scaling_chg_200p0_350p0"
        elif "vh_PTH_200p0_350p0_in" in process: poi = "vh_scaling_chg_200p0_350p0"

        elif "ggh_PTH_350p0_10000p0_in" in process: poi = "ggh_scaling_chg_350p0_10000p0"
        elif "tth_PTH_350p0_10000p0_in" in process: poi = "tth_scaling_chg_350p0_10000p0"
        elif "vbf_PTH_350p0_10000p0_in" in process: poi = "vbf_scaling_chg_350p0_10000p0"
        elif "vh_PTH_350p0_10000p0_in" in process: poi = "vh_scaling_chg_350p0_10000p0"

        else: poi = 1
        
        print("Will scale ", string, " by ", poi)
        
        return poi

class SMEFT_chw(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        # Scaled by factor 10

        self.modelBuilder.doVar("A_tot[-0.255]")
        self.modelBuilder.doVar("B_tot[18.51]")
        self.modelBuilder.out.var("A_tot").setConstant(True) 
        self.modelBuilder.out.var("B_tot").setConstant(True) 

        self.modelBuilder.doVar("A_0p0_15p0[0.0145]")
        self.modelBuilder.doVar("B_0p0_15p0[0.0724]")
        self.modelBuilder.out.var("A_0p0_15p0").setConstant(True) 
        self.modelBuilder.out.var("B_0p0_15p0").setConstant(True)

        self.modelBuilder.doVar("A_15p0_30p0[0.0354]")
        self.modelBuilder.doVar("B_15p0_30p0[0.118]")
        self.modelBuilder.out.var("A_15p0_30p0").setConstant(True) 
        self.modelBuilder.out.var("B_15p0_30p0").setConstant(True)

        self.modelBuilder.doVar("A_30p0_45p0[0.0707]")
        self.modelBuilder.doVar("B_30p0_45p0[0.236]")
        self.modelBuilder.out.var("A_30p0_45p0").setConstant(True) 
        self.modelBuilder.out.var("B_30p0_45p0").setConstant(True)
        
        self.modelBuilder.doVar("A_45p0_80p0[0.134]")
        self.modelBuilder.doVar("B_45p0_80p0[0.51]")
        self.modelBuilder.out.var("A_45p0_80p0").setConstant(True) 
        self.modelBuilder.out.var("B_45p0_80p0").setConstant(True)

        self.modelBuilder.doVar("A_80p0_120p0[0.251]")
        self.modelBuilder.doVar("B_80p0_120p0[1.11]")
        self.modelBuilder.out.var("A_80p0_120p0").setConstant(True) 
        self.modelBuilder.out.var("B_80p0_120p0").setConstant(True)

        self.modelBuilder.doVar("A_120p0_200p0[0.314]")
        self.modelBuilder.doVar("B_120p0_200p0[1.87]")
        self.modelBuilder.out.var("A_120p0_200p0").setConstant(True) 
        self.modelBuilder.out.var("B_120p0_200p0").setConstant(True)

        self.modelBuilder.doVar("A_200p0_350p0[0.409]")
        self.modelBuilder.doVar("B_200p0_350p0[4.37]")
        self.modelBuilder.out.var("A_200p0_350p0").setConstant(True) 
        self.modelBuilder.out.var("B_200p0_350p0").setConstant(True)

        self.modelBuilder.doVar("A_350p0_10000p0[0.458]")
        self.modelBuilder.doVar("B_350p0_10000p0[11.92]")
        self.modelBuilder.out.var("A_350p0_10000p0").setConstant(True) 
        self.modelBuilder.out.var("B_350p0_10000p0").setConstant(True)

        # First approximation
        self.modelBuilder.doVar("chw[0,-0.5,0.5]")
        self.modelBuilder.factory_( "expr::ggh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_0p0_15p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_0p0_15p0, B_0p0_15p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_15p0_30p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_15p0_30p0, B_15p0_30p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_30p0_45p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_30p0_45p0, B_30p0_45p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_45p0_80p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_45p0_80p0, B_45p0_80p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_80p0_120p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_80p0_120p0, B_80p0_120p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_120p0_200p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_120p0_200p0, B_120p0_200p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_200p0_350p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_200p0_350p0, B_200p0_350p0, A_tot, B_tot)")

        self.modelBuilder.factory_( "expr::ggh_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::tth_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)") 
        self.modelBuilder.factory_( "expr::vbf_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)")
        self.modelBuilder.factory_( "expr::vh_scaling_chw_350p0_10000p0(\"(1+@1*@0+@2*@0*@0) * (1 / (1 + @3*@0 + @4*@0*@0))\", chw, A_350p0_10000p0, B_350p0_10000p0, A_tot, B_tot)")

        self.modelBuilder.doSet("POI", ",".join(["chw"]))

    def getYieldScale(self, bin, process):
        string = "%s/%s" % (bin, process)
        
        if "ggh_PTH_0p0_15p0_in" in process: poi = "ggh_scaling_chw_0p0_15p0"
        elif "tth_PTH_0p0_15p0_in" in process: poi = "tth_scaling_chw_0p0_15p0"
        elif "vbf_PTH_0p0_15p0_in" in process: poi = "vbf_scaling_chw_0p0_15p0"
        elif "vh_PTH_0p0_15p0_in" in process: poi = "vh_scaling_chw_0p0_15p0"

        elif "ggh_PTH_15p0_30p0_in" in process: poi = "ggh_scaling_chw_15p0_30p0"
        elif "tth_PTH_15p0_30p0_in" in process: poi = "tth_scaling_chw_15p0_30p0"
        elif "vbf_PTH_15p0_30p0_in" in process: poi = "vbf_scaling_chw_15p0_30p0"
        elif "vh_PTH_15p0_30p0_in" in process: poi = "vh_scaling_chw_15p0_30p0"

        elif "ggh_PTH_30p0_45p0_in" in process: poi = "ggh_scaling_chw_30p0_45p0"
        elif "tth_PTH_30p0_45p0_in" in process: poi = "tth_scaling_chw_30p0_45p0"
        elif "vbf_PTH_30p0_45p0_in" in process: poi = "vbf_scaling_chw_30p0_45p0"
        elif "vh_PTH_30p0_45p0_in" in process: poi = "vh_scaling_chw_30p0_45p0"

        elif "ggh_PTH_45p0_80p0_in" in process: poi = "ggh_scaling_chw_45p0_80p0"
        elif "tth_PTH_45p0_80p0_in" in process: poi = "tth_scaling_chw_45p0_80p0"
        elif "vbf_PTH_45p0_80p0_in" in process: poi = "vbf_scaling_chw_45p0_80p0"
        elif "vh_PTH_45p0_80p0_in" in process: poi = "vh_scaling_chw_45p0_80p0"

        elif "ggh_PTH_80p0_120p0_in" in process: poi = "ggh_scaling_chw_80p0_120p0"
        elif "tth_PTH_80p0_120p0_in" in process: poi = "tth_scaling_chw_80p0_120p0"
        elif "vbf_PTH_80p0_120p0_in" in process: poi = "vbf_scaling_chw_80p0_120p0"
        elif "vh_PTH_80p0_120p0_in" in process: poi = "vh_scaling_chw_80p0_120p0"

        elif "ggh_PTH_120p0_200p0_in" in process: poi = "ggh_scaling_chw_120p0_200p0"
        elif "tth_PTH_120p0_200p0_in" in process: poi = "tth_scaling_chw_120p0_200p0"
        elif "vbf_PTH_120p0_200p0_in" in process: poi = "vbf_scaling_chw_120p0_200p0"
        elif "vh_PTH_120p0_200p0_in" in process: poi = "vh_scaling_chw_120p0_200p0"

        elif "ggh_PTH_200p0_350p0_in" in process: poi = "ggh_scaling_chw_200p0_350p0"
        elif "tth_PTH_200p0_350p0_in" in process: poi = "tth_scaling_chw_200p0_350p0"
        elif "vbf_PTH_200p0_350p0_in" in process: poi = "vbf_scaling_chw_200p0_350p0"
        elif "vh_PTH_200p0_350p0_in" in process: poi = "vh_scaling_chw_200p0_350p0"

        elif "ggh_PTH_350p0_10000p0_in" in process: poi = "ggh_scaling_chw_350p0_10000p0"
        elif "tth_PTH_350p0_10000p0_in" in process: poi = "tth_scaling_chw_350p0_10000p0"
        elif "vbf_PTH_350p0_10000p0_in" in process: poi = "vbf_scaling_chw_350p0_10000p0"
        elif "vh_PTH_350p0_10000p0_in" in process: poi = "vh_scaling_chw_350p0_10000p0"

        else: poi = 1
        
        print("Will scale ", string, " by ", poi)
        
        return poi

smeft_chg = SMEFT_chg()
smeft_chw = SMEFT_chw()
smeft_chg_individual = SMEFT_chg_individual_bins()