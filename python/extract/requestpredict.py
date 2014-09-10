#!/usr/bin/env python3

import os
import sys
import json

# HOWTO:
# Create a PredictIndex object and either use buildFromDisk or readFromDisk to initialize the index
# To pull the entire smoothedPrediction list for any htid, use getPredictions (returns list)
# To pull just page numbers for a specific genre code, use getOnlyGenre (returns dict w/page numbers as key, values are empty lists)
#
# See name == main for example use

class PredictIndex:
    def __init__(self):
        self._index = dict()

    def buildFromDisk(self,sourceDir='/projects/ichass/usesofscale/pagepredicts',verbose=False):
        if verbose:
            print('Searching for predictions in ' + sourceDir)
        for root,dirs,files in os.walk(sourceDir):
            for filename in files:
                if filename.endswith('predict'):
                    htid = filename.replace('.predict','').replace('+',':').replace('=','/')
                    self._index[htid] = root + '/' + filename

        if verbose:
            print('Found ' + str(len(self._index)) + ' predictions')

    def writeToDisk(self,target='',verbose=False):
        if verbose:
            print('Writing predictions index to disk')
        with open('predictions.index',mode='w',encoding='utf-8') as file:
            for htid in sorted(self._index):
                file.write(htid + '\t' + self._index[htid] + '\n')
        if verbose:
            print('Complete')

    def readFromDisk(self,sourceFile='predictions.index',verbose=False):
        if os.path.exists(sourceFile):
            with open(sourceFile,encoding='utf-8') as file:
                lines = file.readlines()
        for line in lines:
            if len(line) < 2:
                continue
            parts = line.strip().split('\t')
            self._index[parts[0]] = parts[1]

        if verbose:
            print('Loaded index with ' + str(len(self._index)) + ' predictions')

    def checkIndex(self,verbose=False):
        missing = 0
        if verbose:
            print('Checking to see if locations in predictions index match files on system')
        for htid in self._index:
            if os.path.exists(self._index[htid]):
                continue
            else:
                missing += 1
        if verbose:
            print('Unable to find ' + str(missing) + ' prediction files')
        return missing

    def getPredictions(self,htid):
        if htid not in self._index:
            return []

        else:
            try:
                with open(self._index[htid],encoding='utf-8') as file:
                    prediction = json.loads(file.read())
                return prediction['smoothedPredictions']
            except:
                print("Unable to read, or more likely parse, genre predictions for " + htid)
                return []

    def getOnlyGenre(self,htid,genre):
        pages = dict()
        with open(self._index[htid],encoding='utf-8') as file:
            prediction = json.loads(file.read())
        for idx,code in enumerate(prediction['smoothedPredictions']):
            if code == genre:
                pages[idx] = list()
        return pages

if __name__ == '__main__':
    args = sys.argv
    debug = True
    if len(args) < 2:
        print('Running in diagnostic mode')
        htids = 'sampleset.txt'
        if not os.path.exists(htids):
            print('Sample file not found. Exiting.')
            quit()
    else:
        if os.path.exists(args[1]):
            print('Preparing to test on ' + args[1])
        htids = args[1]

    htidList = list()
    with open(htids,encoding='utf-8') as file:
        htids = file.readlines()
    for htid in htids:
        htidList.append(htid.strip())

    test = PredictIndex()
    test.readFromDisk(verbose=debug)

    for htid in htidList:
        fictionPages = test.getOnlyGenre(htid,'fic')
        print('Found ' + str(len(fictionPages)) + ' fiction pages in ' + htid)
