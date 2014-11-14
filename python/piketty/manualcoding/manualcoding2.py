# -*- coding: utf-8 -*-

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

from __future__ import with_statement
import os, sys
import random
import csv
import glob
from io import open
import codecs

def add_snippet_to_tree(date, volid, snippet, rootdict):
    u''' Adds a snippet to a tree of dictionaries, where the top branching level
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
    u''' Randomly selects n years, and then selects one volume from
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
    u''' Randomly selects n years, and then selects one sniptuple from
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

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

# HERE IS WHERE THE MAIN FUNCTION BEGINS.
def main():

    # We attempt to use 'glob' to find files with the appropriate names in
    # the local directory. If you prefer you can just hard-code the paths
    # to snippetsource and codedfile.

    snippetpath = glob.glob(u'twentyfivesnippets.tsv')[0]
    possiblecodedpaths = glob.glob(u'codedsnippets.tsv')
    metadatapath = glob.glob(u'unifiedficmetadata.csv')[0]
    badidpath = glob.glob(u'badvolids.txt')[0]


    if len(possiblecodedpaths) < 1:
        codedfile = u"codedsnippets.tsv"
    else:
        codedfile = possiblecodedpaths[0]

    # get the metadata
    authors = dict()
    titles = dict()
    with open(metadatapath, encoding = 'utf-8') as f:
        reader = csv.reader(utf_8_encoder(f))
        skipit = True

        for row in reader:
            if skipit == True:
                skipit = False
                continue
                # That skips the header
            volid = row[0]
            authors[volid] = row[3]
            titles[volid] = row[4]

    # get a list of bad ids
    with open(badidpath, encoding = u'utf-8') as f:
        badids = set([x.rstrip() for x in f.readlines()])

    snippetsbydate = dict()
    dateset = set()

    # The dictionary snippetsbydate is a tree, where the top level
    # branches by year, and the subdictionaries branch by vol. Each
    # leaf is a list of snippets.

    with open(snippetpath, encoding = u'utf-8') as f:
        for line in f:
            line = line.rstrip()
            fields = line.split(u'\t')
            volid = fields[0]
            date = int(fields[1])
            snippet = fields[4]

            if volid in badids or (u'000' + volid) in badids:
                continue

            add_snippet_to_tree(date, volid, snippet, snippetsbydate)
            dateset.add(date)

    datelist = list(dateset)
    datelist.sort()

    snippetswealreadyhave = set()
    bookswealreadyhave = set()
    allowablecodes = set([u'gift', u'inheritance', u'bribe', u'rent', u'interest', u'capital', u'wages', u'price',  u'nonmonetary', u'other'])

    if os.path.isfile(codedfile):

        with open(codedfile, encoding = u'utf-8') as f:
            for line in f:
                line = line.rstrip()
                fields = line.split(u'\t')
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

                if socialcontext != u"nonmonetary":
                    bookswealreadyhave.add(volid)


    print u'You can code up to ' + unicode(len(datelist)) + u' snippets in one session.'
    numbertocode = raw_input(u'How many snippets do you want to code? ')
    numbertocode = int(numbertocode)

    answered = False
    print
    while not answered:
        print u'You can choose a sampling strategy -- either randomly selecting a vol from'
        print u'the population of volumes in a given year, or a snippet from the whole pool'
        print u'of snippets in a given year.'
        user = raw_input(u'Select from 1) volumes or 2) snippets: ')
        print

        if user == u'1':
            tocode = select_from_vols(snippetsbydate, numbertocode, datelist, bookswealreadyhave)
            answered = True
        elif user == u'2':
            tocode = select_from_snippets(snippetsbydate, numbertocode, datelist, snippetswealreadyhave)
            answered = True

    allowabletypes = set([u'q', u'e'])

    print u"Allowable social contexts:"
    print allowablecodes

    # HERE IS WHERE WE ACTUALLY ITERATE THROUGH SNIPPETS AND ASK THE USER
    # TO CODE THEM.

    for sniptuple in tocode:

        date, volid, snippet = sniptuple

        if volid in authors:
            author = authors[volid]
        else:
            author = u''

        if volid in titles:
            title = titles[volid]
        else:
            title = u''

        print unicode(date) + u" | " + author + u" | " + title
        print
        print snippet
        print
        reftype = u"primal chaos"
        while not reftype in allowabletypes:
            reftype = raw_input(u"Is this a Quantifiable snippet or an Error (q or e): ")

        if reftype == u'e':
            # We don't need to ask further questions for these types.
            poundvalue = 0.0
            socialcontext = u"nonmonetary"
            unit = u'none'

        else:
            # A quantifiable snippet requires further questioning.

            print u'I assume the value is denominated in pounds unless you say otherwise.'
            user = raw_input(u"Currency: pounds (hit return). Or 'dollars' or 'francs', etc: ")
            if user == u'dollars' or user == u'd':
                unit = u'dollars'
            elif user == u'francs' or user == u'f':
                unit == u'francs'
            elif user == u'pounds' or len(user) < 1:
                unit = u'pounds'
            else:
                print u"You entered " + user + u", which is an anomalous unit."
                user = raw_input(u"Re-enter that please to confirm: ")
                unit = user

            quantified = False
            while not quantified:
                numericstring = raw_input(u"Face value of money? (count unquantified plurals as x10): ")
                try:
                    poundvalue = float(numericstring)
                    quantified = True
                except:
                    print u"I couldn't interpret that as a float. Try again."

            valid = False
            while not valid:
                socialcontext = raw_input(u"Social context? ")
                if socialcontext in allowablecodes:
                    valid = True
                else:
                    print u"That's not in my list of allowable social contexts."
                    user = raw_input(u"Do you want me to add it to the codelist? (y/n) ")
                    if user == u'y':
                        allowablecodes.add(socialcontext)
                        valid = True

        outline = u'\t'.join([unicode(date), volid, reftype, unit, unicode(poundvalue), socialcontext, snippet])
        with open(codedfile, mode = u'a', encoding = u'utf-8') as f:
            f.write(outline + u'\n')

        print

    print u'Exhausted snippet list. Done.'


if __name__ == u"__main__":
    main()
