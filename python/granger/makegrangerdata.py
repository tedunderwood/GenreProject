import numpy as np
import csv, os, random
from collections import Counter

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

def get_classvector(classpath, volumeIDs):
    with open(classpath, encoding = 'utf-8') as f:
        filelines = f.readlines()
    classdict = dict()
    datedict = dict()
    for line in filelines:
        line = line.rstrip()
        fields = line.split('\t')
        volid = dirty_pairtree(fields[0])
        theclass = fields[1]
        date = int(fields[2])
        if theclass == 'elite':
            classdict[volid] = 1
        elif theclass == 'vulgar':
            classdict[volid] = 0
        else:
            classdict[volid] = 0
            print('Anomalous class for ' + volid)
        datedict[volid] = date

    cleanclassdict = dict()
    cleandatedict = dict()
    for idx, anid in enumerate(volumeIDs):
        dirtyid = dirty_pairtree(anid)
        if dirtyid in classdict:
            cleanclassdict[anid] = classdict[dirtyid]
            cleandatedict[anid] = datedict[dirtyid]
        else:
            print('Missing from class metadata: ' + anid)

    return cleanclassdict, cleandatedict

## MAIN code starts here.

sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/granger/elite/'
extension = '.poe.tsv'
VOCABSIZE = 5000
classpath = '/Users/tunder/Dropbox/GenreProject/python/granger/correctedmeta.tsv'

if not sourcefolder.endswith('/'):
    sourcefolder = sourcefolder + '/'

# This just makes things easier.

# Get a list of files.
allthefiles = os.listdir(sourcefolder)
random.shuffle(allthefiles)

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

classdict, datedict = get_classvector(classpath, volumeIDs)

# make a vocabulary list and a volsize dict
wordcounts = Counter()
volsizes = Counter()
datebins = [1840,1845,1850,1855,1860,1865,1870,1875,1880,1885,1890,1895,1900,1905,1910,1915,1920]
# datebins = [1840,1850,1860,1870,1880,1890,1900,1910,1920]
NUMBINS = len(datebins)

for volid, volpath in zip(volumeIDs, volumepaths):
    with open(volpath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            word = fields[0]
            if len(word) > 1 and word[0].isalpha():
                count = int(fields[1])
                wordcounts[word] += 1
                volsizes[volid] += count

etymo = set()
with open('/Users/tunder/Dropbox/PythonScripts/mine/metadata/ReMergedEtymologies.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.split('\t')
        date = int(fields[1])
        if date > 800 and date < 1150:
            etymo.add(fields[0])

vocablist = [x[0] for x in wordcounts.most_common(VOCABSIZE)]
VOCABSIZE = len(vocablist)
vocabset = set(vocablist)
vocabmapper = dict()
for idx, word in enumerate(vocablist):
    vocabmapper[word] = idx

binsforcategory = dict()
binsizesforcategory = dict()
for category in [0,1]:

    datematrix = list()
    for i in range(NUMBINS):
        newlist = np.zeros(VOCABSIZE)
        datematrix.append(newlist)

    binsforcategory[category] = datematrix
    binsizes = [0] * NUMBINS
    binsizesforcategory[category] = binsizes


datemapper = dict()
for volid in volumeIDs:
    date = datedict[volid]
    for idx, dateceiling in enumerate(datebins):
        if date < dateceiling:
            datemapper[volid] = idx
            category = classdict[volid]
            binsizesforcategory[category][idx] += volsizes[volid]
            break

for volid, volpath in zip(volumeIDs, volumepaths):
    with open(volpath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            word = fields[0]
            if word in vocabset:
                count = int(fields[1])
                dateidx = datemapper[volid]
                category = classdict[volid]
                vocabidx = vocabmapper[word]
                binsforcategory[category][dateidx][vocabidx] += count

# Normalize counts to relative frequencies.
for category in [0, 1]:
    for i in range(NUMBINS):
        binsforcategory[category][i] = binsforcategory[category][i] / binsizesforcategory[category][i]

with open('/Users/tunder/Dropbox/GenreProject/python/granger/elite1860-1919.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(vocablist)
    for idx, row in enumerate(binsforcategory[1]):
        writer.writerow(row)

with open('/Users/tunder/Dropbox/GenreProject/python/granger/vulgar1860-1919.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(vocablist)
    for idx, row in enumerate(binsforcategory[0]):
        writer.writerow(row)


















