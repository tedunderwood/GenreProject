# organize_anovaset.py

import SonicScrewdriver as utils
import csv

rows, columns, table = utils.readtsv('/Volumes/TARDIS/work/metadata/MergedMonographs.tsv')

with open('anovaset.tsv', encoding = 'utf-8') as f:
    filelines = f.readlines()

anovaset = list()

for line in filelines:
    fields = line.split('\t')
    htid = utils.dirty_pairtree(fields[0])
    category = fields[1]
    if category == 'elite':
        category = 'reviewed'
    elif category == 'vulgar':
        category = 'random'

    if htid in rows:
        author = table['author'][htid]
        title = table['title'][htid]
        date = utils.simple_date(htid, table)
        imprint = table['imprint'][htid]
        enumcron = table['enumcron'][htid]
        anovaset.append([htid, category, date, enumcron, author, title, imprint])

with open('anovaset.csv', mode='w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['htid', 'category', 'date', 'enumcron', 'author', 'title', 'imprint'])
    for row in anovaset:
        writer.writerow(row)




