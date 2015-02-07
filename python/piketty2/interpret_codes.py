# interpret_codes

import os, sys
import random
import csv
import glob

import csv
import math
from scipy import median
from collections import Counter

def read_coded_snippets(filepath):
    ''' Reads the snippets and first, applies exchange rates to convert them to pounds.
    Exchange rates are relatively constant in this period.
    It then returns a list of pairs, where each pair consists of a date combined with
    the nominal value of the snippet, in pounds.
    '''

    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()

    date_nominal_pairs = dict()
    prices = Counter()
    totalcount = Counter()

    for line in filelines:
        line = line.rstrip()
        fields = line.split('\t')
        date = int(fields[0])
        volid = fields[1]
        currency = fields[3]
        facevalue = float(fields[4])

        if currency == 'none' or facevalue < .0000001:
            continue
            # This snippet was an error.

        elif currency.startswith('dollar'):
            facevalue = facevalue / 5
        elif currency.startswith('franc'):
            facevalue = facevalue / 25
        elif currency.startswith('florin'):
            facevalue = facevalue / 10

        totalcount[volid] += 1
        if fields[5].startswith('price'):
            prices[volid] += 1

        if volid in date_nominal_pairs:
            date_nominal_pairs[volid].append((date, facevalue))
        else:
            date_nominal_pairs[volid] = [(date, facevalue)]

    return date_nominal_pairs, totalcount, prices

def get_wage_sequence(filepath):
    ''' Creates a dictionary that pairs dates with an estimated average
    annual wage, in pounds, for British workers in that year. We're using
    British wages for purposes of inflation adjustment; although the curve
    is different in the US, it's not different enough to make a huge difference.
    '''
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()

    relative = dict()

    for i in range(1750, 1790):
        relative[i] = 29.3

    for line in filelines:
        line = line.rstrip()
        fields = line.split(',')
        date = int(fields[0])
        rel = float(fields[1])
        relative[date] = rel

    # We know that annual wages in 1911 were £58.6.
    # And the relative index in 1911 is 94.8.
    # Using those facts we can normalize to recreate
    # the nominal wage for each year.

    wage = dict()
    for i in range (1750, 1951):
        wage[i] = (relative[i] / 94.8) * 58.6

    return wage

def normalize(nominal_pairs, wages):
    ''' Uses annual wages to normalize references to money: i.e., it translates the
    reference from a nominal value, in pounds, to a fraction of a worker's annual
    wage in the year of publication.
    '''
    normalized_triplets = list()

    for date, nominalval in nominal_pairs:

        normalized_value = nominalval / wages[date]
        normalized_triplets.append((date, nominalval, normalized_value))

    return normalized_triplets


# get metadata

metapath = glob.glob('anovaset.csv')[0]
metadata = dict()
datedict = dict()
genredict = dict()

with open(metapath, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        htid = row['htid']
        author = row['author']
        title = row['title']
        date = row['date']
        metadata[htid] = (author, title)
        datedict[htid] = date
        genredict[htid] = row['category']

# We attempt to use 'glob' to find files with the appropriate names in
# the local directory.

inputpath = '/Users/tunder/Dropbox/GenreProject/python/piketty2/anovacoded.tsv'

nominal_pairs, counts, prices = read_coded_snippets(inputpath)
wages = get_wage_sequence('labours.csv')

volscoded = [x for x in nominal_pairs.keys()]
with open('codedvoldata.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['volid', 'date', 'genre', 'logval', 'counts', 'prices'])
    for volid in volscoded:
        print(metadata[volid])
        genre = genredict[volid]
        date = datedict[volid]
        count = counts[volid]
        price = prices[volid]
        priceratio = price / (count + 0.001)
        these_pairs = nominal_pairs[volid]
        normalized_triplets = normalize(these_pairs, wages)
        allnominals = list()
        allnormalized = list()
        alllogvals = list()
        for date, nominal_val, normalized_value in normalized_triplets:
            allnominals.append(nominal_val)
            allnormalized.append(normalized_value)
            alllogvals.append(math.log10(normalized_value))

        mednom = median(allnominals)
        mednorm = median(allnormalized)
        medlog = median(alllogvals)
        print(" Median nominal: " + str(mednom))
        print(" Median normalized: " + str(mednorm))
        print(" Median logval: " + str(medlog))
        print()

        writer.writerow([volid, date, genre, medlog, count, priceratio])


