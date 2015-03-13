# denominator_maker.py

# A script that goes through a HathiTrust corpus of 6,942 volumes (1700-1923), plus Hoyt & Richard's
# corpus of 808 vols (1923-1950), simply counting the number of dictionary words in each volume.

import modelingcounter
import os, sys
import SonicScrewdriver as utils
import csv
import pickle
from bagofwords import WordVector, StandardizingVector
from sklearn.linear_model import LogisticRegression

# We start with a number of functions borrowed from other scripts; these were used to
# generate the logistic model, so we use them also here to clean and normalize snippets.

punctuple = ('.', ',', '?', '!', ';', '"', '“', '”', ':', '--', '—', ')', '(', "'", "`", "[", "]", "{", "}")

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

def strip_punctuation(astring):
    global punctuple
    keepclipping = True
    suffix = ""
    while keepclipping == True and len(astring) > 1:
        keepclipping = False
        if astring.endswith(punctuple):
            suffix = astring[-1:] + suffix
            astring = astring[:-1]
            keepclipping = True
    keepclipping = True
    prefix = ""
    while keepclipping == True and len(astring) > 1:
        keepclipping = False
        if astring.startswith(punctuple):
            prefix = prefix + astring[:1]
            astring = astring[1:]
            keepclipping = True
    return(prefix, astring, suffix)

def as_wordlist(line):
    ''' Converts a line into a list of words, splitting
    tokens brutally and unreflectively at punctuation.
    One of the effects will be to split possessives into noun
    and s. But this might not be a bad thing for current
    purposes.
    '''

    line = line.replace('”', ' ')
    line = line.replace(':', ' ')
    line = line.replace(';', ' ')
    line = line.replace('—', ' ')
    line = line.replace('--', ' ')
    line = line.replace('.', ' ')
    line = line.replace(',', ' ')
    line = line.replace('-', ' ')
    line = line.replace('—', ' ')
    line = line.replace("'", ' ')
    line = line.replace('"', ' ')

    # That's not the most efficient way to do this computationally,
    # but it prevents me from having to look up the .translate
    # method.

    words = line.split(' ')

    wordlist = list()

    for word in words:
        word = word.lower()
        prefix, word, suffix = strip_punctuation(word)
        # In case we missed anything.

        if len(word) > 0 and not all_nonalphanumeric(word):
            wordlist.append(word)

    return wordlist


# Now load HathiTrust metadata.

rows, columns, table = utils.readtsv('/Volumes/TARDIS/work/metadata/MergedMonographs.tsv')

ambiguouswords = {'crown', 'crowns', 'guinea', 'guineas', 'nickel', 'sovereign', 'sovereigns', 'pound', 'pounds', 'quid'}

moneywords = {'dollar', 'dollars', 'dime', 'dimes', 'nickel', 'nickels', 'pound', 'pounds', 'shilling', 'shillings', 'sovereign', 'sovereigns','cent', 'cents', 'centime', 'centimes', 'crown', 'crowns', 'halfcrown', 'half-crown','penny', 'pennies', 'pence', 'farthing', 'farthings', 'franc', 'francs', 'guilder', 'guilders', 'florin', 'florins', 'guinea', 'guineas', "ha'penny", 'tuppence', 'twopence', 'sixpence', '|arabicprice|', '|price|', 'quid'}

# Words I explicitly decided not to include: 'quarter', 'quarters', 'mark', 'marks.' Monetary uses
# seemed rare enough relative to others that they'd be more likely to introduce noise than to help.
# |arabicprice| is a code the tokenizer in modelingcounter produces whenever it encounters
# a number connected to £, $, ¢, s, or d. In the output we convert that to |price|, for no very
# good reason.

wealthwords = {'fortune', 'fortunes', 'wealth', 'rich', 'riches', 'money', 'moneys', 'fund', 'funds', 'sum', 'sums', 'price', 'prices', 'priced'}

# This is by no means an exhaustive list. Owe, loan, borrowed, etc.
# If we really want to get at the full range of words potentially
# associated with money, topic modeling would be an appropriate lever.
# We can perhaps enumerate currency terms intuitively, but not these.

alltargetwords = moneywords

sourcedir = "/Volumes/TARDIS/work/moneytexts/"
filelist = os.listdir(sourcedir)
filelist = [x for x in filelist if x.endswith(".txt")]
contexts = []

WINDOWRADIUS = 7

ctr = 0

for filename in filelist:

    htid = utils.pairtreelabel(filename.replace('.fic.txt', ''))

    if htid not in rows:
        print(htid)
        continue
    else:
        date = utils.simple_date(htid, table)

    filepath = os.path.join(sourcedir, filename)
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()
    pagelist = [filelines]

    # The wordcounter module expects a list of pages, each of which is a list of lines.
    # Ebooks have no pages -- at least as I currently receive them -- so we treat it
    # all as one giant page.

    tokenstream = modelingcounter.makestream(pagelist)

    newcontexts = modelingcounter.extract_snippets(tokenstream,  WINDOWRADIUS, alltargetwords)

    approvedcontexts = []

    for snippet, snippettomodel in newcontexts:

        keyword = snippettomodel[WINDOWRADIUS]
        keyword = keyword.lower()
        prefix, keyword, suffix = strip_punctuation(keyword)

        if keyword in wealthwords:
            category = 'wealth'
        elif keyword in ambiguouswords:
            currency = is_money(snippettomodel, WINDOWRADIUS, logisticmodel, features, standardizer)
            if currency:
                category = 'money'
            else:
                category = "notmoney"
        elif keyword in moneywords:
            category = 'money'
        else:
            print('ANOMALY: ' + keyword)
            # Cause that's how I do error handling.
            category = 'null'

        if category == 'money':
            approvedcontexts.append((htid, date, snippet, keyword, category))

    print(ctr)
    ctr += 1

    outfile = "/Volumes/TARDIS/work/moneycontext/twentyfivesnippets.tsv"
    with open(outfile, mode='a', encoding='utf-8') as f:
        for context in approvedcontexts:
            htid, date, alist, keyword, category = context
            snippet = " ".join(alist)
            snippet = snippet.replace('\t', '')
            # Because we don't want stray tabs in our tab-separated values.

            f.write(htid + '\t' + str(date) + '\t' + keyword + '\t' + category + '\t' + snippet + '\n')


sourcedir = "/Volumes/TARDIS/work/US_NOVELS_1923-1950/"

filelist = os.listdir(sourcedir)
fileset = set([x for x in filelist if x.endswith(".txt")])
filelist = list(fileset)

metafile = os.path.join(sourcedir, "US_NOVELS_1923-1950_META.txt")

datedict = dict()
dateset = set()

with open(metafile, newline='', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for fields in reader:
        idcode = fields[0]
        date = int(fields[8])
        datedict[idcode] = date
        dateset.add(date)

for filename in filelist:

    htid = utils.pairtreelabel(filename.replace('.txt', ''))

    if htid not in datedict:
        print(htid)
        continue
    else:
        date = datedict[htid]

    filepath = os.path.join(sourcedir, filename)
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()
    pagelist = [filelines]

    # The wordcounter module expects a list of pages, each of which is a list of lines.
    # Ebooks have no pages -- at least as I currently receive them -- so we treat it
    # all as one giant page.

    tokenstream = modelingcounter.makestream(pagelist)
