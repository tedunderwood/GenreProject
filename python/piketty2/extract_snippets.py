# extract_snippets.py

# This is a much-simplified version of the snippet-extraction module that was
# originally developed in the first /piketty repo as fifteenwordsnippets.py.

# This version differs in large part by dumping the contextual model we
# originally used to filter snippets.

import tokenizer
import os, sys
import SonicScrewdriver as utils
import csv

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

moneywords = {'dollar', 'dollars', 'dime', 'dimes', 'nickel', 'nickels', 'pound', 'pounds', 'shilling', 'shillings', 'sovereign', 'sovereigns','cent', 'cents', 'centime', 'centimes', 'crown', 'crowns', 'halfcrown', 'half-crown','penny', 'pennies', 'pence', 'farthing', 'farthings', 'franc', 'francs', 'guilder', 'guilders', 'florin', 'florins', 'guinea', 'guineas', "ha'penny", 'tuppence', 'twopence', 'sixpence', '|arabicprice|', '|price|', 'quid', 'buck', 'bucks', 'ruble', 'rubles'}

# Words I explicitly decided not to include: 'quarter', 'quarters', 'mark', 'marks.' Monetary uses
# seemed rare enough relative to others that they'd be more likely to introduce noise than to help.
# |arabicprice| is a code the tokenizer in tokenizer produces whenever it encounters
# a number connected to £, $, ¢, s, or d. In the output we convert that to |price|, for no very
# good reason.

alltargetwords = moneywords

sourcedir = "/Users/tunder/Dropbox/GenreProject/python/piketty2/anova/"
filelist = os.listdir(sourcedir)
filelist = [x for x in filelist if x.endswith(".txt")]
contexts = []

WINDOWRADIUS = 12

ctr = 0

for filename in filelist:

    htid = utils.pairtreelabel(filename.replace('.norm.txt', ''))

    if htid not in rows:
        print(htid + ' MISSING')
        continue
    else:
        date = utils.simple_date(htid, table)

    filepath = os.path.join(sourcedir, filename)
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()
    pagelist = [filelines]

    tokenstream = tokenizer.makestream(pagelist)

    newcontexts = tokenizer.extract_snippets(tokenstream,  WINDOWRADIUS, alltargetwords)

    for context in newcontexts:
        keyword = context[WINDOWRADIUS]
        keyword = keyword.lower()
        prefix, keyword, suffix = strip_punctuation(keyword)

        snippet = " ".join(context)
        snippet = snippet.replace('\t', '')
        # Because we don't want stray tabs in our tab-separated values.

        print(htid + '\t' + str(date) + '\t' + keyword + '\t' + snippet)








