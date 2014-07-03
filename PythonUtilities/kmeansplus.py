# K-means ++

# casual python implementation of k-means ++

import numpy as np
import random
import math

datafile = "/Users/tunder/booknlp/normalizedcharacters.tsv"

with open(datafile, encoding='utf-8') as f:
    filelines = f.readlines()

terms = dict()
termindices = dict()
documents = dict()
docindices = dict()
doccounter = 0
termcounter = 0

throttle = 1000000

for line in filelines[0:throttle]:
    line = line.rstrip()
    fields = line.split('\t')

    doc = fields[0]
    term = fields[1]

    if doc not in docindices:
        docindices[doc] = doccounter
        documents[doccounter] = doc
        doccounter += 1

    if term not in termindices:
        termindices[term] = termcounter
        terms[termcounter] = term
        termcounter += 1

D = doccounter
V = termcounter

termdoc = np.zeros((V, D), dtype = 'float64')

for line in filelines[0:throttle]:
    line = line.rstrip()
    fields = line.split('\t')

    docidx = docindices[fields[0]]
    termidx = termindices[fields[1]]
    count = float(fields[2])

    termdoc[termidx, docidx] =  count


for i in range(D):
    termdoc[ : , i] = termdoc[ : , i] / np.sum(termdoc[ : , i])


def docvector(docidx):
    global termdoc
    return termdoc[ : , docidx]

def euclid(vectora, vectorb):
    assert len(vectora) == len(vectorb)
    return np.linalg.norm(vectora - vectorb)

def cossim(vectora, vectorb):
    numerator = np.dot(vectora, vectorb)
    denominator = np.linalg.norm(vectora) * np.linalg.norm(vectorb)
    if denominator == 0:
        return 0
    else:
        return numerator / denominator
    

K = 10

centroids = np.zeros((K, V), dtype = 'float64')

chosenpoints = list()

random.seed()
r = random.randrange(D)
chosenpoints.append(r)

# We only select starting centroids from a limited subset of chars.

Dsub = 12000
if D < Dsub:
    Dsub = D

# The range is k-1 because we already chose one at random.

for i in range(K - 1):
    distances = np.ones(Dsub) * 90000000

    for j in range(Dsub):

        for k in chosenpoints:
            thisdist = euclid(docvector(j), docvector(k))
            if thisdist < distances[j]:
                distances[j] = thisdist

    distances = distances / np.sum(distances)

    r = random.random()
    traversed = 0
    chosen = 0

    for j in range(Dsub):
        traversed += distances[j]
        if r <= traversed:
            chosen = j
            break

    chosenpoints.append(chosen)
    print("Formed cluster #" + str(i))

for idx, point in enumerate(chosenpoints):
    centroids[idx, : ] = docvector(point)

# Main k-means loop

itermax = 25

divisors = np.ones((K))
 
for iteration in range(itermax):

    print("Iteration #" + str(iteration))

    pointassignments = np.ones((D)) * -1

    for i in range(D):

        mindist = 90000000
        closest = -1

        for j in range(K):

            thisdist = euclid(docvector(i), centroids[j, :]) * divisors[j]

            if thisdist < mindist:
                mindist = thisdist
                closest = j

        if closest > -1:
            pointassignments[i] = closest
        else:
            print("Error in point assignment: mindist not found.")

    assert len(pointassignments) == D

    sizes = list()
    
    for j in range(K):

        members = np.where(pointassignments == j)[0]
        sizes.append(len(members))
        
        if len(members) < 1:
            print("Cluster lacks members: reassignment")
            members = [random.randrange(D)]

        newcentroid = np.zeros((V))

        for member in members:
            newcentroid = newcentroid + docvector(member)

        newcentroid = newcentroid / len(members)

        centroids[j, : ] = newcentroid

    print(sizes)
    for j in range(K):
        divisors[j] = divisors[j] + (math.log(sizes[j] + 1) / 1000)

meancentroid = np.zeros((V))

for j in range(K):
    meancentroid = meancentroid + (centroids[j, :] * sizes[j])
meancentroid = meancentroid / D

overrepresentation = np.zeros((K, V))

for j in range(K):
    difference = centroids[j, :] - meancentroid
    orderedindices = difference.argsort()
    print("Cluster " + str(j))

    for termidx in orderedindices[-20:]:
        print(terms[termidx])











