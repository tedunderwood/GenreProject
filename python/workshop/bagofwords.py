# bagofwords.py
#
# The BagOfWords class implements individual volumes as ordered
# lists of features.
#

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

class BagOfWords:

	def __init__(self, filepath, volID, include_punctuation):
		''' Construct a BagOfWords.
		volID is a string label for the volume.
		include_punctuation is a boolean.
		'''

		self.volID = volID

		with open(filepath, encoding = 'utf-8') as f:
			filelines = f.readlines()

		self.rawcounts = dict()
		self.totalcount = 0

		for line in filelines:
			line = line.rstrip()
			fields = line.split('\t')
			if len(fields) != 2:
				print("Illegal line length in " + filepath)
				print(line)
				continue
			else:
				tokentype = fields[0]
				count = fields[1]

				try:
					intcount = int(count)
					if include_punctuation or not all_nonalphanumeric(tokentype):
						self.rawcounts[tokentype] = intcount
						self.totalcount += intcount

				except ValueError:
					print("Cannot parse count " + count + " as integer.")
					continue

		self.numrawcounts = len(self.rawcounts)

	def selectfeatures(self, featurelist):
		''' A BagOfWords is created with merely a dictionary of raw token counts.
		One could call this a sparse table. It has no entries where features are
		missing.

		We need to organize these as an ordered series of features, which includes
		only the features we have chosen to use in the current model, and has zeroes for
		missing values.
		'''

		self.featurelist = featurelist
		self.numfeatures = len(featurelist)
		self.features = Series(self.rawcounts, index = featurelist, dtype = 'float64')
		# Pandas has the nice feature of building a series from a dictionary if it's
		# provided an index of values. So this effectively builds a series of entries
		# ordered by the keys in 'featurelist,' with NaN in places where rawcounts
		# had no corresponding key.

		self.features[self.features.isnull()] = 0
		# This replaces NaN with zero, since missing words are effectively words with
		# count == 0.

	def normalizefrequencies(self):
		''' Simply divides all frequencies by the total token count for this volume.
		'''

		self.features = self.features / self.totalcount

	def standardizefrequencies(self, standardizer):
		''' Convert features to z-scores by centering them on the means and
		scaling them by standard deviation.

		standardizer = an object of class StandardizingVector, presumably created
		either on the corpus that contains this volume, or on the training corpus
		that created the model we are about to use on this volume.
		'''

		assert len(self.features) == len(standardizer.means)

		self.features = (self.features - standardizer.means) / standardizer.stdevs


class StandardizingVector:
	''' An object that computes the means and standard deviations of features
	across a corpus of volumes. These statistics can then be used to standardize
	the feature vectors in volumes.
	'''

	def __init__(self, listofvolumes, featurelist):
		numvolumes = len(listofvolumes)
		numfeatures = len(featurelist)

		# First a simple sanity check. We are talking about volumes with
		# the same number of features, right?

		for avolume in listofvolumes:
			assert avolume.numfeatures == numfeatures

		# And how about a spot check to make sure the lists are really the same?

		for ourfeature, itsfeature in zip(featurelist, listofvolumes[0].featurelist):
			assert ourfeature == itsfeature

		# Okay, we're good. Initialize some pandas series.

		means = list()
		stdevs = list()

		for afeature in featurelist:
			featuredistribution = np.zeros(numvolumes)

			# For each feature, create an array of possible values by polling volumes.

			for volidx, avolume in enumerate(listofvolumes):
				featuredistribution[volidx] = avolume.features[afeature]

			# Then calculate mean and standard deviation for this feature.

			thismean = np.mean(featuredistribution)
			thisstd = np.std(featuredistribution)

			if thisstd == 0:
				print("Problematic standard deviation of zero for feature " + afeature)
				thisstd = 0.0000001
				# Cheesy hack is my middle name.

			means.append(thismean)
			stdevs.append(thisstd)

		self.means = Series(means, index = featurelist)
		self.stdevs = Series(stdevs, index = featurelist)
		self.features = featurelist

		# Because we're going to need the list of features to apply this model
		# to other volumes.

		# Done.

class WordVector:
	''' A WordVector is just like a BagOfWords, except that it has
	a simpler constructor — it just accepts a list of tokens.
	In Java, you could write multiple constructors for one class.
	In Python, I'd have to rewrite the constructor inelegantly to make
	these a single class. So. Two classes.
	'''

	def __init__(self, listofwords):
		''' Construct a WordVector from a list.
		'''

		self.rawcounts = dict()
		self.totalcount = 0

		for word in listofwords:
			self.totalcount += 1
			if word in self.rawcounts:
				self.rawcounts[word] += 1
			else:
				self.rawcounts[word] = 1

		self.numrawcounts = len(self.rawcounts)

	def selectfeatures(self, featurelist):
		''' A WordVector is created with merely a dictionary of raw token counts.
		One could call this a sparse table. It has no entries where features are
		missing.

		We need to organize these as an ordered series of features, which includes
		only the features we have chosen to use in the current model, and has zeroes for
		missing values.
		'''

		self.featurelist = featurelist
		self.numfeatures = len(featurelist)
		self.features = Series(self.rawcounts, index = featurelist, dtype = 'float64')
		# Pandas has the nice feature of building a series from a dictionary if it's
		# provided an index of values. So this effectively builds a series of entries
		# ordered by the keys in 'featurelist,' with NaN in places where rawcounts
		# had no corresponding key.

		self.features[self.features.isnull()] = 0
		# This replaces NaN with zero, since missing words are effectively words with
		# count == 0.

	def normalizefrequencies(self):
		''' Simply divides all frequencies by the total token count for this volume.
		'''

		self.features = self.features / self.totalcount

	def standardizefrequencies(self, standardizer):
		''' Convert features to z-scores by centering them on the means and
		scaling them by standard deviation.

		standardizer = an object of class StandardizingVector, presumably created
		either on the corpus that contains this volume, or on the training corpus
		that created the model we are about to use on this volume.
		'''

		assert len(self.features) == len(standardizer.means)

		self.features = (self.features - standardizer.means) / standardizer.stdevs














