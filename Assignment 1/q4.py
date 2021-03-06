import csv
import json

WAVE_STABILITY_WEEKS = 21
WAVE_STABILITY_MONTHS = 2

with open('meta/covid_cases_weekly.json') as ccwkjs:
    cases_weekly_json = json.load(ccwkjs)

with open('meta/covid_cases_monthly.json') as ccmnjs:
    cases_monthly_json = json.load(ccmnjs)

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

val_dst = cases_monthly_json["1"].keys()
nwks = len(cases_weekly_json)
nmns = len(cases_monthly_json)

data_dst = {}
for d in val_dst:
    data_dst[d] = {
        "p1": {
            "wid": "0",
            "wcases": 0,
            "mcases": 0,
            "mid": "0"
        },
        "p2": {
            "wid": "0",
            "wcases": 0,
            "mcases": 0,
            "mid": "0"
        }
    }
    for i in range(2, nwks):
        if cases_weekly_json[str(i-1)][d] <= cases_weekly_json[str(i)][d] and cases_weekly_json[str(i+1)][d] <= cases_weekly_json[str(i)][d]:
            if data_dst[d]["p1"]["wcases"] < cases_weekly_json[str(i)][d]:
                if abs(i-int(data_dst[d]["p1"]["wid"])) > WAVE_STABILITY_WEEKS:
                    data_dst[d]["p2"]["wcases"] = data_dst[d]["p1"]["wcases"]
                    data_dst[d]["p2"]["wid"] = data_dst[d]["p1"]["wid"]
                data_dst[d]["p1"]["wid"] = str(i)
                data_dst[d]["p1"]["wcases"] = cases_weekly_json[str(i)][d]
            elif data_dst[d]["p2"]["wcases"] < cases_weekly_json[str(i)][d]:
                if abs(i-int(data_dst[d]["p1"]["wid"])) > WAVE_STABILITY_WEEKS:
                    data_dst[d]["p2"]["wid"] = str(i)
                    data_dst[d]["p2"]["wcases"] = cases_weekly_json[str(i)][d]
    for i in range(2, nmns):
        if cases_monthly_json[str(i-1)][d] <= cases_monthly_json[str(i)][d] and cases_monthly_json[str(i+1)][d] <= cases_monthly_json[str(i)][d]:
            if data_dst[d]["p1"]["mcases"] < cases_monthly_json[str(i)][d]:
                if abs(i-int(data_dst[d]["p1"]["mid"])) > WAVE_STABILITY_MONTHS:
                    data_dst[d]["p2"]["mcases"] = data_dst[d]["p1"]["mcases"]
                    data_dst[d]["p2"]["mid"] = data_dst[d]["p1"]["mid"]
                data_dst[d]["p1"]["mid"] = str(i)
                data_dst[d]["p1"]["mcases"] = cases_monthly_json[str(i)][d]
            elif data_dst[d]["p2"]["mcases"] < cases_monthly_json[str(i)][d]:
                if abs(i-int(data_dst[d]["p1"]["mid"])) > WAVE_STABILITY_MONTHS:
                    data_dst[d]["p2"]["mid"] = str(i)
                    data_dst[d]["p2"]["mcases"] = cases_monthly_json[str(i)][d]

with open("out/district-peaks.csv", "w") as dps:
    lines = ["districtid,wave1-weekid,wave2-weekid,wave1-monthid,wave2-monthid\n"]
    for d in val_dst:
        lines.append(distnamekey[d]+","+str(min(int(data_dst[d]["p1"]["wid"]), int(data_dst[d]["p2"]["wid"])))+","
                                    +str(max(int(data_dst[d]["p1"]["wid"]), int(data_dst[d]["p2"]["wid"])))+","
                                    +str(min(int(data_dst[d]["p1"]["mid"]), int(data_dst[d]["p2"]["mid"])))+","
                                    +str(max(int(data_dst[d]["p1"]["mid"]), int(data_dst[d]["p2"]["mid"])))+"\n")
    dps.writelines(lines)

case_st_w = {}
case_st_m = {}
st_dst = {}

for d in val_dst:
    skey = distnamekey[d].split("_")[0]
    if st_dst.get(skey, -1) == -1:
        case_st_w[skey] = {}
        case_st_m[skey] = {}
        st_dst[skey] = []
    st_dst[skey].append(d)

for i in range(1, nwks+1):
    for skey in st_dst.keys():
        for d in st_dst[skey]:
            case_st_w[skey][str(i)] = case_st_w[skey].get(str(i), 0) + cases_weekly_json[str(i)][d]

for i in range(1, nmns+1):
    for skey in st_dst.keys():
        for d in st_dst[skey]:
            case_st_m[skey][str(i)] = case_st_m[skey].get(str(i), 0) + cases_monthly_json[str(i)][d]

data_st = {}
for d in st_dst.keys():
    data_st[d] = {
        "p1": {
            "wid": "0",
            "wcases": 0,
            "mcases": 0,
            "mid": "0"
        },
        "p2": {
            "wid": "0",
            "wcases": 0,
            "mcases": 0,
            "mid": "0"
        }
    }
    for i in range(2, nwks):
        if case_st_w[d][str(i-1)] <= case_st_w[d][str(i)] and case_st_w[d][str(i+1)] <= case_st_w[d][str(i)]:
            if data_st[d]["p1"]["wcases"] < case_st_w[d][str(i)]:
                if abs(i-int(data_st[d]["p1"]["wid"])) > WAVE_STABILITY_WEEKS:
                    data_st[d]["p2"]["wcases"] = data_st[d]["p1"]["wcases"]
                    data_st[d]["p2"]["wid"] = data_st[d]["p1"]["wid"]
                data_st[d]["p1"]["wid"] = str(i)
                data_st[d]["p1"]["wcases"] = case_st_w[d][str(i)]
            elif data_st[d]["p2"]["wcases"] < case_st_w[d][str(i)]:
                if abs(i-int(data_st[d]["p1"]["wid"])) > WAVE_STABILITY_WEEKS:
                    data_st[d]["p2"]["wid"] = str(i)
                    data_st[d]["p2"]["wcases"] = case_st_w[d][str(i)]
    for i in range(2, nmns):
        if case_st_m[d][str(i-1)] <= case_st_m[d][str(i)] and case_st_m[d][str(i+1)] <= case_st_m[d][str(i)]:
            if data_st[d]["p1"]["mcases"] < case_st_m[d][str(i)]:
                if abs(i-int(data_st[d]["p1"]["mid"])) > WAVE_STABILITY_MONTHS:
                    data_st[d]["p2"]["mcases"] = data_st[d]["p1"]["mcases"]
                    data_st[d]["p2"]["mid"] = data_st[d]["p1"]["mid"]
                data_st[d]["p1"]["mid"] = str(i)
                data_st[d]["p1"]["mcases"] = case_st_m[d][str(i)]
            elif data_st[d]["p2"]["mcases"] < case_st_m[d][str(i)]:
                if abs(i-int(data_st[d]["p1"]["mid"])) > WAVE_STABILITY_MONTHS:
                    data_st[d]["p2"]["mid"] = str(i)
                    data_st[d]["p2"]["mcases"] = case_st_m[d][str(i)]

with open("out/state-peaks.csv", "w") as dps:
    lines = ["stateid,wave1-weekid,wave2-weekid,wave1-monthid,wave2-monthid\n"]
    for d in st_dst.keys():
        lines.append(d+","+str(min(int(data_st[d]["p1"]["wid"]), int(data_st[d]["p2"]["wid"])))+","
                                    +str(max(int(data_st[d]["p1"]["wid"]), int(data_st[d]["p2"]["wid"])))+","
                                    +str(min(int(data_st[d]["p1"]["mid"]), int(data_st[d]["p2"]["mid"])))+","
                                    +str(max(int(data_st[d]["p1"]["mid"]), int(data_st[d]["p2"]["mid"])))+"\n")
    dps.writelines(lines)

ov_weekly = {}
for i in range(1, nwks+1):
    ov_weekly[str(i)] = 0
    for csw in case_st_w.keys():
        ov_weekly[str(i)] += case_st_w[csw][str(i)]

ov_monthly = {}
for i in range(1, nmns+1):
    ov_monthly[str(i)] = 0
    for csm in case_st_m.keys():
        ov_monthly[str(i)] += case_st_m[csm][str(i)]

data_ov = {
    "p1": {
        "wid": "0",
        "wcases": 0,
        "mcases": 0,
        "mid": "0"
    },
    "p2": {
        "wid": "0",
        "wcases": 0,
        "mcases": 0,
        "mid": "0"
    }
}
for i in range(2, nwks):
    if ov_weekly[str(i-1)] <= ov_weekly[str(i)] and ov_weekly[str(i+1)] <= ov_weekly[str(i)]:
        if data_ov["p1"]["wcases"] < ov_weekly[str(i)]:
            if abs(i-int(data_ov["p1"]["wid"])) > WAVE_STABILITY_WEEKS:
                data_ov["p2"]["wcases"] = data_ov["p1"]["wcases"]
                data_ov["p2"]["wid"] = data_ov["p1"]["wid"]
            data_ov["p1"]["wid"] = str(i)
            data_ov["p1"]["wcases"] = ov_weekly[str(i)]
        elif data_ov["p2"]["wcases"] < ov_weekly[str(i)]:
            if abs(i-int(data_ov["p1"]["wid"])) > WAVE_STABILITY_WEEKS:
                data_ov["p2"]["wid"] = str(i)
                data_ov["p2"]["wcases"] = ov_weekly[str(i)]
for i in range(2, nmns):
    if ov_monthly[str(i-1)] <= ov_monthly[str(i)] and ov_monthly[str(i+1)] <= ov_monthly[str(i)]:
        if data_ov["p1"]["mcases"] < ov_monthly[str(i)]:
            if abs(i-int(data_ov["p1"]["mid"])) > WAVE_STABILITY_MONTHS:
                data_ov["p2"]["mcases"] = data_ov["p1"]["mcases"]
                data_ov["p2"]["mid"] = data_ov["p1"]["mid"]
            data_ov["p1"]["mid"] = str(i)
            data_ov["p1"]["mcases"] = ov_monthly[str(i)]
        elif data_ov["p2"]["mcases"] < ov_monthly[str(i)]:
            if abs(i-int(data_ov["p1"]["mid"])) > WAVE_STABILITY_MONTHS:
                data_ov["p2"]["mid"] = str(i)
                data_ov["p2"]["mcases"] = ov_monthly[str(i)]

with open("out/overall-peaks.csv", "w") as dps:
    lines = ["overallid,wave1-weekid,wave2-weekid,wave1-monthid,wave2-monthid\n"]
    lines.append(str(1)+","+str(min(int(data_ov["p1"]["wid"]), int(data_ov["p2"]["wid"])))+","
                                +str(max(int(data_ov["p1"]["wid"]), int(data_ov["p2"]["wid"])))+","
                                +str(min(int(data_ov["p1"]["mid"]), int(data_ov["p2"]["mid"])))+","
                                +str(max(int(data_ov["p1"]["mid"]), int(data_ov["p2"]["mid"])))+"\n")
    dps.writelines(lines)