# allthedirtynames.py

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

ctr = 0

allthedirtynames = list()

with open('logisticpredictions.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        recept = row['reviewed']
        docid = row['volid']

        if recept.startswith('not') or recept.startswith('rev'):
            ctr += 1
            allthedirtynames.append(dirty_pairtree(docid))

with open('allthedirtynames.txt', mode = 'w', encoding = 'utf-8') as f:
    for name in allthedirtynames:
        f.write(name + '\n')

print(ctr)



