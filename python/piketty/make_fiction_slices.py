# make_fiction_slices

infile = "/Users/tunder/Dropbox/GenreProject/metadata/filteredfiction.tsv"

with open(infile, encoding = 'utf-8') as f:
	filelines = f.readlines()

volids = [x.split('\t')[0] for x in filelines]

numids = len(volids)

with open("/Users/tunder/Dropbox/GenreProject/metadata/filteredvolids.txt", mode = 'w', encoding = 'utf-8') as f:
	for anid in volids:
		f.write(anid + '\n')


