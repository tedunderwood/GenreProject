import re, os
import random, pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from bagofwords import WordVector, StandardizingVector

root = '/Users/tunder/Dropbox/GLNworkshop/USpoetry'

magazines = ['Bookman', 'Century', 'ContVerse', 'Crisis', 'Fugitive', 'Harpers', 'LittleReview', 'LyricWest', 'Masses', 'Messenger', 'Midland', 'Nation', 'NewRepublic', 'Opportunity', 'Others', 'Poetry', 'Scribners', 'SmartSet']

def clean_text(raw):
  raw = re.sub(r'I\\.', '', raw)
  raw = re.sub(r'\\]', '', raw)
  raw = re.sub(r'[0-9]', '', raw)
  raw = re.sub(r'II', '', raw)
  raw = re.sub(r'[,.;:\"?!*()]', '', raw)
  raw = re.sub(r'-', ' ', raw)
  raw = raw.replace("\\'s", '')
  raw = raw.replace("\\'S", '')
  raw = raw.replace('\n', ' ')
  raw = raw.lower()
  words = raw.split()
  return words

def get_magazine(pathlist):
    magazine = []
    for path in pathlist:
        with open(path, encoding = 'utf-8') as f:
            poem = f.read()
        words = clean_text(poem)
        magazine.extend(words)
    return magazine

def paths_to_wordbags(pathlist):
    wordbags = list()
    for path in pathlist:
        with open(path, encoding = 'utf-8') as f:
            poem = f.read()
        words = clean_text(poem)
        wordbags.append(words)
    return wordbags

def normalized_prediction(wordbags, samplesize, iterations, model, standardizer, featurelist):
    ''' Repeatedly samples a set of texts, represented as wordbags. In each case it 
    constructs a composite text from the sample, and treats it as a volume object
    for a model to make a prediction about. Then it averages those predictions.

    The prediction is 'normalized' in the sense that it's made about texts that are roughly
    the same size. A further refinement could randomly sample n words, so the texts are literally
    the same length.
    '''

    n = samplesize
    if n > len(wordbags):
        n = len(wordbags)

    allpredictions = list()

    for i in range(iterations):
        compositetext = list()
        sampleofbags = random.sample(wordbags, n)
        for bag in sampleofbags:
            compositetext.extend(bag)
        volume = WordVector(compositetext)
        volume.selectfeatures(featurelist)
        volume.normalizefrequencies()
        volume.standardizefrequencies(standardizer)
        data = pd.concat([volume.features], axis = 1)
        data = data.T 
        this_prob = model.predict_proba(data)[0][1]
        allpredictions.append(this_prob)

    meanprediction = sum(allpredictions) / len(allpredictions)

    return meanprediction

with open('/Users/tunder/Dropbox/GenreProject/python/reception/model1919/standardizer.p', mode = 'rb') as f:
    standardizer = pickle.load(f)
with open('/Users/tunder/Dropbox/GenreProject/python/reception/model1919/logisticmodel.p', mode = 'rb') as f:
    model = pickle.load(f)
featurelist = standardizer.features

for magazine in magazines:
    folder = os.path.join(root, magazine)
    filelist = os.listdir(folder)
    pathlist = [os.path.join(folder, x) for x in filelist if not x.startswith('.')]
    wordbags = paths_to_wordbags(pathlist)
    magazine_prob = normalized_prediction(wordbags, 25, 20, model, standardizer, featurelist)
    print(magazine + "  :  " + str(len(wordbags)))
    print(magazine_prob)



