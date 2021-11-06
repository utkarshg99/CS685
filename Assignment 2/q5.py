import json
import numpy as np

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/age_c18.json", "r") as agc18js:
    c18 = json.load(agc18js)

with open("meta/state_map.json", "r") as smp:
    state_map = json.load(smp)

with open("out/age-india.csv", "w") as aicsv:
    lines = ["state/ut,age-group,percentage\n"]
    for i in range(config["SC_ULM"]):
        rest = {}
        for agrp in c18[str(i)].keys():
            if agrp != "Total":
                rest[agrp] = c18[str(i)][agrp]["t"]["pE3"]
        rest = dict(sorted(rest.items(), key=lambda item: item[1], reverse=True))
        rkys = list(rest.keys())
        # lines.append(state_map[str(i)]+","+rkys[0]+","+str(c18[str(i)][rkys[0]]["t"]["pE3"]/census[str(i)]["t"]["p"]*100)+"\n")
        lines.append(str(i//10)+str(i%10)+","+rkys[0]+","+str(c18[str(i)][rkys[0]]["t"]["pE3"]/census[str(i)]["t"]["p"]*100)+"\n")
    aicsv.writelines(lines)