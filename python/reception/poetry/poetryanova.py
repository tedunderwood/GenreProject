import numpy as np
import csv, os, random
from collections import Counter

import lineardiction

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

def forceint(astring):
    try:
        intval = int(astring)
    except:
        intval = 0

    return intval

def get_metadata(classpath, volumeIDs, excludeif, excludeifnot, excludebelow, excludeabove):
    '''
    As the name would imply, this gets metadata matching a given set of volume
    IDs. It returns a dictionary containing only those volumes that were present
    both in metadata and in the data folder.

    It also accepts four dictionaries containing criteria that will exclude volumes
    from the modeling process.
    '''

    metadict = dict()

    with open(classpath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)

        anonctr = 0

        for row in reader:
            volid = dirty_pairtree(row['docid'])
            theclass = row['recept'].strip()

            # I've put 'remove' in the reception column for certain
            # things that are anomalous.
            if theclass == 'remove':
                continue

            bail = False
            for key, value in excludeif.items():
                if row[key] == value:
                    bail = True
            for key, value in excludeifnot.items():
                if row[key] != value:
                    bail = True
            for key, value in excludebelow.items():
                if forceint(row[key]) < value:
                    bail = True
                    print(row[key])
            for key, value in excludeabove.items():
                if forceint(row[key]) > value:
                    bail = True

            if bail:
                continue

            birthdate = forceint(row['birth'])

            pubdate = forceint(row['inferreddate'])

            gender = row['gender'].rstrip()
            nation = row['nationality'].rstrip()

            #if pubdate >= 1880:
                #continue

            if nation == 'ca':
                nation = 'us'
            elif nation == 'ir':
                nation = 'uk'
            # I hope none of my Canadian or Irish friends notice this.

            notes = row['notes'].lower()
            author = row['author']
            if len(author) < 1 or author == '<blank>':
                author = "anonymous" + str(anonctr)
                anonctr += 1
                print(author)

            title = row['title']
            canon = row['canon']

            # I'm creating two distinct columns to indicate kinds of
            # literary distinction. The reviewed column is based purely
            # on the question of whether this work was in fact in our
            # sample of contemporaneous reviews. The obscure column incorporates
            # information from post-hoc biographies, which trumps
            # the question of reviewing when they conflict.

            if theclass == 'vulgar':
                obscure = 'obscure'
                reviewed = 'not'
            elif theclass == 'elite':
                obscure = 'known'
                reviewed = 'rev'
            elif theclass == 'addcanon':
                obscure = 'known'
                reviewed = 'addedbecausecanon'
            else:
                print(theclass)

            if notes == 'well-known':
                obscure = 'known'
            if notes == 'obscure':
                obscure = 'obscure'

            if canon == 'y':
                if theclass == 'addcanon':
                    actually = 'Norton, added'
                else:
                    actually = 'Norton, in-set'
            elif reviewed == 'rev':
                actually = 'reviewed'
            else:
                actually = 'random'

            metadict[volid] = dict()
            metadict[volid]['reviewed'] = reviewed
            metadict[volid]['obscure'] = obscure
            metadict[volid]['pubdate'] = pubdate
            metadict[volid]['birthdate'] = birthdate
            metadict[volid]['gender'] = gender
            metadict[volid]['nation'] = nation
            metadict[volid]['author'] = author
            metadict[volid]['title'] = title
            metadict[volid]['canonicity'] = actually
            metadict[volid]['pubname'] = row['pubname']
            metadict[volid]['firstpub'] = forceint(row['firstpub'])

    # These come in as dirty pairtree; we need to make them clean.

    cleanmetadict = dict()
    allidsinmeta = set([x for x in metadict.keys()])
    allidsindir = set([dirty_pairtree(x) for x in volumeIDs])
    missinginmeta = len(allidsindir - allidsinmeta)
    missingindir = len(allidsinmeta - allidsindir)
    print("We have " + str(missinginmeta) + " volumes in missing in metadata, and")
    print(str(missingindir) + " volumes missing in the directory.")

    for anid in volumeIDs:
        dirtyid = dirty_pairtree(anid)
        if dirtyid in metadict:
            cleanmetadict[anid] = metadict[dirtyid]

    return cleanmetadict

# def get_metadata(classpath, volumeIDs):
#     '''
#     As the name would imply, this gets metadata matching a given set of volume
#     IDs. It returns a dictionary containing only those volumes that were present
#     both in metadata and in the data folder.
#     '''

#     metadict = dict()

#     with open(classpath, encoding = 'utf-8') as f:
#         reader = csv.DictReader(f, delimiter = '\t')

#         for row in reader:
#             volid = dirty_pairtree(row['docid'])
#             theclass = row['recept'].strip()

#             # I've put 'remove' in the reception column for certain
#             # things that are anomalous.
#             if theclass == 'remove':
#                 continue

#             birthdate = forceint(row['birth'])

#             # for the moment, we're not looking at volumes without biographical info
#             if birthdate < 1700:
#                 continue

#             pubdate = forceint(row['date'])
#             gender = row['gender'].rstrip()
#             nation = row['nationality'].rstrip()

#             if nation == 'ca':
#                 nation = 'us'
#             if nation != 'us':
#                 nation = 'uk'
#             # I hope none of my Canadian or Irish friends notice this.

#             notes = row['notes'].lower()
#             author = row['author']
#             title = row['title']

#             # I'm creating two distinct columns to indicate kinds of
#             # literary distinction. The reviewed column is based purely
#             # on the question of whether this work was in fact in our
#             # sample of contemporaneous reviews. The obscure column incorporates
#             # information from post-hoc biographies, which trumps
#             # the question of reviewing when they conflict.

#             if theclass == 'vulgar':
#                 obscure = 'obscure'
#                 reviewed = 'not'
#             else:
#                 obscure = 'known'
#                 reviewed = 'rev'

#             if notes == 'well-known':
#                 obscure = 'known'
#             if notes == 'obscure':
#                 obscure = 'obscure'

#             metadict[volid] = (reviewed, obscure, pubdate, birthdate, gender, nation, author, title)

#     # These come in as dirty pairtree; we need to make them clean.

#     cleanmetadict = dict()
#     allidsinmeta = set([x for x in metadict.keys()])
#     allidsindir = set([dirty_pairtree(x) for x in volumeIDs])
#     missinginmeta = len(allidsindir - allidsinmeta)
#     missingindir = len(allidsinmeta - allidsindir)
#     print("We have " + str(missinginmeta) + " volumes in missing in metadata, and")
#     print(str(missingindir) + " volumes missing in the directory.")

#     for anid in volumeIDs:
#         dirtyid = dirty_pairtree(anid)
#         if dirtyid in metadict:
#             cleanmetadict[anid] = metadict[dirtyid]

#     return cleanmetadict

## MAIN code starts here.

sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/texts/'
extension = '.poe.tsv'
VOCABSIZE = 11000
classpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/masterpoemeta.csv'

if not sourcefolder.endswith('/'):
    sourcefolder = sourcefolder + '/'

# This just makes things easier.

# Get a list of files.
allthefiles = os.listdir(sourcefolder)
random.shuffle(allthefiles)

volumeIDs = list()
volumepaths = list()

for filename in allthefiles:

    if filename.endswith(extension):
        volID = filename.replace(extension, "")
        # The volume ID is basically the filename minus its extension.
        # Extensions are likely to be long enough that there is little
        # danger of accidental occurrence inside a filename. E.g.
        # '.fic.tsv'
        path = sourcefolder + filename
        volumeIDs.append(volID)
        volumepaths.append(path)

# Get the class and date vectors, indexed by volume ID

excludeif = dict()
# excludeif['impaud'] = 'pop'
excludeif['pubname'] = 'TEM'
excludeif['recept'] = 'addcanon'
#excludeif['gender'] = 'm'
excludeifnot = dict()
#excludeifnot['gender'] = 'm'
excludeabove = dict()
excludebelow = dict()

excludebelow['inferreddate'] = 1700
excludeabove['inferreddate'] = 1950

metadict = get_metadata(classpath, volumeIDs, excludeif, excludeifnot, excludebelow, excludeabove)

IDspresent = set([x for x in metadict.keys()])

# make a vocabulary list and a volsize dict
wordcounts = Counter()

for volid, volpath in zip(volumeIDs, volumepaths):
    if volid not in IDspresent:
        continue

    with open(volpath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            word = fields[0]
            if len(word) > 1 and word[0].isalpha():
                count = int(fields[1])
                wordcounts[word] += 1

etymological_categories = ['pre', 'post', 'stopword', 'missing']
etymo = dict()
with open('/Users/tunder/Dropbox/PythonScripts/mine/metadata/ReMergedEtymologies.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.split('\t')
        date = int(fields[1])
        if date > 800 and date < 1150:
            etymo[fields[0]] = 'pre'
        elif date >= 1150 and date < 1700:
            etymo[fields[0]] = 'post'
        else:
            etymo[fields[0]] = 'stopword'

vocablist = [x[0] for x in wordcounts.most_common(VOCABSIZE)]
VOCABSIZE = len(vocablist)
vocabset = set(vocablist)

# Here's the crucial change from make granger data. We map all
# words onto an etymological category
vocabmapper = dict()
for idx, word in enumerate(vocablist):
    if word in etymo:
        vocabmapper[word] = etymo[word]
    else:
        vocabmapper[word] = 'missing'


volsizes = Counter()
prewords = Counter()
postwords = Counter()
linearpredictions = dict()

for volid, volpath in zip(volumeIDs, volumepaths):
    if volid not in IDspresent:
        continue

    with open(volpath, encoding = 'utf-8') as f:
        voldict = dict()
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) > 2 or len(fields) < 2:
                print(line)
                continue

            word = fields[0]
            count = int(fields[1])
            voldict[word] = count

            if word in vocabset:

                volsizes[volid] += count

                etymcategory = vocabmapper[word]
                if etymcategory == 'pre':
                    prewords[volid] += count
                elif etymcategory == 'post':
                    postwords[volid] += count

    linearpredictions[volid] = lineardiction.prediction(voldict)

with open('/Users/tunder/Dropbox/GenreProject/python/reception/poetry/poedata.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    header = ['volid', 'reviewed', 'obscure', 'pubdate', 'birthdate', 'gender', 'nation', 'allwords', 'pre', 'post', 'linear', 'author', 'title']
    writer.writerow(header)
    for volid in IDspresent:
        metadata = metadict[volid]
        reviewed = metadata['reviewed']
        obscure = metadata['obscure']
        pubdate = metadata['pubdate']
        birthdate = metadata['birthdate']
        gender = metadata['gender']
        nation = metadata['nation']
        author = metadata['author']
        title = metadata['title']
        allwords = volsizes[volid]
        pre = prewords[volid]
        post = postwords[volid]
        linear = linearpredictions[volid]
        outrow = [volid, reviewed, obscure, pubdate, birthdate, gender, nation, allwords, pre, post, linear, author, title]
        writer.writerow(outrow)



















