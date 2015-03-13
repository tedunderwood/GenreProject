# manualcoding.py

# Tagging snippets by hand, so we can generalize a little about references
# to money in fiction.

 # The data structure for the coded snippets is as follows:
    # 0) date,
    # 1) volumeid
    # 2) reference type: a (q)uantity of money "five dollars",
        # the (u)nit of currency itself ("pound wise, penny foolish")
        # (p)lural units: "a handful of nickels," "where had the dollars gone?"
        # (e)rror -- something like "crown of his head", shouldn't be here.
        # (m)etaphorical -- the moon looked like a silver dime.
    # 3) poundvalue -- nominal value of money in £. Only for
        # reference types q, u, and p. For reference type (p) we
        # arbitrarily say that unspecified plural == 10x.
    # 4) socialcontext — gift, bribe, inheritance, rent, interest,
        # capital, wages, price. This list can be expanded at will
        # by coders; this script allows you to add to it.
    # 5) snippet.

import os, sys
import random

def main():

    snippetsource = '/Volumes/TARDIS/work/moneycontext/moneysnippets.tsv'

    bydate = dict()
    dateset = set()

    # The dictionary bydate is keyed, well, by date. Each value is a list
    # of sniptuples, triplets that represent snippets.

    with open(snippetsource, encoding = 'utf-8') as f:
        for line in f:
            line = line.rstrip()
            fields = line.split('\t')
            date = int(fields[1])
            sniptuple = (fields[0], fields[1], fields[4])
            # A sniptuple is just the triplet: volID, string date, snippet.

            if date in bydate:
                bydate[date].append(sniptuple)
            else:
                bydate[date] = [sniptuple]
                dateset.add(date)

    datelist = list(dateset)
    datelist.sort()

    codedfile = '/Users/tunder/Dropbox/GenreProject/python/piketty/coded.tsv'

    alreadyhave = set()
    allowablecodes = {'gift', 'inheritance', 'bribe', 'rent', 'interest', 'capital', 'wages', 'price',  'nonmonetary', 'other'}

    if os.path.isfile(codedfile):

        with open(codedfile, encoding = 'utf-8') as f:
            for line in f:
                line = line.rstrip()
                fields = line.split('\t')
                socialcontext = fields[4]
                if socialcontext not in allowablecodes:
                    allowablecodes.add(socialcontext)
                    # That humane-sounding provision just means that we
                    # expand our lists of contexts as we go to reflect the decisions
                    # of previous coders.

                snippet = fields[5]

                alreadyhave.add(snippet)

    tocode = list()

    # Now we iterate through all dates to select one snippet at random from the available
    # snippets for that year. However, first we filter the snippets to remove the ones we
    # alreadyhave.

    for date in datelist:

        allsnippets = bydate[date]

        notcodedyet = []

        for sniptuple in allsnippets:
            snippet = sniptuple[2]
            if snippet not in alreadyhave:
                notcodedyet.append(sniptuple)

        if len(notcodedyet) < 1:
            continue
            # No snippets left to code in this year!
        else:
            choice = random.sample(notcodedyet, 1)[0]
            tocode.append(choice)

    allowabletypes = {'q', 'u', 'p', 'e', 'm'}

    print("Allowable social contexts:")
    print(allowablecodes)

    skip = False
    for sniptuple in tocode:
        if skip == False:
            skip = True
        else:
            continue
        volid, date, snippet = sniptuple
        print(date)
        print(snippet)
        reftype = "primal chaos"
        while not reftype in allowabletypes:
            reftype = input("Reference type (quantity, unit, plural, error, metaphor): ")

        if reftype == 'e' or reftype == 'm':
            # We don't need to ask further questions for these types.
            poundvalue = 0.0
            socialcontext = "nonmonetary"

        else:
            # The user has specified a type that requires further questioning.
            quantifiable = False
            while not quantifiable:
                numericstring = input("£ value of money? (count plurals as x10): ")
                try:
                    poundvalue = float(numericstring)
                    quantifiable = True
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

        outline = '\t'.join([date, volid, reftype, str(poundvalue), socialcontext, snippet])
        with open(codedfile, mode = 'a', encoding = 'utf-8') as f:
            f.write(outline + '\n')


    print('Exhausted snippet list. Done.')

if __name__ == "__main__":
    main()
