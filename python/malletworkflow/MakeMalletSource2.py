import os, sys

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

with open("/Users/tunder/Dropbox/GenreProject/python/fiction/stoplist.txt", encoding = 'utf-8') as f:
    filelines = f.readlines()

stoplist = set([x.rstrip() for x in filelines])

stoplist.add('|romannumeral|')
stoplist.add('|arabic1digit|')
stoplist.add('|arabic2digit|')
stoplist.add('|arabic3digit|')
stoplist.add('|arabic4digit|')
stoplist.add('|arabic5+digit|')
stoplist.add('ihe')
stoplist.add('said')
stoplist.add('say')
stoplist.add('says')

sourcedir = "/Volumes/TARDIS/fiction/"

filelist = os.listdir(sourcedir)

filelist = [x for x in filelist if x.endswith(".fic.tsv")]

countdict = dict()

for afile in filelist:
    filepath = os.path.join(sourcedir, afile)
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()

    for line in filelines:
        line = line.rstrip()
        fields = line.split('\t')
        word = fields[0]
        count = int(fields[1])

        if word in stoplist:
            continue

        if word in countdict:
            countdict[word] += count
        else:
            countdict[word] = count

tuplelist = list()
for word, count in countdict.items():
    tuplelist.append((count, word))

tuplelist.sort(reverse = True)

lexicon = set([x[1] for x in tuplelist[0:50000]])
lexicon.add("$")
lexicon.add("£")
lexicon.add("¢")
currency = {'centime', 'farthing', 'tuppence', "ha'penny", "sixpence", "florin", "guilder", "guineas", "florins", "guilders"}

lexicon = lexicon.union(currency)

for afile in filelist:

    volID = afile.replace(".fic.tsv", "")
    volID = dirty_pairtree(volID)
    filepath = os.path.join(sourcedir, afile)
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()

    listofwords = list()
    for line in filelines:
        line = line.rstrip()
        fields = line.split('\t')
        word = fields[0]
        if not word in lexicon:
            continue

        if word == "$" or word == "£" or word == "¢":
            word = "pricesymbol"
        elif word == "|arabicprice|":
            word = "numericprice"
        elif word == "ha'penny":
            word = "halfpenny"

        if all_nonalphanumeric(word) or word == "|'s|":
            continue

        word = word.replace("'", "")
        word = word.replace("’", "")
        word = word.replace("‘", "")

        count = int(fields[1])
        aslist = [word] * count
        thisword = " ".join(aslist)
        listofwords.append(thisword)

    startofline = volID + '\t' + 'null\t'
    endofline = " ".join(listofwords)

    with open("/Volumes/TARDIS/fiction/alldata.txt", mode= 'a', encoding = 'utf-8') as f:
        f.write(startofline + endofline + '\n')

print('Done.')


