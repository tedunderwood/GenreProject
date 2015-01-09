import SonicScrewdriver as utils

elitefiction = '/Users/tunder/Dropbox/GenreProject/python/reception/elitefiction1919.txt'
with open(elitefiction, encoding = 'utf-8') as f:
    elite = f.readlines()

vulgarfiction = '/Users/tunder/Dropbox/GenreProject/python/reception/vulgarfiction1919.txt'
with open(vulgarfiction,encoding = 'utf-8') as f:
    vulgar = f.readlines()

rows, columns, table = utils.readtsv('/Users/tunder/Dropbox/GenreProject/metadata/filteredfiction.tsv')

ficmetadata = list()
for line in elite:
    htid = line.rstrip()
    if htid not in rows:
        print(htid)
        continue
    date = str(utils.simple_date(htid, table))
    author = table["author"][htid]
    title = table["title"][htid]
    outline = htid + '\t' + 'elite' + '\t' + date + '\t' + author + '\t' + title + '\n'
    ficmetadata.append(outline)
for line in vulgar:
    htid = line.rstrip()
    if htid not in rows:
        print(htid)
        continue
    date = str(utils.simple_date(htid, table))
    author = table["author"][htid]
    title = table["title"][htid]
    outline = htid + '\t' + 'vulgar' + '\t' + date + '\t' + author + '\t' + title + '\n'
    ficmetadata.append(outline)

metapath = '/Users/tunder/Dropbox/GenreProject/python/reception/richficmeta1919.tsv'
with open(metapath, mode = 'w', encoding = 'utf-8') as f:
    for line in ficmetadata:
        f.write(line)
