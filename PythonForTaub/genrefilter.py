#!/usr/bin/env python3

# getpages.py

# Returns pages matching a specified list of genres in a specified list of volumes.

# Version 1
# Written by Ted Underwood and Mike Black, Fall 2014

import sys
from requestpredict import PredictIndex
from FileCabinet import pairtreepath
from argumentparser import simple_parse

def get_pages(filepath):

    failure = False
    pagelist = list()

    try:
        with open(filepath, encoding="utf-8") as f:
            filelines = f.readlines()
    except:
        failure = True

    if failure:
        return pagelist
    else:
        page = list()
        for line in filelines:
            line = line.rstrip()
            if line == "<pb>":
                pagelist.append(page)
                page = list()
            else:
                page.append(line)

        pagelist.append(page)

        return pagelist

def matching_pages(htidList, targetgenres, argdict, threshold):
    '''Fetches pages matching the specified genres in specified volumes.
    The third argument to this function is an 'argument dictionary'
    that transmits certain command-line options to be parsed
    here if necessary.

    Note that this function will only return volumes if the proportion
    of pages matching targetgenres in the volume is > threshold.
    '''

    # The default prediction index is:
    predictIndexFile = 'predictions.index'

    # But we can override this with the "-index" option.
    if "-index" in argdict:
        predictIndexFile = argdict["-index"]

    rootpath = '/projects/ichass/usesofscale/nonserials/'
    # But we can override this with the "-index" option.
    if "-root" in argdict:
        rootpath= argdict["-root"]

    predictions = PredictIndex()
    predictions.readFromDisk(predictIndexFile,verbose=False)

    pull = dict()

    for htid in htidList:

        htid = htid.rstrip()

        listofgenres = predictions.getPredictions(htid)

        # First we check whether there are enough matching pages to justify reading the volume.

        if len(listofgenres) < 1:
            print("Empty prediction for " + htid)
            continue

        matched = 0
        for genre in listofgenres:
            if genre in targetgenres:
                matched += 1

        ratio = matched / len(listofgenres)

        if ratio < threshold:
            continue

        firstpathpart, postfix = pairtreepath(htid,rootpath)
        fullpath = firstpathpart + postfix + '/' + postfix + ".norm.txt"

        pagelist = get_pages(fullpath)

        if len(pagelist) < 1:
            print(htid + " not found.")
            continue

        if len(pagelist) != len(listofgenres):
            print("Discrepancy in htid " + htid + " with " + str(len(pagelist)) + " pages but " + str(len(listofgenres)) + " predicted genres.")
            continue

        # We have now tested all the conditions that could cause us to abort this process.
        # We discovered none of them. So proceed to filter the pages and add them to the
        # result.

        pull[htid] = dict()

        for idx, page in enumerate(pagelist):
            thisgenre = listofgenres[idx]
            if thisgenre in targetgenres:
                pull[htid][idx] = page

    return pull

if __name__ == '__main__':

    args = sys.argv
    argdict = simple_parse(args)

    pull = execute_request(argdict)

    for htid, pages in pull.items():
        print(htid)
        for pagenum, page in pages.items():
            print("***** " + str(pagenum) + " *****")
            for line in page:
                print(line)

