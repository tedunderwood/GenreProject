import os, csv

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


tedfiles = ['/Users/tunder/Dropbox/GenreProject/python/reception/fiction/amplifiedficmeta.tsv', '/Users/tunder/Dropbox/GenreProject/metadata/richficmeta1879.tsv']

allrows = list()
for afile in tedfiles:
    with open(afile, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
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
    if htid in jordandict:
        matched = True
        matchedid = htid
    elif pairtreelabel(htid) in jordandict:
        matched = True
        matchedid = pairtreelabel(htid)

    if matched:

        enricher = jordandict[matchedid]
        for field in addfields:
            if field in enricher:
                row[field] = enricher[field]

        if 'firstpub' not in row:
            if 'firstpub' in enricher:
                row['firstpub'] = enricher['firstpub']
            else:
                row['firstpub'] = ''

        if 'gender' not in row or row['gender'] == '':
            if 'augender' in enricher:
                row['gender'] = enricher['augender']
            else:
                row['gender'] = ''

        if 'nationality' not in row or row['nationality'] == '':
            if 'national origin' in enricher:
                row['nationality'] = enricher['national origin']
            else:
                row['nationality'] = ''

        if 'birth' not in row or row['birth'] == '':
            if 'aubirth' in enricher:
                row['birth'] = enricher['aubirth']
            else:
                row['birth'] = ''


        row['actualdate'] = enricher['date']
        row['inferreddate'] = row.pop('date')

    else:
        if row['recept'] != 'vulgar':
            print(htid)
            print(row['recept'])

        row['actualdate'] = row.pop('date')
        row['inferreddate'] = row['actualdate']

fields = ['docid', 'actualdate', 'inferreddate', 'firstpub', 'recept', 'recordid', 'OCLC', 'author', 'imprint', 'enumcron', 'title', 'pubrev', 'judge', 'impaud', 'yrrev', 'pubname', 'birth', 'gender', 'nationality', 'othername', 'notes', 'canon']

with open('/Users/tunder/Dropbox/GenreProject/python/reception/fiction/masterficmeta.csv', mode='w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fields, extrasaction = 'raise')
    writer.writeheader()
    for row in allrows:
        writer.writerow(row)


