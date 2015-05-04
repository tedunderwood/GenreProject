# Reads all volumes meeting a given set of criteria,
# and uses a leave-one-out strategy to distinguish
# reviewed volumes (class 1) from random
# class 0. In cases where an author occurs more
# than once in the dataset, it leaves out all
# volumes by that author whenever making a prediction
# about one of them.

import numpy as np
import pandas as pd
import csv, os, random, sys
from collections import Counter
from multiprocessing import Pool
from sklearn.linear_model import LogisticRegression
import modelingprocess
import metafilter
from scipy.stats import norm

usedate = False

def appendif(key, value, dictionary):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

def forceint(astring):
    try:
        intval = int(astring)
    except:
        intval = 0

    return intval

def get_metadata(classpath, volumeIDs, excludeif, excludeifnot, excludebelow, excludeabove):
    '''
    As the name would imply, this gets metadata matching a given set of volume
    IDs. It returns a dictionary containing only those volumes that were present
    both in metadata and in the data folder.

    It also accepts four dictionaries containing criteria that will exclude volumes
    from the modeling process.
    '''

    metadict = dict()

    with open(classpath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')

        anonctr = 0

        for row in reader:
            volid = dirty_pairtree(row['docid'])
            theclass = row['recept'].strip()

            # I've put 'remove' in the reception column for certain
            # things that are anomalous.
            if theclass == 'remove':
                continue

            bail = False
            for key, value in excludeif.items():
                if row[key] == value:
                    bail = True
            for key, value in excludeifnot.items():
                if row[key] != value:
                    bail = True
            for key, value in excludebelow.items():
                if forceint(row[key]) < value:
                    bail = True
                    print(row[key])
            for key, value in excludeabove.items():
                if forceint(row[key]) > value:
                    bail = True

            if bail:
                continue

            birthdate = forceint(row['birth'])

            pubdate = forceint(row['date'])

            gender = row['gender'].rstrip()
            nation = row['nationality'].rstrip()

            #if pubdate >= 1880:
                #continue

            if nation == 'ca':
                nation = 'us'
            elif nation == 'ir':
                nation = 'uk'
            # I hope none of my Canadian or Irish friends notice this.

            notes = row['notes'].lower()
            author = row['author']
            if len(author) < 1:
                author = "anonymous" + str(anonctr)
                anonctr += 1

            title = row['title']
            canon = row['canon']

            # I'm creating two distinct columns to indicate kinds of
            # literary distinction. The reviewed column is based purely
            # on the question of whether this work was in fact in our
            # sample of contemporaneous reviews. The obscure column incorporates
            # information from post-hoc biographies, which trumps
            # the question of reviewing when they conflict.

            if theclass == 'vulgar':
                obscure = 'obscure'
                reviewed = 'not'
            elif theclass == 'elite':
                obscure = 'known'
                reviewed = 'rev'
            elif theclass == 'addcanon':
                obscure = 'known'
                reviewed = 'addedbecausecanon'
            else:
                print(theclass)

            if notes == 'well-known':
                obscure = 'known'
            if notes == 'obscure':
                obscure = 'obscure'

            if canon == 'y':
                if theclass == 'addcanon':
                    actually = 'Norton, added'
                else:
                    actually = 'Norton, in-set'
            elif reviewed == 'rev':
                actually = 'reviewed'
            else:
                actually = 'random'

            metadict[volid] = (reviewed, obscure, pubdate, birthdate, gender, nation, author, title, actually)

    # These come in as dirty pairtree; we need to make them clean.

    cleanmetadict = dict()
    allidsinmeta = set([x for x in metadict.keys()])
    allidsindir = set([dirty_pairtree(x) for x in volumeIDs])
    missinginmeta = len(allidsindir - allidsinmeta)
    missingindir = len(allidsinmeta - allidsindir)
    print("We have " + str(missinginmeta) + " volumes in missing in metadata, and")
    print(str(missingindir) + " volumes missing in the directory.")

    for anid in volumeIDs:
        dirtyid = dirty_pairtree(anid)
        if dirtyid in metadict:
            cleanmetadict[anid] = metadict[dirtyid]

    return cleanmetadict

def get_features(wordcounts, wordlist):
    numwords = len(wordlist)
    wordvec = np.zeros(numwords)
    for idx, word in enumerate(wordlist):
        if word in wordcounts:
            wordvec[idx] = wordcounts[word]

    return wordvec

def get_features_with_date(wordcounts, wordlist, date, totalcount):
    numwords = len(wordlist)
    wordvec = np.zeros(numwords + 1)
    for idx, word in enumerate(wordlist):
        if word in wordcounts:
            wordvec[idx] = wordcounts[word]

    wordvec = wordvec / (totalcount + 0.0001)
    wordvec[numwords] = date
    return wordvec

def sliceframe(dataframe, yvals, excludedrows, testrow):
    numrows = len(dataframe)
    newyvals = list(yvals)
    for i in excludedrows:
        del newyvals[i]
        # NB: This only works if we assume that excluded rows
        # has already been sorted in descending order !!!!!!!

    trainingset = dataframe.drop(dataframe.index[excludedrows])

    newyvals = np.array(newyvals)
    testset = dataframe.iloc[testrow]

    return trainingset, newyvals, testset

def normalizearray(featurearray, usedate):
    '''Normalizes an array by centering on means and
    scaling by standard deviations. Also returns the
    means and standard deviations for features, so that
    they can be pickled.
    '''

    numinstances, numfeatures = featurearray.shape
    means = list()
    stdevs = list()
    lastcolumn = numfeatures - 1
    for featureidx in range(numfeatures):

        thiscolumn = featurearray.iloc[ : , featureidx]
        thismean = np.mean(thiscolumn)

        thisstdev = np.std(thiscolumn)

        if (not usedate) or featureidx != lastcolumn:
            # If we're using date we don't normalize the last column.
            means.append(thismean)
            stdevs.append(thisstdev)
            featurearray.iloc[ : , featureidx] = (thiscolumn - thismean) / thisstdev
        else:
            print('FLAG')
            means.append(thismean)
            thisstdev = 0.1
            stdevs.append(thisstdev)
            featurearray.iloc[ : , featureidx] = (thiscolumn - thismean) / thisstdev
            # We set a small stdev for date.

    return featurearray, means, stdevs

def binormal_select(vocablist, positivecounts, negativecounts, totalpos, totalneg, k):
    all_scores = np.zeros(len(vocablist))

    for idx, word in enumerate(vocablist):
        # For each word we create a vector the length of vols in each class
        # that contains real counts, plus zeroes for all those vols not
        # represented.

        positives = np.zeros(totalpos, dtype = 'int64')
        if word in positivecounts:
            positives[0: len(positivecounts[word])] = positivecounts[word]

        negatives = np.zeros(totalneg, dtype = 'int64')
        if word in negativecounts:
            negatives[0: len(negativecounts[word])] = negativecounts[word]

        featuremean = np.mean(np.append(positives, negatives))

        tp = sum(positives > featuremean)
        fp = sum(positives <= featuremean)
        tn = sum(negatives > featuremean)
        fn = sum(negatives <= featuremean)
        tpr = tp/(tp+fn) # true positive ratio
        fpr = fp/(fp+tn) # false positive ratio

        bns_score = abs(norm.ppf(tpr) - norm.ppf(fpr))
        # See Forman

        if np.isinf(bns_score) or np.isnan(bns_score):
            bns_score = 0

        all_scores[idx] = bns_score

    zipped = [x for x in zip(all_scores, vocablist)]
    zipped.sort(reverse = True)
    with open('bnsscores.tsv', mode='w', encoding = 'utf-8') as f:
        for score, word in zipped:
            f.write(word + '\t' + str(score) + '\n')

    return [x[1] for x in zipped[0:k]]

## MAIN code starts here.

# sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/texts/'
# extension = '.fic.tsv'
# classpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/masterficmeta.csv'
# outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/predictions.csv'

sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/texts/'
extension = '.poe.tsv'
classpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/masterpoemeta.csv'
outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/nonfic/nonficpredictions.csv'

if not sourcefolder.endswith('/'):
    sourcefolder = sourcefolder + '/'

# This just makes things easier.

# Get a list of files.
allthefiles = os.listdir(sourcefolder)
# random.shuffle(allthefiles)

volumeIDs = list()
volumepaths = list()

for filename in allthefiles:

    if filename.endswith(extension):
        volID = filename.replace(extension, "")
        # The volume ID is basically the filename minus its extension.
        # Extensions are likely to be long enough that there is little
        # danger of accidental occurrence inside a filename. E.g.
        # '.fic.tsv'
        path = sourcefolder + filename
        volumeIDs.append(volID)
        volumepaths.append(path)

# Get the class and date vectors, indexed by volume ID
#
# This is also a place where we can simply exclude
# volumes from consideration on the basis on any
# metadata category we want, using the dictionaries
# defined below.

excludeif = dict()
# excludeif['impaud'] = 'pop'
excludeif['pubname'] = 'TEM'
excludeif['recept'] = 'addcanon'
#excludeif['gender'] = 'm'
excludeifnot = dict()
#excludeifnot['gender'] = 'm'
excludeabove = dict()
excludebelow = dict()

excludebelow['inferreddate'] = 1700
excludeabove['inferreddate'] = 1950
futurethreshold = 1950

metadict = metafilter.get_metadata(classpath, volumeIDs, excludeif, excludeifnot, excludebelow, excludeabove)

# Now that we have a list of volumes with metadata, we can select the groups of IDs
# that we actually intend to contrast. If we want to us more or less everything,
# this may not be necessary. But in some cases we want to use randomly sampled subsets.

# IDsToUse = set([x for x in metadict.keys()])

# The default condition here is

category2sorton = 'reviewed'
positive_class = 'rev'
sizecap = 350
# A sizecap less than one means, no sizecap.

IDsToUse, classdictionary = metafilter.balance_classes(metadict, category2sorton, positive_class, sizecap)

print(len(IDsToUse))
user = input('continue? ')
# NOW NONFICTION.

nonids = list()
nonpaths = list()
nonficfiles = os.listdir('religion')
for filename in nonficfiles:

    if filename.endswith('.non.tsv'):
        volID = filename.replace('.non.tsv', "")
        # The volume ID is basically the filename minus its extension.
        # Extensions are likely to be long enough that there is little
        # danger of accidental occurrence inside a filename. E.g.
        # '.fic.tsv'
        path = 'religion/' + filename
        nonids.append(volID)
        nonpaths.append(path)

nonficmetadict = metafilter.get_metadata('religion.csv', nonids, dict(), dict(), dict(), dict())

for key, value in nonficmetadict.items():
    metadict[key] = value

volumeIDs.extend(nonids)
volumepaths.extend(nonpaths)
IDsToUse = IDsToUse.union(set(nonids))
donttrainids = list()

keyset = [x for x in classdictionary.keys()]
for key in keyset:
    if classdictionary[key] == 2:
        donttrainids.append(key)
    classdictionary[key] = 1

print("We have " + str(len(donttrainids)) + " vols being classified but not trained on.")

for anid in nonids:
    classdictionary[anid] = 0

# make a vocabulary list and a volsize dict
wordcounts = Counter()

volspresent = list()
orderedIDs = list()

totalposvols = 0
totalnegvols = 0

for volid, volpath in zip(volumeIDs, volumepaths):
    if volid not in IDsToUse:
        continue
    else:
        volspresent.append((volid, volpath))
        orderedIDs.append(volid)

    classflag = classdictionary[volid]
    if classflag == 1:
        totalposvols += 1
    else:
        totalnegvols += 1

    with open(volpath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) > 2 or len(fields) < 2:
                print(line)
                continue
            word = fields[0]
            if len(word) > 0 and word[0].isalpha():
                count = int(fields[1])
                wordcounts[word] += 1
                # for initial feature selection we just use document freq,
                # so it's just +=1. But we do use the count to also
                # calculate bi-normal separation.

vocablist = [x[0] for x in wordcounts.most_common(3200)]

#vocablist = binormal_select(vocablist, positivecounts, negativecounts, totalposvols, totalnegvols, 3000)
VOCABSIZE = len(vocablist)


# Here we create a list of volumed IDs not to be used for training.
#
donttrainon = list()
for idx1, anid in enumerate(orderedIDs):
    if anid in donttrainids:
        donttrainon.append(idx1)

authormatches = [list(donttrainon) for x in range(len(orderedIDs))]
# For every index in authormatches, identify a set of indexes that have
# the same author. Obvs, there will always be at least one.

# Since we are going to use these indexes to exclude rows, we also add
# all the ids in donttrainon to every volume

for idx1, anid in enumerate(orderedIDs):
    thisauthor = metadict[anid]['author']
    for idx2, anotherid in enumerate(orderedIDs):
        otherauthor = metadict[anotherid]['author']
        if thisauthor == otherauthor and not idx2 in authormatches[idx1]:
            authormatches[idx1].append(idx2)

for alist in authormatches:
    alist.sort(reverse = True)

# I am reversing the order of indexes so that I can delete them from
# back to front, without changing indexes yet to be deleted.

volsizes = dict()
voldata = list()
classvector = list()

for volid, volpath in volspresent:

    with open(volpath, encoding = 'utf-8') as f:
        voldict = dict()
        totalcount = 0
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) > 2 or len(fields) < 2:
                print(line)
                continue

            word = fields[0]
            count = int(fields[1])
            voldict[word] = count
            totalcount += count

    date = metadict[volid]['pubdate']
    date = date - 1700
    if date < 0:
        print('lowdate')
        continue

    features = get_features(voldict, vocablist)
    voldata.append(features / (totalcount + 0.001))


    volsizes[volid] = totalcount
    classflag = classdictionary[volid]
    classvector.append(classflag)

data = pd.DataFrame(voldata)

fivetuples = list()
for i, volid in enumerate(orderedIDs):
    listtoexclude = authormatches[i]
    afivetuple = data, classvector, listtoexclude, i, usedate
    fivetuples.append(afivetuple)

# Now do leave-one-out predictions.
print('Beginning multiprocessing.')

pool = Pool(processes = 12)
res = pool.map_async(modelingprocess.model_one_volume, fivetuples)

# After all files are processed, write metadata, errorlog, and counts of phrases.
res.wait()
resultlist = res.get()

assert len(resultlist) == len(orderedIDs)

logisticpredictions = dict()
for i, volid in enumerate(orderedIDs):
    logisticpredictions[volid] = resultlist[i]

pool.close()
pool.join()

print('Multiprocessing concluded.')

truepositives = 0
truenegatives = 0
falsepositives = 0
falsenegatives = 0

with open(outputpath, mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    header = ['volid', 'reviewed', 'obscure', 'pubdate', 'birthdate', 'gender', 'nation', 'allwords', 'logistic', 'author', 'title', 'pubname', 'actually', 'realclass']
    writer.writerow(header)
    for volid in IDsToUse:
        metadata = metadict[volid]
        reviewed = metadata['reviewed']
        obscure = metadata['obscure']
        pubdate = metadata['pubdate']
        birthdate = metadata['birthdate']
        gender = metadata['gender']
        nation = metadata['nation']
        author = metadata['author']
        title = metadata['title']
        canonicity = metadata['canonicity']
        pubname = metadata['pubname']
        allwords = volsizes[volid]
        logistic = logisticpredictions[volid]
        realclass = classdictionary[volid]
        outrow = [volid, reviewed, obscure, pubdate, birthdate, gender, nation, allwords, logistic, author, title, pubname, canonicity, realclass]
        writer.writerow(outrow)

        if logistic > 0.5 and classdictionary[volid] > 0.5:
            truepositives += 1
        elif logistic <= 0.5 and classdictionary[volid] < 0.5:
            truenegatives += 1
        elif logistic <= 0.5 and classdictionary[volid] > 0.5:
            falsenegatives += 1
        elif logistic > 0.5 and classdictionary[volid] < 0.5:
            falsepositives += 1

trainingset, yvals, testset = sliceframe(data, classvector, [], 0)
newmodel = LogisticRegression(C = .00007)
trainingset, means, stdevs = normalizearray(trainingset, usedate)
newmodel.fit(trainingset, yvals)

coefficients = newmodel.coef_[0] * 1000000

coefficientuples = list(zip(coefficients, (coefficients / np.array(stdevs)), vocablist + ['pub.date']))
coefficientuples.sort()
for coefficient, normalizedcoef, word in coefficientuples:
    print(word + " :  " + str(coefficient))

print()
accuracy = (truepositives + truenegatives) / len(IDsToUse)
print('Accuracy is: ', str(accuracy))

with open('coefficients.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    for triple in coefficientuples:
        coef, normalizedcoef, word = triple
        writer.writerow([word, coef, normalizedcoef])

# user = input('Continue with listing of author clusters?')
# if user == 'n':
#     sys.exit(0)

# matchlens = list()
# for idx1, anid in enumerate(orderedIDs):
#     matches = authormatches[idx1]
#     matchlens.append(len(matches))

# decorated = list(zip(matchlens, orderedIDs, authormatches))
# decorated.sort(reverse = True)
# for i in range(30):
#     thisid = decorated[i][1]
#     print(metadict[thisid]['author'])
#     print('doesnt train on')
#     for idx in decorated[i][2]:
#         subid = orderedIDs[idx]
#         print('  ' + metadict[subid]['author'])
#     print()
futurethreshold = 1950

futureids = list()
for i, volid in enumerate(orderedIDs):
    pubdate = metadict[volid]['pubdate']
    if pubdate > futurethreshold:
        futureids.append(i)

if len(futureids) < 2:
    sys.exit(0)

pastthreshold = futurethreshold - 59
pastids = list()
for i, volid in enumerate(orderedIDs):
    pubdate = metadict[volid]['pubdate']
    if pubdate < pastthreshold:
        pastids.append(i)

futureids.sort(reverse=True)
excludeids = list()
excludeids.extend(pastids)
excludeids.extend(futureids)
excludeids.sort(reverse=True)

trainingset, yvals, testset = sliceframe(data, classvector, excludeids, futureids)
trainingset, means, stdevs = normalizearray(trainingset, usedate)
newmodel.fit(trainingset, yvals)
testset = (testset - means) / stdevs
predictions = [x[1] for x in newmodel.predict_proba(testset)]

truepositives = 0
truenegatives = 0
falsepositives = 0
falsenegatives = 0

logisticpredictions = dict()

for i, idx in enumerate(futureids):
    volid = orderedIDs[idx]
    logistic = predictions[i]
    logisticpredictions[volid] = logistic

    if logistic > 0.5 and classdictionary[volid] > 0.5:
        truepositives += 1
    elif logistic <= 0.5 and classdictionary[volid] < 0.5:
        truenegatives += 1
    elif logistic <= 0.5 and classdictionary[volid] > 0.5:
        falsenegatives += 1
    elif logistic > 0.5 and classdictionary[volid] < 0.5:
        falsepositives += 1

print()
accuracy = (truepositives + truenegatives) / len(futureids)
print('Accuracy is: ', str(accuracy))

selfpredictions = [x[1] for x in newmodel.predict_proba(trainingset)]
i = 0
for volid in orderedIDs:
    pubdate = metadict[volid]['pubdate']
    if pubdate <= futurethreshold and pubdate >= pastthreshold:
        logisticpredictions[volid] = selfpredictions[i]
        i += 1

futurepath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/futurepredictions.csv'

with open(futurepath, mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    header = ['volid', 'reviewed', 'obscure', 'pubdate', 'birthdate', 'gender', 'nation', 'allwords', 'logistic', 'author', 'title', 'pubname', 'actually', 'realclass']
    writer.writerow(header)
    for volid in IDsToUse:
        if volid not in logisticpredictions:
            continue
        metadata = metadict[volid]
        reviewed = metadata['reviewed']
        obscure = metadata['obscure']
        pubdate = metadata['pubdate']
        birthdate = metadata['birthdate']
        gender = metadata['gender']
        nation = metadata['nation']
        author = metadata['author']
        title = metadata['title']
        canonicity = metadata['canonicity']
        pubname = metadata['pubname']
        allwords = volsizes[volid]
        logistic = logisticpredictions[volid]
        realclass = classdictionary[volid]
        outrow = [volid, reviewed, obscure, pubdate, birthdate, gender, nation, allwords, logistic, author, title, pubname, canonicity, realclass]
        writer.writerow(outrow)












