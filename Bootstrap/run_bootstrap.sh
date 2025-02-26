law run Trees2WSData --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1 --workflow slurm --batch-flavor slurm/psi
law run Background --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --batch-flavor slurm/psi
law run MakeYields --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --batch-flavor slurm/psi
law run MakeDatacard --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1 --workflow slurm --batch-flavor slurm/psi
law run PrepareTheDirectory --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1 --batch-flavor slurm/psi
law run RunText2Workspace --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1 --batch-flavor slurm/psi
law run UnblindedFitSystSingle --variable PTH --year 2023 --number-of-bootstraps 1000 --bootstrap-flag True --version v1 --batch-flavor slurm/psi --workflow slurm