import json

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

with open("meta/vaccine_overall.json") as vco:
    vacc_overall = json.load(vco)

with open("meta/state_district.json") as sdjs:
    state_district_map = json.load(sdjs)

with open("meta/census.json") as cns:
    census = json.load(cns)

with open("meta/census_vacc_common.json") as cvcjs:
    districts_common = json.load(cvcjs)

ov1d = vacc_overall["1D"]
ov2d = vacc_overall["2D"]
ovm = vacc_overall["m"]
ovf = vacc_overall["f"]
dkeys = []
d2_ratio = {dkey: ov2d[dkey]/census[dkey]["tot"] for dkey in districts_common}
d1_ratio = {dkey: ov1d[dkey]/census[dkey]["tot"] for dkey in districts_common}
sd1_ratio = {}
sd2_ratio = {}
onum1 = onum2 = oden = 0

for st in state_district_map:
    den = num1 = num2 = 0
    for dist in state_district_map[st]:
        if dist in districts_common:
            num1 += ov1d[dist]
            num2 += ov2d[dist]
            den += census[dist]["tot"]
            onum1 += ov1d[dist]
            onum2 += ov2d[dist]
            oden += census[dist]["tot"]
    sd1_ratio[st] = num1/den
    sd2_ratio[st] = num2/den

with open("out/vaccinated-dose-ratio-district.csv", "w") as vcdrd:
    lines = ["districtid,vaccinateddose1ratio,vaccinateddose2ratio\n"]
    lst = []
    for k in d1_ratio.keys():
        lst.append((d1_ratio[k], d2_ratio[k], distnamekey[k]))
    lst.sort()
    for l in lst:
        lines.append(l[2]+","+str(l[0])+","+str(l[1])+"\n")
    vcdrd.writelines(lines)

with open("out/vaccinated-dose-ratio-state.csv", "w") as vcdrs:
    lines = ["stateid,vaccinateddose1ratio,vaccinateddose2ratio\n"]
    lst = []
    for k in sd1_ratio.keys():
        lst.append((sd1_ratio[k], sd2_ratio[k], k))
    lst.sort()
    for l in lst:
        lines.append(l[2]+","+str(l[0])+","+str(l[1])+"\n")
    vcdrs.writelines(lines)

with open("out/vaccinated-dose-ratio-overall.csv", "w") as vcdro:
    lines = ["overallid,vaccinateddose1ratio,vaccinateddose2ratio\n", "1,"+str(onum1/oden)+","+str(onum2/oden)+"\n"]
    vcdro.writelines(lines)
