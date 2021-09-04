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