# money in ebooks
#
# A script that simply counts words and phrases likely to be used in
# describing "specific amounts" of money.

import wordcounter
import os, sys
import SonicScrewdriver as utils
import csv

verbose = True
currentdir = os.getcwd()

filepath = os.path.join(currentdir, "moneywords.txt")
with open(filepath, encoding = 'utf-8') as f:
    filelines = f.readlines()
targetwords = [x.rstrip() for x in filelines]

filepath = os.path.join(currentdir, "moneyphrases.txt")
with open(filepath, encoding = 'utf-8') as f:
    filelines = f.readlines()
targetphrases = [tuple(x.rstrip().split(" ")) for x in filelines]

sourcedir = "/Volumes/TARDIS/work/US_NOVELS_1923-1950/"

filelist = os.listdir(sourcedir)

fileset = set([x for x in filelist if x.endswith(".txt")])

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

datelist = sorted(list(dateset))
summedbydate = dict()
for date in datelist:
    summedbydate[date] = dict()

for idcode, date in datedict.items():
    filename = idcode + ".txt"
    if filename not in fileset:
        print("Missing " + filename)
        continue
    filepath = os.path.join(sourcedir, filename)
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()
    pagelist = [filelines]

    # The wordcounter module expects a list of pages, each of which is a list of lines.
    # Ebooks have no pages -- at least as I currently receive them -- so we treat it
    # all as one giant page.

    tokenstream = wordcounter.makestream(pagelist)
    wordcounts, wordsfused, triplets, alphanum_tokens = wordcounter.count_tokens(tokenstream, targetwords=targetwords, targetphrases=targetphrases, verbose = verbose)

    thisyear = summedbydate[date]
    for word, count in wordcounts.items():
        utils.addtodict("moneywords", count, thisyear)

    utils.addtodict("totalwords", alphanum_tokens, thisyear)

outfile = "/Users/tunder/Dropbox/Documents/Conferences (UIUC)/Rutgers talk/1950data.tsv"
with open(outfile, mode='w', encoding='utf-8') as f:
    f.write('year\tmoneywords\ttotalwords\n')
    for date in datelist:
        outline = str(date) + '\t' + str(summedbydate[date]["moneywords"]) + '\t' + str(summedbydate[date]["totalwords"]) + '\n'
        f.write(outline)









