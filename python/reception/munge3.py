metapath = '/Users/tunder/Dropbox/GenreProject/python/reception/richficmeta1919.tsv'
with open(metapath, encoding = 'utf-8') as f:
    filelines = f.readlines()

outfile = '/Users/tunder/Dropbox/GenreProject/python/reception/ficmeta1919.tsv'
with open(outfile, mode = 'w', encoding = 'utf-8') as f:
    for line in filelines:
        fields = line.split('\t')
        if fields[1] == 'vulgar':
            code = 0
        else:
            code = 1

        f.write(fields[0] + '\t' + str(code) + '\n')
