# select_corpus.py
#
# This module imports metadata about reviewed volumes; selects a set of
# volumes in the "reviewed" class, and then uses a larger generic
# metadata corpus to select a matching chronological distribution of
# random volumes.
#
# It differs from the original version of the script in using
# a newer metadata set.

import csv, os
import SonicScrewdriver as utils
import random

selecteddates = dict()
selected = list()
selectedmeta = dict()

def get_meta():
    meta = dict()
    meta['aubirth'] = input('Authors year of birth? ')
    meta['augender'] = input ('Authors gender? ')
    meta['national origin'] = input('Authors nationality? ')
    meta['firstpub'] = input('Date of first publication? ')
    return meta

reviews = '/Users/tunder/Dropbox/ted/reception/reviewed/lists/ReviewedTitles1860-1879_200.csv'
with open(reviews, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:

        htid = utils.clean_pairtree(row['HTid'])
        pubdate = int(row['date'][0:4])
        firstpub = int(row['firstpub'])
        yrrev = int(row['yrrev'])

        if pubdate > yrrev + 5:
            date = yrrev
            print(str(pubdate) + " => " + str(yrrev))
        else:
            date = pubdate

        jgenre = row['Jgenre']

        if jgenre == 'fic':
            selecteddates[htid] = date
            selected.append(htid)
            selectedmeta[htid] = row
            selectedmeta[htid]['firstpub'] = firstpub

bydate = dict()
authors = dict()
titles = dict()
datesbyhtid = dict()

with open('/Users/tunder/work/genre/metadata/ficmeta.csv', encoding = 'utf-8') as f:
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
controlmeta = dict()
usedfromselected = list()

skip = int(input('Skip how many? '))
for theid in selected[skip:]:
    date = selecteddates[theid]
    usedfromselected.append(theid)
    print(theid)
    print(date)
    if theid in authors:
        print(authors[theid])
    else:
        print("Missing author.")
    if theid in titles:
        print(titles[theid])
    else:
        print("Missing title.")

    found = False
    while not found:
        candidates = bydate[date]
        choice = random.sample(candidates, 1)[0]
        print(choice)
        print(authors[choice])
        print(titles[choice])
        acceptable = input("ACCEPT? (y/n): ")
        if acceptable == "y":
            controlset.add(choice)
            found = True
            controlmeta[choice] = get_meta()
            controlmeta[choice]['author'] = authors[choice]
            controlmeta[choice]['title'] = titles[choice]
        if acceptable == 'quit':
            break
    if acceptable == 'quit':
        break

ficmetadata = list()
user = input("Write metadata for reviewed set ?")
if user == 'y':
    for htid in usedfromselected:
        date = str(selecteddates[htid])
        meta = selectedmeta[htid]
        author = meta['author']
        title = meta['title']
        if 'aubirth' in meta:
            birth = meta['aubirth']
        else:
            print(author)
            print(title)
            print(date)
            birth = input('Authors year of birth? ')
            meta['augender'] = input ('Authors gender? ')
            meta['national origin'] = input('Authors nationality? ')

        gender = meta['augender']
        nation = meta['national origin']
        firstpub = meta['firstpub']
        if nation.startswith('British'):
            nation = 'uk'
        if nation.startswith('America'):
            nation = 'us'

        outline = htid + '\t' + 'elite' + '\t' + str(date) + '\t' + author + '\t' + title + '\t' + str(birth) + '\t' + gender + '\t' + nation + '\t' + str(firstpub) + '\n'
        ficmetadata.append(outline)

for htid in controlset:
    if htid not in datesbyhtid:
        print(htid)
        continue
    date = str(datesbyhtid[htid])
    meta = controlmeta[htid]
    author = meta['author']
    title = meta['title']
    birth = meta['aubirth']
    gender = meta['augender']
    nation = meta['national origin']
    firstpub = meta['firstpub']

    outline = htid + '\t' + 'vulgar' + '\t' + str(date) + '\t' + author + '\t' + title + '\t' + str(birth) + '\t' + gender + '\t' + nation + '\t' + str(firstpub) + '\n'
    ficmetadata.append(outline)

metapath = '/Users/tunder/Dropbox/GenreProject/metadata/richficmeta1879.tsv'
if os.path.isfile(metapath):
    fileexists = True
else:
    fileexists = False

with open(metapath, mode = 'a', encoding = 'utf-8') as f:
    if not fileexists:
        f.write('\t'.join(['docid', 'recept', 'date', 'author', 'title', 'birth', 'gender', 'nationality', 'firstpub', 'othername', 'notes', 'canon']) + '\n')
    for line in ficmetadata:
        f.write(line)







