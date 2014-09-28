# refine fiction

import SonicScrewdriver as utils

def passfilter(genrestring):
	fields = genrestring.split(';')
	if "Autobiography" in fields or "Biography" in fields:
		return False
	else:
		return True

rows19c, columns19c, table19c = utils.readtsv('/Volumes/TARDIS/work/metadata/19cMetadata.tsv')

rows20c, columns20c, table20c = utils.readtsv('/Volumes/TARDIS/work/metadata/20cMonographMetadata.tsv')

with open("/Users/tunder/Dropbox/GenreProject/python/piketty/roughfiction.txt", encoding = 'utf-8') as f:
	filelines = f.readlines()

idlist = [utils.pairtreelabel(x.split('\t')[0]) for x in filelines]

filteredrows = list()

missing = 0

for anid in idlist:
	if anid in rows19c:
		genrestring = table19c["genres"][anid]
		rowdict = dict()
		for col in columns19c:
			rowdict[col] = table19c[col][anid]
	elif anid in rows20c:
		genrestring = table20c["genres"][anid]
		rowdict = dict()
		for col in columns20c:
			rowdict[col] = table20c[col][anid]
	else:
		print("Missing " + anid)
		missing += 1
		continue

	if passfilter(genrestring):
		filteredrows.append(rowdict)
	else:
		print("Biography " + anid)

outpath = "/Users/tunder/Dropbox/GenreProject/metadata/filteredfiction2.tsv"
with open(outpath, mode='w', encoding = 'utf-8') as f:
	outline = ""
	for column in columns20c:
		outline = outline + column + '\t'
	outline = outline.rstrip() + '\n'
	f.write(outline)
	for row in filteredrows:
		outline = ""
		for column in columns20c:
			outline = outline + row[column] + '\t'
		outline = outline.rstrip() + '\n'
		f.write(outline)


print(missing)


