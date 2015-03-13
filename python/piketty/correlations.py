#!/usr/bin/env python3

# Script tested in Python 3.3.4.

# correlations.py

# This reads in a list of coded snippets and converts the face value of the money to
# a number that is relative to a worker's average yearly wage. This involves two
# conversions: first, figuring exchange rates, and then normalizing relative to
# inflation.

import csv
import glob
import numpy as np
import math
from scipy.stats.stats import pearsonr

with open('/Users/tunder/Dropbox/GenreProject/python/piketty/badvolids.txt', encoding = 'utf-8') as f:
    badids = [x.rstrip() for x in f.readlines()]

snippetpath = glob.glob('manualcoding/twentyfivesnippets.tsv')[0]

snippetcounts = dict()
# This will be a dictionary, keyed by volid, where the value
# is a count of the number of snippets assigned to that vol.

with open(snippetpath, encoding = 'utf-8') as f:
    for line in f:
        line = line.rstrip()
        fields = line.split('\t')
        volid = fields[0]
        if volid in snippetcounts:
            snippetcounts[volid] += 1
        else:
            snippetcounts[volid] = 1

metadatapath = glob.glob('manualcoding/unifiedficmetadata.csv')[0]

volsbydate = dict()
# This will be a dictionary, keyed by date, where the value is a
# list of volume ids associated with that date.

authors = dict()
titles = dict()
datesbyvol = dict()
wordcounts = dict()
with open(metadatapath, encoding = 'utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)
    # That skips the header
    for row in reader:
        volid = row[0]
        date = int(row[1])
        if date in volsbydate:
            volsbydate[date].append(volid)
        else:
            volsbydate[date] = [volid]
        datesbyvol[volid] = date
        wordcount = row[2]
        author = row[3]
        title = row[4]
        wordcounts[volid] = int(wordcount)
        titles[volid] = title
        authors[volid] = author

def read_coded_snippets(filepath):
    ''' Reads the snippets and first, applies exchange rates to convert them to pounds.
    Exchange rates are relatively constant in this period.
    It then returns a list of pairs, where each pair consists of a date combined with
    the nominal value of the snippet, in pounds.
    '''
    global badids

    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()

    earliest_pairs = list()
    early_nominal_pairs = list()
    late_nominal_pairs = list()
    latest_pairs = list()

    for line in filelines:
        line = line.rstrip()
        fields = line.split('\t')
        date = int(fields[0])
        volid = fields[1]
        if volid.startswith('10'):
            volid = '000' + volid
        if volid in badids:
            print('badid')
            continue
        currency = fields[3]
        facevalue = float(fields[4])

        if currency == 'none' or facevalue < .0000001:
            continue
            # This snippet was an error.

        elif currency.startswith('dollar'):
            facevalue = facevalue / 5
        elif currency.startswith('franc'):
            facvalue = facevalue / 25
        elif currency.startswith('florin'):
            facevalue = facevalue / 10

        if date < 1800:
            earliest_pairs.append((volid, facevalue))
        elif date < 1850:
            early_nominal_pairs.append((volid, facevalue))
        elif date <= 1900:
            late_nominal_pairs.append((volid, facevalue))
        else:
            latest_pairs.append((volid, facevalue))

    return [earliest_pairs, early_nominal_pairs, late_nominal_pairs, latest_pairs]

all_nominal_pairs = read_coded_snippets('manualcoding/TedRichSnippets.tsv')

for pairlist in all_nominal_pairs:
    facevalues = list()
    snippetspervol = list()

    for volid, faceval in pairlist:
        facevalues.append(faceval)
        snippetspervol.append(snippetcounts[volid] / wordcounts[volid])

    print(pearsonr(facevalues, snippetspervol))







