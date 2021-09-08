import csv, json

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

with open('meta/covid_cases_vaccinated.json') as ccvjs:
    ccvdt = json.load(ccvjs)

states_dt = {}
dist_dt = {}
ov_covi = 0
ov_cova = 0

for k in ccvdt.keys():
    if ccvdt[k] != {}:
        vld = ccvdt[k].get("2021-08-14", {})
        vcv = vld.get("covishield", -1)
        vcx = vld.get("covaxin", -1)
        if vld != 0 and vcv != -1 and vcx != -1:
            ov_covi += vcv
            ov_cova += vcx
            dist_dt[k] = vcv/vcx if vcx != 0 else 1e9
            dkey = distnamekey[k]
            st_cd = dkey[:2]
            if states_dt.get(st_cd, {}) == {}:
                states_dt[st_cd] = {
                    "covi": vcv,
                    "cova": vcx,
                    "rat": dist_dt[k]
                }
            else:
                states_dt[st_cd]["covi"] += vcv
                states_dt[st_cd]["cova"] += vcx
                states_dt[st_cd]["rat"] = states_dt[st_cd]["covi"]/states_dt[st_cd]["cova"] if states_dt[st_cd]["cova"] != 0 else 1e9

ov = ov_covi/ov_cova
vacRatios = {
    "district": dist_dt,
    "state": states_dt,
    "overall": ov
}

distl = [(dist_dt[k], distnamekey[k]) for k in dist_dt.keys()]
statel = [(states_dt[k]["rat"], k) for k in states_dt.keys()]
distl.sort()
statel.sort()

with open("out/vaccine-type-ratio-district.csv", "w") as vctrd:
    lines = ["districtid,vaccineratio\n"]
    for d in distl:
        lines.append(d[1]+","+str(d[0])+"\n")
    vctrd.writelines(lines)

with open("out/vaccine-type-ratio-state.csv", "w") as vctrs:
    lines = ["stateid,vaccineratio\n"]
    for s in statel:
        lines.append(s[1]+","+str(s[0])+"\n")
    vctrs.writelines(lines)

with open("out/vaccine-type-ratio-overall.csv", "w") as vctro:
    vctro.writelines(["overallid,vaccineratio\n", "1,"+str(ov)+"\n"])

with open("meta/vacc_ratios.json", "w") as vcrjs:
    json.dump(vacRatios, vcrjs, indent="\t")