import csv
import json
from collections import deque, OrderedDict

with open('data/neighbor-districts.json') as ndjson:
    nds = json.load(ndjson)

ndsmap_dist_keyed = {}
for key in nds.keys():
    ndsmap_dist_keyed[key.split('/')[0]] = key

dist_list = []
dist_key_list = {}
with open('data/district_wise.csv', newline='') as dswcsv:
    csvDict = csv.DictReader(dswcsv)
    for row in csvDict:
        if(int(row["SlNo"])!=0 and row["District"] != "Unknown"):
            dist_key_list[row["District"].lower().replace(" ", "_")] = row["District_Key"]
            dist_list.append(row["District"].lower().replace(" ", "_"))

qu1 = []
qu2 = []
qu3 = []
modjsn_raw = {}

for nds_dist in ndsmap_dist_keyed:
    if nds_dist in dist_list:
        qu1.clear()
        qu2 = deque([district.split('/')[0] for district in nds[ndsmap_dist_keyed[nds_dist]]])
        qu3 = [district.split('/')[0] for district in nds[ndsmap_dist_keyed[nds_dist]]]
        while(len(qu2) != 0):
            if qu2[0] == nds_dist:
                pass
            elif qu2[0] in dist_list:
                qu1.append(dist_key_list[qu2[0]])
            else:
                for d in nds[ndsmap_dist_keyed[qu2[0]]]:
                    if d.split('/')[0] not in qu3:
                        qu2.append(d.split('/')[0])
                        qu3.append(d.split('/')[0])
            qu2.popleft()
        modjsn_raw[dist_key_list[nds_dist]] = qu1[:]
        modjsn_raw[dist_key_list[nds_dist]].sort()

od_keys = list(modjsn_raw.keys())
od_keys.sort()
modjsn = OrderedDict()
for od_key in od_keys:
    modjsn[od_key] = modjsn_raw[od_key]

with open("out/neighbor-districts-modified.json", mode="w") as ndmjs:
    json.dump(modjsn, ndmjs, indent="\t")

with open("meta/dist_name_key.json", mode="w") as dsnk:
    json.dump(dist_key_list, dsnk, indent="\t")