#!/usr/bin/env python3

# wordcounter II -- this is not really a lineal version of wordcounter; rather
# it's a branch that I use to deal with special problems associated with currency words

# wordcounter.py

# Ted Underwood / version 1 / Sept 8, 2014
#
# This module is based on NormalizeVolume.py, a more complex workflow that does initial normalization
# of text files. This is a greatly simplified version that merely counts words in already-corrected
# texts. However, it retains some complexities that distinguish it from a really generic word-
# counter. For instance, it normalizes hyphenation and fuses phrases like "up stairs" into a
# single word. It also bundles numbers into collective features: |romannumeral|,
# |arabicprice|, |arabic1digit|, |arabic2digit|, etc. up to |arabic5+digit|.
#
# Finally, it records punctuation marks as features, and counts the possessive apostrophe-s
# as an abstract feature (|'s|) distinct from the noun.

# It doesn't bundle personal names or place names, but that could be done at a later stage.

import FileCabinet

pathdictionary = FileCabinet.loadpathdictionary()
rulepath = pathdictionary['volumerulepath']

## The following lines generate a translation map that zaps all
## non-alphanumeric characters in a token.

delchars = ''.join(c for c in map(chr, range(256)) if not c.isalpha())
alleraser = str.maketrans('', '', delchars)

## Translation map that erases most punctuation, including hyphens.
Punctuation = '.,():-—;"!?•$%@“”#<>+=/[]*^\'{}_■~\\|«»©&~`£·'
mosteraser = str.maketrans('', '', Punctuation)

punctuple = ('.', ',', '?', '!', ';', '"', '“', '”', ':', '--', '—', ')', '(', "'", "`", "[", "]", "{", "}")
punctnohyphen = ['.', ',', '?', '!', ';', '"', '“', '”', ':', ')', '(', "'", "`", "[", "]", "{", "}"]
specialfeatures = {"arabicprice", "arabic1digit", "arabic2digit", "arabic3digit", "arabic4digit", "arabic5+digit", "romannumeral", "personalname"}
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

delim = '\t'

romannumerals = set()
with open(rulepath + 'romannumerals.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    romannumerals.add(line)

lexicon = dict()

with open(rulepath + 'MainDictionary.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    fields = line.split(delim)
    englflag = int(fields[1])
    lexicon[fields[0]] = englflag

# personalnames = set()
# with open(rulepath + 'PersonalNames.txt', encoding = 'utf-8') as file:
#     filelines = file.readlines()

# for line in filelines:
#     line = line.rstrip()
#     line = line.lower()
#     personalnames.add(line)

# placenames = set()
# with open(rulepath + 'PlaceNames.txt', encoding = 'utf-8') as file:
#     filelines = file.readlines()

# for line in filelines:
#     line = line.rstrip()
#     line = line.lower()
#     placenames.add(line)

hyphenrules = dict()

with open(rulepath + 'HyphenRules.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()
filelines.reverse()
# Doing this so that unhyphenated forms get read before hyphenated ones.

for line in filelines:
    line = line.rstrip()
    fields = line.split(delim)
    Word = fields[0].rstrip()
    Corr = fields[1].rstrip()
    hyphenrules[Word] = Corr
    if " " not in Corr:
        lexicon[Corr] = 1
    # Because there may be some forms produced by these rules not in the main lexicon.

fuserules = dict()
with open(rulepath + 'FusingRules.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for Line in filelines:
    Line = Line.rstrip()
    LineParts = Line.split(delim)
    Word = LineParts[0].rstrip()
    Word = tuple(Word.split(' '))
    Corr = LineParts[1].rstrip()
    fuserules[Word] = Corr

    # We should also add the corrections to the lexicon.
    if " " not in Corr:
        lexicon[Corr] = 1

## End loading of rulesets.

def increment_dict(anitem, adictionary):
    if anitem in adictionary:
        adictionary[anitem] += 1
    else:
        adictionary[anitem] = 1

    return adictionary[anitem]

def commasplit(matchobj):
    '''Function that we're going to use below to process regexes.'''
    astring = matchobj.group(0)
    astring = astring.replace(',', ', ')
    return astring

def makestream(pagelist):
    '''Converts a list of pages to a list of tokens
    Linebreaks and pagebreaks are ignored.'''

    linelist = list()
    for page in pagelist:
        linelist.extend(page)

    tokens = list()
    for line in linelist:
        if len(line) < 1:
            continue
        if line == "\n":
            continue

        line = line.rstrip()
        if line == "<pb>":
            continue

        lineparts = line.split()
        tokens.extend(lineparts)

    return tokens

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

def normalize_case(astring):
    if astring.islower():
        case = 'lower'
    elif astring.replace("'", "").isupper():
        case = 'upper'
    elif astring.istitle():
        case = 'title'
    elif astring.replace("'", "").istitle():
        case = "title"
    # The replace part is important lest all possessive words get interpreted
    # as heterogenous-case.
    else:
        case = 'heterogenous'

    if case != "heterogenous":
        normalizedstring = astring.lower()
    else:
        normalizedstring = astring

    return normalizedstring, case

def mostly_numeric(astring):
    counter = 0
    for c in astring:
        if c.isdigit():
            counter += 1
    if len(astring) < 1:
        return False
    elif counter/len(astring) > .35:
        return True
    else:
        return False

def arabic_digits(astring):
    pricecodes = ["$", "£", "¢"]
    counter = 0
    anydigits = False

    for c in astring:
        if c.isdigit():
            counter += 1
            anydigits = True
        elif c == ".":
            counter += 1
        elif c == "%":
            counter += 1
        else:
            pass

    if not anydigits:
        return "none"

    priceflag = False
    for code in pricecodes:
        if astring.count(code) > 0:
            priceflag = True

    if astring.endswith("s") or astring.endswith("d"):
        priceflag = True

    if len(astring) < 1 or counter/len(astring) < .49:
        return "none"
    elif priceflag == True:
        return "|arabicprice|"
    elif counter < 2:
        return "|arabic1digit|"
    elif counter < 3:
        return "|arabic2digit|"
    elif counter < 4:
        return "|arabic3digit|"
    elif counter < 5:
        return "|arabic4digit|"
    else:
        return "|arabic5+digit|"

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

def count_word(aword, countdict, targetwords):
    countthis = False
    if len(targetwords) < 1:
        countthis = True
    elif aword in targetwords:
        countthis = True

    if countthis:
        if aword in countdict:
            countdict[aword] += 1
        else:
            countdict[aword] = 1

    return countthis

def count_tokens(tokens, targetwords = [], targetphrases = [], verbose = False):
    ''' This function is originally designed to count words in a stream that has already passed
    through normalization by the MultiNormalizeOCR module and tokenization by the function as_stream,
    in this module. But it can be applied to token streams from other sources, as long as the stream
    meets minimal assumptions: 1) tokens in a flat list, 2) OCR has already been corrected, 3) words
    mistakenly fused have already been separated as far as possible, because we do nothing here to
    separate them.

    We do however fuse some multi-word phrases. If the stream has come through MultiNormalizeOCR,
    hyphenation and word-division will already have been normalized. But we don't assume that, since
    it's possible that this function could be used to count words in clean text from a different source.

    As a default assumption, this function will count all words and return them in a dict() where
    keys are words and values are counts. However, it's possible to pass in special lists if you
    want to count only certain words or phrases. If keyword arguments are provided for EITHER
    targetwords or targetphrases, then the function will count ONLY the words/phrases
    in those lists.

    We lowercase all words and strip trailing apostrophe-s. We also convert numbers into collective
    features such as |romannumeral| or |arabic3digit|.
    '''

    global lexicon, hyphenrules, fuserules, romannumerals, counts

    streamlen = len(tokens)
    skipflag = 0
    wordsfused = 0
    triplets = 0
    alphanum_tokens = 0

    # The phrases in targetphrases are stored as tuples. But we also need them to be in the list
    # of targetwords as space-separated strings. Otherwise they won't be recognized by count_word.

    for aphrase in targetphrases:
        stringversion = " ".join(aphrase)
        if not stringversion in targetwords:
            targetwords.append(stringversion)

    counts = dict()

    for i in range(0, streamlen):

        thisword = tokens[i]

        if len(thisword) < 1:
            continue

        if len(thisword) > 30:
            continue
            # Because that's unlikely to be useful!

        if (thisword.startswith('<') and thisword.endswith('>')) or thisword == '\n':
            # Really, neither of these conditions should hold, but just in case.
            continue

        # skipflag is a boolean that we set in cases where we fused words
        # and need to skip one or more

        if skipflag > 0:
            skipflag = skipflag - 1
            continue

        if all_nonalphanumeric(thisword):
            count_word(thisword, counts, targetwords)
            continue

        # This is an alphanumeric token: a word or number, not punctuation.
        alphanum_tokens += 1

        if i < (streamlen - 1):
            nextword = tokens[i + 1]
        else:
            nextword = "#EOFile"

        thisword = thisword.lower()
        nextword = nextword.lower()

        # It's possible that there are some cases where single words like "twenty-five" are
        # represented as "twenty - five." Would be nice to fuse these if possible.

        if (nextword == "-" or nextword == "—") and i < (streamlen - 2):
            afterword = tokens[i + 2].lower()
            aprefix, afterword, asuffix = strip_punctuation(afterword)
            possiblehyphenate = thisword + "-" + afterword
            if possiblehyphenate in lexicon:
                count_word(possiblehyphenate, counts, targetwords)
                skipflag = 2
                triplets += 1


        # Because it's almost never useful to treat all possible arabic numbers as distinct features,
        # we treat them collectively, either by counting digits or by categorizing them as a "price."
        # arabic_digits assesses whether this word falls into any of those categories, and returns
        # either "none" or a category name.

        arabic = arabic_digits(thisword)
        if arabic != "none":
            # This is a number.
            # We want to permit searching for numbers as part of phrases, so we need to check now
            # whether e.g. ("|arabic2digit|", "pounds") is in targetphrases

            if (arabic, nextword) in targetphrases:
                fused = arabic + " " + nextword
                count_word(fused, counts, targetwords)
                skipflag = 1
                wordsfused += 1
            else:
                count_word(arabic, counts, targetwords)

            continue

        thisprefix, thisword, thissuffix = strip_punctuation(thisword)

        if not all_nonalphanumeric(nextword):
            nextprefix, nextword, nextsuffix = strip_punctuation(nextword)
            # The if clause prevents us from reducing a nonalphanumeric token to zero.
            # Actually that might not cause any problems, but let's not do it.

        ## We also strip and record apostrophe-s to simplify checks.

        thispossessive = False
        nextpossessive = False

        if thisword.endswith("'s") and len(thisword) > 4:
            thispossessive = True
            thisword = thisword[0:-2]

        if nextword.endswith("'s") and len(nextword) > 4:
            nextpossessive = True
            nextword = nextword[0:-2]

        # We record punctuation in the word counts

        if len(thisprefix) > 0:
            count_word(thisprefix, counts, targetwords)

        if len(thissuffix) > 0:
            count_word(thissuffix, counts, targetwords)

        # Also possessives, which might be meaningful features.

        if thispossessive:
            count_word("|'s|", counts, targetwords)

        # In principle we should do that for nextword as well, in cases of fusion. But that's
        # going to be a rare occurrences, and we're talking about very common features here, so
        # it's an edge case perhaps better ignored.

        if thisword in romannumerals:
            count_word("|romannumeral|", counts, targetwords)
            continue

        # Is this part of a phrase that needs fusing?

        if (thisword, nextword) in targetphrases:
            newtoken = thisword + " " + nextword
            count_word(newtoken, counts, targetwords)
            wordsfused += 1
            skipflag = 1
            continue

        if (thisword, nextword) in fuserules:
            newtoken = fuserules[(thisword,nextword)]
            count_word(newtoken, counts, targetwords)
            wordsfused += 1
            skipflag = 1
            continue

        # This could be a word whose hyphenated (or unhyphenated) state needs normalization.

        if thisword in hyphenrules:
            newtoken = hyphenrules[thisword]
            # Newtoken could actually be more than one word, for instance because we normalize
            # "air-pump" as "air pump". So create a list that could have one or more than one member.

            wordparts = newtoken.split(" ")
            for aword in wordparts:
                count_word(aword, counts, targetwords)
            continue

        if "-" in thisword:
            # We break hyphenates up into component parts unless they are explicitly in the lexicon.
            # Note that the corrected forms in hyphenrules and fuserules get added to the lexicon.

            if thisword in lexicon:
                count_word(thisword, counts, targetwords)
            else:
                wordparts = thisword.split("-")
                for aword in wordparts:
                    count_word(aword, counts, targetwords)
            continue

        # We've tested all the fancy stuff, and it wasn't needed, so just do the basic.
        count_word(thisword, counts, targetwords)


    return counts, wordsfused, triplets, alphanum_tokens


def extract_snippets(tokens, WINDOW, targetwords = {}):
    ''' Get words on either side of a targetword.
    WINDOW = the window radius.
    Right now this function is built to return all prices,
    whether |arabicprice| is in targetwords or not.
    '''

    sniptuples = []
    streamlen = len(tokens)
    WINDOWDIAMETER = (2 * WINDOW) + 1

    for idx, token in enumerate(tokens):

        if idx < (WINDOW + 1):
            continue
        if (idx + WINDOW + 2) > streamlen:
            continue

        prefix, word, suffix = strip_punctuation(token)
        word = word.lower()
        code = arabic_digits(word)

        if code == "|arabicprice|":
            priceflag = True
        else:
            priceflag = False

            # We set that flag to make it possible to search
            # for all prices. It's still not possible to search for other numbers, though
            # I could enable that here.

        if (word in targetwords) or priceflag:
            snippet = tokens[idx - WINDOW : idx + WINDOW + 1]

            snippettomodel = []

            # We compress the very large range of possible numbers into
            # two numeric codes.
            for i in range(WINDOWDIAMETER):
                prefix, thisword, suffix = strip_punctuation(snippet[i].lower())
                code = arabic_digits(thisword)
                if code == "|arabicprice|":
                    thisword = "|price|"
                elif code != "none":
                    thisword = "|number|"

                snippettomodel.append(thisword)

            sniptuples.append((snippet, snippettomodel))

    return sniptuples







