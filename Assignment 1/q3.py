import csv, json, datetime

with open('out/neighbor-districts-modified.json') as ndjson:
    nds = json.load(ndjson)

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

convt_data={}
lst = []
lst_tmp = []
for k in distnamekey.keys():
    convt_data[k] = {}

with open('districts.csv', newline='') as dswcsv:
    csvDict = csv.DictReader(dswcsv)
    for row in csvDict:
        if(row["District"] != "Unknown"):
            if row["District"].lower().replace(" ", "_") in distnamekey.keys():
                convt_data[row["District"].lower().replace(" ", "_")][row["Date"]] = {
                    "con":row["Confirmed"],
                    "rec":row["Recovered"],
                    "det":row["Deceased"],
                    "oth":row["Other"]
                }
            else:
                lst.append(row["District"].lower().replace(" ", "_"))

for k in distnamekey.keys():
    if convt_data[k] == {}:
        lst_tmp.append(k)

with open("meta/q3_log.txt", "w") as mq3:
    mq3.write(str(set(lst))+"\n")
    mq3.write(str(lst_tmp)+"\n")

with open("meta/covid_cases.json", "w") as ccjs:
    json.dump(convt_data, ccjs, indent="\t")