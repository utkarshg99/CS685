import json, datetime, math

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

with open("meta/vaccine_weekly.json") as vcw:
    vacc_week = json.load(vcw)

ov1d = vacc_overall["1D"]
ov2d = vacc_overall["2D"]
ovm = vacc_overall["m"]
ovf = vacc_overall["f"]
week_nos = [int(k) for k in vacc_week.keys()]
frate = {dist: vacc_week[str(max(week_nos))][dist]["1D"]/7 for dist in districts_common}
pop_left = {dist: census[dist]["tot"] - ov1d[dist] for dist in districts_common}
f_dates = {}
st_stats = {}

for st in state_district_map.keys():
    startDate = datetime.datetime.strptime("08/14/21", "%m/%d/%y")
    st_stats[st] = {
        "popl": 0,
        "vacr": 0,
        "date": startDate
    }
    for dist in state_district_map[st]:
        if dist in districts_common:
            st_stats[st]["popl"] += pop_left[dist]
            st_stats[st]["vacr"] += frate[dist]
    if st_stats[st]["popl"] > 0:
        st_stats[st]["date"] = startDate + datetime.timedelta(days = math.ceil(st_stats[st]["popl"]/st_stats[st]["vacr"]))

with open("out/complete-vaccination.csv", "w") as cmpvac:
    lines = ["stateid,populationleft,rateofvaccination,date\n"]
    for st in st_stats.keys():
        lines.append(st+","+str(st_stats[st]["popl"])+","+str(st_stats[st]["vacr"])+","+st_stats[st]["date"].strftime('%d-%m-%Y')+"\n")
    cmpvac.writelines(lines)