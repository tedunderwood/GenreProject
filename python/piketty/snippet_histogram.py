#!/usr/bin/env python3

# Script tested in Python 3.3.4.

# snippet_histogram.py
#
# Assesses the distribution of snippets across volumes
# with different numbers of snippets per vol.

import glob, csv

snippetpath = glob.glob('manualcoding/twentyfivesnippets.tsv')[0]
metadatapath = glob.glob('manualcoding/unifiedficmetadata.csv')[0]

volsbydate = dict()
# This will be a dictionary, keyed by date, where the value is a
# list of volume ids associated with that date.

authors = dict()
titles = dict()
datesbyvol = dict()
wordcounts = dict()
with open(metadatapath, encoding = 'utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)
    # That skips the header
    for row in reader:
        volid = row[0]
        date = int(row[1])
        if date in volsbydate:
            volsbydate[date].append(volid)
        else:
            volsbydate[date] = [volid]
        datesbyvol[volid] = date
        wordcount = row[2]
        author = row[3]
        title = row[4]
        wordcounts[volid] = int(wordcount)
        titles[volid] = title
        authors[volid] = author

snippetcounts = dict()
# This will be a dictionary, keyed by volid, where the value
# is a count of the number of snippets assigned to that vol.

with open(snippetpath, encoding = 'utf-8') as f:
    for line in f:
        line = line.rstrip()
        fields = line.split('\t')
        volid = fields[0]
        if volid in snippetcounts:
            snippetcounts[volid] += 1
        else:
            snippetcounts[volid] = 1

listofhistograms = list()

for floor in range(1750, 1950, 50):
    # This iterates through four fifty-year periods.
    # For each period we create a histogram.

    histogram = [0] * 30

    volsinthisfloor = 0
    tripletsforfloor = list()

    for date in range(floor, floor+50):
        if date in volsbydate:
            thesevols = volsbydate[date]
            volsinthisfloor += len(thesevols)
        else:
            continue

        for vol in thesevols:
            if vol in snippetcounts:
                count = snippetcounts[vol]
                index = 1 + int(count/10)
                wordcount = wordcounts[vol]
                ratio = count / wordcount
                tripletsforfloor.append((ratio, count, vol))
            else:
                count = 0
                index = 0
                tripletsforfloor.append((0, 0, vol))

            if index > 0 and index < 30:
                histogram[index] += count
            elif index == 0:
                histogram[0] += 1
            elif count >= 30:
                histogram[29] += count
                print(str(floor) + " : " + str(count) + " : " + vol)

    listofhistograms.append(histogram)
    print(floor)
    print("Has " + str(volsinthisfloor) + " volumes.")

    tripletsforfloor.sort(reverse = True)
    outfile = 'period' + str(floor) + 'vols.csv'
    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['s/w_ratio', 'snippets', 'words', 'volid', 'date', 'author', 'title'])
        for ratio, count, vol in tripletsforfloor:
            outlist = [ratio, count, wordcounts[vol], vol, datesbyvol[vol], authors[vol], titles[vol]]
            writer.writerow(outlist)

with open('histogram.csv', mode='w', encoding = 'utf-8') as f:
    for idx, histogram in enumerate(listofhistograms):
        for snippetspervol, totalsnippets in enumerate(histogram):
            outline = str(idx) + ',' + str(snippetspervol) + ',' + str(totalsnippets) + '\n'
            f.write(outline)






