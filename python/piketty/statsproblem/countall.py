# count all
import numpy as np
import matplotlib.pyplot as plt
import csv

with open('/Users/tunder/Dropbox/GenreProject/python/piketty/badvolids.txt', encoding = 'utf-8') as f:
    badids = set([x.rstrip() for x in f.readlines()])

datafile = '/Volumes/TARDIS/work/moneycontext/fifteenwords.tsv'

def addtodict(key, value, dictionary):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value

positivesbyyear = dict()
negativesbyyear = dict()

dateset = set()
with open(datafile, encoding = 'utf-8') as f:
    for line in f:
        fields = line.split('\t')
        volid = fields[0]
        if volid in badids or '000' in badids:
            continue

        date = int(fields[1])
        category = fields[3]

        if category == 'notmoney':
            addtodict(date, 1, negativesbyyear)
            dateset.add(date)
        elif category == 'money':
            addtodict(date, 1, positivesbyyear)
            dateset.add(date)

datelist = list(dateset)
datelist.sort()
datelen = len(datelist)
ratio = np.zeros(datelen)

with open('snippettotals.csv', mode='w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'positives', 'negatives', 'total'])
    for idx, i in enumerate(datelist):
        if i in positivesbyyear:
            pos = positivesbyyear[i]
        else:
            pos = 1

        if i in negativesbyyear:
            neg = negativesbyyear[i]
        else:
            neg = 0

        ratio[idx] = neg / (pos + neg)
        row = [datelist[idx], pos, neg, (pos + neg)]
        writer.writerow(row)

plt.scatter(datelist, ratio)
plt.show()



