import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/age_c18.json", "r") as agc18js:
    c18 = json.load(agc18js)

with open("meta/state_map.json", "r") as smp:
    state_map = json.load(smp)

with open("out/age-gender-a.csv", "w") as al3csv:
    lines = ["state/ut,age-group-males,ratio-males,age-group-females,ratio-females\n"]
    for i in range(config["SC_ULM"]):
        agrps_m = {}
        agrps_f = {}
        for agrp in c18[str(i)].keys():
            if agrp != "Total" and agrp != "Age not stated":
                # agrps_m[agrp] = c18[str(i)][agrp]["t"]["mE3"]/census[str(i)]["t"]["m"]
                # agrps_f[agrp] = c18[str(i)][agrp]["t"]["fE3"]/census[str(i)]["t"]["f"]
                agrps_m[agrp] = c18[str(i)][agrp]["t"]["mE3"]/(c18[str(i)][agrp]["t"]["mE3"] + c18[str(i)][agrp]["t"]["mE2"] + c18[str(i)][agrp]["t"]["mE1"])
                agrps_f[agrp] = c18[str(i)][agrp]["t"]["fE3"]/(c18[str(i)][agrp]["t"]["fE3"] + c18[str(i)][agrp]["t"]["fE2"] + c18[str(i)][agrp]["t"]["fE1"])
        agrps_m = dict(sorted(agrps_m.items(), key=lambda item: item[1], reverse=True))
        agrps_f = dict(sorted(agrps_f.items(), key=lambda item: item[1], reverse=True))
        agp_m = list(agrps_m.keys())
        agp_f = list(agrps_f.keys())
        # lines.append(f'{state_map[str(i)]},{agp_m[0]},{agrps_m[agp_m[0]]},{agp_f[0]},{agrps_f[agp_f[0]]}\n')
        lines.append(f'{str(i//10)+str(i%10)},{agp_m[0]},{agrps_m[agp_m[0]]},{agp_f[0]},{agrps_f[agp_f[0]]}\n')
    al3csv.writelines(lines)

with open("out/age-gender-b.csv", "w") as al2csv:
    lines = ["state/ut,age-group-males,ratio-males,age-group-females,ratio-females\n"]
    for i in range(config["SC_ULM"]):
        agrps_m = {}
        agrps_f = {}
        for agrp in c18[str(i)].keys():
            if agrp != "Total" and agrp != "Age not stated":
                # agrps_m[agrp] = c18[str(i)][agrp]["t"]["mE2"]/census[str(i)]["t"]["m"]
                # agrps_f[agrp] = c18[str(i)][agrp]["t"]["fE2"]/census[str(i)]["t"]["f"]
                agrps_m[agrp] = c18[str(i)][agrp]["t"]["mE2"]/(c18[str(i)][agrp]["t"]["mE3"] + c18[str(i)][agrp]["t"]["mE2"] + c18[str(i)][agrp]["t"]["mE1"])
                agrps_f[agrp] = c18[str(i)][agrp]["t"]["fE2"]/(c18[str(i)][agrp]["t"]["fE3"] + c18[str(i)][agrp]["t"]["fE2"] + c18[str(i)][agrp]["t"]["fE1"])
        agrps_m = dict(sorted(agrps_m.items(), key=lambda item: item[1], reverse=True))
        agrps_f = dict(sorted(agrps_f.items(), key=lambda item: item[1], reverse=True))
        agp_m = list(agrps_m.keys())
        agp_f = list(agrps_f.keys())
        # lines.append(f'{state_map[str(i)]},{agp_m[0]},{agrps_m[agp_m[0]]},{agp_f[0]},{agrps_f[agp_f[0]]}\n')
        lines.append(f'{str(i//10)+str(i%10)},{agp_m[0]},{agrps_m[agp_m[0]]},{agp_f[0]},{agrps_f[agp_f[0]]}\n')
    al2csv.writelines(lines)

with open("out/age-gender-c.csv", "w") as al1csv:
    lines = ["state/ut,age-group-males,ratio-males,age-group-females,ratio-females\n"]
    for i in range(config["SC_ULM"]):
        agrps_m = {}
        agrps_f = {}
        for agrp in c18[str(i)].keys():
            if agrp != "Total" and agrp != "Age not stated":
                # agrps_m[agrp] = c18[str(i)][agrp]["t"]["mE1"]/census[str(i)]["t"]["m"]
                # agrps_f[agrp] = c18[str(i)][agrp]["t"]["fE1"]/census[str(i)]["t"]["f"]
                agrps_m[agrp] = c18[str(i)][agrp]["t"]["mE1"]/(c18[str(i)][agrp]["t"]["mE3"] + c18[str(i)][agrp]["t"]["mE2"] + c18[str(i)][agrp]["t"]["mE1"])
                agrps_f[agrp] = c18[str(i)][agrp]["t"]["fE1"]/(c18[str(i)][agrp]["t"]["fE3"] + c18[str(i)][agrp]["t"]["fE2"] + c18[str(i)][agrp]["t"]["fE1"])
        agrps_m = dict(sorted(agrps_m.items(), key=lambda item: item[1], reverse=True))
        agrps_f = dict(sorted(agrps_f.items(), key=lambda item: item[1], reverse=True))
        agp_m = list(agrps_m.keys())
        agp_f = list(agrps_f.keys())
        # lines.append(f'{state_map[str(i)]},{agp_m[0]},{agrps_m[agp_m[0]]},{agp_f[0]},{agrps_f[agp_f[0]]}\n')
        lines.append(f'{str(i//10)+str(i%10)},{agp_m[0]},{agrps_m[agp_m[0]]},{agp_f[0]},{agrps_f[agp_f[0]]}\n')
    al1csv.writelines(lines)