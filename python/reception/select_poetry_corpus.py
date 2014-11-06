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

        if jgenre == 'poe':
            selecteddates[htid] = date
            selected.add(htid)

rows, columns, table = utils.readtsv('/Users/tunder/Dropbox/GenreProject/metadata/filteredpoetry.tsv')

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

ficmetadata = list()
for line in selected:
    htid = line.rstrip()
    if htid not in rows:
        print(htid)
        continue
    date = str(utils.simple_date(htid, table))
    author = table["author"][htid]
    title = table["title"][htid]
    outline = htid + '\t' + 'elite' + '\t' + date + '\t' + author + '\t' + title + '\n'
    ficmetadata.append(outline)
for line in controlset:
    htid = line.rstrip()
    if htid not in rows:
        print(htid)
        continue
    date = str(utils.simple_date(htid, table))
    author = table["author"][htid]
    title = table["title"][htid]
    outline = htid + '\t' + 'vulgar' + '\t' + date + '\t' + author + '\t' + title + '\n'
    ficmetadata.append(outline)

metapath = '/Users/tunder/Dropbox/GenreProject/metadata/richpoemeta1919.tsv'
with open(metapath, mode = 'w', encoding = 'utf-8') as f:
    for line in ficmetadata:
        f.write(line)

metapath = '/Users/tunder/Dropbox/GenreProject/metadata/poemeta1919.tsv'
with open(metapath, mode = 'w', encoding = 'utf-8') as f:
    for line in ficmetadata:
        fields = line.split('\t')
        if fields[1] == 'elite':
            code = "1"
        elif fields[1] == 'vulgar':
            code = "0"
        else:
            print('error')
        outline = fields[0] + '\t' + code + '\n'
        f.write(outline)







