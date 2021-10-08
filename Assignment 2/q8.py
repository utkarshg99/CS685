import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/age_c18.json", "r") as agc18js:
    c18 = json.load(agc18js)

with open("meta/lit_c19_literate.json", "r") as litc19js:
    c19_lit = json.load(litc19js)

with open("meta/state_map.json", "r") as smp:
    state_map = json.load(smp)

with open("out/age-literacy-3.csv", "w") as al3csv:
    lines = ["state/ut,age-group,literacy-group,ratio-of-3\n"]
    for i in range(config["SC_ULM"]):
        agrps = {}
        lgrps = {}
        for agrp in c18[str(i)].keys():
            if agrp != "Total":
                agrps[agrp] = c18[str(i)][agrp]["t"]["pE3"]/census[str(i)]["t"]["p"]
        for lgrp in c19_lit[str(i)].keys():
            lgrps[lgrp] = c19_lit[str(i)][lgrp]["t"]["pE3"]/census[str(i)]["t"]["p"]
        agrps = dict(sorted(agrps.items(), key=lambda item: item[1], reverse=True))
        lgrps = dict(sorted(lgrps.items(), key=lambda item: item[1], reverse=True))
        agp = list(agrps.keys())
        lgp = list(lgrps.keys())
        lines.append(state_map[str(i)]+","+agp[0]+","+lgp[0]+","+str(agrps[agp[0]]*lgrps[lgp[0]])+"\n")
    al3csv.writelines(lines)

with open("out/age-literacy-2.csv", "w") as al2csv:
    lines = ["state/ut,age-group,literacy-group,ratio-of-2\n"]
    for i in range(config["SC_ULM"]):
        agrps = {}
        lgrps = {}
        for agrp in c18[str(i)].keys():
            if agrp != "Total":
                agrps[agrp] = c18[str(i)][agrp]["t"]["pE2"]/census[str(i)]["t"]["p"]
        for lgrp in c19_lit[str(i)].keys():
            lgrps[lgrp] = c19_lit[str(i)][lgrp]["t"]["pE2"]/census[str(i)]["t"]["p"]
        agrps = dict(sorted(agrps.items(), key=lambda item: item[1], reverse=True))
        lgrps = dict(sorted(lgrps.items(), key=lambda item: item[1], reverse=True))
        agp = list(agrps.keys())
        lgp = list(lgrps.keys())
        lines.append(state_map[str(i)]+","+agp[0]+","+lgp[0]+","+str(agrps[agp[0]]*lgrps[lgp[0]])+"\n")
    al2csv.writelines(lines)

with open("out/age-literacy-1.csv", "w") as al2csv:
    lines = ["state/ut,age-group,literacy-group,ratio-of-1\n"]
    for i in range(config["SC_ULM"]):
        agrps = {}
        lgrps = {}
        for agrp in c18[str(i)].keys():
            if agrp != "Total":
                agrps[agrp] = c18[str(i)][agrp]["t"]["pE1"]/census[str(i)]["t"]["p"]
        for lgrp in c19_lit[str(i)].keys():
            lgrps[lgrp] = c19_lit[str(i)][lgrp]["t"]["pE2"]/census[str(i)]["t"]["p"] # IMPORTANT
        agrps = dict(sorted(agrps.items(), key=lambda item: item[1], reverse=True))
        lgrps = dict(sorted(lgrps.items(), key=lambda item: item[1], reverse=True))
        agp = list(agrps.keys())
        lgp = list(lgrps.keys())
        lines.append(state_map[str(i)]+","+agp[0]+","+lgp[0]+","+str(agrps[agp[0]]*lgrps[lgp[0]])+"\n")
    al2csv.writelines(lines)