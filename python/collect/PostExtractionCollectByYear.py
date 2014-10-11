# PostExtractionSubset.py

import sys, os
import SonicScrewdriver as utils

def dirty_pairtree(htid):
	period = htid.find('.')
	prefix = htid[0:period]
	postfix = htid[(period+1): ]
	if '=' in postfix:
		postfix = postfix.replace('+',':')
		postfix = postfix.replace('=','/')
	dirtyname = prefix + "." + postfix
	return dirtyname

def add_counts(wordcounts, year, word, count):
	if year in wordcounts:

		if word in wordcounts[year]:
			wordcounts[year][word] += count
		else:
			wordcounts[year][word] = count

	else:
		wordcounts[year] = dict()
		wordcounts[year][word] = count

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

metafile = '/Users/tunder/Dropbox/GenreProject/metadata/filteredfiction.tsv'

rows, columns, table = utils.readtsv(metafile)

datedict = dict()
wordcounts = dict()
undated = set()

with open('/Volumes/TARDIS/work/forandrew/colors.tsv', encoding = 'utf-8') as f:

	for line in f:

		line = line.rstrip()
		fields = line.split('\t')

		volid = fields[0]
		word = fields[1]
		count = int(fields[2])

		if volid in datedict:
			date = datedict[volid]
		elif volid in rows:
			datetype = table["datetype"][volid]
			firstdate = table["startdate"][volid]
			seconddate = table["enddate"][volid]
			textdate = table["textdate"][volid]
			date = utils.infer_date(datetype, firstdate, seconddate, textdate)
			datedict[volid] = date
		else:
			print(volid + " missing in metadata.")
			date = 0

		if date > 1699 and date < 1924:
			add_counts(wordcounts, date, word, count)
		else:
			undated.add(volid)

with open('/Volumes/TARDIS/work/forandrew/colors.tsv', mode = 'w', encoding = 'utf-8') as f:
	for year, subdictionary in wordcounts.items():
		for word, count in subdictionary.items():
			outline = str(year) + '\t' + word + '\t' + str(count) + '\n'
			f.write(outline)

print('Done.')
print(str(len(undated)) + " undated files.")











