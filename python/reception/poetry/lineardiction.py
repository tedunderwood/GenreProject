# Linear model of diction.

import csv
from collections import Counter
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
import numpy as np
import pandas as pd

def get_genre(datapath, targetgenre):
    genrecounts = dict()

    with open(datapath, encoding = 'utf-8') as f:

        reader = csv.reader(f)
        for row in reader:
            genre = row[2]
            if genre == targetgenre:
                year = int(row[3])
                word = row[0]
                count = int(row[1])
                if year in genrecounts:
                    genrecounts[year][word] += count
                else:
                    genrecounts[year] = Counter()
                    genrecounts[year][word] += count

    return genrecounts

def add_genres(genrelist):
    newcounts = dict()
    for genre in genrelist:
        for year, wordcounts in genre.items():
            if year in newcounts:
                for word, count in wordcounts.items():
                    newcounts[year][word] += count
            else:
                newcounts[year] = Counter()
                for word, count in wordcounts.items():
                    newcounts[year][word] += count

    return newcounts

def filter_genre(agenre, cutoff):

    newcounts = dict()
    for year, wordcounts in agenre.items():
        if year >= cutoff:
            newcounts[year] = wordcounts

    return newcounts

def most_common(listofgenres, n):
    wordtotals = Counter()
    for genre in listofgenres:
        for year, wordcounts in genre.items():
            for word, count in wordcounts.items():
                wordtotals[word] += count

    wordlist = [x[0] for x in wordtotals.most_common(n)]
    return wordlist

def normalize(agenre):
    for year, wordcounts in agenre.items():
        totalcount = 0
        for word, count in wordcounts.items():
            totalcount += count
        for word, count in wordcounts.items():
            wordcounts[word] = wordcounts[word] / (totalcount + .001)

def get_features(wordcounts, wordlist):
    numwords = len(wordlist)
    wordvec = np.zeros(numwords)
    for idx, word in enumerate(wordlist):
        if word in wordcounts:
            wordvec[idx] = wordcounts[word]

    return wordvec


def genres_to_pandaframe(positivegenres, negativegenre, wordlist, method):
    '''
    Turns two (or more) dictionaries containing wordcount data for instances (years)
    into a pandas dataframe containing the data and a vector of class
    labels or y values.
    '''
    listofinstances = list()
    listofyvals = list()

    for genre in positivegenres:
        for instance, wordcounts in genre.items():
            featureseries = get_features(wordcounts, wordlist)
            listofinstances.append(featureseries)
            if method == 'straight':
                listofyvals.append(1)
            else:
                listofyvals.append(instance - 1780)

    for instance, wordcounts in negativegenre.items():
        featureseries = get_features(wordcounts, wordlist)
        listofinstances.append(featureseries)
        listofyvals.append(0)

    data = pd.DataFrame(listofinstances)
    yvals = np.array(listofyvals)

    return data, yvals

yeardatapath = '/Volumes/TARDIS/work/mysql/yeargenjoint.csv'

fiction = get_genre(yeardatapath, 'fic')
poetry = get_genre(yeardatapath, 'poe')
nonfic = get_genre(yeardatapath, 'non')

fiction = filter_genre(fiction, 1860)
poetry = filter_genre(poetry, 1860)
nonfic = filter_genre(nonfic, 1860)

normalize(fiction)
normalize(poetry)
normalize(nonfic)

commonwords = most_common([poetry, nonfic], 3200)
featurelist = commonwords[200:]

with open('/Users/tunder/Dropbox/DataMunging/rulesets/MainDictionary.txt', encoding = 'utf-8') as f:
    maindict = set([x.split('\t')[0] for x in f])

with open('/Users/tunder/Dropbox/DataMunging/rulesets/PersonalNames.txt', encoding = 'utf-8') as f:
    names = set([x.rstrip().lower() for x in f])

with open('/Users/tunder/Dropbox/DataMunging/rulesets/PlaceNames.txt', encoding = 'utf-8') as f:
    places = set([x.rstrip().lower() for x in f])

places.add('iv')
places.add('ix')

filteredfeatures = list()
for word in featurelist:
    if len(word) < 2:
        print(word)
        continue

    if word in maindict and not (word in names or word in places):
        filteredfeatures.append(word)
    else:
        print(word)

data, yvals = genres_to_pandaframe([poetry], nonfic, filteredfeatures, 'straight')

model = Ridge(alpha = 0.001)
model.fit(data, yvals)

coefficients = list(zip(model.coef_, featurelist))
coefficients.sort()
for coefficient, word in coefficients:
    print(word + " :  " + str(coefficient))

outlist = list()
for year, wordcounts in poetry.items():
    features = get_features(wordcounts, filteredfeatures)
    selfpredict = model.predict(features)
    outline = 'poe' + ',' + str(year) + ',' + str(selfpredict) + '\n'
    outlist.append(outline)

for year, wordcounts in fiction.items():
    features = get_features(wordcounts, filteredfeatures)
    selfpredict = model.predict(features)
    outline = 'fic' + ',' + str(year) + ',' + str(selfpredict) + '\n'
    outlist.append(outline)

for year, wordcounts in nonfic.items():
    features = get_features(wordcounts, filteredfeatures)
    selfpredict = model.predict(features)
    outline = 'non' + ',' + str(year) + ',' + str(selfpredict) + '\n'
    outlist.append(outline)

with open('/Users/tunder/Dropbox/GenreProject/python/reception/poetry/selfpredict.csv', mode='w', encoding = 'utf-8') as f:
    for line in outlist:
        f.write(line)

def prediction(voldict):
    global filteredfeatures, model

    totalcount = 0
    for word, count in voldict.items():
        totalcount += count

    numwords = len(filteredfeatures)
    wordvec = np.zeros(numwords)
    for idx, word in enumerate(filteredfeatures):
        if word in voldict:
            wordvec[idx] = voldict[word] / (totalcount + .001)

    yval = model.predict(wordvec)
    return yval



