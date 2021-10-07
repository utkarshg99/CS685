import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/state_c17.json", "r") as stc17:
    sttw = json.load(stc17)

with open("meta/state_map.json", "r") as smp:
    state_map = json.load(smp)

rat3to2 = {}
rat2to1 = {}
for i in range(1, config["SC_ULM"]):
    rat3to2[str(i)] = sttw[str(i)]["t3"]["p"] / sttw[str(i)]["e2"]["p"]
    rat2to1[str(i)] = sttw[str(i)]["e2"]["p"] / sttw[str(i)]["e1"]["p"]
rat3to2 = dict(sorted(rat3to2.items(), key=lambda item: item[1]))
rat2to1 = dict(sorted(rat2to1.items(), key=lambda item: item[1]))

with open("out/3-to-2-ratio.csv", "w") as picsv:
    lines = []
    kys = list(rat3to2.keys())
    lines.append(state_map[kys[-1]] + "\n")
    lines.append(state_map[kys[-2]] + "\n")
    lines.append(state_map[kys[-3]] + "\n")
    lines.append(state_map[kys[0]] + "\n")
    lines.append(state_map[kys[1]] + "\n")
    lines.append(state_map[kys[2]] + "\n")
    picsv.writelines(lines)

with open("out/2-to-1-ratio.csv", "w") as picsv:
    lines = []
    kys = list(rat2to1.keys())
    lines.append(state_map[kys[-1]] + "\n")
    lines.append(state_map[kys[-2]] + "\n")
    lines.append(state_map[kys[-3]] + "\n")
    lines.append(state_map[kys[0]] + "\n")
    lines.append(state_map[kys[1]] + "\n")
    lines.append(state_map[kys[2]] + "\n")
    picsv.writelines(lines)