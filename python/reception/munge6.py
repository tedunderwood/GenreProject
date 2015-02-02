import SonicScrewdriver as utils

with open('/Users/tunder/Dropbox/GenreProject/metadata/getficids1899.txt', encoding = 'utf-8') as f:
    ids = [x.rstrip() for x in f.readlines()]

newids = list()
for anid in ids:
    newid = utils.dirty_pairtree(anid)
    newids.append(newid)

with open('/Users/tunder/Dropbox/GenreProject/metadata/dirtyficids1899.txt', mode = 'w', encoding = 'utf-8') as f:
    for anid in newids:
        f.write(anid + '\n')



