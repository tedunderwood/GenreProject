# code_specific_volume.py

# Randomly selects 12 snippets from a volume, gets you to code them
# manually, and then reports the log of (reference / wage)

 # The data structure for the coded snippets is as follows:
    # 0) date,
    # 1) volumeid
    # 2) reference type: a (q)uantity of money "five dollars",
        # or an (e)rror -- not money or not quantifiable

    # 3) unit of currency in which money is denominated

    # 4) value -- nominal value of money.

    # 5) socialcontext — gift, bribe, inheritance, rent, interest,
        # capital, wages, price, etc. This list can be expanded at will
        # by coders; this script allows you to add to it.

    # 6) snippet.

import os, sys
import random
import csv
import glob

import csv
import math
from scipy import median

def read_coded_snippets(filepath):
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

# HERE IS WHERE THE MAIN FUNCTION BEGINS.
def main():

    # We attempt to use 'glob' to find files with the appropriate names in
    # the local directory.

    snippetpath = glob.glob('twentyfivesnippets.tsv')[0]

    vol2code = input('Volume to code? ')
    what2call = input('What to call it? ')
    outputfile = what2call + '.tsv'

    # get the metadata
    metadatapath = glob.glob('unifiedficmetadata.csv')[0]
    voldate = 0

    with open(metadatapath, encoding = 'utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        # That skips the header
        for row in reader:
            volid = row[0]
            date = int(row[1])
            if volid == vol2code:
                voldate = date

    if voldate < 1750:
        print("Didn't find that volume.")
        sys.exit(0)

    snippetsinvol = list()

    with open(snippetpath, encoding = 'utf-8') as f:
        for line in f:
            line = line.rstrip()
            fields = line.split('\t')
            volid = fields[0]
            date = int(fields[1])
            snippet = fields[4]

            if volid == vol2code:
                snippetsinvol.append(snippet)


    numbertocode =15
    if numbertocode > len(snippetsinvol):
        numbertocode = len(snippetsinvol)

    allowabletypes = {'q', 'e'}

    # HERE IS WHERE WE ACTUALLY ITERATE THROUGH SNIPPETS AND ASK THE USER
    # TO CODE THEM.

    random.shuffle(snippetsinvol)
    for snippet in snippetsinvol[0:numbertocode]:

        print()
        print(snippet)
        print()
        reftype = "primal chaos"
        while not reftype in allowabletypes:
            reftype = input("Is this a Quantifiable snippet or an Error (q or e): ")

        if reftype == 'e':
            # We don't need to ask further questions for these types.
            poundvalue = 0.0
            socialcontext = "nonmonetary"
            unit = 'none'

        else:
            # A quantifiable snippet requires further questioning.

            print('I assume the value is denominated in pounds unless you say otherwise.')
            user = input("Currency: pounds (hit return). Or 'dollars' or 'francs', etc: ")
            if user == 'dollars' or user == 'd':
                unit = 'dollars'
            elif user == 'francs' or user == 'f':
                unit = 'francs'
            elif user == 'pounds' or len(user) < 1:
                unit = 'pounds'
            else:
                print("You entered " + user + ", which is an anomalous unit.")
                user = input("Re-enter that please to confirm: ")
                unit = user

            quantified = False
            while not quantified:
                numericstring = input("Face value of money? (count unquantified plurals as x10): ")
                try:
                    poundvalue = float(numericstring)
                    quantified = True
                except:
                    print("I couldn't interpret that as a float. Try again.")

            valid = False
            while not valid:
                socialcontext = input("Social context? ")
                valid = True
                # When you're coding specific volumes, everything is permitted.

        outline = '\t'.join([str(voldate), vol2code, reftype, unit, str(poundvalue), socialcontext, snippet])
        with open(outputfile, mode = 'a', encoding = 'utf-8') as f:
            f.write(outline + '\n')

        print()

    print('Exhausted snippet list. Done.')

    # Now it's time to convert these babies into log (nominal value / annual wage)

    nominal_pairs = read_coded_snippets(outputfile)
    wages = get_wage_sequence('labours.csv')
    normalized_triplets = normalize(nominal_pairs, wages)
    allnominals = list()
    allnormalized = list()
    alllogvals = list()
    for date, nominal_val, normalized_value in normalized_triplets:
        allnominals.append(nominal_val)
        allnormalized.append(normalized_value)
        alllogvals.append(math.log10(normalized_value))

    print(" Median nominal: " + str(median(allnominals)))
    print(" Median normalized: " + str(median(allnormalized)))
    print(" Median logval: " + str(median(alllogvals)))




if __name__ == "__main__":
    main()
