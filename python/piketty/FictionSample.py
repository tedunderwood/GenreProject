# FictionSample

import sys, os
import FileCabinet
import SonicScrewdriver as utils
import shutil
import random
from difflib import SequenceMatcher

sampleperyear = 50

def infer_date(startdate, enddate, textdate):
	'''Receives two dates, as strings, with no guarantee that either one
	will be numeric. Returns a date that represents either a shaky consensus
	about the earliest probable date for this item, or 0, indicating no
	consensus.
	'''

	if "--" in textdate and "estimate" in textdate:
		return 0
	# Because that's something like <estimate="18--?">

	try:
		intdate = int(startdate)
	except:
		# No readable date
		if startdate.endswith('uu'):
			# Two missing places is too many.
			intdate = 0
		elif startdate.endswith('u'):
			# but one is okay
			try:
				decade = int(startdate[0:3])
				intdate = decade * 10
			except:
				# something's weird. fail.
				intdate = 0
		else:
			intdate = 0

	try:
		intenddate = int(enddate)
	except:
		intenddate = 0

	if intenddate - intdate > 25:
		# A gap of more than twenty-five years is too much.
		intdate = 0

	return intdate

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


metafile = '/Users/tunder/Dropbox/GenreProject/metadata/filteredfiction.tsv'
rows, columns, table = utils.readtsv(metafile)

dateindex = dict()

for volid in rows:
	startdate = table["startdate"][volid]
	enddate = table["enddate"][volid]
	textdate = table["textdate"][volid]

	intdate = infer_date(startdate, enddate, textdate)

	if intdate >= 1750 and intdate <= 1950:
		if intdate in dateindex:
			dateindex[intdate].append(volid)
		else:
			dateindex[intdate] = [volid]

selectedids = list()
authtitles = list()

for i in range(1750, 1951):
	print('\n' + str(i))
	if i in dateindex:
		population = dateindex[i]
		popsize = len(population)

		if sampleperyear >= popsize:
			sample = population
		else:
			initialsample = random.sample(population, sampleperyear)
			sample = list()

			for volid in initialsample:
				authorA = table["author"][volid]
				titleA = table["title"][volid]
				maxmatch = 0

				for atuple in authtitles:
					authorB, titleB = atuple
					authmatch = SequenceMatcher(None, authorA, authorB)
					authsimilarity = authmatch.quick_ratio()
					titlematch = SequenceMatcher(None, titleA, titleB)
					titlesimilarity = titlematch.quick_ratio()
					thismatch = authsimilarity * titlesimilarity
					if thismatch > maxmatch:
						maxmatch = thismatch

				if maxmatch < 0.85:
					sample.append(volid)
				else:
					print(maxmatch)

			if len(sample) < sampleperyear:
				for volid in initialsample:
					population.remove(volid)

				stillneeded = sampleperyear - len(sample)
				print("Still needed: " + str(stillneeded) + "from population " + str(len(population)))

				if stillneeded >= len(population):
					secondsample = population
				else:
					secondsample = random.sample(population, stillneeded)

				sample.extend(secondsample)

		selectedids.extend(sample)
		for volid in sample:
			author = table["author"][volid]
			title = table["title"][volid]
			authtitles.append((author, title))

utils.writetsv(columns, selectedids, table, "/Users/tunder/Dropbox/GenreProject/metadata/topicmodelingsample.tsv")




