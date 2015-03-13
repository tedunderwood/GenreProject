# makecontexts
#
# A script that extracts three words on either side of a word related to money.

import modelingcounter
import os, sys
import SonicScrewdriver as utils
import csv

rows, columns, table = utils.readtsv('/Volumes/TARDIS/work/metadata/MergedMonographs.tsv')

verbose = True

targetwords = {'crown', 'crowns', 'guinea', 'guineas', 'nickel', 'sovereign', 'sovereigns', 'pound', 'pounds', 'quid'}

sourcedir = "/Volumes/TARDIS/work/moneytexts/"

filelist = os.listdir(sourcedir)

filelist = [x for x in filelist if x.endswith(".txt")]

contexts = []

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

    newcontexts = modelingcounter.extract_context(tokenstream, targetwords)

    for alist in newcontexts:
        contexts.append((htid, date, alist))

outfile = "/Volumes/TARDIS/work/moneycontext/contexts.tsv"
with open(outfile, mode='w', encoding='utf-8') as f:
    for context in contexts:
        htid, date, alist = context
        outline = " ".join(alist)
        f.write(htid + '\t' + str(date) + '\t' + outline + '\n')









