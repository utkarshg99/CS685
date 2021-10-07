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
fls = [f for f in listdir("data/C17") if isfile(join("data/C17", f)) and f.startswith("DDW")]
for fl in fls:
    sc = int(int(fl.split("-")[2][:4])/100)
    c17[str(sc)] = pd.read_excel(join("data/C17", fl), header=0, skiprows=4)

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
    sttw[str(i)] = {
        "e1": {"m": 0, "f": 0, "p": 0}, 
        "e2": {"m": 0, "f": 0, "p": 0},
        "t1": {"m": 0, "f": 0, "p": 0},
        "t2": {"m": 0, "f": 0, "p": 0},
        "t3": {"m": 0, "f": 0, "p": 0},
        "lang": {}}
    spds = c17[str(i)]
    for ind in spds.index:
        if pd.notna(spds['4'][ind]):
            sttw[str(i)]["t1"]["p"] += int(spds["5"][ind])
            sttw[str(i)]["t1"]["m"] += int(spds["6"][ind])
            sttw[str(i)]["t1"]["f"] += int(spds["7"][ind])
            sttw[str(i)]["lang"][spds['4'][ind].strip()] = sttw[str(i)]["lang"].get(spds['4'][ind].strip(), {"p": 0, "m": 0, "f": 0})
            sttw[str(i)]["lang"][spds['4'][ind].strip()]["p"] += int(spds["5"][ind])
            sttw[str(i)]["lang"][spds['4'][ind].strip()]["m"] += int(spds["6"][ind])
            sttw[str(i)]["lang"][spds['4'][ind].strip()]["f"] += int(spds["7"][ind])

        if pd.notna(spds['9'][ind]):
            sttw[str(i)]["t2"]["p"] += int(spds["10"][ind])
            sttw[str(i)]["t2"]["m"] += int(spds["11"][ind])
            sttw[str(i)]["t2"]["f"] += int(spds["12"][ind])
            sttw[str(i)]["lang"][spds['9'][ind].strip()] = sttw[str(i)]["lang"].get(spds['9'][ind].strip(), {"p": 0, "m": 0, "f": 0})
            sttw[str(i)]["lang"][spds['9'][ind].strip()]["p"] += int(spds["10"][ind])
            sttw[str(i)]["lang"][spds['9'][ind].strip()]["m"] += int(spds["11"][ind])
            sttw[str(i)]["lang"][spds['9'][ind].strip()]["f"] += int(spds["12"][ind])
        
        if pd.notna(spds['14'][ind]):
            sttw[str(i)]["t3"]["p"] += int(spds["15"][ind])
            sttw[str(i)]["t3"]["m"] += int(spds["16"][ind])
            sttw[str(i)]["t3"]["f"] += int(spds["17"][ind])
            sttw[str(i)]["lang"][spds['14'][ind].strip()] = sttw[str(i)]["lang"].get(spds['14'][ind].strip(), {"p": 0, "m": 0, "f": 0})
            sttw[str(i)]["lang"][spds['14'][ind].strip()]["p"] += int(spds["15"][ind])
            sttw[str(i)]["lang"][spds['14'][ind].strip()]["m"] += int(spds["16"][ind])
            sttw[str(i)]["lang"][spds['14'][ind].strip()]["f"] += int(spds["17"][ind])
    
    sttw[str(i)]["e1"]["p"] = sttw[str(i)]["t1"]["p"] - sttw[str(i)]["t2"]["p"]
    sttw[str(i)]["e1"]["m"] = sttw[str(i)]["t1"]["m"] - sttw[str(i)]["t2"]["m"]
    sttw[str(i)]["e1"]["f"] = sttw[str(i)]["t1"]["f"] - sttw[str(i)]["t2"]["f"]
    sttw[str(i)]["e2"]["p"] = sttw[str(i)]["t2"]["p"] - sttw[str(i)]["t3"]["p"]
    sttw[str(i)]["e2"]["m"] = sttw[str(i)]["t2"]["m"] - sttw[str(i)]["t3"]["m"]
    sttw[str(i)]["e2"]["f"] = sttw[str(i)]["t2"]["f"] - sttw[str(i)]["t3"]["f"]




with open("meta/state_c17.json", "w") as stc17:
    json.dump(sttw, stc17, indent="\t")