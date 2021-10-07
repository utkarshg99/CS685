import json
import numpy as np

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/age_c18.json", "r") as c18js:
    c18 = json.load(c18js)

with open("out/geography-india.csv", "w") as picsv:
    lines = ["urban-percentage,rural-percentage,p-value\n"]
    pval = 0
    u_arr = []
    r_arr = []
    for i in range(1, config["SC_ULM"]):
        u_arr.append(c18[str(i)]["Total"]["u"]["pE3"])
        r_arr.append(c18[str(i)]["Total"]["r"]["pE3"])
    u_arr = np.array(u_arr)
    r_arr = np.array(r_arr)
    diff_mean = u_arr.mean() - r_arr.mean()
    vard = np.sqrt((u_arr.var() + r_arr.var()) / (config["SC_ULM"] - 2))
    pval = vard / diff_mean

    lines.append(str(c18["0"]["Total"]["u"]["pE3"]/census["0"]["u"]["p"]*100)+","+
                str(c18["0"]["Total"]["r"]["pE3"]/census["0"]["r"]["p"]*100)+","+str(pval)+"\n")
    picsv.writelines(lines)