import os, sys
import numpy as np
import pandas as pd
from bagofwords import BagOfWords, StandardizingVector
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
import SonicScrewdriver as utils
import random

def dirty_pairtree(htid):
	period = htid.find('.')
	prefix = htid[0:period]
	postfix = htid[(period+1): ]
	if '=' in postfix:
		postfix = postfix.replace('+',':')
		postfix = postfix.replace('=','/')
	dirtyname = prefix + "." + postfix
	return dirtyname

def select_common_features(trainingset, n):
	''' Very simply, selects the top n features in the training set.
	Not a sophisticated feature-selection strategy, but in many
	cases it gets the job done.
	'''
	allwordcounts = dict()

	for avolume in trainingset:
		utils.add_dicts(avolume.rawcounts, allwordcounts)
		# The add_dicts function will add up all the raw counts into
		# a single master dictionary.

	descendingbyfreq = utils.sortkeysbyvalue(allwordcounts, whethertoreverse = True)
	# This returns a list of 2-tuple (frequency, word) pairs.

	if n > len(descendingbyfreq):
		n = len(descendingbyfreq)
		print("We only have " + str(n) + " features.")

	# List comprehension that gets the second element of each tuple, up to
	# a total of n tuples.

	topfeatures = [x[1] for x in descendingbyfreq[0 : n] if (len(x[1]) > 1 and not x[1].startswith('|'))]

	return topfeatures

def get_classvector(classpath, volumeIDs):
	with open(classpath, encoding = 'utf-8') as f:
		filelines = f.readlines()
	classdict = dict()
	for line in filelines:
		line = line.rstrip()
		fields = line.split('\t')
		volid = utils.clean_pairtree(fields[0])
		theclass = fields[1]
		if theclass == 'elite':
			intclass = 1
		elif theclass == 'vulgar':
			intclass = 0
		else:
			intclass = int(theclass)
		classdict[volid] = intclass

	if len(volumeIDs) < 1:
		volumeIDs = [x for x in classdict.keys()]

	classvector = np.zeros(len(volumeIDs))
	for idx, anid in enumerate(volumeIDs):
		if anid in classdict:
			classvector[idx] = classdict[anid]
		else:
			print('Missing from class metadata: ' + anid)

	return classvector, volumeIDs

def train_a_model(sourcefolder, extension, include_punctuation, maxfeatures, outputfolder, classpath):

	if not os.path.exists(outputfolder):
		os.makedirs(outputfolder)

	if not sourcefolder.endswith('/'):
		sourcefolder = sourcefolder + '/'
	if not outputfolder.endswith('/'):
		outputfolder = outputfolder + '/'
	# This just makes things easier.

	# Get a list of files available. Ultimately we're only going to use volumes
	# that are both in our files and in the metadata. The ordering will be
	# driven by the filenames, which we shuffle.
	allthefiles = os.listdir(sourcefolder)
	random.shuffle(allthefiles)

	# Now let's create a set of all the ids available in metadata.
	# Giving this function an empty list tells it that we want
	# all available ids.

	classvector, idsinmetadata = get_classvector(classpath, [])
	print(len(idsinmetadata))
	idsinmetadata = set(idsinmetadata)

	volumeIDs = list()
	volumepaths = list()

	for filename in allthefiles:

		if filename.endswith(extension):
			volID = filename.replace(extension, "")
			# The volume ID is basically the filename minus its extension.
			# Extensions are likely to be long enough that there is little
			# danger of accidental occurrence inside a filename. E.g.
			# '.fic.tsv'
			if volID in idsinmetadata:
				path = sourcefolder + filename
				volumeIDs.append(volID)
				volumepaths.append(path)


	# We have volumeIDs in a list whose sequence matches complete
	# paths to each file. We're going to achieve the pairing by zipping two lists,
	# rather than with a dict, because ordering also matters here.

	# Now get the class vector, indexed by volume ID

	classvector, shouldbethesameIDs = get_classvector(classpath, volumeIDs)
	print(len(classvector))
	print(len(volumeIDs))
	assert len(classvector) == len(volumeIDs)

	# Now we actually read volumes and create a training corpus, which will
	# be a list of bags of words.

	trainingset = list()
	for volID, filepath in zip(volumeIDs, volumepaths):
		volume = BagOfWords(filepath, volID, include_punctuation)
		# That reads the volume from disk.
		trainingset.append(volume)

	# We select the most common words as features.
	featurelist = select_common_features(trainingset, maxfeatures)
	numfeatures = len(featurelist)
	# Note that the number of features we actually got is not necessarily
	# the same as maxfeatures.

	for volume in trainingset:
		volume.selectfeatures(featurelist)
		volume.normalizefrequencies()
		# The volume now contains feature frequencies:
		# raw counts have been divided by the total number of words in the volume.

	standardizer = StandardizingVector(trainingset, featurelist)
	# This object calculates the means and standard deviations of all features
	# across the training set.

	listofvolumefeatures = list()
	for volume in trainingset:
		volume.standardizefrequencies(standardizer)
		# We have now converted frequencies to z scores. This is important for
		# regularized logistic regression -- otherwise the regularization
		# gets distributed unevenly across variables because they're scaled
		# differently.

		listofvolumefeatures.append(volume.features)

	# Now let's make a data frame by concatenating each volume as a separate column,
	# aligned on the features that index rows.

	data = pd.concat(listofvolumefeatures, axis = 1)
	data.columns = volumeIDs

	# Name the columns for volumes. Then transpose the matrix:

	data = data.T

	# So that we have a matrix with features (variables) as columns and instances (volumes)
	# as rows. Would have been easier to make this directly, but I don't know a neat
	# way to do it in pandas.

	logisticmodel = LogisticRegression(C = 0.1)
	classvector = classvector.astype('int')
	logisticmodel.fit(data, classvector)

	# Let's sort the features by their coefficient in the model, and print.

	coefficients = list(zip(logisticmodel.coef_[0], featurelist))
	coefficients.sort()
	for coefficient, word in coefficients:
		print(word + " :  " + str(coefficient))

	# Pickle and write the model & standardizer. This will allow us to apply the model to
	# new documents of unknown genre.

	modelfile = outputfolder + "logisticmodel.p"
	with open(modelfile, mode = 'wb') as f:
		pickle.dump(logisticmodel, f)
	standardizerfile = outputfolder + "standardizer.p"
	with open(standardizerfile, mode = 'wb') as f:
		pickle.dump(standardizer, f)

	accuracy_tries = cross_validation.cross_val_score(logisticmodel, data, classvector, cv=10)
	print(accuracy_tries)
	print(np.sum(accuracy_tries) / len(accuracy_tries))

	random.shuffle(classvector)
	print('\nASSVECTOR!\n')
	accuracy_tries = cross_validation.cross_val_score(logisticmodel, data, classvector, cv=10)
	print(accuracy_tries)
	print(np.sum(accuracy_tries) / len(accuracy_tries))

	# Yay, we're done.

if __name__ == "__main__":

	sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/granger/elite/'
	extension = '.poe.tsv'
	include_punctuation = False
	maxfeatures = 1600
	outputfolder = '/Users/tunder/Dropbox/GenreProject/python/reception/model1879/'
	metapath = '/Users/tunder/Dropbox/GenreProject/metadata/richpoemeta1879.tsv'

	train_a_model(sourcefolder, extension, include_punctuation, maxfeatures, outputfolder, metapath)











