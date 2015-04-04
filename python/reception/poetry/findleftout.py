import os

files = os.listdir('pre1840')
files = set([x.replace('.poe.tsv', '') for x in files])

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

def clean_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if ':' in postfix:
        postfix = postfix.replace(':','+')
        postfix = postfix.replace('/','=')
    cleanname = prefix + "." + postfix
    return cleanname

with open('pre1840ids.txt', encoding = 'utf-8') as f:
    filelines = f.readlines()

allids = list()
for line in filelines:
    thisid = clean_pairtree(line.strip())
    allids.append(thisid)

leftout = list()
for afilename in allids:
    if afilename not in files:
        print(afilename)
        leftout.append(dirty_pairtree(afilename))

with open('leftoutpre1840ids.txt', mode = 'w', encoding = 'utf-8') as f:
    for anid in leftout:
        f.write(anid + '\n')

