## This script creates page part training data.

## The goal is to pair a file of page-level feature counts with
## a file mapping page ranges to genres. We start with a file of
## feature counts, because it's easier to get the text when you've got
## the counts than vice-versa.

import bz2
import LocalFileCabinet
from zipfile import ZipFile
import math

## Start by loading metadata

from LoadMetadata import loadmetadata
print("Loading metadata.")
      
metadata = loadmetadata()

print("Metadata loaded.")

outpath = "/Users/tunderwood/Dropbox/PythonScripts/mine/pagepartdata/"

alreadymapped = set()

try:
    with open(outpath + 'pagemap.tsv', encoding = 'utf-8') as file:
        filelines = file.readlines()

    for line in filelines:
        htid = line.split('\t')[0]
        alreadymapped.add(htid)
except:
    next

## If it doesn't exist yet, no biggie.

outdata = list()
volcount = 0
currentDocID = ""

volumelimit = 10
localdatapath = "/Volumes/obelisk/zipped/non_serials/"

allowablegenrecodes = {'aut', 'bio', 'com', 'trg', 'dra', 'fic',
'lyr', 'non', 'trv', 'poe', 'ora', 'let', 'mis', 'juv', 'title',
'adver', 'impri', 'bookp', 'toc', 'epigr', 'subsc', 'front', 'index',
'notes', 'gloss', 'bibli', 'catal', 'back', 'poepr', 'argum', 'libra', 'errat'}

def percentcapitalized(listoflines):
    '''Reports the percentage of lines that begin with a capital letter.
    Note that the counts are initialized to 1 rather than 0 -- mostly to
    avoid div by zero errors, though you can call it Laplacian correction.'''
    linecount = 1
    capcount = 1
    
    for aline in listoflines:
        if len(aline) < 2:
            continue
        linecount += 1
        for char in aline:
            if char.isupper():
                capcount += 1
            if char.islower():
                break

    return capcount/linecount

def mean_and_stdev(listofnumbers):
    ''' Returns the mean and standard deviation of the list.'''
    meanval = sum(listofnumbers)/len(listofnumbers)
    variance = 0
    for number in listofnumbers:
        variance += (number - meanval)**2

    return meanval, math.sqrt(variance / len(listofnumbers))
    
def getgenrecode(index):
    ''' Keeps querying the user for a genrecode until it gets
    an allowable one.
    '''
    global allowablegenrecodes
    print("Genrecode for page ", index, ' ', end = '')
    user = input(': ')
    
    userlist = user.split(',')
    genrecode = userlist[0]
    if len(userlist) > 1:
        targetnum = int(userlist[1])
    else:
        targetnum = -1

    if genrecode == "skip":
        return "skip", targetnum
    if genrecode == "stop":
        return "stop", -1
        
    if genrecode == "f":
        genrecode = "front"
    if genrecode =="b":
        genrecode = "back"
    if genrecode not in allowablegenrecodes:
        print("That's not an allowable genrecode.")
        genrecode, targetnum = getgenrecode(index)

    return genrecode, targetnum
    
            
def mapvolume(pagedict, maxpages):
    '''
    This function allows the user to browse a given volume, assigning
    genrecodes to pageranges along the way. The base strategy is to move forward
    page by page querying the user for a genrecode on each page. But once the
    user recognizes a pattern they can say, for instance, "non,600" -- meaning,
    skip forward to page 600 and label *everything* between here and 600 "nonfiction."
    In practice, the algorithm checks along the way to see if the format has changed.
    Right now it does this only by checking whether the percent of capitalized lines
    is more than 2.25 standard deviations from the mean. In practice, that catches a lot
    of changes -- shifts to verse, or advertisements, or indexes/notes, etc. Other
    supplementary warnings are imaginable. For instance, it could use the <div>s created by
    Mike Black's header-removing algorithm as a clue to document parts. That would probably be good.
    '''
    
    global allowablegenrecodes
    
    proceed = True
    index = 0
    forward = True
    volmap = dict()
    
    while proceed and index <= maxpages:
        # The user can stop searching pages by entering 'stop' -- which doesn't enter
        # a genrecode for current page -- or 'code,stop' which enters code, and then stops
        
        for aline in pagedict[index]:
            print(aline, end = '')

        print('\n')
        
        genrecode, targetnum = getgenrecode(index)
        if genrecode == "stop":
            proceed = False
            continue
        
        if targetnum < 0:
            volmap[index] = genrecode
            if forward:
                index += 1
            else:
                index -= 1
            continue
        
        else:
            if genrecode == "stop":
                proceed = False
                continue

            if genrecode == "skip":
                index = targetnum
                continue

            ## If the targetnumber is greater than index, fast-forward to the target.
            ## If the target is past the end of the volume, stop there and start working
            ## backward.
            
            if targetnum >= index:
                increment = 1
            if targetnum > maxpages:
                forward = False
                targetnum = maxpages
            if targetnum < index:
                increment = -1
                forward = True
            if targetnum < 1:
                targetnum = 1
                
            percents = list()
            count = 0
            
            for i in range(index, targetnum, increment):
                newpage = pagedict[i]

                ## We don't include very short pages in our list of capitalization
                ## percentages because they throw off the standard deviation
                if len(newpage) < 3:
                    volmap[i] = genrecode
                    continue
                                   
                pct = percentcapitalized(newpage)
                percents.append(pct)
                mean, std = mean_and_stdev(percents)
                if count > 3 and abs(pct - mean) > (std * 2.25):
                    print("page: ", i)
                    for aline in newpage:
                        print(aline, end = '')
                    print('Still classify as', genrecode, end = '')
                    user = input('? (y/n/correct code) ')
                    
                    if user == 'n':
                        index = i
                        ## If you end by breaking you want to keep moving in the same direction
                        
                        if increment == -1:
                            forward = False
                        else:
                            forward = True
                        break
                    elif user in allowablegenrecodes:
                        volmap[i] = user
                        percents.pop()
                        continue
                    else:
                        next
                
                volmap[i] = genrecode
                count += 1
                    
            index = i

    # Now check to see if all pages have a genrecode.
    previousgenre = ""
    for akey in range(1, maxpages):
        if akey in volmap:
            previousgenre = volmap[akey]
            print("Page", akey, ":", previousgenre)
            if previousgenre not in allowablegenrecodes:
                print('CODE NOT RECOGNIZED.')
            continue
        else:
            if previousgenre == "":
                print('Error in processing.')
                return dict()
            else:
                volmap[akey] = previousgenre
                print('Assuming that page', akey, 'is genre', previousgenre)

    user = ""
    while user!= "accept":
        print('You may now change any codes by entering pagenumber-comma-correctedcode')
        user = input('or accept this codelist by saying accept: ')
        userlist = user.split(',')
        if len(userlist) > 1:
            targetnum = int(userlist[0])
            genrecode = userlist[1]
            volmap[targetnum] = genrecode
            
    return volmap       

## HERE BEGINNETH THE MAIN BODY OF THE MODULE.
##
## I should enclose this in if __name__ == "main" but I'm lazy.

with bz2.BZ2File("/Users/tunderwood/Hathi/pre1900nonserials0.txt.bz2", mode = 'r', buffering = 1000000) as file:
    
    while volcount < volumelimit:
        line = file.readline()
        line = str(line, encoding = 'utf-8')
        fields = line.split(',')
        doc = fields[0]
        if doc == currentDocID:
            continue
        if doc in alreadymapped:
            continue
        else:
            filepath, postfix = LocalFileCabinet.pairtreepath(doc, localdatapath)
            filename = filepath + postfix + '/' + postfix + ".txt"
            try:
                with open(filename, mode = 'r', encoding = 'utf-8') as textfile:
                    filelines = textfile.readlines()
            except IOError as e:
                print(filename, 'not found locally.')
                currentDocID = doc
                continue

            if doc in metadata:
                metarecord = metadata[doc]
            else:
                print('No metadata for', doc)
                currentDocID = doc
                continue
            
            print(metarecord[2], metarecord[3], metarecord[5])
            user = input('Map this volume? (y/n) ')
            if user == 'y':

                
                pagedict = dict()
                pagecounter = 0
                page = list()
                
                for line in filelines:
                    if line == '<pb>\n':
                        pagedict[pagecounter] = page
                        pagecounter += 1
                        page = list()
                    else:
                        page.append(line)

                if len(page) > 0:
                    pagedict[pagecounter] = page

                print('The volume has', pagecounter, 'pages.')

                pagemap = mapvolume(pagedict, pagecounter - 1)
                if len(pagemap) < 1:
                    continue
                else:
                    outfile = outpath + "pagemap.tsv"
                    with open(outfile, mode='a', encoding = 'utf-8') as mapfile:
                        for key, value in pagemap.items():
                            outline = doc + '\t' + str(key) + '\t' + value + '\n'
                            mapfile.write(outline)
                    thisdoc = doc
                    outfile = outpath + "pagecounts.tsv"
                    with open(outfile, mode='a', encoding = 'utf-8') as countfile:
                        countfile.write(line)
                        while doc == thisdoc:
                            line = file.readline()
                            line = str(line, encoding = 'utf-8')
                            fields = line.split(',')
                            doc = fields[0]
                            if doc == thisdoc:
                                countfile.write(line)
                            else:
                                break

            elif user == "stop":
                break
            else:
                currentDocID = doc
                continue
                        

        

        
            
            

        
        
