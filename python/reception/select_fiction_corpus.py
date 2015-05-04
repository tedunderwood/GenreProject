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
import os.path

selecteddates = dict()
selected = list()

reviews = '/Users/tunder/Dropbox/ted/reception/reviewed/lists/ReviewedTitles1880-1899_200.csv'
with open(reviews, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:

        htid = utils.clean_pairtree(row['HTid'])
        pubdate = int(row['date'])
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
birthdates = dict()
matched = list()

skip = int(input('Skip how many? '))
for theid in selected[skip:]:
    date = selecteddates[theid]
    print(theid)
    print(date)
    if theid not in authors:
        print("missing")
        continue
    author = authors[theid]
    title = titles[theid]
    print(author)
    print(title)
    birthday = input('birthdate? ')
    birthdates[theid] = birthday
    matched.append(theid)

    found = False
    while not found:
        candidates = bydate[date]
        choice = random.sample(candidates, 1)[0]
        print(authors[choice])
        print(titles[choice])
        acceptable = input("ACCEPT? (y/n): ")
        if acceptable == "y":
            controlset.add(choice)
            birthday = input("Date of birth (0 for unknown): ")
            birthdates[choice] = birthday
            found = True
        elif acceptable == 'quit':
            break
        elif acceptable == 'skip':
            found = True
    if acceptable == 'quit':
        break

ficmetadata = list()
user = input("Write metadata for reviewed set ?")
if user == 'y':
    for line in matched:
        htid = utils.clean_pairtree(line.rstrip())
        if htid not in datesbyhtid:
            print(htid)
            continue
        date = str(datesbyhtid[htid])
        author = authors[htid]
        title = titles[htid]
        print(author)
        print(title)
        print(date)
        if htid in birthdates:
            birthday = birthdates[htid]
        else:
            birthday = input('birthdate? ')
        outline = [htid, 'elite', date, birthday, author, title]
        ficmetadata.append(outline)
for line in controlset:
    htid = utils.clean_pairtree(line.rstrip())
    if htid not in datesbyhtid:
        print(htid)
        continue
    date = str(datesbyhtid[htid])
    author = authors[htid]
    title = titles[htid]
    birthday = birthdates[htid]
    outline = [htid, 'vulgar', date, birthday, author, title]
    ficmetadata.append(outline)

metapath = '/Users/tunder/Dropbox/GenreProject/metadata/richficmeta1899.csv'
if os.path.exists(metapath):
    headeralready = True
else:
    headeralready = False

with open(metapath, mode = 'a', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    if not headeralready:
        writer.writerow(['htid', 'class', 'pubdate', 'birthdate', 'author', 'title'])
    for row in ficmetadata:
        writer.writerow(row)







