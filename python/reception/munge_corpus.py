elitefiction = '/Users/tunder/Dropbox/GenreProject/python/reception/elitefiction1919.txt'
with open(elitefiction, encoding = 'utf-8') as f:
    elite = f.readlines()

vulgarfiction = '/Users/tunder/Dropbox/GenreProject/python/reception/vulgarfiction1919.txt'
with open(vulgarfiction,encoding = 'utf-8') as f:
    vulgar = f.readlines()

ficmetadata = list()
for line in elite:
    outline = line.rstrip() + '\t' + '1\n'
    ficmetadata.append(outline)
for line in vulgar:
    outline = line.rstrip() + '\t' + '0\n'
    ficmetadata.append(outline)

metapath = '/Users/tunder/Dropbox/GenreProject/python/reception/meta1919.tsv'
with open(metapath, mode = 'w', encoding = 'utf-8') as f:
    for line in ficmetadata:
        f.write(line)
