import csv, json

with open('out/neighbor-districts-modified.json') as ndjson:
    nds = json.load(ndjson)

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

with open("meta/state_codes.json") as stcdsjs:
    state_codes = json.load(stcdsjs)

convt_data={}
state_unk_detailed={}
lst = []
not_in_cowin = []
for k in distnamekey.keys():
    convt_data[k] = {}
for scd in state_codes.keys():
    state_unk_detailed[state_codes[scd]] = {}

with open('data/districts.csv', newline='') as dswcsv:
    csvDict = csv.DictReader(dswcsv)
    for row in csvDict:
        if(row["District"] != "Unknown"):
            if row["District"].lower().replace(" ", "_") in distnamekey.keys():
                convt_data[row["District"].lower().replace(" ", "_")][row["Date"]] = {
                    "con":int(row["Confirmed"]),
                    "rec":int(row["Recovered"]),
                    "det":int(row["Deceased"]),
                    "oth":int(row["Other"])
                }
            else:
                lst.append(row["District"].lower().replace(" ", "_"))
        else:
            state_unk_detailed[state_codes[row["State"]]][row["Date"]] = {
                "con":int(row["Confirmed"]),
                "rec":int(row["Recovered"]),
                "det":int(row["Deceased"]),
                "oth":int(row["Other"])
            }

for k in distnamekey.keys():
    if convt_data[k] == {}:
        not_in_cowin.append(k)

with open("meta/covid_cases.json", "w") as ccjs:
    json.dump(convt_data, ccjs, indent="\t")

startDate = "2020-03-13"
endDate = "2021-08-15"
d, m, y = 13, 3, 2020
mnt_day = {"1":31,"2":28,"3":31,"4":30,"5":31,"6":30,"7":31,"8":31,"9":30,"10":31,"11":30,"12":31}
str_date = startDate
w = 0
nds = 5
wkdt = {}
mndt = {}
ovdt = {}

wk_typ1 = []
wk_typ2 = []
mnth = []

state_unk = {
    "wk": {},
    "mn": {}
}

while str_date != endDate:
    d+=1
    if d > mnt_day[str(m)]:
        d=1
        m+=1
        if m > 12:
            m=1
            y+=1
    nds += 1
    w += 1 if nds > 7 else 0
    nds = 1 if nds > 7 else nds
    if m > 9 and d > 9:
        str_date = str(y)+"-"+str(m)+"-"+str(d) 
    elif m > 9 and d <= 9:
        str_date = str(y)+"-"+str(m)+"-0"+str(d)
    elif d > 9 and m <= 9:
        str_date = str(y)+"-0"+str(m)+"-"+str(d)
    else:
        str_date = str(y)+"-0"+str(m)+"-0"+str(d)
    if nds == 6:
        wk_typ1.append(str_date)
    if nds == 3:
        wk_typ2.append(str_date)
    if d == 14:
        mnth.append(str_date)

for i in range(0, len(wk_typ1)-1):
    wkdt[str(2*i+1)] = {}
    for k in distnamekey.keys():
        if k not in not_in_cowin:
            wkdt[str(2*i+1)][k] = convt_data[k].get(wk_typ1[i+1], {"con": 0})["con"]-convt_data[k].get(wk_typ1[i], {"con": 0})["con"]
    state_unk["wk"][str(2*i+1)] = {}
    for skey in state_unk_detailed.keys():
        if state_unk_detailed[skey].get(wk_typ1[i+1], {"con": 0})["con"] != 0:
            state_unk["wk"][str(2*i+1)][skey] = state_unk_detailed[skey].get(wk_typ1[i+1], {"con": 0})["con"]-state_unk_detailed[skey].get(wk_typ1[i], {"con": 0})["con"]
        else:
            state_unk["wk"][str(2*i+1)][skey] = 0

for i in range(0, len(wk_typ2)-1):
    wkdt[str(2*i+2)] = {}
    for k in distnamekey.keys():
        if k not in not_in_cowin:
            wkdt[str(2*i+2)][k] = convt_data[k].get(wk_typ2[i+1], {"con": 0})["con"]-convt_data[k].get(wk_typ2[i], {"con": 0})["con"]
    state_unk["wk"][str(2*i+2)] = {}
    for skey in state_unk_detailed.keys():
        if state_unk_detailed[skey].get(wk_typ2[i+1], {"con": 0})["con"] != 0:
            state_unk["wk"][str(2*i+2)][skey] = state_unk_detailed[skey].get(wk_typ2[i+1], {"con": 0})["con"]-state_unk_detailed[skey].get(wk_typ2[i], {"con": 0})["con"]
        else:
            state_unk["wk"][str(2*i+2)][skey] = 0

for i in range(0, len(mnth)-1):
    mndt[str(i+1)] = {}
    for k in distnamekey.keys():
        if k not in not_in_cowin:
            mndt[str(i+1)][k] = convt_data[k].get(mnth[i+1], {"con": 0})["con"]-convt_data[k].get(mnth[i], {"con": 0})["con"]
    state_unk["mn"][str(i+1)] = {}
    for skey in state_unk_detailed.keys():
        if state_unk_detailed[skey].get(mnth[i+1], {"con": 0})["con"] != 0:
            state_unk["mn"][str(i+1)][skey] = state_unk_detailed[skey].get(mnth[i+1], {"con": 0})["con"]-state_unk_detailed[skey].get(mnth[i], {"con": 0})["con"]
        else:
            state_unk["mn"][str(i+1)][skey] = 0

with open("meta/state_unknown.json", "w") as suk:
    json.dump(state_unk, suk, indent="\t")

with open("meta/covid_cases_weekly.json", "w") as cccjs:
    json.dump(wkdt, cccjs, indent="\t")

with open("meta/covid_cases_monthly.json", "w") as cccjs:
    json.dump(mndt, cccjs, indent="\t")

with open("meta/week_month_map.json", "w") as cccjs:
    json.dump({
        "week_type1": wk_typ1,
        "week_type2": wk_typ2,
        "month": mnth
    }, cccjs, indent="\t")

with open("out/cases-week.csv", "w") as cwcsv:
    lines = ["districtid,weekid,cases\n"]
    nwks = len(wkdt.keys())
    dsts = wkdt["1"].keys()
    for j in dsts:
        for k in range(1, nwks+1):
            if k%2 == 1:
                lines.append(distnamekey[j]+","+str(int((k+1)/2))+","+str(wkdt[str(k)][j])+"\n")
    cwcsv.writelines(lines)
    
with open("out/cases-month.csv", "w") as cmncsv:
    lines = ["districtid,monthid,cases\n"]
    nmns = len(mndt.keys())
    dsts = mndt["1"].keys()
    for j in dsts:
        for k in range(1, nmns+1):
            lines.append(distnamekey[j]+","+str(k)+","+str(mndt[str(k)][j])+"\n")
    cmncsv.writelines(lines)

with open("out/cases-overall.csv", "w") as covcsv:
    lines = ["districtid,overallid,cases\n"]
    dsts = mndt["1"].keys()
    for d in dsts:
        lines.append(distnamekey[d]+","+str(1)+","+str(convt_data[d].get("2021-08-14",{"con": 0})["con"] 
                    - convt_data[d].get("2020-03-14",{"con": 0})["con"])+"\n")
    covcsv.writelines(lines)