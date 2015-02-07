# sort_anovaset.py

import SonicScrewdriver as utils
import csv

rows, columns, table = utils.readtsv('/Volumes/TARDIS/work/metadata/19cmetadata.tsv')

with open('anovaset.txt', encoding = 'utf-8') as f:
    filelines = f.readlines()
    wholeset = [x.rstrip() for x in filelines]

the19c = list()
the20c = list()

for anid in wholeset:
    if anid in rows:
        the19c.append(anid)
    else:
        the20c.append(anid)

with open('anova19c.txt', mode = 'w', encoding = 'utf-8') as f:
    for anid in the19c:
        f.write(anid + '\n')

with open('anova20c.txt', mode = 'w', encoding = 'utf-8') as f:
    for anid in the20c:
        f.write(anid + '\n')



