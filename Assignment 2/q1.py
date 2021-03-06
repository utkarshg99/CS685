import json

with open("meta/config.json", "r") as mcjs:
    config = json.load(mcjs)

with open("meta/census.json", "r") as cnss:
    census = json.load(cnss)

with open("meta/state_c17.json", "r") as stc17:
    sttw = json.load(stc17)

with open("out/percent-india.csv", "w") as picsv:
    lines = ["state-code,percent-one,percent-two,percent-three\n"]
    for i in range(config["SC_ULM"]):
        lines.append(f'{str(i//10)+str(i%10)},{sttw[str(i)]["e1"]["p"]/census[str(i)]["t"]["p"]*100},{sttw[str(i)]["e2"]["p"]/census[str(i)]["t"]["p"]*100},{sttw[str(i)]["t3"]["p"]/census[str(i)]["t"]["p"]*100}\n')
    picsv.writelines(lines)