metapath = '/Users/tunder/Dropbox/GenreProject/metadata/poemeta1919.tsv'
with open(metapath, encoding = 'utf-8') as f:
    filelines = f.readlines()

getpoe = [x.split('\t')[0] for x in filelines]

outpath = '/Users/tunder/Dropbox/GenreProject/python/reception/getpoe.txt'
with open(outpath, mode = 'w', encoding = 'utf-8') as f:
    for htid in getpoe:
        f.write(htid + '\n')
