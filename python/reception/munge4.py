import SonicScrewdriver as utils

metapath = '/Users/tunder/Dropbox/GenreProject/metadata/richpoemeta1859.tsv'
with open(metapath, encoding = 'utf-8') as f:
    filelines = f.readlines()

getpoe = [x.split('\t')[0] for x in filelines]

outpath = '/Users/tunder/Dropbox/GenreProject/python/reception/getpoe.txt'
with open(outpath, mode = 'w', encoding = 'utf-8') as f:
    for htid in getpoe:
        htid = utils.dirty_pairtree(htid)
        f.write(htid + '\n')
