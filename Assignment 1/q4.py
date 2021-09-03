import csv, json

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