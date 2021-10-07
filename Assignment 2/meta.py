import pandas as pd
import json

from pandas.core.indexes.base import Index

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

# Reading Census
census_df = pd.read_excel("data/DDW_PCA0000_2011_Indiastatedist.xlsx", header=0).dropna()

# Reading C13
agec13_df = pd.read_excel("data/DDW-0000C-13.xls", skiprows=4, header=0).dropna()

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

# Extract Data From Census
census = {}
for ind in census_df.index:
    sc = int(census_df["State"][ind])
    census[str(sc)] = census.get(str(sc), {
        "u": {"m": 0, "f": 0, "p": 0, "ml": 0, "fl": 0, "pl": 0, "mi": 0, "fi": 0, "pi": 0}, 
        "r": {"m": 0, "f": 0, "p": 0, "ml": 0, "fl": 0, "pl": 0, "mi": 0, "fi": 0, "pi": 0}, 
        "t": {"m": 0, "f": 0, "p": 0, "ml": 0, "fl": 0, "pl": 0, "mi": 0, "fi": 0, "pi": 0}, 
    })
    
    if census_df["Level"][ind].strip() == "DISTRICT":
        continue

    if census_df["TRU"][ind].strip() == "Total":
        census[str(sc)]["t"]["m"] = int(census_df["TOT_M"][ind])
        census[str(sc)]["t"]["f"] = int(census_df["TOT_F"][ind])
        census[str(sc)]["t"]["p"] = int(census_df["TOT_P"][ind])
        census[str(sc)]["t"]["ml"] = int(census_df["M_LIT"][ind])
        census[str(sc)]["t"]["fl"] = int(census_df["F_LIT"][ind])
        census[str(sc)]["t"]["pl"] = int(census_df["P_LIT"][ind])
        census[str(sc)]["t"]["mi"] = int(census_df["M_ILL"][ind])
        census[str(sc)]["t"]["fi"] = int(census_df["F_ILL"][ind])
        census[str(sc)]["t"]["pi"] = int(census_df["P_ILL"][ind])

    elif census_df["TRU"][ind].strip() == "Urban":
        census[str(sc)]["u"]["m"] = int(census_df["TOT_M"][ind])
        census[str(sc)]["u"]["f"] = int(census_df["TOT_F"][ind])
        census[str(sc)]["u"]["p"] = int(census_df["TOT_P"][ind])
        census[str(sc)]["u"]["ml"] = int(census_df["M_LIT"][ind])
        census[str(sc)]["u"]["fl"] = int(census_df["F_LIT"][ind])
        census[str(sc)]["u"]["pl"] = int(census_df["P_LIT"][ind])
        census[str(sc)]["u"]["mi"] = int(census_df["M_ILL"][ind])
        census[str(sc)]["u"]["fi"] = int(census_df["F_ILL"][ind])
        census[str(sc)]["u"]["pi"] = int(census_df["P_ILL"][ind])

    elif census_df["TRU"][ind].strip() == "Rural":
        census[str(sc)]["r"]["m"] = int(census_df["TOT_M"][ind])
        census[str(sc)]["r"]["f"] = int(census_df["TOT_F"][ind])
        census[str(sc)]["r"]["p"] = int(census_df["TOT_P"][ind])
        census[str(sc)]["r"]["ml"] = int(census_df["M_LIT"][ind])
        census[str(sc)]["r"]["fl"] = int(census_df["F_LIT"][ind])
        census[str(sc)]["r"]["pl"] = int(census_df["P_LIT"][ind])
        census[str(sc)]["r"]["mi"] = int(census_df["M_ILL"][ind])
        census[str(sc)]["r"]["fi"] = int(census_df["F_ILL"][ind])
        census[str(sc)]["r"]["pi"] = int(census_df["P_ILL"][ind])

# Extract Data From C13
def getAgeRangeDict():
    rDic = {}
    for r in config["AGE_LIM"]:
        rDic[r["RN"]] = {
            "u": {"m": 0, "f": 0, "p": 0},
            "r": {"m": 0, "f": 0, "p": 0},
            "t": {"m": 0, "f": 0, "p": 0}
        }
    rDic[config["AGE_MX"]] = {
        "u": {"m": 0, "f": 0, "p": 0},
        "r": {"m": 0, "f": 0, "p": 0},
        "t": {"m": 0, "f": 0, "p": 0}
    }
    rDic["Total"] = {
        "u": {"m": 0, "f": 0, "p": 0},
        "r": {"m": 0, "f": 0, "p": 0},
        "t": {"m": 0, "f": 0, "p": 0}
    }
    rDic["Age not stated"] = {
        "u": {"m": 0, "f": 0, "p": 0},
        "r": {"m": 0, "f": 0, "p": 0},
        "t": {"m": 0, "f": 0, "p": 0}
    }
    return rDic

agec13 = {}
for ind in agec13_df.index:
    sc = int(agec13_df["sc"][ind])
    agec13[str(sc)] = agec13.get(str(sc), getAgeRangeDict())
    try:
        age = int(agec13_df[1][ind])
        if age >= 70:
            agec13[str(sc)][config["AGE_MX"]]["t"]["p"] += int(agec13_df[2][ind])
            agec13[str(sc)][config["AGE_MX"]]["t"]["m"] += int(agec13_df[3][ind])
            agec13[str(sc)][config["AGE_MX"]]["t"]["f"] += int(agec13_df[4][ind])
            agec13[str(sc)][config["AGE_MX"]]["r"]["p"] += int(agec13_df[5][ind])
            agec13[str(sc)][config["AGE_MX"]]["r"]["m"] += int(agec13_df[6][ind])
            agec13[str(sc)][config["AGE_MX"]]["r"]["f"] += int(agec13_df[7][ind])
            agec13[str(sc)][config["AGE_MX"]]["u"]["p"] += int(agec13_df[8][ind])
            agec13[str(sc)][config["AGE_MX"]]["u"]["m"] += int(agec13_df[9][ind])
            agec13[str(sc)][config["AGE_MX"]]["u"]["f"] += int(agec13_df[10][ind])
        else:
            for r in config["AGE_LIM"]:
                if r["MX"] >= age and r["MN"] <= age:
                    agec13[str(sc)][r["RN"]]["t"]["p"] += int(agec13_df[2][ind])
                    agec13[str(sc)][r["RN"]]["t"]["m"] += int(agec13_df[3][ind])
                    agec13[str(sc)][r["RN"]]["t"]["f"] += int(agec13_df[4][ind])
                    agec13[str(sc)][r["RN"]]["r"]["p"] += int(agec13_df[5][ind])
                    agec13[str(sc)][r["RN"]]["r"]["m"] += int(agec13_df[6][ind])
                    agec13[str(sc)][r["RN"]]["r"]["f"] += int(agec13_df[7][ind])
                    agec13[str(sc)][r["RN"]]["u"]["p"] += int(agec13_df[8][ind])
                    agec13[str(sc)][r["RN"]]["u"]["m"] += int(agec13_df[9][ind])
                    agec13[str(sc)][r["RN"]]["u"]["f"] += int(agec13_df[10][ind])
                    break
    except:
        ikey = ""
        if agec13_df[1][ind].strip() == "100+":
            ikey = config["AGE_MX"]
        elif agec13_df[1][ind].strip() == "All ages":
            ikey = "Total"
        else:
            ikey = "Age not stated"
        agec13[str(sc)][ikey]["t"]["p"] += int(agec13_df[2][ind])
        agec13[str(sc)][ikey]["t"]["m"] += int(agec13_df[3][ind])
        agec13[str(sc)][ikey]["t"]["f"] += int(agec13_df[4][ind])
        agec13[str(sc)][ikey]["r"]["p"] += int(agec13_df[5][ind])
        agec13[str(sc)][ikey]["r"]["m"] += int(agec13_df[6][ind])
        agec13[str(sc)][ikey]["r"]["f"] += int(agec13_df[7][ind])
        agec13[str(sc)][ikey]["u"]["p"] += int(agec13_df[8][ind])
        agec13[str(sc)][ikey]["u"]["m"] += int(agec13_df[9][ind])
        agec13[str(sc)][ikey]["u"]["f"] += int(agec13_df[10][ind])

# Extract Data From C18
def getAgeRangeDictC18():
    rDic = {}
    for r in config["AGE_LIM"]:
        rDic[r["RN"]] = {
            "u": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "r": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "t": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0}
        }
    rDic[config["AGE_MX"]] = {
        "u": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
        "r": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
        "t": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0}
    }
    rDic["Total"] = {
        "u": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
        "r": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
        "t": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0}
    }
    rDic["Age not stated"] = {
        "u": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
        "r": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
        "t": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0}
    }
    return rDic

c18 = {}
for ind in age_df.index:
    sc = int(age_df["1"][ind])
    c18[str(sc)] = c18.get(str(sc), getAgeRangeDictC18())
    agrp = age_df["5"][ind].strip()
    if age_df["4"][ind].strip() == "Total":
        tcd = "t"
    elif age_df["4"][ind].strip() == "Rural":
        tcd = "r"
    else:
        tcd = "u"
    c18[str(sc)][agrp][tcd]["pE3"] = int(age_df["9"][ind])
    c18[str(sc)][agrp][tcd]["mE3"] = int(age_df["10"][ind])
    c18[str(sc)][agrp][tcd]["fE3"] = int(age_df["11"][ind])
    c18[str(sc)][agrp][tcd]["pE2"] = int(age_df["6"][ind]) - int(age_df["9"][ind])
    c18[str(sc)][agrp][tcd]["mE2"] = int(age_df["7"][ind]) - int(age_df["10"][ind])
    c18[str(sc)][agrp][tcd]["fE2"] = int(age_df["8"][ind]) - int(age_df["11"][ind])
    c18[str(sc)][agrp][tcd]["pE1"] = agec13[str(sc)][agrp][tcd]["p"] - int(age_df["6"][ind])
    c18[str(sc)][agrp][tcd]["mE1"] = agec13[str(sc)][agrp][tcd]["m"] - int(age_df["7"][ind])
    c18[str(sc)][agrp][tcd]["fE1"] = agec13[str(sc)][agrp][tcd]["f"] - int(age_df["8"][ind])

# Extract Data From C19
def getLiteracyDict():
    rDic = {
        "LIT": {
            "u": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "r": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "t": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0}
        },
        "ILL": {
            "u": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "r": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "t": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0}
        },
        "TOT": {
            "u": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "r": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0},
            "t": {"mE1": 0, "fE1": 0, "pE1": 0, "mE2": 0, "fE2": 0, "pE2": 0, "mE3": 0, "fE3": 0, "pE3": 0}
        }
    }
    return rDic

c19 = {}
for ind in lit_df.index:
    sc = int(lit_df["1"][ind])
    c19[str(sc)] = c19.get(str(sc), getLiteracyDict())
    if lit_df["4"][ind].strip() == "Total":
        tcd = "t"
    elif lit_df["4"][ind].strip() == "Rural":
        tcd = "r"
    else:
        tcd = "u"
    if lit_df["5"][ind].strip() == "Total":
        litgrp = "TOT"
        lit_m = "m"
        lit_f = "f"
        lit_p = "p"
    elif lit_df["5"][ind].strip() == "Literate":
        litgrp = "LIT"
        lit_m = "ml"
        lit_f = "fl"
        lit_p = "pl"
    elif lit_df["5"][ind].strip() == "Illiterate":
        litgrp = "ILL"
        lit_m = "mi"
        lit_f = "fi"
        lit_p = "pi"
    else:
        continue
    c19[str(sc)][litgrp][tcd]["pE3"] = int(lit_df["9"][ind])
    c19[str(sc)][litgrp][tcd]["mE3"] = int(lit_df["10"][ind])
    c19[str(sc)][litgrp][tcd]["fE3"] = int(lit_df["11"][ind])
    c19[str(sc)][litgrp][tcd]["pE2"] = int(lit_df["6"][ind]) - int(lit_df["9"][ind])
    c19[str(sc)][litgrp][tcd]["mE2"] = int(lit_df["7"][ind]) - int(lit_df["10"][ind])
    c19[str(sc)][litgrp][tcd]["fE2"] = int(lit_df["8"][ind]) - int(lit_df["11"][ind])
    c19[str(sc)][litgrp][tcd]["pE1"] = census[str(sc)][tcd][lit_p] - int(lit_df["6"][ind])
    c19[str(sc)][litgrp][tcd]["mE1"] = census[str(sc)][tcd][lit_m] - int(lit_df["7"][ind])
    c19[str(sc)][litgrp][tcd]["fE1"] = census[str(sc)][tcd][lit_f] - int(lit_df["8"][ind])

with open("meta/state_c17.json", "w") as stc17:
    json.dump(sttw, stc17, indent="\t")

with open("meta/census.json", "w") as cnss:
    json.dump(census, cnss, indent="\t")

with open("meta/age_c13.json", "w") as agc:
    json.dump(agec13, agc, indent="\t")

with open("meta/age_c18.json", "w") as agc18:
    json.dump(c18, agc18, indent="\t")

with open("meta/lit_c19.json", "w") as litc19:
    json.dump(c19, litc19, indent="\t")