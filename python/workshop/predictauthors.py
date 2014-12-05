import re, os
import csv
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
    lengths = list()

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
        lengths.append(len(compositetext))

    meanprediction = sum(allpredictions) / len(allpredictions)
    meanlength = sum(lengths) / len(lengths)

    return meanprediction, meanlength

with open('/Users/tunder/Dropbox/GenreProject/python/reception/model1919/standardizer.p', mode = 'rb') as f:
    standardizer = pickle.load(f)
with open('/Users/tunder/Dropbox/GenreProject/python/reception/model1919/logisticmodel.p', mode = 'rb') as f:
    model = pickle.load(f)
featurelist = standardizer.features

pathsbyauthor = dict()

# Let's create a dictionary of authors that points to
# paths for all their works.

for magazine in magazines:
    filename = magazine + 'Data.csv'
    metadatapath = os.path.join(root, filename)
    with open(metadatapath, encoding = 'latin-1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'AUTHOR' not in row:
                continue
            if 'FILENAME' not in row:
                continue
            if len(row['FILENAME']) > 1:
                folder = os.path.join(root, magazine)
                filepath = os.path.join(folder, row['FILENAME'])
                author = row['AUTHOR']
                if author in pathsbyauthor:
                    pathsbyauthor[author].append(filepath)
                else:
                    pathsbyauthor[author] = [filepath]

# Now, for each author, characterize the probability that they'll be
# reviewed in one of the magazines on our list. Use ten samples
# of ten randomly selected texts for each author.

authortetrads = list()

for author, pathlist in pathsbyauthor.items():
    if len(pathlist) < 11:
        continue

    wordbags = paths_to_wordbags(pathlist)
    author_prob, meanlength = normalized_prediction(wordbags, 10, 10, model, standardizer, featurelist)
    authortetrads.append((author_prob, author, len(wordbags), meanlength))

authortetrads.sort()
with open('authorprobs.csv', mode='w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['author', 'probofreview', 'poems', 'samplewords'])
    for tetrad in authortetrads:
        probability, author, numtexts, meanlength = tetrad
        print()
        avglen = round(meanlength/10)
        print(author + ", with " + str(numtexts) + ' texts, and ' + str(avglen) + ' average length.')
        print(probability)
        writer.writerow([author, probability, numtexts, meanlength])






