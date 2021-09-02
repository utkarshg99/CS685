import csv, json, datetime

with open('out/neighbor-districts-modified.json') as ndjson:
    nds = json.load(ndjson)

with open('meta/dist_name_key.json') as dsnk:
    distnamekey = json.load(dsnk)

with open('district.csv', newline='') as dswcsv:
    csvDict = csv.DictReader(dswcsv)
    for row in csvDict:
        if(row["District"] != "Unknown"):
            pass