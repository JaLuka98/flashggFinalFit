# 2022+2023 rapidity observed uncertainty breakdown

This directory is a controlled sandbox for the first observed rapidity POI:

```bash
r_YH_0p0_0p15
```

It contains a copy of the combined 2022+2023 rapidity datacard with nuisance
groups appended at the end, plus symlinks to the original model directories:

```bash
Datacard_rapidity_2022_2023_with_groups.txt
Models_rapidity_2022 -> ../output_2022_2023_rapidity/Combine/Models_rapidity_2022
Models_rapidity_2023 -> ../output_2022_2023_rapidity/Combine/Models_rapidity_2023
```

The nuisance groups added to the datacard are:

```text
photonScale
photonResolution
photonSF
pileup
lumi
theory
mcStat
```

They are intentionally explicit: only nuisance names found in the rapidity
datacard are included.

## Compile the workspace

Run from this directory:

```bash
./compile_workspace.sh
```

This writes:

```bash
Datacard_rapidity_2022_2023_with_groups.root
```

The command is the same multi-signal map as
`output_2022_2023_rapidity/Combine/t2w_jobs/t2w_rapidity.sh`, but pointed at
the grouped datacard in this directory.

## Observed scans and breakdown

Run:

```bash
./run_first_poi_breakdown.sh
```

The script performs:

1. A profiled observed best-fit with `--saveWorkspace`.
2. The total likelihood scan from that postfit workspace.
3. Cumulative frozen-group scans:
   - photon scale + photon resolution
   - photon scale + photon resolution + photon SFs
   - plus pileup + lumi
   - plus theory
   - plus MC stat
4. The correct stat-only scan, freezing `allConstrainedNuisances` while loading
   the postfit snapshot with `--snapshotName MultiDimFit`.
5. A `plot1DScan.py` breakdown plot:

```bash
breakdown_r_YH_0p0_0p15.pdf
breakdown_r_YH_0p0_0p15.png
```

The default scan settings are:

```bash
POINTS=40
RANGE=r_YH_0p0_0p15=0.8,2.0
```

Override them if needed, e.g.

```bash
POINTS=200 RANGE=r_YH_0p0_0p15=0.3,2.4 ./run_first_poi_breakdown.sh
```

## Important detail

The stat-only scan is not run directly from the original workspace. It is run
from the saved best-fit output with:

```bash
--snapshotName MultiDimFit --freezeParameters MH,allConstrainedNuisances
```

This follows the Combine tutorial recipe for uncertainty breakdowns: constrained
nuisance parameters must be frozen at their profiled best-fit values, otherwise
the stat-only curve can be shifted relative to the total scan.

The group-freezing order matters when groups are correlated. If the first pass
points to a large non-photon residual, repeat the same scan sequence with a
different group order before drawing a physics conclusion.
