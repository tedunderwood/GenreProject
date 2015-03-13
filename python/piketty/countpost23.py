# count post23

# tokenize post-23 books

import wordcounter
import os, sys
import SonicScrewdriver as utils

sourcedir = "/Volumes/TARDIS/work/US_NOVELS_1923-1950/"
outdir = "/Volumes/TARDIS/work/uscounts/"

filelist = os.listdir(sourcedir)

fileset = set([x for x in filelist if x.endswith(".txt")])

tuplelist = []
verbose = True

for filename in fileset:
    filepath = os.path.join(sourcedir, filename)
    with open(filepath, encoding = 'utf-8') as f:
        filelines = f.readlines()
    pagelist = [filelines]

    # The wordcounter module expects a list of pages, each of which is a list of lines.
    # Ebooks have no pages -- at least as I currently receive them -- so we treat it
    # all as one giant page.

    tokenstream = wordcounter.makestream(pagelist)
    wordcounts, wordsfused, triplets, alphanum_tokens = wordcounter.count_tokens(tokenstream, targetwords=[], targetphrases=[], verbose = verbose)

    outfilename = filename.replace('.txt', '.fic.tsv')
    outfile = os.path.join(outdir, outfilename)
    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        for word, count in wordcounts.items():
            if len(word) > 0:
                outline = word + '\t' + str(count) + '\n'
                f.write(outline)

    tuplelist.append((outfilename, alphanum_tokens))
    print(filename)

outfile = "/Volumes/TARDIS/work/uscounts/summary.tsv"
with open(outfile, mode='w', encoding='utf-8') as f:
    for filename, tokencount in tuplelist:
        outline = filename + '\t' + str(tokencount) + '\n'
        f.write(outline)









