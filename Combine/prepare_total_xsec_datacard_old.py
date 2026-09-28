#!/usr/bin/env python3
"""
Utility to extend an existing fiducial datacard with the ingredients needed
to perform an inclusive total cross-section measurement.
"""

from __future__ import annotations

import argparse
import math
import pathlib
import runpy
import sys
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import numpy as np


MODE_SUFFIX_MAP = {
    "ggh": "ggH",
    "vbf": "VBFH",
    "vh": "VH",
    "wh": "WH",
    "zh": "ZH",
    "tth": "ttH",
    "bbh": "bbH",
    "thq": "tHq",
    "thw": "tHW",
    "th": "tH",
}

SOURCE_NAME_MAP = {
    "scale": "CMS_acc_scale",
    "pdf": "CMS_acc_pdf",
    "alphaS": "CMS_acc_alphaS",
}

# The acceptance inputs sometimes label alpha_s as just "alpha".
VARIATION_ALIASES = {
    "scale": ("scale",),
    "pdf": ("pdf",),
    "alphaS": ("alphaS", "alpha"),
}

DIRECTION_ALIASES = {
    "up": ("up", "Up", "UP"),
    "dn": ("dn", "Dn", "DN", "down", "Down", "DOWN"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add total cross-section nuisances to a fiducial datacard."
    )
    parser.add_argument(
        "--acceptances-file",
        required=True,
        help="Path to the python file that contains the acceptance numbers.",
    )
    parser.add_argument(
        "--input-datacard",
        required=True,
        help="Existing fiducial datacard that will be used as input.",
    )
    parser.add_argument(
        "--output-datacard",
        required=True,
        help="New datacard path where the updated content will be written.",
    )
    return parser.parse_args()


def load_acceptance_namespace(path: pathlib.Path) -> MutableMapping[str, object]:
    """Executes the acceptance file and returns the resulting namespace."""
    if not path.exists():
        raise FileNotFoundError(f"Acceptances file '{path}' does not exist")
    init_globals = {"np": np}
    return runpy.run_path(path.as_posix(), init_globals=init_globals)


def _to_float(value: object) -> float:
    """Converts arrays/lists of size 1 and numpy scalars to python floats."""
    if isinstance(value, (list, tuple)):
        if len(value) != 1:
            raise ValueError(
                f"Expected a single value but got {len(value)} entries: {value}"
            )
        value = value[0]
    if isinstance(value, np.ndarray):
        if value.size != 1:
            raise ValueError(
                f"Expected a scalar numpy array but got shape {value.shape}"
            )
        value = value.item()
    if hasattr(value, "item") and not isinstance(value, (float, int)):
        value = value.item()
    return float(value)


def _find_key_case_insensitive(
    namespace: Mapping[str, object], target: str
) -> str | None:
    target_lower = target.lower()
    for key in namespace:
        if key.lower() == target_lower:
            return key
    return None


def get_acceptance_value(
    namespace: Mapping[str, object], suffix: str, source: str | None = None, direction: str | None = None
) -> float:
    """
    Fetches an acceptance value from the namespace, accounting for different
    ways variations may be named.
    """
    if source is None:
        key = _find_key_case_insensitive(namespace, f"Acc_{suffix}")
        if key is None:
            raise KeyError(f"Could not find nominal acceptance Acc_{suffix}")
        return _to_float(namespace[key])

    aliases = VARIATION_ALIASES[source]
    direction_aliases = DIRECTION_ALIASES[direction] if direction else (None,)
    for alias in aliases:
        for dir_alias in direction_aliases:
            dir_snippet = f"_{dir_alias}" if dir_alias else ""
            key_name = f"Acc_{alias}{dir_snippet}_{suffix}"
            key = _find_key_case_insensitive(namespace, key_name)
            if key:
                return _to_float(namespace[key])
    raise KeyError(
        f"Could not find acceptance variation for {source} {direction} in mode {suffix}"
    )


def get_process_names(lines: Sequence[str]) -> List[str]:
    for line in lines:
        stripped = line.strip()
        if not stripped or not stripped.startswith("process"):
            continue
        tokens = line.split()
        if len(tokens) <= 1:
            continue
        values = tokens[1:]
        try:
            _ = [int(v) for v in values]
        except ValueError:
            return values
    raise RuntimeError("Failed to find the process definition line in the datacard.")


def analyse_processes(processes: Sequence[str]) -> Tuple[
    Dict[int, Dict[str, str | bool]], Dict[str, set]
]:
    """
    Returns per-process metadata plus the components (in/out) required per mode.
    """
    info: Dict[int, Dict[str, str | bool]] = {}
    requirements: Dict[str, set] = {}
    for index, proc in enumerate(processes):
        is_signal = proc.endswith("_hgg")
        parts = proc.split("_")
        mode = parts[0].lower() if is_signal else None
        component = None
        if "_in_" in proc:
            component = "in"
        elif "_out_" in proc:
            component = "out"
        if is_signal and component:
            requirements.setdefault(mode, set()).add(component)
        info[index] = {
            "name": proc,
            "is_signal": is_signal,
            "mode": mode,
            "component": component,
        }
    return info, requirements


def map_mode_to_suffix(mode: str) -> str:
    suffix = MODE_SUFFIX_MAP.get(mode.lower())
    if suffix:
        return suffix
    # Default to uppercase version if no explicit mapping exists.
    return mode.upper()


def build_acceptance_ratios(
    namespace: Mapping[str, object], requirements: Mapping[str, Iterable[str]]
) -> Dict[str, Dict[str, Dict[str, Tuple[float, float]]]]:
    ratios: Dict[str, Dict[str, Dict[str, Tuple[float, float]]]] = {
        source: {} for source in SOURCE_NAME_MAP
    }
    for mode, needed_components in requirements.items():
        suffix = map_mode_to_suffix(mode)
        nominal = get_acceptance_value(namespace, suffix)
        for source in SOURCE_NAME_MAP:
            var_up = get_acceptance_value(namespace, suffix, source=source, direction="up")
            var_dn = get_acceptance_value(namespace, suffix, source=source, direction="dn")
            mode_dict: Dict[str, Tuple[float, float]] = {}
            if "in" in needed_components:
                mode_dict["in"] = (var_dn / nominal, var_up / nominal)
            if "out" in needed_components:
                denom = 1.0 - nominal
                if math.isclose(denom, 0.0, rel_tol=0, abs_tol=1e-9):
                    raise ZeroDivisionError(
                        f"Cannot compute acceptance variation for out-of-fiducial {mode} "
                        f"because the nominal acceptance is {nominal:.6f}"
                    )
                mode_dict["out"] = (
                    (1.0 - var_dn) / denom,
                    (1.0 - var_up) / denom,
                )
            ratios[source][mode] = mode_dict
    return ratios


def format_ratio(value_down: float, value_up: float) -> str:
    def fmt(val: float) -> str:
        formatted = f"{val:.5f}"
        formatted = formatted.rstrip("0").rstrip(".")
        return formatted if formatted else "0"

    return f"{fmt(value_down)}/{fmt(value_up)}"


def build_nuisance_values(
    processes_info: Mapping[int, Mapping[str, object]],
    ratios: Mapping[str, Mapping[str, Mapping[str, Tuple[float, float]]]],
    source: str,
) -> List[str]:
    values: List[str] = []
    for index in range(len(processes_info)):
        info = processes_info[index]
        if not info["is_signal"]:
            values.append("-")
            continue
        mode = info["mode"]
        component = info["component"]
        if not component:
            values.append("-")
            continue
        mode_dict = ratios.get(source, {}).get(mode, {})
        if component not in mode_dict:
            values.append("-")
            continue
        down, up = mode_dict[component]
        values.append(format_ratio(down, up))
    return values


def build_br_values(processes_info: Mapping[int, Mapping[str, object]]) -> List[str]:
    return [
        "0.98/1.021" if info["is_signal"] else "-"
        for info in processes_info.values()
    ]


def update_kmax_line(lines: List[str], num_new_nuisances: int) -> None:
    import re

    pattern = re.compile(r"(\s*kmax\s+)(\S+)(.*)", re.IGNORECASE)
    for idx, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        prefix, value, suffix = match.groups()
        if value == "*":
            return
        try:
            updated_value = str(int(value) + num_new_nuisances)
        except ValueError:
            return
        lines[idx] = f"{prefix}{updated_value}{suffix}"
        return


def add_new_lines(lines: List[str], new_lines: Sequence[str]) -> List[str]:
    output = lines[:]
    if output and output[-1].strip():
        output.append("")
    output.extend(new_lines)
    return output


def main() -> int:
    args = parse_args()
    input_path = pathlib.Path(args.input_datacard)
    output_path = pathlib.Path(args.output_datacard)
    acceptance_path = pathlib.Path(args.acceptances_file)

    lines = input_path.read_text().splitlines()
    processes = get_process_names(lines)
    processes_info, requirements = analyse_processes(processes)
    acceptance_namespace = load_acceptance_namespace(acceptance_path)
    ratios = build_acceptance_ratios(acceptance_namespace, requirements)

    br_values = build_br_values(processes_info)
    new_lines = [
        " ".join(["CMS_BR_hgg", "lnN", *br_values]),
    ]

    for source, nuisance_name in SOURCE_NAME_MAP.items():
        values = build_nuisance_values(processes_info, ratios, source)
        new_lines.append(" ".join([nuisance_name, "lnN", *values]))

    update_kmax_line(lines, len(new_lines))
    updated_lines = add_new_lines(lines, new_lines)
    output_path.write_text("\n".join(updated_lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
