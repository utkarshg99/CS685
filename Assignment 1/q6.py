import csv, json

dkeys = []
districts_census_all = []
districts_common = []
dist_vac_rat = {}
census = {}
dist_ratios = {}
state_ratios = {}
totm = totf = vm = vf =0

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

with open("meta/vaccine_overall.json") as vco:
    vacc_overall = json.load(vco)

with open("meta/state_district.json") as sdjs:
    state_district_map = json.load(sdjs)

ov1d = vacc_overall["1D"]
ov2d = vacc_overall["2D"]
ovm = vacc_overall["m"]
ovf = vacc_overall["f"]

for k in ov1d.keys():
    dkeys.append(k)

with open("census.csv", newline='') as ccsv:
    rows = csv.DictReader(ccsv)
    for row in rows:
        if row["Level"] == "DISTRICT" and row["TRU"] == "Total":
            if row["Name"].lower().replace(" ", "_") in dkeys:
                districts_common.append(row["Name"].lower().replace(" ", "_"))
            districts_census_all.append(row["Name"].lower().replace(" ", "_"))
            census[row["Name"].lower().replace(" ", "_")] = {
                "tot": int(row["TOT_P"]),
                "m": int(row["TOT_M"]),
                "f": int(row["TOT_F"])
            }

for dist in districts_common:
    dist_ratios[dist] = {
        "mfv": ovm[dist]/ovf[dist],
        "mfp": census[dist]["m"]/census[dist]["f"] 
    }
    dist_ratios[dist]["popr"] = dist_ratios[dist]["mfv"]/dist_ratios[dist]["mfp"]

for st in state_district_map.keys():
    state_ratios[st] = {
        "totm": 0,
        "totf": 0,
        "vm": 0,
        "vf": 0,
        "mfv": 0,
        "mfp": 0,
        "popr": 0
    }
    for dist in state_district_map[st]:
        if dist in districts_common:
            state_ratios[st]["totm"] += census[dist]["m"]
            state_ratios[st]["totf"] += census[dist]["f"]
            state_ratios[st]["vm"] += ovm[dist]
            state_ratios[st]["vf"] += ovf[dist]
            totm += census[dist]["m"]
            totf += census[dist]["f"]
            vm += ovm[dist]
            vf += ovf[dist]
    state_ratios[st]["mfv"] = state_ratios[st]["vm"]/state_ratios[st]["vf"] if state_ratios[st]["vf"] != 0 else 1e9
    state_ratios[st]["mfp"] = state_ratios[st]["totm"]/state_ratios[st]["totf"] if state_ratios[st]["totf"] != 0 else 1e9
    state_ratios[st]["popr"] = state_ratios[st]["mfv"]/state_ratios[st]["mfp"] if state_ratios[st]["mfp"] != 0 else 1e9

with open("out/district-vaccination-population-ratio.csv", "w") as vcprd:
    lines = ["districtid,vaccinationratio,populationratio,ratioofratios\n"]
    lst = []
    for dkey in dist_ratios.keys():
        lst.append((dist_ratios[dkey]["popr"], dkey))
    lst.sort()
    for l in lst:
        dkey = l[1]
        lines.append(distnamekey[dkey]+","+str(dist_ratios[dkey]["mfv"])+","+str(dist_ratios[dkey]["mfp"])+","+str(dist_ratios[dkey]["popr"])+"\n")
    vcprd.writelines(lines)

with open("out/state-vaccination-population-ratio.csv", "w") as vcprs:
    lines = ["stateid,vaccinationratio,populationratio,ratioofratios\n"]
    lst = []
    for skey in state_ratios.keys():
        lst.append((state_ratios[skey]["popr"], skey))
    lst.sort()
    for l in lst:
        skey = l[1]
        lines.append(skey+","+str(state_ratios[skey]["mfv"])+","+str(state_ratios[skey]["mfp"])+","+str(state_ratios[skey]["popr"])+"\n")
    vcprs.writelines(lines)

with open("out/overall-vaccination-population-ratio.csv", "w") as vcpro:
    lines = ["overallid,vaccinationratio,populationratio,ratioofratios\n", "1,"+str(vm/vf)+","+str(totm/totf)+","+str((vm/vf)/(totm/totf))+"\n"]
    vcpro.writelines(lines)

with open("meta/census.json", "w") as cns:
    json.dump(census, cns, indent="\t")

with open("meta/census_vacc_common.json", "w") as cnsv:
    json.dump(districts_common, cnsv, indent="\t")