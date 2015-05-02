# add_supplement_to_poemaster.py

# This script adds files from the Graham's Magazine - Westminster Review
# supplement to the master poetry metadata file.

# At the same time it creates a list of poetry volids.

import csv

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

supplement = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/GrMWRsupplement.csv'

dirtyIDs = list()
allrows = list()

with open(supplement, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        htid = row['docid']
        genre = row['jgenre']
        if genre.startswith('po'):
            dirtyIDs.append(dirty_pairtree(htid))
            row.pop('jgenre')
            allrows.append(row)

fieldnames.pop(fieldnames.index('jgenre'))
cleanpoetry = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/GrMWRpoetry.csv'
with open(cleanpoetry, mode='w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    for row in allrows:
        writer.writerow(row)

getpoetry = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/GrMWRids.txt'
with open(getpoetry, mode='w', encoding = 'utf-8') as f:
    for anid in dirtyIDs:
        f.write(anid + '\n')





