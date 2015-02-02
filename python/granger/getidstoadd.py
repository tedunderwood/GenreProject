# getidstoadd

import SonicScrewdriver as utils
import os

with open('/Users/tunder/Dropbox/GenreProject/python/granger/correctedmeta.tsv', encoding = 'utf-8') as f:
    filelines = f.readlines()

ids2get = [x.split('\t')[0] for x in filelines]

fileswehave = os.listdir('/Users/tunder/Dropbox/GenreProject/python/granger/elite/')
idswehave = set([x.replace('.poe.tsv','') for x in fileswehave if x.endswith('.poe.tsv')])

with open('/Users/tunder/Dropbox/GenreProject/python/granger/ids2get.tsv', mode = 'w', encoding = 'utf-8') as f:
    for anid in ids2get:
        if anid not in idswehave and utils.clean_pairtree(anid) not in idswehave:
            f.write(utils.dirty_pairtree(anid) + '\n')
