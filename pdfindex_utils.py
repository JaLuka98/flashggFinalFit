"""Helpers for discovering available pdfindex categories in datacard workspaces."""

import json
import os


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


def update_override_file(override_path, year, variable, pdf_indices):
    """Update *override_path* with the provided *pdf_indices* for (*year*, *variable*)."""

    if not pdf_indices:
        return

    os.makedirs(os.path.dirname(override_path), exist_ok=True)

    data = {}
    if os.path.exists(override_path):
        try:
            with open(override_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            # start from scratch when the file exists but is not valid JSON
            data = {}

    year_entry = data.setdefault(year, {})
    year_entry[variable] = sorted(pdf_indices)

    with open(override_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
