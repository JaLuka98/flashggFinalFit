import numpy
import pandas 

path = "/eos/cms/store/group/phys_higgs/cmshgg/2023_2022_Hgg_differentials/particleLevel/2026_01_28/2022/GluGluHtoGG_M-120_2022postEE/158b0868-e5b9-11ee-a84f-06a8935abeef_%2FEvents%3B1_0-34124.parquet"

df = pandas.read_parquet(path)

for key in df.columns:
    print(key)