#!/usr/bin/env python3
"""
collapse_nuisances.py
=====================
Summarise CMS HGG datacard nuisances into combined single-nuisance replacements.

Two independent operations are performed:

1.  CMS_hgg_scale_*  →  CMS_hgg_scale_shape
    ─────────────────────────────────────────
    All lines whose nuisance name begins with "CMS_hgg_scale" are collapsed
    into one new line.  Each data column is treated independently:

    • Parse every entry in that column across all scale rows.
      An entry can be:
        – "-"           → no variation (skip this row for this column)
        – "X"           → symmetric variation  (up = +X, down = 1/X or just X)
        – "X/Y"         → asymmetric variation (up = max(X,Y), down = min(X,Y))

    • Collect all numeric upper-variation values and all lower-variation values
      seen for that column.

    • The combined upper variation  = max of all uppers collected.
      The combined lower variation  = min of all lowers collected.

    • If no variation was seen in the column at all → write "-".
    • If combined_upper == combined_lower (effectively symmetric) → write the
      single value.
    • Otherwise → write "combined_upper/combined_lower".

2.  CMS_hgg_pdfWeight_*  →  CMS_hgg_pdfWeight_shape
    ──────────────────────────────────────────────────
    All lines whose nuisance name begins with "CMS_hgg_pdfWeight" are collapsed
    into one new line.  Each data column is treated independently:

    • Entries are either "-" (no variation) or a single symmetric number X.
    • Treat "-" as 0.0 for the calculation.
    • The combined value per column is:
            sqrt( sum(x_i^2) / N )
      where N is the total number of pdf-weight rows (including those with "-").
    • If the result rounds to 1.000 (no measurable effect), write "-".
    • Otherwise write the formatted combined value.

The two original blocks of nuisance lines are each replaced by the single
summary line.  All other lines in the datacard are preserved verbatim.

Usage
-----
    python collapse_nuisances.py input_datacard.txt output_datacard.txt

    # or, to overwrite in place (keeps a .bak backup):
    python collapse_nuisances.py datacard.txt

Author:  auto-generated helper script
"""

import sys
import re
import math
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# Helper utilities
# ──────────────────────────────────────────────────────────────────────────────

def parse_entry(token: str):
    """
    Parse one datacard cell and return (up, down) as floats, or None if "-".

    Token formats:
        "-"         → None  (no variation for this row / column)
        "1.023"     → (1.023, 1.023)   symmetric
        "1.023/0.978" → (1.023, 0.978) asymmetric – caller decides up/down
    """
    token = token.strip()
    if token == "-":
        return None
    if "/" in token:
        parts = token.split("/")
        a, b = float(parts[0]), float(parts[1])
        # "bigger/smaller" convention: up = larger, down = smaller
        up   = max(a, b)
        down = min(a, b)
        return (up, down)
    # symmetric
    val_1 = float(token)
    val_2 = 1 - (1 - val_1)
    return (max(val_1, val_2), min(val_1, val_2))


def format_variation(up: float, down: float, decimals: int = 3) -> str:
    """
    Format a (up, down) pair back into a datacard token.

    If up == down (within floating-point noise) write a single number,
    otherwise write "up/down".
    """
    fmt = f"{{:.{decimals}f}}"
    up_s   = fmt.format(up)
    down_s = fmt.format(down)
    if up_s == down_s:
        return up_s
    elif float(down_s) > 1:
        return up_s
    return f"{up_s}/{down_s}"


# ──────────────────────────────────────────────────────────────────────────────
# Column-level reduction functions
# ──────────────────────────────────────────────────────────────────────────────

def reduce_scale_column(values):
    """
    Given a list of (up, down) tuples (one per scale row, None entries excluded),
    return the combined token for CMS_hgg_scale_shape.

    Rule:
        combined_up   = max of all up   values
        combined_down = min of all down values
    """
    if not values:
        return "-"
    all_ups   = [v[0] for v in values]
    all_downs = [v[1] for v in values]
    return format_variation(max(all_ups), min(all_downs))


def reduce_pdf_column(tokens, n_rows: int) -> str:
    """
    Given a list of raw token strings (one per pdf-weight row, including "-"),
    return the combined token for CMS_hgg_pdfWeight_shape.

    Rule:
        x_i = 0  if token == "-"
            = float(token) otherwise   (guaranteed symmetric, no "/" expected)
        result = sqrt( sum(x_i^2) / n_rows )

    If the result == 1.000 after formatting (negligible) → "-".
    """
    squared_sum = 0.0
    for tok in tokens:
        tok = tok.strip()
        if tok == "-":
            x = 1.000
        else:
            # Should be a plain number like "1.003"
            x = float(tok)
        squared_sum += x * x

    if n_rows == 0:
        return "-"

    result = math.sqrt(squared_sum / n_rows)
    formatted = f"{result:.3f}"
    if formatted == "1.000":
        return "-"
    return formatted


# ──────────────────────────────────────────────────────────────────────────────
# Line parser for nuisance rows
# ──────────────────────────────────────────────────────────────────────────────

def parse_nuisance_line(line: str):
    """
    Split a nuisance line into (name, kind, [column_tokens]).

    A nuisance line looks like:
        CMS_hgg_scale_0_shape   lnN   token0 token1 token2 ...

    Returns:
        (name: str, kind: str, tokens: list[str])
    or None if the line does not look like a nuisance row.
    """
    # Ignore separator lines and blank lines
    stripped = line.strip()
    if not stripped or stripped.startswith("-") or stripped.startswith("#"):
        return None

    parts = stripped.split()
    if len(parts) < 3:
        return None
    # The 'kind' field for the nuisances we care about is always 'lnN'
    if parts[1] != "lnN":
        return None

    name   = parts[0]
    kind   = parts[1]
    tokens = parts[2:]
    return name, kind, tokens


# ──────────────────────────────────────────────────────────────────────────────
# Main processing function
# ──────────────────────────────────────────────────────────────────────────────

def process_datacard(input_path: str, output_path: str):
    """
    Read the datacard at *input_path*, apply both nuisance collapses, and
    write the result to *output_path*.
    """
    input_path  = Path(input_path)
    output_path = Path(output_path)

    print(f"Reading:  {input_path}")
    lines = input_path.read_text().splitlines(keepends=True)
    print(f"  Total lines: {len(lines)}")

    # ── Pass 1: identify the scale and pdfWeight rows ─────────────────────────

    scale_rows  = []   # list of (line_index, name, kind, tokens)
    pdf_rows    = []   # list of (line_index, name, kind, tokens)

    for i, line in enumerate(lines):
        parsed = parse_nuisance_line(line)
        if parsed is None:
            continue
        name, kind, tokens = parsed
        if name.startswith("CMS_hgg_scale"):
            scale_rows.append((i, name, kind, tokens))
        elif name.startswith("CMS_hgg_pdfWeight"):
            pdf_rows.append((i, name, kind, tokens))

    print(f"  Found {len(scale_rows)} CMS_hgg_scale_* rows.")
    print(f"  Found {len(pdf_rows)} CMS_hgg_pdfWeight_* rows.")

    # Determine number of data columns (should be the same for all rows)
    if not scale_rows and not pdf_rows:
        print("Nothing to collapse – writing file unchanged.")
        output_path.write_text("".join(lines))
        return

    n_cols = 0
    if scale_rows:
        n_cols = len(scale_rows[0][3])
    elif pdf_rows:
        n_cols = len(pdf_rows[0][3])

    print(f"  Number of data columns: {n_cols}")

    # ── Pass 2a: build the combined CMS_hgg_scale_shape row ──────────────────

    combined_scale_tokens = []

    if scale_rows:
        for col in range(n_cols):
            # Collect non-None parsed variations from every scale row
            col_values = []
            for _, _, _, tokens in scale_rows:
                if col < len(tokens):
                    parsed_val = parse_entry(tokens[col])
                    if parsed_val is not None:
                        col_values.append(parsed_val)

            combined_scale_tokens.append(reduce_scale_column(col_values))

    # ── Pass 2b: build the combined CMS_hgg_pdfWeight_shape row ──────────────

    combined_pdf_tokens = []

    if pdf_rows:
        n_pdf_rows = len(pdf_rows)
        for col in range(n_cols):
            col_raw = []
            for _, _, _, tokens in pdf_rows:
                if col < len(tokens):
                    col_raw.append(tokens[col])
                else:
                    col_raw.append("-")

            combined_pdf_tokens.append(reduce_pdf_column(col_raw, n_pdf_rows))

    # ── Pass 3: build the replacement lines ───────────────────────────────────

    # We want consistent column spacing.  Use a fixed-width name field of 56
    # characters (same style as the rest of the file), then "lnN", then tokens
    # separated by single spaces.

    def make_line(nuisance_name: str, tokens: list) -> str:
        """Format a nuisance line with the same wide-column style."""
        col_str = " ".join(tokens)
        return f"{nuisance_name:<56}lnN   {col_str}\n"

    scale_replacement_line = (
        make_line("CMS_hgg_scale_shape", combined_scale_tokens)
        if scale_rows else None
    )

    pdf_replacement_line = (
        make_line("CMS_hgg_pdfWeight_shape", combined_pdf_tokens)
        if pdf_rows else None
    )

    # ── Pass 4: assemble the output, replacing blocks ─────────────────────────

    # Build a set of line indices to *remove* (all original scale/pdf lines)
    scale_indices = {i for i, *_ in scale_rows}
    pdf_indices   = {i for i, *_ in pdf_rows}

    # We want to insert the replacement just before the first removed line in
    # each group so the output structure is maintained.
    first_scale_idx = min(scale_indices) if scale_indices else None
    first_pdf_idx   = min(pdf_indices)   if pdf_indices   else None

    output_lines = []
    scale_inserted = False
    pdf_inserted   = False

    for i, line in enumerate(lines):
        # Handle scale block
        if i in scale_indices:
            if not scale_inserted:
                output_lines.append(scale_replacement_line)
                scale_inserted = True
            # Skip the original line (do not append it)
            continue

        # Handle pdf block
        if i in pdf_indices:
            if not pdf_inserted:
                output_lines.append(pdf_replacement_line)
                pdf_inserted = True
            continue

        # All other lines are kept verbatim
        output_lines.append(line)

    # ── Write output ──────────────────────────────────────────────────────────

    output_path.write_text("".join(output_lines))

    final_lines = len(output_lines)
    removed     = len(scale_rows) + len(pdf_rows)
    added       = (1 if scale_rows else 0) + (1 if pdf_rows else 0)
    print(f"\nDone.")
    print(f"  Lines removed (original nuisances): {removed}")
    print(f"  Lines added   (collapsed nuisances): {added}")
    print(f"  Output lines: {final_lines}  (was {len(lines)})")
    print(f"Writing: {output_path}")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) == 2:
        inp = sys.argv[1]
        backup = inp + ".bak"
        Path(backup).write_bytes(Path(inp).read_bytes())
        print(f"Backup saved to: {backup}")
        out = inp
    elif len(sys.argv) == 3:
        inp = sys.argv[1]
        out = sys.argv[2]
    else:
        print("Usage:")
        print("  python collapse_nuisances.py input.txt output.txt")
        print("  python collapse_nuisances.py datacard.txt          # overwrites in-place")
        sys.exit(1)

    process_datacard(inp, out)
