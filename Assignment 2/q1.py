import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/state_c17.json", "r") as stc17:
    sttw = json.load(stc17)

with open("out/percent-india.csv", "w") as picsv:
    # lines = ["state-code,1-language,2-language,3-language\n"]
    # for i in range(config["SC_ULM"]):
    #     lines.append(str(i)+","+str(sttw[str(i)]["e1"]["p"]/census[str(i)]["t"]["p"]*100)+","+
    #                 str(sttw[str(i)]["e2"]["p"]/census[str(i)]["t"]["p"]*100)+","+
    #                 str(sttw[str(i)]["t3"]["p"]/census[str(i)]["t"]["p"]*100)+"\n")
    lines = []
    lines.append(str(sttw["0"]["e1"]["p"]/census["0"]["t"]["p"]*100)+"\n")
    lines.append(str(sttw["0"]["e2"]["p"]/census["0"]["t"]["p"]*100)+"\n")
    lines.append(str(sttw["0"]["t3"]["p"]/census["0"]["t"]["p"]*100)+"\n")
    picsv.writelines(lines)