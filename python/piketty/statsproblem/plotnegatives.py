#plotnegatives

import numpy as np
import matplotlib.pyplot as plt
import csv

negativeproportions = dict()
with open('snippettotals.csv', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)
    for line in reader:
        date = int(line[0])
        proportion = int(line[2]) / int(line[1])
        negativeproportions[date] = proportion

falseneg = np.zeros(21)
allneg = np.zeros(21)

with open('falsenegatives.tsv') as f:
    for line in f:
        if len(line) <3:
            continue
        else:
            fields = line.split('\t')
            date = int(fields[0])
            decade = int((date-1750) / 10)

            allneg[decade] += 1
            if fields[1] == 'pos':
                falseneg[decade] += 1

falserates = falseneg / allneg

x = np.zeros(201)
y = np.zeros(201)

ctr = 0
for year in range(1750, 1951):
    idx = int((year-1750) / 10)
    rate = falserates[idx]

    if year in negativeproportions:
        missingpositives = rate * negativeproportions[year]
    else:
        missingpositives = 0

    x[ctr] = year
    y[ctr] = missingpositives
    ctr += 1

plt.scatter(x, y)
plt.show()

