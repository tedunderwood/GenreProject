# My goal in this script is to package up the modeling and
# evaluation processes we actually ran to produce the article,
# so they can be replicated without a lot of fuss.

import parallel_crossvalidate as pc
import sys

allowable = set("full", "quarters")

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

    # For more historically-interesting kinds of questions, we can limit the part
    # of the dataset that gets TRAINED on, while permitting the whole dataset to
    # be PREDICTED. (Note that we always exclude authors from their own training
    # set; this is in addition to that.) The variables futurethreshold and
    # pastthreshold set the chronological limits of the training set, inclusive
    # of the threshold itself.

    ## THRESHOLDS

    futurethreshold = 1925
    pastthreshold = 1800

    paths = (sourcefolder, extension, classpath, outputpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove)
    thresholds = (pastthreshold, futurethreshold)

    create_model(paths, exclusions, thresholds)




