#correct poetry list

# I used Hathi dates for Jordan's files, which is generally
# good, except in cases where he's taken a much later publication.

import csv
import SonicScrewdriver as utils

def getcorrectdates(filepath, datedict):
    with open(filepath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            htid = row['HTid']
            pubdate = int(row['date'])
            firstpub = int(row['firstpub'])
            yrrev = int(row['yrrev'])

            if pubdate > yrrev + 5:
                date = yrrev
                print(str(pubdate) + " => " + str(yrrev))
            else:
                date = pubdate

            datedict[htid] = date

datedict = dict()
getcorrectdates('/Users/tunder/Dropbox/ted/reception/reviewed/lists/ReviewedTitles1900-1919_200.csv', datedict)
getcorrectdates('/Users/tunder/Dropbox/ted/reception/reviewed/lists/ReviewedTitles1880-1899_200.csv', datedict)
print('  ---  ')
outlines = list()
with open('/Users/tunder/Dropbox/GenreProject/python/granger/allpoemeta.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        thisdate = int(fields[2])
        if fields[0] in datedict:
            realdate = datedict[fields[0]]
        else:
            realdate = thisdate

        if thisdate != realdate:
            fields[2] = str(realdate)
            print(str(thisdate) + " => " + str(realdate))
        outline = '\t'.join(fields)
        outlines.append(outline)

with open('/Users/tunder/Dropbox/GenreProject/python/granger/correctedmeta.tsv', mode='w', encoding = 'utf-8') as f:
    for line in outlines:
        f.write(line + '\n')

