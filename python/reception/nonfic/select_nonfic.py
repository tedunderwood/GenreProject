# select_nonfic.py

import csv, random
import SonicScrewdriver as utils

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

ficpoe = list()

with open('/Users/tunder/work/genre/metadata/ficmeta.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ficpoe.append(dirty_pairtree(row['htid']))

with open('/Users/tunder/work/genre/metadata/poemeta.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ficpoe.append(dirty_pairtree(row['htid']))

with open('/Users/tunder/work/genre/metadata/drameta.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ficpoe.append(dirty_pairtree(row['htid']))

with open('nonfic.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ficpoe.append(row['docid'])

ficpoe = set(ficpoe)
datedict = dict()

with open('/Volumes/TARDIS/work/metadata/MergedMonographs.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    rowct = 0
    scict = 0
    for row in reader:
        htid = row['HTid']

        rowct += 1

        if htid in ficpoe or rowct < 10:
            continue
        else:
            loc = row['LOCnum']
            date = utils.date_row(row)
            if date < 1820 or date > 1919:
                continue
            if date in datedict:
                if len(datedict[date]) > 100:
                    continue

                if loc.startswith('B'):
                    datedict[date].append(row)
                    continue

            else:
                if loc.startswith('B'):
                    datedict[date] = [row]



with open('religion.csv', mode = 'w', encoding = 'utf-8') as f:
    fieldnames = ['docid', 'actualdate', 'inferreddate', 'firstpub', 'recept', 'recordid', 'OCLC', 'author', 'imprint', 'enumcron', 'title', 'pubrev', 'judge', 'impaud',]
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    for key, options in datedict.items():
        random.shuffle(options)
        for i in range(3):
            value = options[i]
            row = dict()
            row['docid'] = value['HTid']
            row['firstpub'] = key
            row['inferreddate'] = key
            row['actualdate'] = key
            row['recept'] = 'nonfic'
            row['recordid'] = ''
            row['OCLC'] = ''
            row['author'] = value['author']
            row['imprint'] = value['imprint']
            if len(row['imprint']) > 25:
                row['imprint'] = row['imprint'][0:24]
            row['enumcron'] = value['enumcron']
            row['title'] = value['title']
            row['pubrev'] = value['LOCnum']
            row['judge'] = ''
            row['impaud'] = ''
            writer.writerow(row)

print(scict)





