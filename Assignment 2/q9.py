import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/lit_c19_literate.json", "r") as litc19js:
    c19_lit = json.load(litc19js)

with open("meta/state_map.json", "r") as smp:
    state_map = json.load(smp)

with open("out/literacy-gender-3.csv", "w") as al3csv:
    lines = ["state/ut,literacy-group,males,literacy-group,females\n"]
    for i in range(config["SC_ULM"]):
        lgrps_m = {}
        lgrps_f = {}
        for lgrp in c19_lit[str(i)].keys():
            if lgrp != "Total":
                lgrps_m[lgrp] = c19_lit[str(i)][lgrp]["t"]["mE3"]/census[str(i)]["t"]["m"]
                lgrps_f[lgrp] = c19_lit[str(i)][lgrp]["t"]["fE3"]/census[str(i)]["t"]["f"]
        lgrps_m = dict(sorted(lgrps_m.items(), key=lambda item: item[1], reverse=True))
        lgrps_f = dict(sorted(lgrps_f.items(), key=lambda item: item[1], reverse=True))
        lgp_m = list(lgrps_m.keys())
        lgp_f = list(lgrps_f.keys())
        lines.append(f'{state_map[str(i)]},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
    al3csv.writelines(lines)

with open("out/literacy-gender-2.csv", "w") as al2csv:
    lines = ["state/ut,literacy-group,males,literacy-group,females\n"]
    for i in range(config["SC_ULM"]):
        lgrps_m = {}
        lgrps_f = {}
        for lgrp in c19_lit[str(i)].keys():
            if lgrp != "Total":
                lgrps_m[lgrp] = c19_lit[str(i)][lgrp]["t"]["mE2"]/census[str(i)]["t"]["m"]
                lgrps_f[lgrp] = c19_lit[str(i)][lgrp]["t"]["fE2"]/census[str(i)]["t"]["f"]
        lgrps_m = dict(sorted(lgrps_m.items(), key=lambda item: item[1], reverse=True))
        lgrps_f = dict(sorted(lgrps_f.items(), key=lambda item: item[1], reverse=True))
        lgp_m = list(lgrps_m.keys())
        lgp_f = list(lgrps_f.keys())
        lines.append(f'{state_map[str(i)]},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
    al2csv.writelines(lines)

# with open("out/literacy-gender-1.csv", "w") as al1csv:
#     lines = ["state/ut,literacy-group,males,literacy-group,females\n"]
#     for i in range(config["SC_ULM"]):
#         lgrps_m = {}
#         lgrps_f = {}
#         for lgrp in c19_lit[str(i)].keys():
#             if lgrp != "Total":
#                 lgrps_m[lgrp] = (census[str(i)]["t"]["ml"] - c19_lit[str(i)][lgrp]["t"]["mE2"] - c19_lit[str(i)][lgrp]["t"]["mE3"])/census[str(i)]["t"]["m"]
#                 lgrps_f[lgrp] = (census[str(i)]["t"]["fl"] - c19_lit[str(i)][lgrp]["t"]["fE2"] - c19_lit[str(i)][lgrp]["t"]["fE3"])/census[str(i)]["t"]["f"]
#         lgrps_m = dict(sorted(lgrps_m.items(), key=lambda item: item[1], reverse=True))
#         lgrps_f = dict(sorted(lgrps_f.items(), key=lambda item: item[1], reverse=True))
#         lgp_m = list(lgrps_m.keys())
#         lgp_f = list(lgrps_f.keys())
#         lines.append(f'{state_map[str(i)]},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
#     al1csv.writelines(lines)