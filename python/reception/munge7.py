import SonicScrewdriver as utils

with open('/Users/tunder/Dropbox/GenreProject/metadata/richficmeta1879.tsv', encoding = 'utf-8') as f:
    ids = [x.split('\t')[0] for x in f.readlines()]

newids = list()
for anid in ids:
    newid = utils.dirty_pairtree(anid)
    newids.append(newid)

with open('/Users/tunder/Dropbox/GenreProject/python/reception/fiction/getfic1879.txt', mode = 'w', encoding = 'utf-8') as f:
    for anid in newids:
        f.write(anid + '\n')



