import json
import numpy as np

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/lit_c19_literate.json", "r") as litc19js:
    c19_lit = json.load(litc19js)

with open("meta/state_map.json", "r") as smp:
    state_map = json.load(smp)

with open("meta/c8_lit.json", "r") as c8_ld:
    c8_lit = json.load(c8_ld)

with open("out/literacy-india.csv", "w") as aicsv:
    lines = ["state/ut,literacy-group,percentage\n"]
    for i in range(config["SC_ULM"]):
        rest = {}
        for lgrp in c19_lit[str(i)].keys():
            if lgrp != "TOT":
                rest[lgrp] = c19_lit[str(i)][lgrp]["t"]["pE3"]/c8_lit[str(i)]["Total"][lgrp]["p"]
        rest = dict(sorted(rest.items(), key=lambda item: item[1], reverse=True))
        rkys = list(rest.keys())
        lines.append(str(i//10)+str(i%10)+","+rkys[0]+","+str(c19_lit[str(i)][rkys[0]]["t"]["pE3"]/c8_lit[str(i)]["Total"][rkys[0]]["p"]*100)+"\n")
    aicsv.writelines(lines)