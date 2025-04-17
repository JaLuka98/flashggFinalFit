law run ToyFitCategoryFirstStep --variable PTH --year 2023 --number-of-toys 1000 --batch-flavor slurm/psi --version v1 --slurm-partition short --slurm-max-runtime 01:00:00
law run ToysFitSystSingle --variable PTH --year 2023 --number-of-toys 1000 --batch-flavor slurm/psi --version v1 --slurm-partition short --slurm-max-runtime 01:00:00

# To get the hesse
law run AsimovCovCorrHesse --variable PTH --year 2023 --batch-flavor slurm/psi --version v1 --slurm-partition short --slurm-max-runtime 01:00:00
law run AsimovCovCorr --year 2023 --variable PTH --batch-flavor slurm/psi --version v1 --slurm-partition short --slurm-max-runtime 01:00:00

# To get the Asimov to compare with the toys
law run CreateAsimovFitFirstStep --variable PTH --year 2023 --workers 2 --batch-flavor slurm/psi
law run CreateAsimovFit --variable PTH --year 2023 --workers 2 --batch-flavor slurm/psi --version v1 --slurm-partition standard --slurm-max-runtime 02:00:00





rm -r /pnfs/psi.ch/cms/trivcat/store/user/niharrin/ntuples/midRun3/samples/January/2025_01_20_intermediateNTuples_2023/finalfits/PTH/Combine/Models_PTH/runFits_PTH/toy_*/higgsCombineToyBestFit_*