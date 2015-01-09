metapath = '/Users/tunder/Dropbox/GenreProject/python/reception/richficmeta1919.tsv'
with open(metapath, encoding = 'utf-8') as f:
    filelines = f.readlines()

revisedfic = [x.split('\t')[0] for x in filelines]

outpath = '/Users/tunder/Dropbox/GenreProject/python/reception/revisedfic.txt'
with open(outpath, mode = 'w', encoding = 'utf-8') as f:
    for htid in revisedfic:
        f.write(htid + '\n')
