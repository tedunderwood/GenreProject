# manualcoding.py

# Tagging snippets by hand, so we can generalize a little about references
# to money in fiction.

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

def add_snippet_to_tree(date, volid, snippet, rootdict):
    ''' Adds a snippet to a tree of dictionaries, where the top branching level
    is date, and then each datedict branches on volid.
    '''

    if date in rootdict:

        datedict = rootdict[date]

        if volid in datedict:
            datedict[volid].append(snippet)
        else:
            datedict[volid] = [snippet]

    else:
        rootdict[date] = dict()
        rootdict[date][volid] = [snippet]

    # No return value is needed because we've mutated the parameters that were
    # passed in to us.

def select_from_vols(rootdict, numtoselect, datelist, volsalreadyhad):
    ''' Randomly selects n years, and then selects one volume from
    the whole population of vols in that year. Finally selects one
    snippet randomly from each volume.

    Returns a list of sniptuples, which are
    (year, volid, snippet) triplets.
    '''

    assert numtoselect <= len(datelist)

    yearstoget = random.sample(datelist, numtoselect)

    sniptuples = list()
    for year in yearstoget:
        yeardict = rootdict[year]
        volumes = [x for x in yeardict.keys() if x not in volsalreadyhad]
        if len(volumes) > 0:
            candidate = random.sample(volumes, 1)[0]
            snippetsinvol = yeardict[candidate]
            chosen = random.sample(snippetsinvol, 1)[0]
            sniptuple = (year, candidate, chosen)
            sniptuples.append(sniptuple)

    return sniptuples

def select_from_snippets(rootdict, numtoselect, datelist, snippetsalreadyhad):
    ''' Randomly selects n years, and then selects one sniptuple from
    the whole population of snippets in each year. A sniptuple is a
    (year, volid, snippet) triplet.
    '''

    assert numtoselect <= len(datelist)

    yearstoget = random.sample(datelist, numtoselect)
    # randomly sample numtoselect years from the datelist

    sniptuples = list()
    for year in yearstoget:
        # for each randomly samples year, get all the vols in that year
        yeardict = rootdict[year]
        volumes = [x for x in yeardict.keys()]

        # now let's create a list of all sniptuples in the year
        stuplepopulation = list()
        for avol in volumes:
            snippets = yeardict[avol]
            for snippet in snippets:
                if not snippet in snippetsalreadyhad:
                    stuple = (year, avol, snippet)
                    stuplepopulation.append(stuple)
        sniptuples.append(random.sample(stuplepopulation, 1)[0])

    return sniptuples

# HERE IS WHERE THE MAIN FUNCTION BEGINS.
def main():

    # We attempt to use 'glob' to find files with the appropriate names in
    # the local directory. If you prefer you can just hard-code the paths
    # to snippetsource and codedfile.

    snippetpath = glob.glob('twentyfivesnippets.tsv')[0]
    possiblecodedpaths = glob.glob('codedsnippets.tsv')
    metadatapath = glob.glob('unifiedficmetadata.csv')[0]

    if len(possiblecodedpaths) < 1:
        codedfile = "codedsnippets.tsv"
    else:
        codedfile = possiblecodedpaths[0]

    # get the metadata
    authors = dict()
    titles = dict()
    with open(metadatapath, encoding = 'utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        # That skips the header
        for row in reader:
            volid = row[0]
            authors[volid] = row[3]
            titles[volid] = row[4]

    snippetsbydate = dict()
    dateset = set()

    # The dictionary snippetsbydate is a tree, where the top level
    # branches by year, and the subdictionaries branch by vol. Each
    # leaf is a list of snippets.

    with open(snippetpath, encoding = 'utf-8') as f:
        for line in f:
            line = line.rstrip()
            fields = line.split('\t')
            volid = fields[0]
            date = int(fields[1])
            snippet = fields[4]

            add_snippet_to_tree(date, volid, snippet, snippetsbydate)
            dateset.add(date)

    datelist = list(dateset)
    datelist.sort()

    snippetswealreadyhave = set()
    bookswealreadyhave = set()
    allowablecodes = {'gift', 'inheritance', 'bribe', 'rent', 'interest', 'capital', 'wages', 'price',  'nonmonetary', 'other'}

    if os.path.isfile(codedfile):

        with open(codedfile, encoding = 'utf-8') as f:
            for line in f:
                line = line.rstrip()
                fields = line.split('\t')
                socialcontext = fields[5]
                if socialcontext not in allowablecodes:
                    allowablecodes.add(socialcontext)
                    # That humane-sounding provision just means that we
                    # expand our lists of contexts as we go to reflect the decisions
                    # of previous coders.

                volid = fields[1]
                snippet = fields[6]

                snippetswealreadyhave.add(snippet)

                # We only add this volume to 'books we already have' if we've successfully
                # coded some snippet from the book as a monetary value.

                if socialcontext != "nonmonetary":
                    bookswealreadyhave.add(volid)


    print('You can code up to ' + str(len(datelist)) + ' snippets in one session.')
    numbertocode = input('How many snippets do you want to code? ')
    numbertocode = int(numbertocode)

    answered = False
    print()
    while not answered:
        print('You can choose a sampling strategy -- either randomly selecting a vol from')
        print('the population of volumes in a given year, or a snippet from the whole pool')
        print('of snippets in a given year.')
        user = input('Select from 1) volumes or 2) snippets: ')
        print()

        if user == '1':
            tocode = select_from_vols(snippetsbydate, numbertocode, datelist, bookswealreadyhave)
            answered = True
        elif user == '2':
            tocode = select_from_snippets(snippetsbydate, numbertocode, datelist, snippetswealreadyhave)
            answered = True

    allowabletypes = {'q', 'e'}

    print("Allowable social contexts:")
    print(allowablecodes)

    # HERE IS WHERE WE ACTUALLY ITERATE THROUGH SNIPPETS AND ASK THE USER
    # TO CODE THEM.

    for sniptuple in tocode:

        date, volid, snippet = sniptuple

        if volid in authors:
            author = authors[volid]
        else:
            author = ''

        if volid in titles:
            title = titles[volid]
        else:
            title = ''

        print(str(date) + " | " + author + " | " + title)
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
            user = input("Pounds (hit return). Or 'dollars' or 'francs', etc: ")
            if user == 'dollars':
                unit = 'dollars'
            elif user == 'francs':
                unit == 'francs'
            elif user == 'pounds' or len(user) < 2:
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
                if socialcontext in allowablecodes:
                    valid = True
                else:
                    print("That's not in my list of allowable social contexts.")
                    user = input("Do you want me to add it to the codelist? (y/n) ")
                    if user == 'y':
                        allowablecodes.add(socialcontext)
                        valid = True

        outline = '\t'.join([str(date), volid, reftype, unit, str(poundvalue), socialcontext, snippet])
        with open(codedfile, mode = 'a', encoding = 'utf-8') as f:
            f.write(outline + '\n')

        print()

    print('Exhausted snippet list. Done.')


if __name__ == "__main__":
    main()
