# My goal in this script is to package up the modeling and
# evaluation processes we actually ran to produce the article,
# so they can be replicated without a lot of fuss.

import parallel_crossvalidate as pc
import sys

allowable = {"full", "quarters"}

def instructions():
    print("Your options are: ")
    print()
    print("full -- model the full 700-volume dataset using default settings")
    print("quarters -- create four quarter-century models")
    print()

args = sys.argv
if len(args) > 1:
    command = args[1]
    if command not in allowable:
        instructions()
        sys.exit(0)

else:
    instructions()
    command = ""
    while command not in allowable:
        command = input('Which option do you want to run? ')

assert command in allowable

if command == 'full':

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/texts/'
    extension = '.poe.tsv'
    classpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/finalpoemeta.csv'
    outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/1845apredictions.csv'

    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1950
    sizecap = 350

    # For more historically-interesting kinds of questions, we can limit the part
    # of the dataset that gets TRAINED on, while permitting the whole dataset to
    # be PREDICTED. (Note that we always exclude authors from their own training
    # set; this is in addition to that.) The variables futurethreshold and
    # pastthreshold set the chronological limits of the training set, inclusive
    # of the threshold itself.

    ## THRESHOLDS

    futurethreshold = 1925
    pastthreshold = 1800

    # CLASSIFY CONDITIONS

    positive_class = 'rev'
    category2sorton = 'reviewed'
    datetype = 'firstpub'

    paths = (sourcefolder, extension, classpath, outputpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    thresholds = (pastthreshold, futurethreshold)
    classifyconditions = (category2sorton, positive_class, datetype)

    accuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

elif command == 'quarters':
    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/texts/'
    extension = '.poe.tsv'
    classpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/finalpoemeta.csv'

    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1950

    sizecap = 350

    # CLASSIFY CONDITIONS

    positive_class = 'rev'
    category2sorton = 'reviewed'
    datetype = 'firstpub'

    quarteroptions = [('/Users/tunder/Dropbox/GenreProject/python/reception/poetry/1820bpredictions.csv', 1800, 1844), ('/Users/tunder/Dropbox/GenreProject/python/reception/poetry/1845bpredictions.csv', 1845, 1869), ('/Users/tunder/Dropbox/GenreProject/python/reception/poetry/1870bpredictions.csv', 1870, 1894), ('/Users/tunder/Dropbox/GenreProject/python/reception/poetry/1895bpredictions.csv', 1895, 1825)]

    for outputpath, pastthreshold, futurethreshold in quarteroptions:

        print(pastthreshold)
        paths = (sourcefolder, extension, classpath, outputpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        thresholds = (pastthreshold, futurethreshold)
        classifyconditions = (category2sorton, positive_class, datetype)

        rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

        print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
        tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

        print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))









