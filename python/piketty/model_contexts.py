# model_contexts.py

import SonicScrewdriver as utils
import os, sys
import random
from bagofwords import WordVector, StandardizingVector
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation

def strip_punctuation(astring):
    global punctuple
    keepclipping = True
    suffix = ""
    while keepclipping == True and len(astring) > 1:
        keepclipping = False
        if astring.endswith(punctuple):
            suffix = astring[-1:] + suffix
            astring = astring[:-1]
            keepclipping = True
    keepclipping = True
    prefix = ""
    while keepclipping == True and len(astring) > 1:
        keepclipping = False
        if astring.startswith(punctuple):
            prefix = prefix + astring[:1]
            astring = astring[1:]
            keepclipping = True
    return(prefix, astring, suffix)

def make_vector(snippet):
    wordlist = as_wordlist(snippet)
    vector = WordVector(wordlist)

    return vector

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

def as_wordlist(line):
    ''' Converts a line into a list of words, splitting
    tokens brutally and unreflectively at punctuation.
    One of the effects will be to split possessives into noun
    and s. But this might not be a bad thing for current
    purposes.
    '''

    line = line.replace('”', ' ')
    line = line.replace(':', ' ')
    line = line.replace(';', ' ')
    line = line.replace('—', ' ')
    line = line.replace('--', ' ')
    line = line.replace('.', ' ')
    line = line.replace(',', ' ')
    line = line.replace('-', ' ')
    line = line.replace('—', ' ')
    line = line.replace("'", ' ')
    line = line.replace('"', ' ')

    # That's not the most efficient way to do this computationally,
    # but it prevents me from having to look up the .translate
    # method.

    words = line.split(' ')

    wordlist = list()

    for word in words:
        word = word.lower()
        prefix, word, suffix = strip_punctuation(word)
        # In case we missed anything.

        if len(word) > 0 and not all_nonalphanumeric(word):
            wordlist.append(word)

    return wordlist

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

    topfeatures = [x[1] for x in descendingbyfreq[0 : n]]

    return topfeatures

def normalizedsample(datedict, N, alreadyhave):
    '''
    Returns N snippets from each date in the datedict, with the constraints
    that a) obviously you can't return more than exist and b) you can tell it
    not to return snippets you already have.
    '''

    exclude = set(alreadyhave)
    returnlist = []

    for date, snippetlist in datedict.items():
        numinyear = len(snippetlist)
        if N >= numinyear:
            thisyear = snippetlist
        else:
            thisyear = random.sample(snippetlist, N)

        newones = set(thisyear) - exclude

        returnlist.extend(newones)

    return returnlist


## BEGIN MAIN.

punctuple = ('.', ',', '?', '!', ';', '"', '“', '”', ':', '--', '—', ')', '(', "'", "`", "[", "]", "{", "}")

maxfeatures = 1000

infile = "/Volumes/TARDIS/work/moneycontext/contexts.tsv"

outputfolder = "/Volumes/TARDIS/work/moneycontext/"

bydate = dict()

with open(infile, encoding = 'utf-8') as f:
    for line in f:
        trim = line.rstrip()
        fields = trim.split('\t')
        date = int(fields[1])

        snippet = fields[2]

        if "8vo" in snippet:
            continue
            # Because those are ads.

        if date in bydate:
            bydate[date].append(snippet)
        else:
            bydate[date] = [snippet]

trainingfile = "/Volumes/TARDIS/work/moneycontext/training.tsv"

training = []
money = []
notmoney = []

if os.path.isfile(trainingfile):

    with open(trainingfile, encoding = 'utf-8') as f:
        for line in f:
            trim = line.rstrip()
            fields = trim.split('\t')
            training.append(fields[1])
            if fields[0] == "0":
                notmoney.append(fields[1])
            else:
                money.append(fields[1])

N = int(input("How many snippets per year to sort? "))

tosort = normalizedsample(bydate, N, training)

print('\n')
print(str(len(tosort)) + " total snippets to sort.\n")

newmoney = []
newnotmoney = []

for snippet in tosort:
    print(snippet)
    user = input("Is this money? ")
    if user == "n":
        newnotmoney.append(snippet)
    else:
        newmoney.append(snippet)

# Append the new snippets to the training file.

with open(trainingfile, mode = 'a', encoding = 'utf-8') as f:
    for snippet in newmoney:
        f.write("1" + '\t' + snippet + '\n')
        money.append(snippet)
    for snippet in newnotmoney:
        f.write("0" + '\t' + snippet + '\n')
        notmoney.append(snippet)

# Now we actually read volumes and create a training corpus, which will
# be a list of WordVectors.

trainingset = list()
classvector = list()
idctr = 0
snippetIDs = list()

for snippet in money:
    trainingset.append(make_vector(snippet))
    classvector.append(1)
    snippetIDs.append(str(idctr))
    idctr += 1

for snippet in notmoney:
    trainingset.append(make_vector(snippet))
    classvector.append(0)
    snippetIDs.append(str(idctr))
    idctr += 1

zipiterator = zip(trainingset, classvector)
listofpairs = [x for x in zipiterator]
random.shuffle(listofpairs)
unzipped = [list(x) for x in zip(*listofpairs)]
trainingset = unzipped[0]
classvector = unzipped[1]
classvector = pd.Series(classvector)

# We select the most common words as features.
featurelist = select_common_features(trainingset, maxfeatures)
numfeatures = len(featurelist)
# Note that the number of features we actually got is not necessarily
# the same as maxfeatures.

for snippet in trainingset:
    snippet.selectfeatures(featurelist)
    snippet.normalizefrequencies()
    # The snippet now contains feature frequencies:
    # raw counts have been divided by the total number of words in the snippet.

standardizer = StandardizingVector(trainingset, featurelist)
# This object calculates the means and standard deviations of all features
# across the training set.

listofsnippetfeatures = list()
for snippet in trainingset:
    snippet.standardizefrequencies(standardizer)
    # We have now converted frequencies to z scores. This is important for
    # regularized logistic regression -- otherwise the regularization
    # gets distributed unevenly across variables because they're scaled
    # differently.

    listofsnippetfeatures.append(snippet.features)

# Now let's make a data frame by concatenating each snippet as a separate column,
# aligned on the features that index rows.

data = pd.concat(listofsnippetfeatures, axis = 1)
data.columns = snippetIDs

# Name the columns for snippets. Then transpose the matrix:

data = data.T

# So that we have a matrix with features (variables) as columns and instances (snippets)
# as rows. Would have been easier to make this directly, but I don't know a neat
# way to do it in pandas.

logisticmodel = LogisticRegression(C = 0.001)
classvector = classvector.astype('int')
logisticmodel.fit(data, classvector)

# Let's sort the features by their coefficient in the model, and print.

coefficients = list(zip(logisticmodel.coef_[0], featurelist))
coefficients.sort()
# for coefficient, word in coefficients:
#     print(word + " :  " + str(coefficient))

# Pickle and write the model & standardizer. This will allow us to apply the model to
# new documents of unknown genre.

modelfile = outputfolder + "logisticmodel.p"
with open(modelfile, mode = 'wb') as f:
    pickle.dump(logisticmodel, f)
standardizerfile = outputfolder + "standardizer.p"
with open(standardizerfile, mode = 'wb') as f:
    pickle.dump(standardizer, f)
featurelistfile = outputfolder + 'featurelist.p'
with open(featurelistfile, mode = 'wb') as f:
    pickle.dump(featurelist, f)

accuracy_tries = cross_validation.cross_val_score(logisticmodel, data, classvector, cv=5)
print(accuracy_tries)
print(np.sum(accuracy_tries)/len(accuracy_tries))

# Yay, we're done.

print('Done.')











