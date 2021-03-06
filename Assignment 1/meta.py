import csv, json

with open('data/neighbor-districts.json') as ndjson:
    nds = json.load(ndjson)

dlist1 = [nd.split("/")[0] for nd in nds.keys()]
dlist2 = []

state_code = {}
state_code_backmap = {}
state_to_dist = {}

with open('data/district_wise.csv', newline='') as dswcsv:
    csvDict = csv.DictReader(dswcsv)
    for row in csvDict:
        if int(row["SlNo"])!=0 and row["District"] != "Unknown":
            dlist2.append(row["District"].lower().replace(" ", "_"))
        if row["State_Code"] != "UN":
            state_code[row["State"]] = row["State_Code"]
            state_code_backmap[row["State_Code"]] = row["State"]
            if state_to_dist.get(row["State_Code"], 0) == 0:
                state_to_dist[row["State_Code"]] = []
            if int(row["SlNo"])!=0 and row["District"] != "Unknown":
                state_to_dist[row["State_Code"]].append(row["District"].lower().replace(" ", "_"))

# def editDistDP(str1, str2, m, n):
#     dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
#     for i in range(m + 1):
#         for j in range(n + 1):
#             if i == 0:
#                 dp[i][j] = j
#             elif j == 0:
#                 dp[i][j] = i
#             elif str1[i-1] == str2[j-1]:
#                 dp[i][j] = dp[i-1][j-1]
#             else:
#                 dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
#     return dp[m][n]

# for i in dlist1:
#     for j in dlist2:
#         if abs(editDistDP(i, j, len(i), len(j))) == 1:
#             if i not in dlist2:
#                 print(i+","+j)

with open("meta/state_codes.json", "w") as scdjs:
    json.dump(state_code, scdjs, indent="\t")

with open("meta/state_codes_backmap.json", "w") as scdjs:
    json.dump(state_code_backmap, scdjs, indent="\t")

with open("meta/state_district.json", "w") as scdjs:
    json.dump(state_to_dist, scdjs, indent="\t")