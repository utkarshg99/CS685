import json
import numpy as np

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/age_c18.json", "r") as c18js:
    c18 = json.load(c18js)

with open("out/geography-india.csv", "w") as picsv:
    lines = ["state-code,urban-percentage,rural-percentage,p-value\n"]
    # pval = 0
    # u_arr = []
    # r_arr = []
    # for i in range(1, config["SC_ULM"]):
    #     u_arr.append(c18[str(i)]["Total"]["u"]["pE3"])
    #     r_arr.append(c18[str(i)]["Total"]["r"]["pE3"])
    # u_arr = np.array(u_arr)
    # r_arr = np.array(r_arr)
    # diff_mean = u_arr.mean() - r_arr.mean()
    # vard = np.sqrt((u_arr.var() + r_arr.var()) / (config["SC_ULM"] - 2))
    # pval = vard / diff_mean

    # lines.append(str(c18["0"]["Total"]["u"]["pE3"]/census["0"]["u"]["p"]*100)+","+
    #             str(c18["0"]["Total"]["r"]["pE3"]/census["0"]["r"]["p"]*100)+","+str(pval)+"\n")
    # picsv.writelines(lines)
    for i in range(config["SC_ULM"]):
        u_tot = c18[str(i)]["Total"]["u"]["pE1"]+c18[str(i)]["Total"]["u"]["pE2"]+c18[str(i)]["Total"]["u"]["pE3"]
        r_tot = c18[str(i)]["Total"]["r"]["pE1"]+c18[str(i)]["Total"]["r"]["pE2"]+c18[str(i)]["Total"]["r"]["pE3"]
        arr = np.array([c18[str(i)]["Total"]["u"]["pE3"]/c18[str(i)]["Total"]["r"]["pE3"], c18[str(i)]["Total"]["u"]["pE2"]/c18[str(i)]["Total"]["r"]["pE2"], c18[str(i)]["Total"]["u"]["pE1"]/c18[str(i)]["Total"]["r"]["pE1"]])
        b_arr = u_tot/r_tot*np.ones((3))
        diff_mean = arr.mean() - b_arr.mean()
        vard = np.sqrt((arr.var() + b_arr.var()) / (len(arr) + len(b_arr) - 2))
        pval = vard / diff_mean
        lines.append(f'{str(i)}{100*c18[str(i)]["Total"]["u"]["pE3"]/u_tot},{100*c18[str(i)]["Total"]["r"]["pE3"]/r_tot},{pval}\n')
    picsv.writelines(lines)