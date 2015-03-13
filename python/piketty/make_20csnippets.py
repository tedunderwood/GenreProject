# makecontexts
#
# A script that extracts three words on either side of a word related to money.

import modelingcounter
import os, sys
import SonicScrewdriver as utils
import csv

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

verbose = True

targetwords = {'crown', 'crowns', 'guinea', 'guineas', 'nickel', 'sovereign', 'sovereigns', 'pound', 'pounds', 'quid'}

contexts = []

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

    newcontexts = modelingcounter.extract_context(tokenstream, targetwords)

    for alist in newcontexts:
        contexts.append((htid, date, alist))

outfile = "/Volumes/TARDIS/work/moneycontext/contexts.tsv"
with open(outfile, mode='a', encoding='utf-8') as f:
    for context in contexts:
        htid, date, alist = context
        outline = " ".join(alist)
        f.write(htid + '\t' + str(date) + '\t' + outline + '\n')









