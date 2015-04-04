def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

with open('pre1840ids.txt', encoding = 'utf-8') as f:
    filelines = f.readlines()

with open('pre1840ids.txt', mode = 'w', encoding = 'utf-8') as f:
    for anid in filelines:
        anid = dirty_pairtree(anid.strip())
        f.write(anid + '\n')

