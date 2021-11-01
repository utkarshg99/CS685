import json
import numpy as np

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/state_c17.json", "r") as stc17:
    sttw = json.load(stc17)

with open("out/gender-india.csv", "w") as picsv:
    lines = ["state-code,male-percentage,female-percentage,p-value\n"]
    # pval = 0
    # m_arr = []
    # f_arr = []
    # for i in range(1, config["SC_ULM"]):
    #     m_arr.append(sttw[str(i)]["t3"]["m"])
    #     f_arr.append(sttw[str(i)]["t3"]["f"])
    # m_arr = np.array(m_arr)
    # f_arr = np.array(f_arr)
    # diff_mean = m_arr.mean() - f_arr.mean()
    # vard = np.sqrt((m_arr.var() + f_arr.var()) / (config["SC_ULM"] - 2))
    # pval = vard / diff_mean

    # lines.append(str(sttw["0"]["t3"]["m"]/census["0"]["t"]["m"]*100)+","+
    #             str(sttw["0"]["t3"]["f"]/census["0"]["t"]["f"]*100)+","+str(pval)+"\n")
    for i in range(config["SC_ULM"]):
        arr = np.array([sttw[str(i)]["t3"]["m"]/sttw[str(i)]["t3"]["f"], sttw[str(i)]["e2"]["m"]/sttw[str(i)]["e2"]["f"], sttw[str(i)]["e1"]["m"]/sttw[str(i)]["e1"]["f"]])
        b_arr = sttw[str(i)]["t1"]["m"]/sttw[str(i)]["t1"]["f"]*np.ones((3))
        diff_mean = arr.mean() - b_arr.mean()
        vard = np.sqrt((arr.var() + b_arr.var()) / (len(arr) + len(b_arr) - 2))
        pval = vard / diff_mean
        lines.append(f'{str(i)}{100*sttw[str(i)]["t3"]["m"]/sttw[str(i)]["t1"]["m"]},{100*sttw[str(i)]["t3"]["f"]/sttw[str(i)]["t1"]["f"]},{pval}\n')
    picsv.writelines(lines)