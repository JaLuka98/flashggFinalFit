#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

CONFIGS = {
    "2022": ROOT / "config/2022_inclusive.yml",
    "2023": ROOT / "config/2023_inclusive.yml",
    "2024": ROOT / "config/2024_inclusive.yml",
    "2022_2023_2024": ROOT / "config/2022_2023_2024_inclusive.yml",
}

GROUPS = {
    "best": "Best resolution",
    "medium": "Medium resolution",
    "worst": "Worst resolution",
    "all": "All categories",
    "weighted": "S/(S+B) weighted categories",
}

LUMI_LABELS = {
    "2022": "34.7 fb^{-1} (13.6 TeV)",
    "2023": "27.6 fb^{-1} (13.6 TeV)",
    "2024": "109.8 fb^{-1} (13.6 TeV)",
    "2022_2023_2024": "172.1 fb^{-1} (13.6 TeV)",
}

MAX_WORKERS = 8


def read_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def output_dir(config):
    return Path(config["outputFolder"].rstrip("/"))


def datacard_path(config, label):
    return output_dir(config) / "Combine" / f"Datacard_{label}.root"


def cats_for(label, group):
    cat = {"best": "cat0", "medium": "cat1", "worst": "cat2"}[group]

    if label == "2022_2023_2024":
        return f"Y22_{cat},Y23_{cat},Y24_{cat}"

    return cat


def write_labels(path, label):
    labels = {
        "cat0": "Best resolution",
        "cat1": "Medium resolution",
        "cat2": "Worst resolution",
        "all": label,
    }

    with open(path, "w") as f:
        json.dump(labels, f, indent=2)


def run_plot(datacard, workdir, year_label, group, cats):
    group_label = GROUPS[group]
    ext = f"_{datacard.stem.replace('Datacard_', '')}_{group}"
    labels_path = workdir / f"labels_{group}.json"
    write_labels(labels_path, group_label)

    command = [
        sys.executable,
        str(ROOT / "Plots/makeSplusBModelPlot.py"),
        "--inputWSFile",
        str(datacard),
        "--cats",
        cats,
        "--doZeroes",
        "--translateCats",
        str(labels_path),
        "--lumiLabel",
        LUMI_LABELS[year_label],
        "--ext",
        ext,
    ]

    if "," in cats or cats == "all":
        command += ["--doSumCategories", "--skipIndividualCatPlots"]

    if group == "weighted":
        command.append("--doCatWeights")

    print(" ".join(command))
    subprocess.run(command, cwd=workdir, check=True)


def main():
    os.environ["ANALYSIS_PATH"] = str(ROOT)
    os.environ["PYTHONPATH"] = f"{ROOT / 'commonTools'}:{os.environ.get('PYTHONPATH', '')}"

    jobs = []

    for label, config_path in CONFIGS.items():
        config = read_config(config_path)
        datacard = datacard_path(config, label)
        workdir = output_dir(config) / "Combine" / "splusb_model_plots"
        workdir.mkdir(parents=True, exist_ok=True)

        if not datacard.exists():
            raise FileNotFoundError(datacard)

        for group in GROUPS:
            cats = "all" if group in ["all", "weighted"] else cats_for(label, group)
            jobs.append((datacard, workdir, label, group, cats))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(run_plot, *job) for job in jobs]
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    main()
