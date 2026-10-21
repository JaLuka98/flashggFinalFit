"""Clean a single-channel card cut out of a combined card with `combineCards.py --ic`.

- strips the `ch1_` prefix combineCards adds, so bin names match the combined card;
- drops rate nuisances (lnN, shape, ...) with no entry in any remaining bin;
- drops `param` / `discrete` lines whose name matches --drop (nuisances of the other channel);
- removes dropped nuisances from `group` lines and sets kmax to '*'.

Usage: python3 clean_card.py in.txt out.txt --drop 'REGEX'
"""
import argparse
import re

RATE_TYPES = {"lnN", "lnU", "shape", "shapeN", "shape?", "shapeU", "gmN"}

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--drop", default=None, help="regex for param/discrete names to remove")
args = parser.parse_args()
drop = re.compile(args.drop) if args.drop else None

kept, dropped = set(), set()
out = []
with open(args.input) as f:
    for line in f:
        line = re.sub(r"(?<![A-Za-z0-9_])ch1_", "", line)
        tok = line.split()
        if not tok:
            out.append(line)
            continue
        if tok[0] == "kmax":
            out.append("kmax * number of nuisance parameters\n")
            continue
        if len(tok) > 1 and tok[1] in RATE_TYPES:
            values = tok[3:] if tok[1] == "gmN" else tok[2:]
            if all(v == "-" for v in values):
                dropped.add(tok[0])
                continue
            kept.add(tok[0])
        elif len(tok) > 1 and tok[1] in ("param", "discrete"):
            if drop and drop.search(tok[0]):
                dropped.add(tok[0])
                continue
            kept.add(tok[0])
        out.append(line)

final = []
for line in out:
    tok = line.split()
    if len(tok) > 2 and tok[1] == "group":
        members = [m for m in tok[3:] if m not in dropped]
        if not members:
            continue
        line = "%s group = %s\n" % (tok[0], " ".join(members))
    final.append(line)

with open(args.output, "w") as f:
    f.writelines(final)
print("%s: kept %d nuisances, dropped %d" % (args.output, len(kept), len(dropped)))
