law run Trees2WSData --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1 --workflow slurm
law run Background --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000
law run MakeYields --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000
law run MakeDatacard --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1
law run PrepareTheDirectory --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1
law run RunText2Workspace --variable PTH --year 2023 --bootstrap-flag True --number-of-bootstraps 1000 --version v1
law run UnblindedFitSystSingle --variable PTH --year 2023 --number-of-bootstraps 2 --bootstrap-flag True --version v1 --workflow slurm