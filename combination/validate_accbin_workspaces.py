#!/usr/bin/env python3
"""Read-only checks of rebuilt combined workspaces against cards and old yields."""
import argparse
import gc
import json
import math
import re
from pathlib import Path

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
REPO = Path(__file__).resolve().parents[1]
SOURCES = [f"CMS_HIG25015_{s}_accMatrix" for s in ("QCDscale", "pdf", "alphaS")]


def yields(w):
    found = {}
    for f in w.allFunctions():
        match = re.match(r"n_exp(_final)?_bin(.+)_proc_(.+)$", f.GetName())
        if match:
            key = (match[2], match[3])
            if key not in found or match[1]:
                found[key] = f
    return found


def nominal(path):
    f = ROOT.TFile.Open(str(path))
    assert f and not f.IsZombie(), path
    w = f.Get("w")
    assert w, path
    result = {k: v.getVal() for k, v in yields(w).items()}
    f.Close()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--obs", required=True)
    args = parser.parse_args()
    obs = args.obs
    old = REPO / ("output_asimov_inclusive_HggH4l" if obs == "inclusive" else f"output_combination_{obs}")
    new = REPO / f"output_combination_accbin_{obs}"
    reference = nominal(old / "workspaces" / f"Datacard_{obs}_comb.root")
    gc.collect()
    f = ROOT.TFile.Open(str(new / "workspaces" / f"Datacard_{obs}_comb.root"))
    assert f and not f.IsZombie()
    w = f.Get("w")
    assert w and abs(w.var("MH").getVal() - 125.07) < 1e-6
    assert not w.obj("ModelConfig").GetParametersOfInterest().find("MH"), "MH must not be a POI"
    functions = yields(w)
    assert set(functions) == set(reference), "different expected-yield inventory"
    values = {k: v.getVal() for k, v in functions.items()}
    for key, value in values.items():
        assert math.isfinite(value), (key, value)
        assert math.isclose(value, reference[key], rel_tol=1e-9, abs_tol=1e-9), (key, value, reference[key])
    negative = {"/".join(k): v for k, v in values.items() if v < 0}
    channel_totals = {}
    for (channel, process), value in values.items():
        channel_totals[channel] = channel_totals.get(channel, 0.0) + value
    assert all(v >= 0 for v in channel_totals.values()), "negative nominal integrated channel yield"
    lines = [x.split() for x in (new / "cards" / f"Datacard_{obs}_comb.txt").read_text().splitlines() if x.strip()]
    ps = next(x[1:] for x in lines if x[0] == "process" and not x[1].lstrip("-").isdigit())
    bs = next(x[1:] for x in lines if x[0] == "bin" and len(x) == len(ps) + 1)
    checks = {}
    for name in SOURCES:
        row = next(x[2:] for x in lines if x[0] == name)
        factors = dict(zip(zip(bs, ps), row))
        nuisance = w.var(name)
        assert nuisance and abs(nuisance.getVal()) < 1e-10
        worst = 0.0
        for direction in (-1, 1):
            nuisance.setVal(direction)
            for key, function in functions.items():
                if values[key] == 0:
                    continue
                factor = factors[key]
                expected = 1.0
                if factor != "-":
                    pair = [float(x) for x in factor.split("/")]
                    expected = pair[0 if direction == -1 else 1] if len(pair) == 2 else pair[0] ** direction
                    # ProcessNormalization::addAsymmLogNormal uses this exact
                    # simplification for nearly reciprocal pairs.
                    if len(pair) == 2 and abs(pair[0] * pair[1] - 1) < 1e-5:
                        expected = pair[1] ** direction
                ratio = function.getVal() / values[key]
                worst = max(worst, abs(ratio - expected))
                assert math.isclose(ratio, expected, rel_tol=1e-8, abs_tol=1e-8), (name, key, direction, ratio, expected)
            nuisance.setVal(0)
        checks[name] = worst
    result = {"observable": obs, "nominal_yields_compared": len(values), "nominal_yields_unchanged": True,
              "MH_constant_in_workspace": bool(w.var("MH").isConstant()),
              "MH_not_POI": True, "MH": w.var("MH").getVal(),
              "pois": [p.GetName() for p in w.obj("ModelConfig").GetParametersOfInterest()],
              "preexisting_negative_process_yields": negative,
              "nominal_integrated_channel_yields_nonnegative": True,
              "max_abs_response_error": checks}
    f.Close()
    (new / "workspace_validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
