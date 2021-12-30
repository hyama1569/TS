import textstat
from collections import Counter
import os
import sys
import random

path_en = sys.argv[1]
path_sen = sys.argv[2]
percent = sys.argv[3]

os.makedirs("./data_" + percent + "percent", exist_ok=True)

diff = []
with open(path_en, "r") as f1, open(path_sen, "r") as f2:
    for line1, line2 in zip(f1, f2):
        diff.append(abs(textstat.flesch_kincaid_grade(line1) - textstat.flesch_kincaid_grade(line2)))
c = Counter(diff)
a = sorted(list(c.items()), key=lambda x:x[0])

percent_f = float(percent) / 100

## check whether there is data on the same difference in FKGL
## if between == True, there exists such data.
now = int(len(diff) * percent_f)
between = False
for i in a:
    now -= i[1]
    if now < 0:
        theta = i[0]
        between = True
        break
    if now == 0:
        theta = i[0]
        break

## delete no-difference data in FKGL
## if between==True, there are many candidates to delete. So select data to delete randomly
if between == False:
    with open(path_en, "r") as f1, open(path_sen, "r") as f2, open("./data_" + percent + "percent/" + path_en, "x") as f3, open("./data_" + percent + "percent/" + path_sen, "x") as f4:
        for line1, line2 in zip(f1, f2):
            if abs(textstat.flesch_kincaid_grade(line1) - textstat.flesch_kincaid_grade(line2)) > theta:
                f3.write(line1)
                f4.write(line2)

else:
    random.seed(0)
    data = []
    rest = int(len(diff) * percent_f)
    with open(path_en ,"r") as f1, open(path_sen, "r") as f2:
        for i, (line1, line2) in enumerate(zip(f1, f2)):
            data.append((i, line1, line2, abs(textstat.flesch_kincaid_grade(line1) - textstat.flesch_kincaid_grade(line2))))
            if abs(textstat.flesch_kincaid_grade(line1) - textstat.flesch_kincaid_grade(line2)) < theta:
                rest -= 1
        between_data = [i for i in data if i[3] == theta]
        between_data_sampled = random.sample(between_data, rest) #select data to delete
        between_data_sampled_index = [i[0] for i in between_data_sampled]

        data = [i for i in data if i[3] >= theta]
        data = [i for i in data if i[0] not in between_data_sampled_index]
    with open("./data_" + percent + "percent/" + path_en, "x") as f3, open("./data_" + percent + "percent/" + path_sen, "x") as f4:
        for i in data:
            f3.write(i[1])
            f4.write(i[2])

