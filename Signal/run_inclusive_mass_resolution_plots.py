#!/usr/bin/env python3

import os
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SIGNAL_DIR = ROOT / "Signal"

CONFIGS = {
    "2022": ROOT / "config/2022_inclusive.yml",
    "2023": ROOT / "config/2023_inclusive.yml",
    "2024": ROOT / "config/2024_inclusive.yml",
    "2022_2023_2024": ROOT / "config/2022_2023_2024_inclusive.yml",
}

PLOT_YEARS = {
    "2022": ["2022preEE", "2022postEE", "2022preEE,2022postEE"],
    "2023": ["2023preBPix", "2023postBPix", "2023preBPix,2023postBPix"],
    "2024": ["2024"],
    "2022_2023_2024": ["2022preEE,2022postEE,2023preBPix,2023postBPix,2024"],
}

CATEGORIES = {
    "best": "best_resolution=cat0",
    "medium": "medium_resolution=cat1",
    "worst": "worst_resolution=cat2",
    "all": "all",
}

CATEGORY_LABELS = {
    "best_resolution": "Best resolution",
    "medium_resolution": "Medium resolution",
    "worst_resolution": "Worst resolution",
}

LABEL = "Simulation Preliminary"
DO_FWHM = False
MAX_WORKERS = 8


def read_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def packaged_file(config, label, cat):
    output_dir = Path(config["outputFolder"].rstrip("/"))
    ext = config[f"packaged_{label}"].get("ext", "")
    return output_dir / f"outdir_packaged{ext}" / f"CMS-HGG_sigfit_packaged{ext}_{cat}.root"


def rooiter(items):
    iterator = items.iterator()
    item = iterator.Next()
    while item:
        yield item
        item = iterator.Next()


def import_workspace_objects(output_file, input_files):
    import ROOT

    output_workspace = ROOT.RooWorkspace("wsig_13TeV", "wsig_13TeV")
    workspace_import = getattr(output_workspace, "import")

    for input_file in input_files:
        root_file = ROOT.TFile.Open(str(input_file))
        workspace = root_file.Get("wsig_13TeV")

        for item in rooiter(workspace.allVars()):
            workspace_import(item, ROOT.RooFit.RecycleConflictNodes(), ROOT.RooFit.Silence())

        for item in rooiter(workspace.allFunctions()):
            workspace_import(item, ROOT.RooFit.RecycleConflictNodes(), ROOT.RooFit.Silence())

        for item in rooiter(workspace.allPdfs()):
            workspace_import(item, ROOT.RooFit.RecycleConflictNodes(), ROOT.RooFit.Silence())

        for item in workspace.allData():
            workspace_import(item)

        root_file.Close()

    output_root = ROOT.TFile(str(output_file), "RECREATE")
    output_workspace.Write()
    output_root.Close()


def make_runplotter_inputs(label, config):
    ext = f"inclusive_mass_resolution_{label}"
    output_dir = Path(config["outputFolder"].rstrip("/"))
    outdir = output_dir / f"outdir_{ext}"
    outdir.mkdir(parents=True, exist_ok=True)
    category_labels = outdir / "category_labels.json"

    with open(category_labels, "w") as f:
        json.dump(CATEGORY_LABELS, f, indent=2)

    for cat in ["cat0", "cat1", "cat2"]:
        dst = outdir / f"CMS-HGG_sigfit_{ext}_{cat}.root"

        if dst.exists() or dst.is_symlink():
            dst.unlink()

        if label == "2022_2023_2024":
            input_files = [
                packaged_file(read_config(CONFIGS["2022"]), "2022", cat),
                packaged_file(read_config(CONFIGS["2023"]), "2023", cat),
                packaged_file(read_config(CONFIGS["2024"]), "2024", cat),
            ]

            missing_files = [path for path in input_files if not path.exists()]
            if missing_files:
                raise FileNotFoundError(missing_files[0])

            import_workspace_objects(dst, input_files)
        else:
            src = packaged_file(config, label, cat)
            if not src.exists():
                raise FileNotFoundError(src)

            dst.symlink_to(src)

    return ext, output_dir, category_labels


def run_plotter(output_dir, ext, years, category, category_labels):
    command = [
        sys.executable,
        "RunPlotter.py",
        "--procs",
        "all",
        "--years",
        years,
        "--cats",
        category,
        "--ext",
        ext,
        "--label",
        LABEL,
        "--translateCats",
        str(category_labels),
    ]

    if DO_FWHM:
        command.append("--doFWHM")

    print(" ".join(command))
    env = os.environ.copy()
    env["RUNPLOTTER_SIGNAL_DIR"] = str(output_dir)
    subprocess.run(command, cwd=SIGNAL_DIR, env=env, check=True)


def main():
    os.environ["ANALYSIS_PATH"] = str(ROOT)
    os.environ["PYTHONPATH"] = f"{ROOT / 'commonTools'}:{os.environ.get('PYTHONPATH', '')}"

    jobs = []

    for label, config_path in CONFIGS.items():
        config = read_config(config_path)
        ext, output_dir, category_labels = make_runplotter_inputs(label, config)

        for years in PLOT_YEARS[label]:
            for category in CATEGORIES.values():
                jobs.append((output_dir, ext, years, category, category_labels))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(run_plotter, *job) for job in jobs]
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    main()
