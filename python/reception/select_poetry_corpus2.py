# select_corpus.py
#
# This module imports metadata about reviewed volumes; selects a set of
# volumes in the "reviewed" class, and then uses a larger generic
# metadata corpus to select a matching chronological distribution of
# random volumes.
#
# It differs from the original version of the script in using
# a newer metadata set.

import csv
import SonicScrewdriver as utils
import random

selecteddates = dict()
selected = set()

reviews = '/Users/tunder/Dropbox/ted/reception/reviewed/lists/ReviewedTitles1860-1879_200.csv'
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
authors = dict()
titles = dict()
datesbyhtid = dict()

with open('/Users/tunder/work/genre/metadata/poemeta.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        htid = row['htid']
        authors[htid] = row['author']
        titles[htid] = row['title']

        date = utils.date_row(row)
        datesbyhtid[htid] = date
        if htid in selected:
            continue
        if date in bydate:
            bydate[date].append(htid)
        else:
            bydate[date] = [htid]

controlset = set()

for theid, date in selecteddates.items():
    found = False
    while not found:
        candidates = bydate[date]
        choice = random.sample(candidates, 1)[0]
        print(authors[choice])
        print(titles[choice])
        acceptable = input("ACCEPT? (y/n): ")
        if acceptable == "y":
            controlset.add(choice)
            found = True

ficmetadata = list()
for line in selected:
    htid = utils.clean_pairtree(line.rstrip())
    if htid not in datesbyhtid:
        print(htid)
        continue
    date = str(datesbyhtid[htid])
    author = authors[htid]
    title = titles[htid]
    outline = htid + '\t' + 'elite' + '\t' + date + '\t' + author + '\t' + title + '\n'
    ficmetadata.append(outline)
for line in controlset:
    htid = utils.clean_pairtree(line.rstrip())
    if htid not in datesbyhtid:
        print(htid)
        continue
    date = str(datesbyhtid[htid])
    author = authors[htid]
    title = titles[htid]
    outline = htid + '\t' + 'vulgar' + '\t' + date + '\t' + author + '\t' + title + '\n'
    ficmetadata.append(outline)

metapath = '/Users/tunder/Dropbox/GenreProject/metadata/richpoemeta1879.tsv'
with open(metapath, mode = 'a', encoding = 'utf-8') as f:
    for line in ficmetadata:
        f.write(line)







