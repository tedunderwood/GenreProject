# select_corpus.py
#
# This module imports metadata about reviewed volumes; selects a set of
# volumes in the "reviewed" class, and then uses a larger generic
# metadata corpus to select a matching chronological distribution of
# random volumes.

import csv
import SonicScrewdriver as utils
import random

selecteddates = dict()
selected = set()

reviews = '/Users/tunder/Dropbox/ted/reception/reviewed/lists/ReviewedTitles.csv'
with open(reviews) as f:
    reader = csv.reader(f)
    for fields in reader:
        htid = fields[0]
        if htid == "HTid":
            continue
        jgenre = fields[13]
        date = int(fields[1])

        if jgenre == 'fic':
            selecteddates[htid] = date
            selected.add(htid)

rows, columns, table = utils.readtsv('/Users/tunder/Dropbox/GenreProject/metadata/filteredfiction.tsv')

bydate = dict()

for row in rows:
    if row in selected:
        continue

    date = utils.simple_date(row, table)

    if date in bydate:
        bydate[date].append(row)
    else:
        bydate[date] = [row]

controlset = set()

for theid, date in selecteddates.items():
    found = False
    while not found:
        candidates = bydate[date]
        choice = random.sample(candidates, 1)[0]
        print(table["author"][choice])
        print(table["title"][choice])
        acceptable = input("ACCEPT? (y/n): ")
        if acceptable == "y":
            controlset.add(choice)
            found = True

elitefiction = '/Users/tunder/Dropbox/GenreProject/python/reception/elitefiction1919.txt'
with open(elitefiction, mode='w', encoding = 'utf-8') as f:
    for htid in selected:
        f.write(htid + '\n')

vulgarfiction = '/Users/tunder/Dropbox/GenreProject/python/reception/vulgarfiction1919.txt'
with open(vulgarfiction, mode='w', encoding = 'utf-8') as f:
    for htid in controlset:
        f.write(htid + '\n')

getallfiction = '/Users/tunder/Dropbox/GenreProject/python/reception/allfiction1919.txt'
with open(getallfiction, mode='w', encoding = 'utf-8') as f:
    for htid in controlset:
        f.write(htid + '\n')
    for htid in selected:
        f.write(htid + '\n')








