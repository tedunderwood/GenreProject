#!/usr/bin/env python3

# Script tested in Python 3.3.4.

# conversions.py

# This reads in a list of coded snippets and converts the face value of the money to
# a number that is relative to a worker's average yearly wage. This involves two
# conversions: first, figuring exchange rates, and then normalizing relative to
# inflation.

import csv
import math

def get_special_cases():
    with open('/Users/tunder/Dropbox/GenreProject/python/piketty/badvolids.txt', encoding = 'utf-8') as f:
        badids = [x.rstrip() for x in f.readlines()]

    correcteddates = dict()
    with open('correctedmetadata.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 5 and len(row[5]) > 0:
                newdate = int(row[5])
                if newdate < 1750:
                    badids.append(row[0])
                elif newdate < 1950:
                    correcteddates[row[0]] = newdate

    return badids, correcteddates

def read_coded_snippets(filepath, badids, correcteddates):
    ''' Reads the snippets and first, applies exchange rates to convert them to pounds.
    Exchange rates are relatively constant in this period.
    It then returns a list of pairs, where each pair consists of a date combined with
    the nominal value of the snippet, in pounds.
    '''

    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()

    date_nominal_pairs = list()

    for line in filelines:
        line = line.rstrip()
        fields = line.split('\t')
        date = int(fields[0])
        volid = fields[1]
        if volid in badids:
            print('badid')
            continue
        if volid in correcteddates:
            date = correcteddates[volid]
            print(volid + ' corrected.')
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

        date_nominal_pairs.append((date, facevalue))

    return date_nominal_pairs

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

def main():
    badids, correcteddates = get_special_cases()
    nominal_pairs = read_coded_snippets('codedsnippets.tsv', badids, correcteddates)
    wages = get_wage_sequence('labours.csv')
    normalized_triplets = normalize(nominal_pairs, wages)
    with open('codedsnippets.csv', mode = 'w', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'nominalval', 'normval', 'logval'])
        for date, nominal_val, normalized_value in normalized_triplets:
            row = [date, nominal_val, normalized_value, math.log10(normalized_value)]
            writer.writerow(row)

if __name__ == '__main__':
    main()









