#!/usr/bin/env python3

# extract.py
# Ted Underwood / version 1 / Sept 8, 2014
#
# This is the top-level script guiding the workflow. In its full generality, it's designed to:
#
#    * extract a particular set of features
#    * from pages matching a particular genre or set of genres
#    * in a particular set of volumes
#
# The primary function of this top-level script is to parse command-line options and coordinate
# the work done in other modules.
#
# Allowable command-line options include
#
# -g or -genre    A genre or comma-separated list of genres to fetch.
# -id             A specified volume to fetch.
# -idfile         Path to a file listing multiple volume IDs.
# -index          Overrides default index for prediction files.
# -root           Overrides default rootpath.
# -wordlist       Overrides default feature set (all features.)
# -phraselist     Defines a list of two-word phrases to be extracted. At present we don't
#                 provide for longer phrases. Default is, no such list.
# -rh             Remove running headers from the selected volumes.
# -o              Output folder. Otherwise defaults to output folder in PathDictionary.
# -v              Verbose.
# -sub            Make subdirectories for the top-level HathiTrust domains within the
#                 output folder.
#
# The only options that are mandatory are the ones providing volumes to process, and genre(s) to
# select. All the other options have default settings.

# This script assumes there is a file PathDictionary.txt in its directory; it needs a path to
# the folder containing parsing rules.

import sys, os
import argumentparser
import FileCabinet
import genrefilter
import header
import wordcounter

pathdictionary = FileCabinet.loadpathdictionary()
rulepath = pathdictionary['volumerulepath']

with open(rulepath + 'romannumerals.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

romannumerals = set([x.rstrip() for x in filelines])

def clean_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if ':' in postfix:
        postfix = postfix.replace(':','+')
        postfix = postfix.replace('/','=')
    cleanname = prefix + "." + postfix
    return cleanname

def sort_wordcounts(countdict):
    tuplelist = list()
    for word, count in countdict.items():
        tuplelist.append((count, word))

    tuplelist.sort(reverse = True)
    return tuplelist

def collapsed_list(pagedict):
    pagelist = list()
    for pagenum, page in pagedict.items():
        pagelist.append(page)
    return pagelist

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

def process_volumes(volumedictionary, targetwords, targetphrases, argdict, outputfolder, fileswritten, genrelabel, make_subdirectories, verbose):

    ''' Accepts a dictionary where volume IDs are keys and the values are themselves dictionaries
    that pair page numbers with pages (lists of lines).

    Processes these volumes by removing headers, if that option has been selected, counting features,
    and then writing those features to file in an appropriate subdirectory.
    '''
    global romannumerals

    for volID, pagedictionary in volumedictionary.items():

        pagelist = collapsed_list(pagedictionary)

        if "-rh" in argdict:
            pagelist, removed = header.remove_headers(pagelist, romannumerals)

            # if verbose:
            #     print(removed)

        tokenstream = wordcounter.makestream(pagelist)
        wordcounts, wordsfused, triplets = wordcounter.count_tokens(tokenstream, targetwords=targetwords, targetphrases=targetphrases, verbose = verbose)

        sortedcounts = sort_wordcounts(wordcounts)

        if len(sortedcounts) > 0:

            filename = clean_pairtree(volID)

            if make_subdirectories:
                prefix = filename.split(".")[0]
                subdirectory = outputfolder + prefix
                if not os.path.isdir(subdirectory):
                    os.makedirs(subdirectory)
                thisdirectory = subdirectory + '/'
            else:
                thisdirectory = outputfolder

            outpath = thisdirectory + filename + '.' + genrelabel + '.tsv'

            # We write for instance as
            # /projects/ichass/usesofscale/extracted/loc/loc.ark+=13960=t02z1cb4d.fic.tsv

            totalcount = 0

            with open(outpath, mode='w', encoding = 'utf-8') as f:
                for count, word in sortedcounts:
                    outline = word + '\t' + str(count) + '\n'
                    f.write(outline)
                    if not all_nonalphanumeric(word) and not word == "|'s|":
                        totalcount += count

            fileswritten.append((filename, totalcount))

        # if verbose:
        #     print(volID + "\tfused: " + str(wordsfused) + "\ttriplets: " + str(triplets))


def main(argdict):
    ''' The main body of this module. Its one argument is a dictionary of command-line options
    that pairs options (such as '-o') with the arguments that followed them on the command line.
    '''

    global pathdictionary

    # We need a list of genres to get. The argument of the command line
    # option "-genre" can be a single genre or a list of genres separated
    # by commas.

    if "-genre" in argdict:
        targetgenres = argdict["-genre"].split(",")
    elif "-g" in argdict:
        targetgenres = argdict["-g"].split(",")
    else:
        print("No genres requested. Quitting.")
        sys.exit(0)

    # We take the first genre in the list of targetgenres as a label for this process.
    genrelabel = targetgenres[0]

    # We need a list of HathiTrust volume IDs. Can get this in a couple of forms.

    if "-idfile" in argdict:
        # A filename containing a list of IDs to load.
        htidListFile = argdict["-idfile"]
    elif "-id" in argdict:
        # Or a singe ID.
        htidList = [argdict["-id"]]
        htidListFile = ""
    else:
        print("No IDs requested. Quitting.")
        sys.exit(0)
        # If we get neither of the above, quit.

    if len(htidListFile) > 0:
        with open(htidListFile,encoding='utf-8') as file:
            htidList = file.readlines()

    if '-v' in argdict:
        verbose = True
    else:
        verbose = False

    if "-sub" in argdict:
        make_subdirectories = True
        print("Sending output to subdirectories.")
    else:
        make_subdirectories = False

    if '-wordlist' in argdict:
        filepath = argdict['-wordlist']
        with open(filepath, encoding = 'utf-8') as f:
            filelines = f.readlines()
        targetwords = [x.rstrip() for x in filelines]
    else:
        targetwords = []

    if '-phraselist' in argdict:
        filepath = argdict['-phraselist']
        with open(filepath, encoding = 'utf-8') as f:
            filelines = f.readlines()
        targetphrases = [tuple(x.rstrip().split(" ")) for x in filelines]
        # The file will list space-delimited phrases.
        # We convert them into tuples of words.
    else:
        targetphrases = []

    if '-o' in argdict:
        outputfolder = argdict['-o']
    else:
        outputfolder = pathdictionary['outpath']

    # Default value for the percentage of pages that must match targetgenre in order for us
    # to process the volume at all.
    threshold = 0.1

    fileswritten = list()
    numIDs = len(htidList)

    # The list of volumes to process may well be too long to fit them all into memory.
    # So we iterate through it, a hundred volumes at a time. A hundred volumes might be
    # a large number, except that in most cases many volumes will not be read by
    # genrefilter because the percentage of pages matching the genre target is too low.

    floor = 0

    while floor < numIDs:
        ceiling = floor + 100
        if ceiling > numIDs:
            ceiling = numIDs

        subset = htidList[floor : ceiling]

        volumedictionary = genrefilter.matching_pages(subset, targetgenres, argdict, threshold)

        process_volumes(volumedictionary, targetwords, targetphrases, argdict, outputfolder, fileswritten, genrelabel, make_subdirectories, verbose)

        floor = ceiling

    # Now output fileswritten.

    outputpath = outputfolder + 'filenames.txt'

    if not os.path.exists(outputpath):
        with open(outputpath, mode = 'w', encoding = 'utf-8') as f:
            f.write('filename\talphanumericwordcount\n')

    with open(outputpath, mode='a', encoding = 'utf-8') as f:
        for filename, wordcount in fileswritten:
            f.write(filename + '\t' + str(wordcount) + '\n')

    print("Done.")

if __name__ == '__main__':

    args = sys.argv
    argdict = argumentparser.simple_parse(args)
    main(argdict)


