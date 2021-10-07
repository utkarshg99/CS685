import json
import numpy as np

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/state_c17.json", "r") as stc17:
    sttw = json.load(stc17)

with open("out/gender-india.csv", "w") as picsv:
    lines = ["male-percentage,female-percentage,p-value\n"]
    pval = 0
    m_arr = []
    f_arr = []
    for i in range(1, config["SC_ULM"]):
        m_arr.append(sttw[str(i)]["t3"]["m"])
        f_arr.append(sttw[str(i)]["t3"]["f"])
    m_arr = np.array(m_arr)
    f_arr = np.array(f_arr)
    diff_mean = m_arr.mean() - f_arr.mean()
    vard = np.sqrt((m_arr.var() + f_arr.var()) / (config["SC_ULM"] - 2))
    pval = vard / diff_mean

    lines.append(str(sttw["0"]["t3"]["m"]/census["0"]["t"]["m"]*100)+","+
                str(sttw["0"]["t3"]["f"]/census["0"]["t"]["f"]*100)+","+str(pval)+"\n")
    picsv.writelines(lines)