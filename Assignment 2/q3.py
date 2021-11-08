import json
import numpy as np
from scipy.stats import t as t_

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/age_c18.json", "r") as c18js:
    c18 = json.load(c18js)

with open("out/geography-india-a.csv", "w") as picsv_a:
    with open("out/geography-india-b.csv", "w") as picsv_b:
        with open("out/geography-india-c.csv", "w") as picsv_c:
            lines_c = ["state-code,urban-percentage,rural-percentage,p-value\n"]
            lines_b = ["state-code,urban-percentage,rural-percentage,p-value\n"]
            lines_a = ["state-code,urban-percentage,rural-percentage,p-value\n"]
            for i in range(config["SC_ULM"]):
                u_tot = c18[str(i)]["Total"]["u"]["pE1"]+c18[str(i)]["Total"]["u"]["pE2"]+c18[str(i)]["Total"]["u"]["pE3"]
                r_tot = c18[str(i)]["Total"]["r"]["pE1"]+c18[str(i)]["Total"]["r"]["pE2"]+c18[str(i)]["Total"]["r"]["pE3"]
                arr = np.array([c18[str(i)]["Total"]["u"]["pE3"]/c18[str(i)]["Total"]["r"]["pE3"], c18[str(i)]["Total"]["u"]["pE2"]/c18[str(i)]["Total"]["r"]["pE2"], c18[str(i)]["Total"]["u"]["pE1"]/c18[str(i)]["Total"]["r"]["pE1"]])
                b_arr = u_tot/r_tot*np.ones((3))
                diff_mean = arr.mean() - b_arr.mean()
                vard = np.sqrt(arr.var(ddof = 1)/len(arr) + b_arr.var(ddof = 1)/len(b_arr))
                tstat = diff_mean / vard
                df = (vard**4)/ ((arr.var(ddof = 1)/len(arr)**2/(len(arr)-1)) + ((b_arr.var(ddof = 1)/len(b_arr))**2)/(len(b_arr)-1))
                pval = (1 - t_.cdf(abs(tstat), df))*2
                lines_c.append(f'{str(i//10)+str(i%10)},{100*c18[str(i)]["Total"]["u"]["pE3"]/u_tot},{100*c18[str(i)]["Total"]["r"]["pE3"]/r_tot},{pval}\n')
                lines_b.append(f'{str(i//10)+str(i%10)},{100*c18[str(i)]["Total"]["u"]["pE2"]/u_tot},{100*c18[str(i)]["Total"]["r"]["pE2"]/r_tot},{pval}\n')
                lines_a.append(f'{str(i//10)+str(i%10)},{100*c18[str(i)]["Total"]["u"]["pE1"]/u_tot},{100*c18[str(i)]["Total"]["r"]["pE1"]/r_tot},{pval}\n')
            picsv_c.writelines(lines_c)
            picsv_b.writelines(lines_b)
            picsv_a.writelines(lines_a)