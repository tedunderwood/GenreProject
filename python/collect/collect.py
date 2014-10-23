#! python3
# collect.py

# This script collects files containing feature counts for specified volume IDs,
# or specified words in those volumes, and gathers them in a folder for
# further processing. (Often, in practice, this means that the folder gets
# downloaded elsewhere.)
#
# USAGE:
# python3 rootdir slicepath extension wordpath outdir
#
# where

# rootdir == a directory of files that have already been filtered for genre at
# the page level, and organized into subdirectories by namespace (i.e., the library
# prefix that Hathitrust assigns to a volume)
#
# slicepath == a path to a file listing volume IDs to retrieve
#
# extension == the extension we expect files to have
#
# wordpath == path to a file of words that we're going to filter for, or "none"
# if we want to accept all words
#
# outdir = where to put the filtered files
#
# for instance:
# python3 /projects/ichass/usesofscale/fiction/


import sys, os
import SonicScrewdriver as utils
import shutil

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

if wordpath == "none":
	getallwords = True
else:
	getallwords = False
	with open(wordpath, encoding = 'utf-8') as f:
		filelines = f.readlines()
	wordstoget = set([x.strip() for x in filelines])

# metafile = '/projects/ichass/usesofscale/hathimeta/MergedMonographs.tsv'

# rows, columns, table = utils.readtsv(metafile)

subdirectories = dict()
dirlist = list()

for o in os.listdir(d):
	if os.path.isdir(os.path.join(d,o)):
		subdirectories[o] = os.path.join(d,o)
		dirlist.append(o)

wordcounts = dict()

lexicon = set()

with open('/projects/ichass/usesofscale/rules/MainDictionary.txt', encoding ='utf-8') as f:
	filelines = f.readlines()

for line in filelines:
	fields = line.split('\t')
	lexicon.add(fields[0])

dirslice = set(dirlist[startdir : enddir])

for subdir, subdirpath in subdirectories.items():
	if subdir not in dirslice:
		continue

	filelist = [o for o in os.listdir(subdirpath) if not o.startswith('.')]

	for filename in filelist:
		dirtyID = filename.replace(extension, '')
		dirtyID = dirty_pairtree(dirtyID)

		if not dirtyID in idstoget and not getall:
			continue

		filepath = os.path.join(subdirpath, filename)
		outpath = os.path.join(outdir, filename)


		if getallwords:
			shutil.copyfile(filepath, outpath)

		else:
			thisfilelist = list()

			with open(filepath, encoding='utf-8') as f:
				filelines = f.readlines()

			totaltokens = 0
			totalwords = 0
			with open(outpath, mode = 'w ', encoding = 'utf-8') as f:
				for line in filelines:
					line = line.rstrip()
					fields = line.split('\t')
					word = fields[0]
					count = int(fields[1])
					if word in wordstoget:
						f.write(line)
					if not all_nonalphanumeric(word):
						totaltokens += count
					if word in lexicon:
						totalwords += count
				outline = "total#antokens" + '\t' + str(totaltokens) + '\n'
				f.write(outline)
				outline = "total#dwords" + '\t' + str(totalwords) + '\n'

print('Done.')











