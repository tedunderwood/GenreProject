# summarizesubset.py

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

extension = ".fic.tsv"

args = sys.argv

d = args[1]
# We assume that the root directory to collect is passed in as the first command-line
# argument.

slicepath = args[2]

extension = args[3]

wordpath = args[4]

outdir = args[5]

directoryslices = {"0", "5", "10", "15", "20", "25"}

if slicepath == "none" or slicepath == "na":
	idstoget = set()
	getall = True
	startdir = 0
	enddir = 100
	# We allow mining all volumes in the directory, by setting a flag.

elif slicepath in directoryslices:
	# We also permit subsetting the corpus by directory
	idstoget = set()
	getall = True
	startdir = int(slicepath)
	enddir = startdir + 5

else:
	with open(slicepath, encoding = 'utf-8') as f:
		filelines = f.readlines()
	idstoget = set([x.strip() for x in filelines])
	getall = False
	startdir = 0
	enddir = 100

with open(wordpath, encoding = 'utf-8') as f:
	filelines = f.readlines()
wordstoget = set([x.strip() for x in filelines])

metafile = '/projects/ichass/usesofscale/hathimeta/MergedMonographs.tsv'

rows, columns, table = utils.readtsv(metafile)

subdirectories = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

wordcounts = dict()
counter = 0

if slicepath in directoryslices:
	outputpath = os.path.join(outdir, slicepath + ".tsv")
else:
	outputpath = os.path.join(outdir, "extracted_words.tsv")

# Get a dictionary so you can count dictionary words.

lexicon = set()

with open('/projects/ichass/usesofscale/rules/MainDictionary.txt', encoding ='utf-8') as f:
	filelines = f.readlines()

for line in filelines:
	fields = line.split('\t')
	lexicon.add(fields[0])

for subdir in subdirectories[startdir : enddir]:
	filelist = [o for o in os.listdir(subdir) if not o.startswith('.')]

	for filename in filelist:
		dirtyID = filename.replace(extension, '')
		dirtyID = dirty_pairtree(dirtyID)

		if not dirtyID in idstoget and not getall:
			print(dirtyID + '\t' + str(counter))
			counter += 1
			continue

		filepath = os.path.join(subdir, filename)

		# if dirtyID in rows:
		# 	datetype = table["datetype"][dirtyID]
		# 	firstdate = table["startdate"][dirtyID]
		# 	seconddate = table["enddate"][dirtyID]
		# 	textdate = table["textdate"][dirtyID]
		# 	date = utils.infer_date(datetype, firstdate, seconddate, textdate)
		# else:
		# 	date = 0

		if True:

			thisfiledict = dict()

			with open(filepath, encoding='utf-8') as f:
				filelines = f.readlines()

			totaltokens = 0
			totalwords = 0
			with open(outputpath, mode = 'a', encoding = 'utf-8') as f:
				for line in filelines:
					line = line.rstrip()
					fields = line.split('\t')
					word = fields[0]
					count = int(fields[1])
					if word in wordstoget:
						outline = dirtyID + '\t' + word + '\t' + str(count) + '\n'
						f.write(outline)
					if not all_nonalphanumeric(word):
						totaltokens += count
					if word in lexicon:
						totalwords += count
				outline = dirtyID + '\t' + "total#antokens" + '\t' + str(totaltokens) + '\n'
				f.write(outline)
				outline = dirtyID + '\t' + "total#dwords" + '\t' + str(totalwords) + '\n'
				f.write(outline)

print('Done.')











