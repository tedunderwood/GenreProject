# CommonFunctions.py
# Version May 26, 2014

def addtodict(word, count, lexicon):
	'''Adds an integer (count) to dictionary (lexicon) under
	the key (word), or increments lexicon[word] if key present. '''

	if word in lexicon:
		lexicon[word] += count
	else:
		lexicon[word] = count

def sortkeysbyvalue(lexicon, whethertoreverse = False):
	'''Accepts a dictionary where keys point to a (presumably numeric) value, and
	returns a list of keys sorted by value.'''

	tuplelist = list()
	for key, value in lexicon.items():
		tuplelist.append((value, key))

	tuplelist = sorted(tuplelist, reverse = whethertoreverse)
	return tuplelist