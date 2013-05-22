'''This script loads volumes described in a "slice" of volume IDs, and
    counts words at the page level in the "clean.txt" file.

    That work gets done in the Volume module.

    
'''

import FileCabinet
import Volume
import Context
import sys

# DEFINE CONSTANTS.
delim = '\t'
debug = False

# LOAD PATHS.
slicename = sys.argv[1]
outfilename = sys.argv[2]

## We assume the slice name has been passed in as an argument.

pathdictionary = FileCabinet.loadpathdictionary('/home/tunder/python/tokenize/PathDictionary.txt')

datapath = pathdictionary['datapath']
slicepath = pathdictionary['slicepath'] + slicename + '.txt'
metadatapath = pathdictionary['metadatapath']
metaoutpath = pathdictionary['slicepath'] + slicename + 'acc.txt'
errorpath = pathdictionary['slicepath'] + slicename + 'errorlog.txt'
longSpath = pathdictionary['slicepath'] + slicename + 'longS.txt'
       
with open(slicepath, encoding="utf-8") as file:
    HTIDlist = file.readlines()

HTIDs = set()

for thisID in HTIDlist:
    thisID = thisID.rstrip()
    HTIDs.add(thisID)

del HTIDlist

## discard bad volume IDs

with open(metadatapath + "badIDs.txt", encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    line = line.split(delim)
    if line[0] in HTIDs:
        HTIDs.discard(line[0])

processedmeta = list()
errorlog = list()
longSfiles = list()
totaladded = dict()
totaldeleted = dict()

for thisID in HTIDs:
    
    filepath, postfix = FileCabinet.pairtreepath(thisID, datapath)
    filename = filepath + postfix + '/' + postfix + ".clean.txt"

    try:
        with open(filename, encoding='utf-8') as file:
            lines = file.readlines()
            successflag = True
    except IOError as e:
        successflag = False

    if not successflag:
        print(thisID + " is missing.")
        errorlog.append(thisID + '\t' + "missing")
        continue
        
    tokens, aretokensverse, pagefeatures = Volume.as_stream(lines, verbose=debug)

    tokencount = len(tokens)
    
    if len(tokens) < 10:
        print(thisID, "has only tokencount", len(tokens))
        errorlog.append(thisID + '\t' + 'short')

    correct_tokens, pages = Volume.correct_stream(tokens, aretokensverse, verbose = debug)
    if not correct_tokens == tokens:
        errorlog.append(thisID + '\t' + 'corrected stream changed.')

    assert len(pagefeatures) == len(pages)

with open(outfilename, mode = 'a', encoding = 'utf-8') as file:
    for index, page in enumerate(pages):
        textlines, caplines = pagefeatures[index]

        file.write(thisid + ',' + str(index) + ',' + "0" + "," + "#textlines" + ',' + str(textlines) + '\n')
        file.write(thisid + ',' + str(index) + ',' + "0" + "," + "#caplines" + ',' + str(caplines) + '\n')
        
        for key, value in page.items():
            word, verseflag = key
            if "," in word:
                continue
            ## Don't want to mess up my csv.

            file.write(thisid + ',' + str(index) + ',' + verseflag + "," + word + ',' + str(value) + '\n')
            

# Write the errorlog.

if len(errorlog) > 0:
    with open(errorpath, mode = 'w', encoding = 'utf-8') as file:
        for line in errorlog:
            file.write(line + '\n')

# Done.


