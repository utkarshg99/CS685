import pandas as pd
import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

# Reading Census
census_df = pd.read_excel("data/DDW_PCA0000_2011_Indiastatedist.xlsx", header=0).dropna()

# Reading C17
c17 = {}
from os import listdir
from os.path import isfile, join
fls = [f for f in listdir("data/C17") if isfile(join("data/C17", f))]
for fl in fls:
    sc = int(fl.split("-")[2][:4])
    c17[str(sc)] = pd.read_excel("data/C17/"+fl, header=0, skiprows=4)
    # c17[str(sc)] = pd.read_excel("data/C17/"+fl, header=0, skiprows=4).fillna(-1)
    # lst_int = [1, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17]
    # for li in lst_int:
    #     c17[str(sc)][str(li)] = c17[str(sc)][str(li)].astype(int)

# Reading C18
age_df = pd.read_excel("data/DDW-C18-0000.xlsx", header=0, skiprows=4).dropna()
lst_int = [1, 2, 6, 7, 8, 9, 10, 11]
for li in lst_int:
    age_df[str(li)] = age_df[str(li)].astype(int)

# Reading C19
lit_df = pd.read_excel("data/DDW-C19-0000.xlsx", header=0, skiprows=4).dropna()
lst_int = [1, 2, 6, 7, 8, 9, 10, 11]
for li in lst_int:
    lit_df[str(li)] = lit_df[str(li)].astype(int)

# Extract Data From C17
sttw = {}
for i in range(config["SC_ULM"]):
    sttw[str(i)] = {"e1": 0, "e2": 0, "e3": 0, "t1": 0, "t2": 0, "t3": 0}
    spds = c17[str(i)]