"""Layer 1: per-bin-out trees vs October trees (same events, out split per bin) and codes vs Linus' Gen definition."""
import sys, glob, os, re, json
import numpy as np, uproot
sys.path[:0] = [os.environ["WT"] + "/commonTools"]
from commonObjects import differentialProcTable_ as T

OCT, PBO = os.environ["OCT"], os.environ["PBO"]
GENVAR = {"NJ": "GenNJ", "PTJ0": "GenPTJ0", "PTH": "GenPTH", "rapidity": "GenYH", "MassJ0J1": "GenMassJ0J1"}
NEG = {"PTJ0", "MassJ0J1"}

def bounds(name):
    lo, hi = name.split("_")[1:3]
    f = lambda s: -float(s[1:].replace("p", ".")) if s.startswith("m") else float(s.replace("p", "."))
    return f(lo), f(hi)

def gen_code(obs, g, fid):
    """Linus' Gen-variable definition (with the sentinel guard), as a code per event; 0 = no bin."""
    out = np.zeros(len(g), dtype=int)
    for code, name in T[obs]:
        lo, hi = bounds(name)
        m = (g >= lo) & (g < hi) if obs in NEG else (g > -900) & (np.abs(g) >= lo) & (np.abs(g) < hi)
        m &= fid if name.endswith("_in") else ~fid
        assert not np.any(out[m]), f"{obs}: overlapping bins at {name}"
        out[m] = code
    return out

obs, year, sample = sys.argv[1:4]
br = f"diffVariable_{GENVAR[obs]}"
MCSUB = os.environ.get("MCSUB", "mc")  # mc, or mc_merged_cats for the merged-category trees
fo = glob.glob(f"{OCT}/{year}/{obs}/root/{MCSUB}/{sample}/*.root")[0]
fp = glob.glob(f"{PBO}/{year}/{obs}/root/{MCSUB}/{sample}/*.root")[0]
uo, up = uproot.open(fo), uproot.open(fp)
ko = sorted(k.split(";")[0] for k in uo.keys() if "RECO" in k)
kp = sorted(k.split(";")[0] for k in up.keys() if "RECO" in k)
assert ko == kp, f"tree lists differ: {set(ko) ^ set(kp)}"
table = dict(T[obs]); outs = {c for c, n in T[obs] if n.endswith("_out")}
problems, ntrees, nev, ngen, w0, wall = [], 0, 0, 0, 0.0, 0.0
for k in ko:
    a = uo[k].arrays(["weight", "CMS_hgg_mass", "fiducialGeometricFlag", br], library="np")
    b = up[k].arrays(["weight", "CMS_hgg_mass", "fiducialGeometricFlag", br], library="np")
    ntrees += 1; nev += len(a["weight"])
    if len(a["weight"]) != len(b["weight"]) or not (np.array_equal(a["weight"], b["weight"]) and np.array_equal(a["CMS_hgg_mass"], b["CMS_hgg_mass"])):
        problems.append(f"{k}: events differ"); continue
    ca, cb = a[br].astype(int), b[br].astype(int)
    same_in = (ca == cb) | np.isin(cb, list(outs))
    if not np.all(same_in): problems.append(f"{k}: in-codes changed for {np.sum(~same_in)} events")
    oct_out = ~np.isin(ca, [c for c, n in T[obs] if n.endswith("_in")]) & (ca != 0)
    if not np.array_equal(oct_out, np.isin(cb, list(outs))): problems.append(f"{k}: out events differ from October out code")
    # code 0 = no gen bin (e.g. no gen diphoton, GenPTH = -999): skipped by Trees2WS, as in October
    if not np.all(np.isin(cb, list(table) + [0])): problems.append(f"{k}: codes outside table {sorted(set(cb) - set(table) - {0})}")
    if "01sigma" not in k: w0 += b["weight"][cb == 0].sum(); wall += b["weight"].sum()
    if "01sigma" not in k:  # nominal trees carry the Gen variable: compare with Linus' definition
        g = up[k][GENVAR[obs]].array(library="np"); fid = b["fiducialGeometricFlag"].astype(bool)
        gc = gen_code(obs, g, fid); ngen += len(g)
        bad = gc != cb
        if np.any(bad):
            problems.append(f"{k}: {bad.sum()} events ({b['weight'][bad].sum()/b['weight'].sum():.2%} of weight) code != Gen definition, e.g. code {cb[bad][:3]} gen {g[bad][:3]} genbin {gc[bad][:3]}")
print(f"{obs} {year} {MCSUB}/{sample}: {ntrees} trees, {nev} events, {ngen} nominal events vs Gen definition, "
      f"code 0 (no gen bin) {w0 / max(wall, 1e-12):.2%} of nominal weight -> {'OK' if not problems else str(len(problems)) + ' PROBLEMS'}")
for p in problems[:8]: print("   ", p)
