# CollectByYear.py

import sys, os
import FileCabinet
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


extension = ".fic.tsv"

args = sys.argv

d = args[1]
# We assume that the root directory to collect is passed in as the first command-line
# argument.

prepost = args[2]
# We take the second command-line argument as a flag that tells us whether this dataset is
# pre or post 1900. We have different metadata tables for the two datasets.

if prepost == "post":
	metafile = '/projects/ichass/usesofscale/20cmeta/MonographMetadata.tsv'
else:
	metafile = '/projects/ichass/usesofscale/hathimeta/ExtractedMetadata.tsv'

rows, columns, table = utils.readtsv(metafile)

subdirectories = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

wordcounts = dict()

for subdir in subdirectories:
	filelist = [o for o in os.listdir(subdir) if not o.startswith('.')]

	for filename in filelist:
		dirtyID = filename.replace(extension, '')
		dirtyID = dirty_pairtree(dirtyID)
		filepath = os.path.join(subdir, filename)

		if dirtyID in rows:
			date = table["date"][dirtyID]
			try:
				intdate = int(date[0:4])
			except:
				# No readable date
				intdate = 0
		else:
			intdate = 0

		if intdate > 1699 and intdate < 2000:

			print(dirtyID)

			with open(filepath, encoding='utf-8') as f:
				filelines = f.readlines()

			for line in filelines:
				line = line.rstrip()
				fields = line.split('\t')
				word = fields[0]
				count = int(fields[1])
				add_counts(wordcounts, intdate, word, count)

outputpath = os.path.join(d, 'summedbyyear.tsv')
with open(outputpath, mode='w', encoding = 'utf-8') as f:
	for year, subdictionary in wordcounts.items():

		for word, count in subdictionary.items():
			outline = str(year) +'\t' + word + '\t' + str(count) + '\n'
			f.write(outline)

print('Done.')











