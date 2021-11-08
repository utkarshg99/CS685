import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/lit_c19_literate.json", "r") as litc19js:
    c19_lit = json.load(litc19js)

with open("meta/lit_c19.json", "r") as litc19js:
    c19_illit = json.load(litc19js)

with open("meta/state_map.json", "r") as smp:
    state_map = json.load(smp)

with open("meta/c8_lit.json", "r") as c8_ld:
    c8_lit = json.load(c8_ld)

with open("out/literacy-gender-a.csv", "w") as al3csv:
    lines = ["state/ut,literacy-group-males,ratio-males,literacy-group-females,ratio-females\n"]
    for i in range(config["SC_ULM"]):
        lgrps_m = {}
        lgrps_f = {}
        for lgrp in c19_lit[str(i)].keys():
            if lgrp != "Total":
                lgrps_m[lgrp] = c19_lit[str(i)][lgrp]["t"]["mE3"]/c8_lit[str(i)]["Total"][lgrp]["m"]
                lgrps_f[lgrp] = c19_lit[str(i)][lgrp]["t"]["fE3"]/c8_lit[str(i)]["Total"][lgrp]["f"]
        lgrps_m["Illiterate"] = c19_illit[str(i)]["ILL"]["t"]["mE3"]/(c19_illit[str(i)]["ILL"]["t"]["mE3"] + c19_illit[str(i)]["ILL"]["t"]["mE2"] + c19_illit[str(i)]["ILL"]["t"]["mE1"])
        lgrps_f["Illiterate"] = c19_illit[str(i)]["ILL"]["t"]["fE3"]/(c19_illit[str(i)]["ILL"]["t"]["fE3"] + c19_illit[str(i)]["ILL"]["t"]["fE2"] + c19_illit[str(i)]["ILL"]["t"]["fE1"])
        lgrps_m = dict(sorted(lgrps_m.items(), key=lambda item: item[1], reverse=True))
        lgrps_f = dict(sorted(lgrps_f.items(), key=lambda item: item[1], reverse=True))
        lgp_m = list(lgrps_m.keys())
        lgp_f = list(lgrps_f.keys())
        # lines.append(f'{state_map[str(i)]},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
        lines.append(f'{str(i//10)+str(i%10)},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
    al3csv.writelines(lines)

with open("out/literacy-gender-b.csv", "w") as al2csv:
    lines = ["state/ut,literacy-group-males,ratio-males,literacy-group-females,ratio-females\n"]
    for i in range(config["SC_ULM"]):
        lgrps_m = {}
        lgrps_f = {}
        for lgrp in c19_lit[str(i)].keys():
            if lgrp != "Total":
                lgrps_m[lgrp] = c19_lit[str(i)][lgrp]["t"]["mE2"]/c8_lit[str(i)]["Total"][lgrp]["m"]
                lgrps_f[lgrp] = c19_lit[str(i)][lgrp]["t"]["fE2"]/c8_lit[str(i)]["Total"][lgrp]["f"]
        lgrps_m["Illiterate"] = c19_illit[str(i)]["ILL"]["t"]["mE2"]/(c19_illit[str(i)]["ILL"]["t"]["mE3"] + c19_illit[str(i)]["ILL"]["t"]["mE2"] + c19_illit[str(i)]["ILL"]["t"]["mE1"])
        lgrps_f["Illiterate"] = c19_illit[str(i)]["ILL"]["t"]["fE2"]/(c19_illit[str(i)]["ILL"]["t"]["fE3"] + c19_illit[str(i)]["ILL"]["t"]["fE2"] + c19_illit[str(i)]["ILL"]["t"]["fE1"])
        lgrps_m = dict(sorted(lgrps_m.items(), key=lambda item: item[1], reverse=True))
        lgrps_f = dict(sorted(lgrps_f.items(), key=lambda item: item[1], reverse=True))
        lgp_m = list(lgrps_m.keys())
        lgp_f = list(lgrps_f.keys())
        # lines.append(f'{state_map[str(i)]},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
        lines.append(f'{str(i//10)+str(i%10)},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
    al2csv.writelines(lines)

with open("out/literacy-gender-c.csv", "w") as al1csv:
    lines = ["state/ut,literacy-group-males,ratio-males,literacy-group-females,ratio-females\n"]
    for i in range(config["SC_ULM"]):
        lgrps_m = {}
        lgrps_f = {}
        for lgrp in c19_lit[str(i)].keys():
            if lgrp != "Total":
                lgrps_m[lgrp] = (c8_lit[str(i)]["Total"][lgrp]["m"] - c19_lit[str(i)][lgrp]["t"]["mE2"] - c19_lit[str(i)][lgrp]["t"]["mE3"])/c8_lit[str(i)]["Total"][lgrp]["m"]
                lgrps_f[lgrp] = (c8_lit[str(i)]["Total"][lgrp]["f"] - c19_lit[str(i)][lgrp]["t"]["fE2"] - c19_lit[str(i)][lgrp]["t"]["fE3"])/c8_lit[str(i)]["Total"][lgrp]["f"]
        lgrps_m["Illiterate"] = c19_illit[str(i)]["ILL"]["t"]["mE1"]/(c19_illit[str(i)]["ILL"]["t"]["mE3"] + c19_illit[str(i)]["ILL"]["t"]["mE2"] + c19_illit[str(i)]["ILL"]["t"]["mE1"])
        lgrps_f["Illiterate"] = c19_illit[str(i)]["ILL"]["t"]["fE1"]/(c19_illit[str(i)]["ILL"]["t"]["fE3"] + c19_illit[str(i)]["ILL"]["t"]["fE2"] + c19_illit[str(i)]["ILL"]["t"]["fE1"])
        lgrps_m = dict(sorted(lgrps_m.items(), key=lambda item: item[1], reverse=True))
        lgrps_f = dict(sorted(lgrps_f.items(), key=lambda item: item[1], reverse=True))
        lgp_m = list(lgrps_m.keys())
        lgp_f = list(lgrps_f.keys())
        # lines.append(f'{state_map[str(i)]},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
        lines.append(f'{str(i//10)+str(i%10)},{lgp_m[0]},{lgrps_m[lgp_m[0]]},{lgp_f[0]},{lgrps_f[lgp_f[0]]}\n')
    al1csv.writelines(lines)