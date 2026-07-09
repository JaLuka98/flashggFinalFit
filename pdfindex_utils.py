"""Helpers for discovering available pdfindex categories in datacard workspaces."""

import json
import os


_COMBINED_YEAR_MAP = {
    # Two-year Run-3 combination (aka 2223 campaign)
    "2223": ["2022", "2023"],
    "2022_2023": ["2022", "2023"],
    # Full Run-3 combinations
    "222324": ["2022", "2023", "2024"],
    "2022_2023_2024": ["2022", "2023", "2024"],
    "Run3": ["2022", "2023", "2024"],
}


def _load_root():
    """Import ROOT lazily to avoid slowing down callers that do not need it."""

    import ROOT  # pylint: disable=import-error

    return ROOT


def extract_pdf_indices(workspace_path):
    """Return all pdfindex category names present in *workspace_path*."""

    if not os.path.exists(workspace_path):
        return []

    ROOT = _load_root()
    f = ROOT.TFile.Open(workspace_path)
    if not f or f.IsZombie():
        return []

    workspace = f.Get("w")
    if not workspace:
        return []

    result = []
    cats = workspace.allCats()
    iterator = cats.createIterator()
    obj = iterator.Next()
    while obj:
        name = obj.GetName()
        if name.startswith("pdfindex_"):
            result.append(name)
        obj = iterator.Next()

    # keep order stable for reproducible commands
    return sorted(set(result))


def _candidate_components(year):
    """Return the list of base years represented by *year*, if any."""

    if year in _COMBINED_YEAR_MAP:
        return _COMBINED_YEAR_MAP[year]
    if "_" in year:
        return year.split("_")
    return None


def _merge_combined_year_entries(data):
    """Ensure combined-year entries equal the union of their component years."""

    changed = False
    candidates = set(_COMBINED_YEAR_MAP.keys())
    candidates.update(key for key in data if _candidate_components(key))

    for combined_year in sorted(candidates):
        components = _candidate_components(combined_year)
        if not components:
            continue
        if not all(component in data for component in components):
            continue

        combined_entry = data.setdefault(combined_year, {})
        variables = set()
        for component in components:
            variables.update(data[component].keys())

        for variable in variables:
            merged = set()
            for component in components:
                merged.update(data[component].get(variable, []))
            if not merged:
                continue
            merged_list = sorted(merged)
            if combined_entry.get(variable) != merged_list:
                combined_entry[variable] = merged_list
                changed = True

    return changed


def update_override_file(override_path, year, variable, pdf_indices):
    """Update *override_path* with the provided *pdf_indices* for (*year*, *variable*).

    When *year* is a combined label (e.g. "2223" or "2022_2023"), the stored
    indices are automatically merged from the underlying component years so that
    the JSON file always contains a usable entry for multi-year combinations.
    """

    pdf_indices = pdf_indices or []

    os.makedirs(os.path.dirname(override_path), exist_ok=True)

    data = {}
    if os.path.exists(override_path):
        try:
            with open(override_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            # start from scratch when the file exists but is not valid JSON
            data = {}

    changed = False
    if pdf_indices:
        year_entry = data.setdefault(year, {})
        normalized = sorted(set(pdf_indices))
        if normalized and year_entry.get(variable) != normalized:
            year_entry[variable] = normalized
            changed = True

    if _merge_combined_year_entries(data):
        changed = True

    if changed:
        with open(override_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
