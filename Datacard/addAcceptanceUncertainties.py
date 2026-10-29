#!/usr/bin/env python3
"""
Add (or validate) the theory acceptance uncertainties of the Hgg signal templates
in a datacard: one lnN row per source (QCD scale, PDF, alphaS), shared by all
Higgs processes, with a value per (production mode, gen bin, in/out).

Inputs are the HiggsDNA fiducial calculator outputs
(higgs_dna/scripts/fiducial/fiducial_xsec_calculator.py), one file per
production mode, e.g. fidXS_YH_ggH.py, containing per gen bin b
    AccBin[b] = sum w(fiducial and bin b) / sum w(bin b)
    AccBin_<src>_up/dn use the same variation in numerator and denominator.
Legacy Acc arrays describe fractions of the whole sample, not within-bin
acceptances. They are only available via --acceptance-prefix Acc for auditing.

Convention:
    <prod>_<var>_<bin>_in  :  AccBin_var[b] / AccBin[b]
    <prod>_<var>_<bin>_out :  (1 - AccBin_var[b]) / (1 - AccBin[b])
written as "down/up" (QCDscale as "up/down", see FLIPPED_SOURCES). The value is the same for every era and category.
Gen bins are matched by position: bin i of the card <-> bin i of the file.

Examples:
  # validate the rows already present in a card
  python3 addAcceptanceUncertainties.py --datacard Datacard_rapidity.txt \
      --fidxs-dir .../higgs_dna/scripts/fiducial --obs YH --validate

  # (re)write the rows
  python3 addAcceptanceUncertainties.py --datacard Datacard_rapidity.txt \
      --fidxs-dir .../higgs_dna/scripts/fiducial --obs YH --output Datacard_rapidity_acc.txt
"""

import argparse
import re
import runpy
import sys
from collections import defaultdict

import numpy as np

# Card process label for each HiggsDNA observable (only where they differ)
CARD_VARIABLE = {"YH": "YH", "PTH": "PTH", "NJ": "NJ", "PTJ0": "PTJ0", "MassJ0J1": "MassJ0J1"}
# Card production-mode prefix -> HiggsDNA process name
DEFAULT_PROC_MAP = "ggh:ggH,vbf:VBFH,vh:VH,tth:ttH"
# Card source name -> key used in the HiggsDNA output (Acc_<key>_up/dn)
SOURCES = {"QCDscale": "scale", "pdf": "pdf", "alphaS": "alpha"}
# Sources written as "up/down" instead of "down/up", to follow the H4l orientation of the shared nuisance:
# the H4l QCDscale_accMatrix has its scales-up (envelope maximum) variation first (decided 2026-10-28)
FLIPPED_SOURCES = {"scale"}


def get_options():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datacard", required=True, help="Input Hgg datacard")
    p.add_argument("--fidxs-dir", required=True, help="Directory with fidXS_<obs>_<proc>.py files")
    p.add_argument("--obs", required=True, help="HiggsDNA observable label, e.g. YH, PTH, NJ, PTJ0")
    p.add_argument("--acceptance-prefix", choices=["AccBin", "Acc"], default="AccBin",
                   help="Acceptance arrays to read; Acc is for legacy reproduction only")
    p.add_argument("--card-var", default=None, help="Variable label in the card process names (default: from --obs)")
    p.add_argument("--proc-map", default=DEFAULT_PROC_MAP, help="cardPrefix:higgsdnaProc,... (default: %(default)s)")
    p.add_argument("--name-template", default="CMS_HIG25015_{source}_accMatrix",
                   help="Nuisance name, {source} is QCDscale/pdf/alphaS (default: %(default)s)")
    p.add_argument("--output", default=None, help="Write the card with the rows (re)placed here")
    p.add_argument("--validate", action="store_true", help="Compare against the rows already in the card")
    p.add_argument("--tolerance", type=float, default=1e-4, help="Max |difference| accepted by --validate")
    return p.parse_args()


def read_card(path):
    with open(path) as f:
        lines = f.readlines()
    procs = None
    for line in lines:
        t = line.split()
        if t and t[0] == "process" and not re.match(r"^-?\d+$", t[1]):
            procs = t[1:]
            break
    if procs is None:
        sys.exit(f"[ERROR] no process line found in {path}")
    return lines, procs


def edge(label):
    return float(label.replace("m", "-").replace("p", "."))


def parse_columns(procs, prods, card_var):
    """Return, per column, (prod, bin label, in|out) or None for non-matching processes.

    Differential cards: <prod>_<var>_<lo>_<hi>_(in|out)_<era>_hgg
    Inclusive cards:    <prod>_(in|out)_<era>_hgg  -> bin label "inclusive"
    """
    rx = re.compile(rf"^({'|'.join(prods)})_{card_var}_(m?[0-9p]+_m?[0-9p]+)_(in|out)_")
    rx_incl = re.compile(rf"^({'|'.join(prods)})_(in|out)_")
    cols = []
    for p in procs:
        m = rx.match(p)
        if m:
            cols.append((m.group(1), m.group(2), m.group(3)))
            continue
        m = rx_incl.match(p)
        cols.append((m.group(1), "inclusive", m.group(2)) if m else None)
    return cols


def check_edges(prod, bins, boundaries):
    """Match card gen bins to file bins by their edges, not just by count.

    Interior edges must agree exactly. The outermost edges encode the same
    underflow/overflow with different conventions (card: m10000p0/10000p0,
    file: -1000/900/140000 ...), so only a warning is printed when they differ.
    """
    if bins == ["inclusive"]:
        if len(boundaries) != 2:
            sys.exit(f"[ERROR] {prod}: inclusive card needs a single-bin file, got edges {boundaries}")
        return
    card_lo = [edge(b.split("_")[0]) for b in bins]
    card_hi = [edge(b.split("_")[1]) for b in bins]
    if len(boundaries) - 1 != len(bins):
        sys.exit(f"[ERROR] {prod}: card has {len(bins)} gen bins ({bins[0]}..{bins[-1]}), "
                 f"file has {len(boundaries) - 1} (edges {boundaries}). Binnings differ.")
    for i in range(1, len(bins)):
        if abs(card_lo[i] - boundaries[i]) > 1e-6:
            sys.exit(f"[ERROR] {prod}: interior edge mismatch at bin {i}: card {card_lo[i]} vs file {boundaries[i]}")
    for label, c, f in (("lower", card_lo[0], boundaries[0]), ("upper", card_hi[-1], boundaries[-1])):
        if abs(c - f) > 1e-6:
            print(f"  [WARNING] {prod}: outermost {label} edge differs (card {c}, file {f}); "
                  f"assumed to be the same under/overflow bin")


def load_acceptances(fidxs_dir, obs, hdna_proc, prefix="AccBin"):
    path = f"{fidxs_dir}/fidXS_{obs}_{hdna_proc}.py"
    try:
        ns = runpy.run_path(path, init_globals={"np": np})
    except FileNotFoundError:
        sys.exit(f"[ERROR] missing input {path}")
    required = [prefix] + [f"{prefix}_{k}_{d}" for k in SOURCES.values() for d in ("up", "dn")]
    missing = [k for k in required if k not in ns]
    if missing:
        raise ValueError(f"{path}: missing {missing}; refusing to substitute whole-sample Acc arrays")
    acc = {"nom": np.asarray(ns[prefix], float)}
    for key in SOURCES.values():
        acc[f"{key}_up"] = np.asarray(ns[f"{prefix}_{key}_up"], float)
        acc[f"{key}_dn"] = np.asarray(ns[f"{prefix}_{key}_dn"], float)
    acc["boundaries"] = list(ns["Boundaries"])
    edges = np.asarray(acc["boundaries"], float)
    if not np.isfinite(edges).all() or not np.all(np.diff(edges) > 0):
        raise ValueError(f"{path}: non-finite or unordered bin boundaries")
    for key, values in acc.items():
        if key == "boundaries":
            continue
        if values.shape != (len(edges) - 1,) or not np.isfinite(values).all():
            raise ValueError(f"{path}: malformed {prefix} array {key}")
        if np.any(values <= 0) or np.any(values >= 1):
            raise ValueError(f"{path}: {key} outside (0, 1); cannot form positive in/out lnN factors")
    return acc


def fmt(x):
    # same formatting as Combine/prepare_total_xsec_datacard.py, so rewritten
    # cards only differ where the values change
    s = f"{float(x):.5f}".rstrip("0").rstrip(".")
    return s if s else "0"


def kappa(acc, key, i, io):
    nom, dn, up = acc["nom"][i], acc[f"{key}_dn"][i], acc[f"{key}_up"][i]
    if key in FLIPPED_SOURCES:
        dn, up = up, dn
    if io == "in":
        if nom <= 0:
            return "-"
        return f"{fmt(dn / nom)}/{fmt(up / nom)}"
    if nom >= 1:
        return "-"
    return f"{fmt((1 - dn) / (1 - nom))}/{fmt((1 - up) / (1 - nom))}"


def build_rows(procs, cols, accs, name_template):
    # Gen bins in card order (sorted by lower edge), matched to the file by position
    labels = {c[1] for c in cols if c}
    bins = ["inclusive"] if labels == {"inclusive"} else sorted(labels, key=lambda b: edge(b.split("_")[0]))
    rows = {}
    for prod, acc in accs.items():
        check_edges(prod, bins, acc["boundaries"])
    index = {b: i for i, b in enumerate(bins)}
    for source, key in SOURCES.items():
        name = name_template.format(source=source)
        vals = []
        for c in cols:
            vals.append("-" if c is None else kappa(accs[c[0]], key, index[c[1]], c[2]))
        rows[name] = vals
    return rows, bins


def validate(lines, rows, procs, cols, tolerance):
    existing = {}
    for line in lines:
        t = line.split()
        if t and t[0] in rows and len(t) > 2 and t[1] == "lnN":
            existing[t[0]] = t[2:]
    ok = True
    for name, new in rows.items():
        if name not in existing:
            print(f"  {name}: not in the card")
            ok = False
            continue
        if len(existing[name]) != len(new):
            print(f"  {name}: column-count mismatch")
            ok = False
            continue
        worst = defaultdict(float)
        for c, a, b in zip(cols, existing[name], new):
            if c is None:
                if a != "-":
                    print(f"  {name}: unexpected entry {a} on a non-signal column")
                    ok = False
                continue
            if (a == "-") != (b == "-"):
                worst[(c[0], c[2])] = float("inf")
                continue
            if a == "-":
                continue
            d = max(abs(float(x) - float(y)) for x, y in zip(a.split("/"), b.split("/")))
            worst[(c[0], c[2])] = max(worst[(c[0], c[2])], d)
        print(f"  {name}")
        for (prod, io), d in sorted(worst.items()):
            flag = "ok" if d <= tolerance else "DIFFERS"
            print(f"    {prod:4s} {io:3s} max|diff| {d:.1e}  {flag}")
            ok &= d <= tolerance
    return ok


def update_kmax(lines, n_added):
    """Increase a numeric kmax by the number of newly added nuisances (kmax * is left alone)."""
    for i, l in enumerate(lines):
        t = l.split()
        if len(t) > 1 and t[0] == "kmax" and t[1].isdigit():
            lines[i] = l.replace(t[1], str(int(t[1]) + n_added), 1)
            return


def write_card(lines, rows, output):
    names = set(rows)
    n_added = len(names - {l.split()[0] for l in lines if l.split()})
    kept = [l for l in lines if not (l.split() and l.split()[0] in names)]
    update_kmax(kept, n_added)
    # insert after the last lnN row, i.e. inside the systematics block
    last = max(i for i, l in enumerate(kept) if len(l.split()) > 1 and l.split()[1] == "lnN")
    new = [f"{name:<50s}  lnN    {' '.join(vals)}\n" for name, vals in rows.items()]
    out = kept[: last + 1] + new + kept[last + 1:]
    with open(output, "w") as f:
        f.writelines(out)
    print(f"Wrote {output} ({len(new)} rows)")


def main():
    opt = get_options()
    card_var = opt.card_var or CARD_VARIABLE.get(opt.obs, opt.obs)
    proc_map = dict(x.split(":") for x in opt.proc_map.split(","))

    lines, procs = read_card(opt.datacard)
    cols = parse_columns(procs, proc_map, card_var)
    present = sorted({c[0] for c in cols if c})
    if not present:
        sys.exit(f"[ERROR] no <prod>_{card_var}_<bin>_(in|out) or <prod>_(in|out) processes in {opt.datacard}")
    accs = {p: load_acceptances(opt.fidxs_dir, opt.obs, proc_map[p], opt.acceptance_prefix) for p in present}
    rows, bins = build_rows(procs, cols, accs, opt.name_template)
    print(f"{opt.datacard}: {len(procs)} columns, {len(bins)} gen bins, production modes {present}")

    if opt.validate:
        ok = validate(lines, rows, procs, cols, opt.tolerance)
        print("VALIDATION PASSED" if ok else "VALIDATION FAILED")
        if not opt.output:
            sys.exit(0 if ok else 1)
    if opt.output:
        write_card(lines, rows, opt.output)


if __name__ == "__main__":
    main()
