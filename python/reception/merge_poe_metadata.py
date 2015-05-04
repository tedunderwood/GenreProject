# Script I used to merge amplifiedmeta2.csv with Jordan's data.

import os, csv

def forceint(astring):
    if len(astring) > 4:
        astring = astring[0:4]
    try:
        intval = int(astring)
    except:
        intval = 0

    return intval

def pairtreelabel(htid):
    ''' Given a clean htid, returns a dirty one that will match
    the metadata table.'''

    if '+' in htid or '=' in htid:
        htid = htid.replace('+',':')
        htid = htid.replace('=','/')

    return htid

jordandict = dict()

jordandata = '/Users/tunder/Dropbox/ted/reception/reviewed/lists/ReviewedTitlesAll.csv'
with open(jordandata, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        htid = row['HTid']
        jordandict[htid] = row

mergedmonographs = dict()

mergedpath= '/Volumes/TARDIS/work/metadata/MergedMonographs.tsv'
with open(mergedpath, encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        htid = row['HTid']
        mergedmonographs[htid] = row


tedfiles = ['/Users/tunder/Dropbox/GenreProject/python/reception/poetry/amplifiedmeta2.csv']

allrows = list()
for afile in tedfiles:
    with open(afile, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            allrows.append(row)

addfields = ['pubrev', 'judge', 'impaud', 'yrrev', 'pubname', 'imprint', 'recordid', 'OCLC', 'enumcron']

for row in allrows:
    if 'docid' in row:
        htid = row['docid']
    else:
        print(row)
        print('Lacks docid.')
        continue

    matched = False
    inmeta = False
    if htid in jordandict:
        matched = True
        matchedid = htid
    elif pairtreelabel(htid) in jordandict:
        matched = True
        matchedid = pairtreelabel(htid)
    elif htid in mergedmonographs:
        inmeta = True
        matchedid = htid
    elif pairtreelabel(htid) in mergedmonographs:
        inmeta = True
        matchedid = pairtreelabel(htid)


    if matched:

        enricher = jordandict[matchedid]
        for field in addfields:
            if field in enricher:
                row[field] = enricher[field]

        if 'firstpub' not in row or row['firstpub'] == '':
            if 'firstpub' in enricher:
                row['firstpub'] = enricher['firstpub']
            else:
                row['firstpub'] = ''

        row['actualdate'] = enricher['date']
        row['inferreddate'] = row.pop('date')

    elif inmeta:
        enricher = mergedmonographs[matchedid]
        if enricher['enumcron'] != '<blank>':
            row['enumcron'] = enricher['enumcron']
        if enricher['imprint'] != '<blank>':
            row['imprint'] = enricher['imprint']
        if enricher['recordid'] != '<blank>':
            row['recordid'] = enricher['recordid']

        row['actualdate'] = row.pop('date')
        row['inferreddate'] = row['actualdate']

        if row['recept'] == 'elite':
            print('')
            print(htid)
            print(row['recept'])

    else:
        if row['recept'] == 'elite':
            print('')
            print(htid)
            print(row['recept'])

        row['actualdate'] = row.pop('date')
        row['inferreddate'] = row['actualdate']

    if forceint(row['actualdate']) < forceint(row['firstpub']):
        print(htid)
        print("Actual date: " + row['actualdate'])
        print("Date of first pub: " + row['firstpub'])
        row['firstpub'] = str(forceint(row['actualdate']))
        print('Changed to' + row['firstpub'])

fields = ['docid', 'actualdate', 'inferreddate', 'firstpub', 'recept', 'recordid', 'OCLC', 'author', 'imprint', 'enumcron', 'title', 'pubrev', 'judge', 'impaud', 'yrrev', 'pubname', 'birth', 'gender', 'nationality', 'othername', 'notes', 'canon']

with open('/Users/tunder/Dropbox/GenreProject/python/reception/poetry/masterpoemeta.csv', mode='w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fields, extrasaction = 'raise')
    writer.writeheader()
    for row in allrows:
        writer.writerow(row)


