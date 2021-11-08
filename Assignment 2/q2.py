import json
import numpy as np
from scipy.stats import t as t_
from scipy.stats.stats import ttest_ind

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/state_c17.json", "r") as stc17:
    sttw = json.load(stc17)

with open("out/gender-india-c.csv", "w") as picsv_c:
    with open("out/gender-india-b.csv", "w") as picsv_b:
        with open("out/gender-india-a.csv", "w") as picsv_a:
            lines_a = ["state-code,male-percentage,female-percentage,p-value\n"]
            lines_b = ["state-code,male-percentage,female-percentage,p-value\n"]
            lines_c = ["state-code,male-percentage,female-percentage,p-value\n"]
            for i in range(config["SC_ULM"]):
                arr = np.array([sttw[str(i)]["t3"]["m"]/sttw[str(i)]["t3"]["f"], sttw[str(i)]["e2"]["m"]/sttw[str(i)]["e2"]["f"], sttw[str(i)]["e1"]["m"]/sttw[str(i)]["e1"]["f"]])
                b_arr = sttw[str(i)]["t1"]["m"]/sttw[str(i)]["t1"]["f"]*np.ones((3))
                diff_mean = arr.mean() - b_arr.mean()
                vard = np.sqrt(arr.var(ddof = 1)/len(arr) + b_arr.var(ddof = 1)/len(b_arr))
                tstat = diff_mean / vard
                df = (vard**4)/ (((arr.var(ddof = 1)/len(arr))**2/(len(arr)-1)) + ((b_arr.var(ddof = 1)/len(b_arr))**2)/(len(b_arr)-1))
                pval = (1 - t_.cdf(abs(tstat), df))*2
                lines_c.append(f'{str(i//10)+str(i%10)},{100*sttw[str(i)]["t3"]["m"]/sttw[str(i)]["t1"]["m"]},{100*sttw[str(i)]["t3"]["f"]/sttw[str(i)]["t1"]["f"]},{pval}\n')
                lines_b.append(f'{str(i//10)+str(i%10)},{100*sttw[str(i)]["e2"]["m"]/sttw[str(i)]["t1"]["m"]},{100*sttw[str(i)]["e2"]["f"]/sttw[str(i)]["t1"]["f"]},{pval}\n')
                lines_a.append(f'{str(i//10)+str(i%10)},{100*sttw[str(i)]["e1"]["m"]/sttw[str(i)]["t1"]["m"]},{100*sttw[str(i)]["e1"]["f"]/sttw[str(i)]["t1"]["f"]},{pval}\n')
            picsv_c.writelines(lines_c)
            picsv_b.writelines(lines_b)
            picsv_a.writelines(lines_a)