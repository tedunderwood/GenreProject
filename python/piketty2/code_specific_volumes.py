# code_specific_volumes.py

# Based on code_specific_volume in the first /piketty repo,
# this is designed to chew through a whole batch of files.

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

    date_nominal_pairs = dict()

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
        if volid in date_nominal_pairs:
            date_nominal_pairs[volid].append((date, facevalue))
        else:
            date_nominal_pairs[volid] = [(date, facevalue)]

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

    # get metadata

    metapath = glob.glob('anovaset.csv')[0]
    metadata = dict()
    datedict = dict()
    with open(metapath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            htid = row['htid']
            author = row['author']
            title = row['title']
            date = row['date']
            metadata[htid] = (author, title)
            datedict[htid] = date

    # We attempt to use 'glob' to find files with the appropriate names in
    # the local directory.

    snippetpath = glob.glob('anovasnippets.tsv')[0]

    outputpaths = glob.glob('anovacoded.tsv')
    volsalreadycoded = set()

    if len(outputpaths) > 0:
        outputpath = outputpaths[0]

        with open(outputpath, encoding = 'utf-8') as f:
            filelines = f.readlines()
        for line in filelines[1:]:
            htid = line.split('\t')[1]
            volsalreadycoded.add(htid)
    else:
        outputpath = '/Users/tunder/Dropbox/GenreProject/python/piketty2/anovacoded.csv'

    snippets = dict()
    print(volsalreadycoded)

    with open(snippetpath, encoding = 'utf-8') as f:
        filelines = f.readlines()

    for line in filelines:
        fields = line.rstrip().split('\t')
        htid = fields[0]
        if htid in volsalreadycoded:
            continue
        else:
            if htid in snippets:
                snippets[htid].append(fields[3])
            else:
                snippets[htid] = [fields[3]]


    ceiling = 20
    allowabletypes = {'q', 'e'}
    keepgoing = True
    volstocode = [x for x in snippets.keys()]

    for volid in volstocode:

        voldate = datedict[volid]
        print(volid)

        # HERE IS WHERE WE ACTUALLY ITERATE THROUGH SNIPPETS AND ASK THE USER
        # TO CODE THEM.
        snippetsinvol = snippets[volid]
        if ceiling > len(snippetsinvol):
            maxsnippets = len(snippetsinvol)
        else:
            maxsnippets = ceiling

        volumelist = list()

        snippetstocode = random.sample(snippetsinvol, maxsnippets)
        for snippet in snippetstocode:

            print()
            print(snippet)
            print()
            print('Unit of currency or e for error.')
            user = input("Currency: pounds (hit return). Or 'dollars' or 'francs', etc: ")

            if user == 'e':
                reftype = 'e'
                # We don't need to ask further questions for these types.
                poundvalue = 0.0
                socialcontext = "nonmonetary"
                unit = 'none'

            else:
                reftype = 'q'

                if user == 'dollars' or user == 'd':
                    unit = 'dollars'
                elif user == 'francs' or user == 'f':
                    unit = 'francs'
                elif user == 'pounds' or user == 'p' or len(user) < 1:
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

            outline = '\t'.join([str(voldate), volid, reftype, unit, str(poundvalue), socialcontext, snippet])
            volumelist.append(outline)
            # end iteration across snippets

        print('Exhausted snippet list. Done with this vol.')

        with open(outputpath, mode = 'a', encoding = 'utf-8') as f:
            for line in volumelist:
                f.write(line + '\n')

        print()

        user = input('Snippets written to file. Are you up for another volume? ')
        if user == 'n':
            break

        # end iteration across volumes

    # Now it's time to convert these babies into log (nominal value / annual wage)

    nominal_pairs = read_coded_snippets(outputpath)
    wages = get_wage_sequence('labours.csv')

    volscoded = [x for x in nominal_pairs.keys()]
    for volid in volscoded:
        print(metadata[volid])
        these_pairs = nominal_pairs[volid]
        normalized_triplets = normalize(these_pairs, wages)
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
        print()


if __name__ == "__main__":
    main()
