import csv, json

with open("cowin_vaccine_data_districtwise.csv") as cvdd:
    l1 = cvdd.readline().split(",")
    l2 = cvdd.readline().split(",")
    for i in range(len(l1)):
        if l2[i] != "":
            l1[i] = l1[i].strip() + "_" + l2[i]
    l1 = ",".join(l1)
    lx = cvdd.readlines()
    lx.insert(0, l1)
    with open("cowin_vaccine_data_districtwise_modified.csv", "w") as cvddm:
        cvddm.writelines(lx)



ab_states = []
ba_states = []
ab_districts = []
ba_districts = []
states = []
districts = []
state_code = {}

with open("meta/state_codes.json") as scjs:
    state_code_base = json.load(scjs)

with open("meta/covid_cases.json") as ccjs:
    ccases = json.load(ccjs)

with open("census.csv", newline='') as ccsv:
    rows = csv.DictReader(ccsv)
    for row in rows:
        if row["Level"] == "STATE" and row["TRU"] == "Total":
            if row["Name"].lower().replace(" ", "_") not in state_code.keys():
                ab_states.append(row["Name"].lower().replace(" ", "_"))
            states.append(row["Name"].lower().replace(" ", "_"))
        if row["Level"] == "DISTRICT" and row["TRU"] == "Total":
            if row["Name"].lower().replace(" ", "_") not in ccases.keys():
                ab_districts.append(row["Name"].lower().replace(" ", "_"))
            districts.append(row["Name"].lower().replace(" ", "_"))

for k in ccases.keys():
    if k not in districts:
        ba_districts.append(k)

subset_dist = []
edit_dist = []

def editDistDP(str1, str2, m, n):
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[m][n]

for i in ab_districts:
    for j in ba_districts:
        if i in j or j in i:
            subset_dist.append((i, j))
        if abs(editDistDP(i, j, len(i), len(j))) == 3:
            edit_dist.append((i, j))

print(ab_states)
print(ba_states)
print(ab_districts)
print(ba_districts)
print(subset_dist)
print(edit_dist)
print(len(subset_dist))
print(len(edit_dist))
print(len(ab_districts))
print(len(ba_districts))