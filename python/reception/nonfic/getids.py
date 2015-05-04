import csv, random
import SonicScrewdriver as utils

idlist = list()

with open('religion.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        docid = row['docid']
        idlist.append(docid)

with open('religionids.txt', mode = 'w', encoding = 'utf-8') as f:
    for anid in idlist:
        f.write(anid + '\n')
