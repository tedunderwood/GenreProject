# make fiction subset

import SonicScrewdriver as utils

rows, columns, table = utils.readtsv("/Users/tunder/Dropbox/bookNLP/metadata/enrichedmetadataDec6.tsv")

datedict = dict()

selected = []

for row in rows:
	date = int(table["date"][row])

	if date in datedict:
		datedict[date] += 1
	else:
		datedict[date] = 1

	if datedict[date] > 3:
		continue
	else:
		selected.append(row)

with open("/Users/tunder/Dropbox/GenreProject/python/piketty/fictionsubset.txt", mode='w', encoding = 'utf-8') as f:
	for line in selected:
		f.write(line + '\n')



