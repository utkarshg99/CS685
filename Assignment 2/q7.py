import json

with open("meta/state_c17.json", "r") as sc17js:
    c17 = json.load(sc17js)

with open("meta/config.json", "r") as confjs:
    config = json.load(confjs)

regions = {}
for reg in config["REGIONS"].keys():
    regions[reg] = {}
    for i in config["REGIONS"][reg]:
        lngs = c17[str(i)]["lang"]
        for ln in lngs.keys():
            regions[reg][ln] = regions[reg].get(ln, 0) + c17[str(i)]["lang"][ln]["p"]


with open("out/region-india.csv", "w") as ricsv:
    lines = ["region,language-1,language-2,language-3\n"]
    for reg in config["REGIONS"].keys():
        dct = dict(sorted(regions[reg].items(), key=lambda item: item[1], reverse=True))
        lst = list(dct.keys())
        lines.append(reg+","+lst[0]+","+lst[1]+","+lst[2]+"\n")
    ricsv.writelines(lines)