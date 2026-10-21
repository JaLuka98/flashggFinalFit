"""Layer 2: Trees2WS per-bin workspaces vs an independent uproot count of the input trees.

For one input sample and every gen bin of the table: the nominal RooDataSet and every systematic
RooDataHist (<syst>Up/Down01sigma) per category must have the sum of weights of the tree events with
that bin's diffVariable code (nominal tree, resp. the matching systematics tree).

usage: check_trees2ws.py <obs> <ws_dir: .../input_output_<obs>_<era>> <input tree file> <prod> <mass>
"""
import glob
import os
import sys

import numpy as np
import uproot
import ROOT

ROOT.gErrorIgnoreLevel = ROOT.kError
sys.path[:0] = [os.environ["WT"] + "/commonTools"]
from commonObjects import differentialProcTable_ as T  # noqa: E402

GENVAR = {"NJ": "GenNJ", "PTJ0": "GenPTJ0", "PTH": "GenPTH", "rapidity": "GenYH", "MassJ0J1": "GenMassJ0J1"}
obs, ws_dir, tree_file, prod, mass = sys.argv[1:6]
br = f"diffVariable_{GENVAR[obs]}"

# reference: sum of weights per (tree, code)
ref = {}
with uproot.open(tree_file) as f:
    for key in f.keys():
        if "RECO" not in key:
            continue
        name = key.split("/")[-1].split(";")[0]
        if not name.startswith(f"{prod}_{mass}_13TeV_"):
            continue
        a = f[key].arrays([br, "weight"], library="np")
        codes = a[br].astype(int)
        ref[name] = {c: float(a["weight"][codes == c].sum()) for c in np.unique(codes)}
trees = sorted(ref)
nominal = [t for t in trees if "01sigma" not in t]

n_checked, n_syst, problems, empty_ok = 0, 0, [], 0
for code, bin_name in T[obs]:
    files = glob.glob(f"{ws_dir}/ws_{prod}_{bin_name}/*M{mass}*_{prod}_{bin_name}.root")
    if len(files) != 1:
        problems.append(f"{bin_name}: {len(files)} workspace files")
        continue
    tf = ROOT.TFile.Open(files[0])
    ws = next(k.ReadObj() for d in [tf.Get(k.GetName()) for k in tf.GetListOfKeys()] for k in d.GetListOfKeys()
              if k.GetClassName() == "RooWorkspace")
    for t in trees:
        expected = ref[t].get(code, 0.0)
        obj = ws.data(t)
        if obj is None:
            if expected != 0.0:
                problems.append(f"{bin_name} {t}: missing in workspace, expected sumw {expected:.4g}")
            else:
                empty_ok += 1
            continue
        got = obj.sumEntries()
        n_checked += 1
        n_syst += "01sigma" in t
        scale = max(abs(expected), abs(got), 1e-12)
        if abs(got - expected) > 1e-6 * scale + 1e-9:
            problems.append(f"{bin_name} {t}: workspace sumw {got:.6g} vs trees {expected:.6g}")
    tf.Close()

print(f"{obs} {os.path.basename(ws_dir)} {prod} M{mass}: {len(T[obs])} bins x {len(trees)} datasets "
      f"({len(nominal)} nominal); {n_checked} compared ({n_syst} systematic) -> "
      f"{'OK' if not problems else str(len(problems)) + ' PROBLEMS'}")
for p in problems[:10]:
    print("   ", p)
