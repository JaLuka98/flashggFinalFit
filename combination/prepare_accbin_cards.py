#!/usr/bin/env python3
"""Prepare isolated AccBin cards from existing combination cards and audit changes.

Only Hgg entries in the three accMatrix rows change. H4l, all other nuisances,
rates, shapes and POI definitions are preserved. Does not run fits.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("acceptance", REPO / "Datacard/addAcceptanceUncertainties.py")
acc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acc)
OBS = {"inclusive": "PTH", "PTH": "PTH", "rapidity": "YH", "NJ": "NJ", "PTJ0": "PTJ0", "MassJ0J1": "MassJ0J1"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nuisance_rows(lines):
    return {t[0]: t[2:] for line in lines if len(t := line.split()) > 1 and t[1] == "lnN"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--observables", nargs="+", choices=OBS, default=list(OBS))
    args = parser.parse_args()
    proc_map = dict(x.split(":") for x in acc.DEFAULT_PROC_MAP.split(","))
    report = {"inputs": str(args.inputs.resolve()), "acceptance_prefix": "AccBin", "observables": {}}
    for obs in args.observables:
        old = REPO / ("output_asimov_inclusive_HggH4l" if obs == "inclusive" else f"output_combination_{obs}")
        out = REPO / f"output_combination_accbin_{obs}"
        inputs = {p: acc.load_acceptances(str(args.inputs / obs), OBS[obs], mode) for p, mode in proc_map.items()}
        info = {"files": {}, "cards": {}, "max_partition_residual": 0.0, "comparison": {}}
        for p, mode in proc_map.items():
            path = args.inputs / obs / f"fidXS_{OBS[obs]}_{mode}.py"
            info["files"][str(path)] = digest(path)
            a = inputs[p]
            for source in acc.SOURCES.values():
                for direction in ("up", "dn"):
                    varied = a[f"{source}_{direction}"]
                    kin, kout = varied / a["nom"], (1 - varied) / (1 - a["nom"])
                    residual = np.max(np.abs(a["nom"] * kin + (1 - a["nom"]) * kout - 1))
                    assert residual < 1e-12, "in/out partition does not conserve generated bin yield"
                    info["max_partition_residual"] = max(info["max_partition_residual"], float(residual))
        for channel in ("hgg", "h4l", "comb"):
            source = old / "cards" / f"Datacard_{obs}_{channel}.txt"
            lines, procs = acc.read_card(source)
            # These combination cards already use absolute shape paths. Refuse
            # relocation if any shape reference would change its meaning.
            for line in lines:
                t = line.split()
                if t and t[0] == "shapes":
                    if not Path(t[3]).is_absolute() or not Path(t[3]).exists():
                        raise ValueError(f"Cannot safely relocate shape reference: {line}")
            old_rows = nuisance_rows(lines)
            cols = acc.parse_columns(procs, proc_map, OBS[obs])
            updated = lines[:]
            changed = 0
            if channel != "h4l":
                rows, bins = acc.build_rows(procs, cols, inputs, "CMS_HIG25015_{source}_accMatrix")
                for i, line in enumerate(lines):
                    t = line.split()
                    if t and t[0] in rows:
                        assert len(t[2:]) == len(procs)
                        values = [new if col is not None else prev for col, new, prev in zip(cols, rows[t[0]], t[2:])]
                        changed += sum(x != y for x, y in zip(values, t[2:]))
                        updated[i] = f"{t[0]:<50s} lnN {' '.join(values)}\n"
                assert all(n in old_rows for n in rows), "missing acceptance nuisance"
                for before, after in zip(lines, updated):
                    if before != after:
                        assert before.split()[0] in rows, "unrelated row changed"
                if channel == "hgg":
                    assert acc.validate(updated, rows, procs, cols, 1e-10)
                    # Per-process/bin, maximum absolute +/- fractional response.
                    for name, values in rows.items():
                        entries = {}
                        for col, new, previous in zip(cols, values, old_rows[name]):
                            if col is None:
                                continue
                            key = "/".join(col)
                            size = lambda v: 100 * max(abs(float(x) - 1) for x in v.split("/"))
                            entries[key] = {"old": previous, "new": new, "old_percent": size(previous), "new_percent": size(new)}
                        info["comparison"][name] = entries
            else:
                assert updated == lines
            target = out / "cards" / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            text = "".join(updated)
            if target.exists() and target.read_text() != text:
                raise ValueError(f"Refusing to overwrite different existing card {target}")
            target.write_text(text)
            info["cards"][channel] = {"source": str(source), "source_sha256": digest(source), "output": str(target), "output_sha256": digest(target), "changed_entries": changed}
            print(obs, channel, "changed entries", changed, flush=True)
        # Independently ensure combined Hgg/H4l entries match the single-channel cards.
        for channel in ("hgg", "h4l"):
            single, sp = acc.read_card(out / "cards" / f"Datacard_{obs}_{channel}.txt")
            combined, cp = acc.read_card(out / "cards" / f"Datacard_{obs}_comb.txt")
            def keyed(lines, processes):
                bins = next(t[1:] for line in lines if (t := line.split()) and t[0] == "bin" and len(t) == len(processes) + 1)
                return {(b, p): j for j, (b, p) in enumerate(zip(bins, processes))}
            si, ci = keyed(single, sp), keyed(combined, cp)
            sr, cr = nuisance_rows(single), nuisance_rows(combined)
            for name in info["comparison"]:
                for key, j in si.items():
                    assert sr[name][j] == cr[name][ci[key]], (channel, name, key)
        (out / "acceptance_validation.json").write_text(json.dumps(info, indent=2) + "\n")
        report["observables"][obs] = info
    path = REPO / "combination/accbin_validation.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print("Validated cards and wrote", path)


if __name__ == "__main__":
    main()
