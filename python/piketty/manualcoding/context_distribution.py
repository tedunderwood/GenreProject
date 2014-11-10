#!/usr/bin/env python3

# Script tested in Python 3.3.4.

# check_errors.py

# This reads in a list of coded snippets and checks the distribution of
# social contexts matching a specified test condition. For instance,
# by specifying 'nonmonetary' you can check errors. By specifying
# 'inheritance' you can check that.

import csv
import numpy as np
import matplotlib.pyplot as plt

with open('/Users/tunder/Dropbox/GenreProject/python/piketty/badvolids.txt', encoding = 'utf-8') as f:
    badids = [x.rstrip() for x in f.readlines()]

alldistribution = dict()
targetdistribution = dict()

def pricesymbol(snippet):
    if ' $ ' in snippet:
        return True
    elif ' £ ' in snippet:
        return True
    elif ' ¢ ' in snippet:
        return True
    elif ' Â£ ' in snippet:
        return True
    elif '22nd' in snippet:
        return True
    elif '23rd' in snippet:
        return True
    else:
        return False

def special_check(testcondition, snippet):
    if testcondition != 'nonmonetary':
        return True
    elif not pricesymbol(snippet):
        return True
    else:
        return False

def increment_dict(key, dictionary):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1

testcondition = input("Context to check? ")

filepath = "HoytTedRichAll.tsv"
with open(filepath, encoding = 'utf-8') as f:
    filelines = f.readlines()

for line in filelines:
    line = line.rstrip()
    fields = line.split('\t')
    date = int(fields[0])
    volid = fields[1]
    if volid in badids or ("000" + volid) in badids:
        continue
    currency = fields[3]
    facevalue = float(fields[4])

    decade = int(date/10) * 10

    increment_dict(decade, alldistribution)

    context = fields[5]

    if context == testcondition and special_check(context, fields[6]):
        increment_dict(decade, targetdistribution)

outpath = testcondition + '_dist.csv'

numdecades = len(alldistribution)
x = np.zeros(numdecades)
y = np.zeros(numdecades)

with open(outpath, mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['year', 'allsnips', 'errorsnips'])
    idx = 0
    for year, allsnips in alldistribution.items():
        if year in targetdistribution:
            target = targetdistribution[year]
        else:
            target = 0
        row = [year, allsnips, target]
        x[idx] = year
        y[idx] = target / allsnips
        idx += 1

        writer.writerow(row)

plt.scatter(x, y)
plt.show()
