import csv, json
from os import waitpid

startDate = "16/01/2021"
endDate = "15/08/2021"
mnt_day = {"1":31,"2":28,"3":31,"4":30,"5":31,"6":30,"7":31,"8":31,"9":30,"10":31,"11":30,"12":31}
cvdcases = {}
wkdt = {}
mndt = {}
wk_typ1 = []
wk_typ2 = []
mnth = []
vaccdts = []
valdist = []

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

with open("meta/covid_cases.json") as ccjs:
    cvdcases = json.load(ccjs)

with open("meta/covid_cases_weekly.json") as cccjs:
    wkdt = json.load(cccjs)

with open("meta/covid_cases_monthly.json") as cccjs:
    mndt = json.load(cccjs)

with open("meta/week_month_map.json") as cccjs:
    wkmnmap = json.load(cccjs)
    wk_typ1 = wkmnmap["week_type1"]
    wk_typ2 = wkmnmap["week_type2"]
    mnth = wkmnmap["month"]

with open("cowin_vaccine_data_districtwise_modified.csv", newline='') as cvddm:
    csvDict = csv.DictReader(cvddm)
    for row in csvDict:
        d, m, y = 15, 1, 2021
        strDate = startDate
        dkey = row["District_Key"]
        dkey_internal = row["District"].lower().replace(" ", "_")
        valdist.append(dkey_internal)
        while strDate != endDate:
            d+=1
            if d > mnt_day[str(m)]:
                d=1
                m+=1
                if m > 12:
                    m=1
                    y+=1
            if m > 9 and d > 9:
                strDate = str(d)+"/"+str(m)+"/"+str(y) 
                strDate_internal = str(y)+"-"+str(m)+"-"+str(d)
            elif m > 9 and d <= 9:
                strDate = "0"+str(d)+"/"+str(m)+"/"+str(y)
                strDate_internal = str(y)+"-"+str(m)+"-0"+str(d)
            elif d > 9 and m <= 9:
                strDate = str(d)+"/0"+str(m)+"/"+str(y)
                strDate_internal = str(y)+"-0"+str(m)+"-"+str(d)
            else:
                strDate = "0"+str(d)+"/0"+str(m)+"/"+str(y)
                strDate_internal = str(y)+"-0"+str(m)+"-0"+str(d)
            cvdcases[dkey_internal][strDate_internal] = cvdcases[dkey_internal].get(strDate_internal, {})
            cvdcases[dkey_internal][strDate_internal]["indi"] = row.get(strDate+"_Total Individuals Registered", row.get(strDate+"_Total Individuals Vaccinated", 0))
            cvdcases[dkey_internal][strDate_internal]["sess"] = row[strDate+"_Sessions"]
            cvdcases[dkey_internal][strDate_internal]["sts"] = row[strDate+"_Sites "]
            cvdcases[dkey_internal][strDate_internal]["1D"] = row[strDate+"_First Dose Administered"]
            cvdcases[dkey_internal][strDate_internal]["2D"] = row[strDate+"_Second Dose Administered"]
            cvdcases[dkey_internal][strDate_internal]["m"] = row.get(strDate+"_Male(Individuals Vaccinated)", row.get(strDate+"_Male(Doses Administered)", 0))
            cvdcases[dkey_internal][strDate_internal]["f"] = row.get(strDate+"_Female(Individuals Vaccinated)", row.get(strDate+"_Female(Doses Administered)", 0))
            cvdcases[dkey_internal][strDate_internal]["trans"] = row.get(strDate+"_Transgender(Individuals Vaccinated)", row.get(strDate+"_Transgender(Doses Administered)", 0))
            cvdcases[dkey_internal][strDate_internal]["covaxin"] = row[strDate+"_Covaxin (Doses Administered)"]
            cvdcases[dkey_internal][strDate_internal]["covishield"] = row[strDate+"_CoviShield (Doses Administered)"]
            cvdcases[dkey_internal][strDate_internal]["indi"] = int(cvdcases[dkey_internal][strDate_internal]["indi"]) if cvdcases[dkey_internal][strDate_internal]["indi"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["sess"] = int(cvdcases[dkey_internal][strDate_internal]["sess"]) if cvdcases[dkey_internal][strDate_internal]["sess"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["sts"] = int(cvdcases[dkey_internal][strDate_internal]["sts"]) if cvdcases[dkey_internal][strDate_internal]["sts"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["1D"] = int(cvdcases[dkey_internal][strDate_internal]["1D"]) if cvdcases[dkey_internal][strDate_internal]["1D"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["2D"] = int(cvdcases[dkey_internal][strDate_internal]["2D"]) if cvdcases[dkey_internal][strDate_internal]["2D"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["m"] = int(cvdcases[dkey_internal][strDate_internal]["m"]) if cvdcases[dkey_internal][strDate_internal]["m"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["f"] = int(cvdcases[dkey_internal][strDate_internal]["f"]) if cvdcases[dkey_internal][strDate_internal]["f"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["trans"] = int(cvdcases[dkey_internal][strDate_internal]["trans"]) if cvdcases[dkey_internal][strDate_internal]["trans"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["covaxin"] = int(cvdcases[dkey_internal][strDate_internal]["covaxin"]) if cvdcases[dkey_internal][strDate_internal]["covaxin"] != '' else 0
            cvdcases[dkey_internal][strDate_internal]["covishield"] = int(cvdcases[dkey_internal][strDate_internal]["covishield"]) if cvdcases[dkey_internal][strDate_internal]["covishield"] != '' else 0
            vaccdts.append(strDate_internal.strip())

vaccdts = set(vaccdts)

for i in range(0, len(wk_typ1)-1):
    for k in valdist:
        wkdt[str(2*i+1)][k] = {}
        if wk_typ1[i] in vaccdts and wk_typ1[i+1] in vaccdts:
            # print(cvdcases[k].get(wk_typ1[i+1], {"indi": 0}), wk_typ1[i+1], k)
            wkdt[str(2*i+1)][k]["indi"] = cvdcases[k].get(wk_typ1[i+1], {"indi": 0})["indi"]-cvdcases[k].get(wk_typ1[i], {"indi": 0})["indi"]
            wkdt[str(2*i+1)][k]["m"] = cvdcases[k].get(wk_typ1[i+1], {"m": 0})["m"]-cvdcases[k].get(wk_typ1[i], {"m": 0})["m"]
            wkdt[str(2*i+1)][k]["f"] = cvdcases[k].get(wk_typ1[i+1], {"f": 0})["f"]-cvdcases[k].get(wk_typ1[i], {"f": 0})["f"]
            wkdt[str(2*i+1)][k]["trans"] = cvdcases[k].get(wk_typ1[i+1], {"trans": 0})["trans"]-cvdcases[k].get(wk_typ1[i], {"trans": 0})["trans"]
            wkdt[str(2*i+1)][k]["covaxin"] = cvdcases[k].get(wk_typ1[i+1], {"covaxin": 0})["covaxin"]-cvdcases[k].get(wk_typ1[i], {"covaxin": 0})["covaxin"]
            wkdt[str(2*i+1)][k]["covishield"] = cvdcases[k].get(wk_typ1[i+1], {"covishield": 0})["covishield"]-cvdcases[k].get(wk_typ1[i], {"covishield": 0})["covishield"]
            wkdt[str(2*i+1)][k]["1D"] = cvdcases[k].get(wk_typ1[i+1], {"1D": 0})["1D"]-cvdcases[k].get(wk_typ1[i], {"1D": 0})["1D"]
            wkdt[str(2*i+1)][k]["2D"] = cvdcases[k].get(wk_typ1[i+1], {"2D": 0})["2D"]-cvdcases[k].get(wk_typ1[i], {"2D": 0})["2D"]

for i in range(0, len(wk_typ2)-1):
    for k in valdist:
        wkdt[str(2*i+2)][k] = {}
        if wk_typ2[i] in vaccdts and wk_typ2[i+1] in vaccdts:
            wkdt[str(2*i+2)][k]["indi"] = cvdcases[k].get(wk_typ2[i+1], {"indi": 0})["indi"]-cvdcases[k].get(wk_typ2[i], {"indi": 0})["indi"]
            wkdt[str(2*i+2)][k]["m"] = cvdcases[k].get(wk_typ2[i+1], {"m": 0})["m"]-cvdcases[k].get(wk_typ2[i], {"m": 0})["m"]
            wkdt[str(2*i+2)][k]["f"] = cvdcases[k].get(wk_typ2[i+1], {"f": 0})["f"]-cvdcases[k].get(wk_typ2[i], {"f": 0})["f"]
            wkdt[str(2*i+2)][k]["trans"] = cvdcases[k].get(wk_typ2[i+1], {"trans": 0})["trans"]-cvdcases[k].get(wk_typ2[i], {"trans": 0})["trans"]
            wkdt[str(2*i+2)][k]["covaxin"] = cvdcases[k].get(wk_typ2[i+1], {"covaxin": 0})["covaxin"]-cvdcases[k].get(wk_typ2[i], {"covaxin": 0})["covaxin"]
            wkdt[str(2*i+2)][k]["covishield"] = cvdcases[k].get(wk_typ2[i+1], {"covishield": 0})["covishield"]-cvdcases[k].get(wk_typ2[i], {"covishield": 0})["covishield"]
            wkdt[str(2*i+2)][k]["1D"] = cvdcases[k].get(wk_typ2[i+1], {"1D": 0})["1D"]-cvdcases[k].get(wk_typ2[i], {"1D": 0})["1D"]
            wkdt[str(2*i+2)][k]["2D"] = cvdcases[k].get(wk_typ2[i+1], {"2D": 0})["2D"]-cvdcases[k].get(wk_typ2[i], {"2D": 0})["2D"]

for i in range(0, len(mnth)-1):
    for k in valdist:
        mndt[str(i+1)][k] = {}
        if mnth[i] in vaccdts and mnth[i+1] in vaccdts:
            mndt[str(i+1)][k]["indi"] = cvdcases[k].get(mnth[i+1], {"indi": 0})["indi"]-cvdcases[k].get(mnth[i], {"indi": 0})["indi"]
            mndt[str(i+1)][k]["m"] = cvdcases[k].get(mnth[i+1], {"m": 0})["m"]-cvdcases[k].get(mnth[i], {"m": 0})["m"]
            mndt[str(i+1)][k]["f"] = cvdcases[k].get(mnth[i+1], {"f": 0})["f"]-cvdcases[k].get(mnth[i], {"f": 0})["f"]
            mndt[str(i+1)][k]["trans"] = cvdcases[k].get(mnth[i+1], {"trans": 0})["trans"]-cvdcases[k].get(mnth[i], {"trans": 0})["trans"]
            mndt[str(i+1)][k]["covaxin"] = cvdcases[k].get(mnth[i+1], {"covaxin": 0})["covaxin"]-cvdcases[k].get(mnth[i], {"covaxin": 0})["covaxin"]
            mndt[str(i+1)][k]["covishield"] = cvdcases[k].get(mnth[i+1], {"covishield": 0})["covishield"]-cvdcases[k].get(mnth[i], {"covishield": 0})["covishield"]
            mndt[str(i+1)][k]["1D"] = cvdcases[k].get(mnth[i+1], {"1D": 0})["1D"]-cvdcases[k].get(mnth[i], {"1D": 0})["1D"]
            mndt[str(i+1)][k]["2D"] = cvdcases[k].get(mnth[i+1], {"2D": 0})["2D"]-cvdcases[k].get(mnth[i], {"2D": 0})["2D"]

with open("meta/vaccine_weekly.json", "w") as cccjs:
    json.dump(wkdt, cccjs, indent="\t")

with open("meta/vaccine_monthly.json", "w") as cccjs:
    json.dump(mndt, cccjs, indent="\t")

with open("meta/covid_cases_vaccinated.json", "w") as ccvjs:
    json.dump(cvdcases, ccvjs, indent="\t")

with open("out/vaccinated-count-week.csv", "w") as vcw:
    lines=["districtid,weekid,dose1,dose2\n"]
    dkeys = []
    for dkey_int in valdist:
        dkeys.append(distnamekey[dkey_int])
    dkeys.sort()
    for k in dkeys:
        for i in range(0, len(wkdt.keys())):
            dint = k[3:].lower().replace(" ", "_")
            lines.append(k+","+str(i+1)+","+str(wkdt[str(i+1)][dint].get("1D", 0))+","+str(wkdt[str(i+1)][dint].get("2D", 0))+"\n")
    vcw.writelines(lines)

with open("out/vaccinated-count-month.csv", "w") as mcw:
    lines=["districtid,monthid,dose1,dose2\n"]
    dkeys = []
    for dkey_int in valdist:
        dkeys.append(distnamekey[dkey_int])
    dkeys.sort()
    for k in dkeys:
        for i in range(0, len(mndt.keys())):
            dint = k[3:].lower().replace(" ", "_")
            lines.append(k+","+str(i+1)+","+str(mndt[str(i+1)][dint].get("1D", 0))+","+str(mndt[str(i+1)][dint].get("2D", 0))+"\n")
    mcw.writelines(lines)