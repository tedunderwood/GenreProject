futurethreshold = 1899

futureids = list()
for i, volid in enumerate(orderedIDs):
    pubdate = metadict[volid]['pubdate']
    if pubdate > futurethreshold:
        futureids.append(i)

pastthreshold = futurethreshold - 19
pastids = list()
for i, volid in enumerate(orderedIDs):
    pubdate = metadict[volid]['pubdate']
    if pubdate < pastthreshold:
        pastids.append(i)

futureids.sort(reverse=True)
excludeids = list()
excludeids.extend(pastids)
excludeids.extend(futureids)
excludeids.sort(reverse=True)

trainingset, yvals, testset = sliceframe(data, classvector, excludeids, excludeids)
trainingset, means, stdevs = normalizearray(trainingset, usedate)
newmodel.fit(trainingset, yvals)
testset = (testset - means) / stdevs
predictions = [x[1] for x in newmodel.predict_proba(testset)]

truepositives = 0
truenegatives = 0
falsepositives = 0
falsenegatives = 0

logisticpredictions = dict()

for i, idx in enumerate(excludeids):
    volid = orderedIDs[idx]
    logistic = predictions[i]
    logisticpredictions[volid] = logistic

    if logistic > 0.5 and classdictionary[volid] > 0.5:
        truepositives += 1
    elif logistic <= 0.5 and classdictionary[volid] < 0.5:
        truenegatives += 1
    elif logistic <= 0.5 and classdictionary[volid] > 0.5:
        falsenegatives += 1
    elif logistic > 0.5 and classdictionary[volid] < 0.5:
        falsepositives += 1

print()
accuracy = (truepositives + truenegatives) / len(excludeids)
print('Accuracy is: ', str(accuracy))

selfpredictions = [x[1] for x in newmodel.predict_proba(trainingset)]
i = 0
for volid in orderedIDs:
    pubdate = metadict[volid]['pubdate']
    if pubdate <= futurethreshold and pubdate >= pastthreshold:
        logisticpredictions[volid] = selfpredictions[i]
        i += 1

futurepath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/futurepredictions.csv'

with open(futurepath, mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    header = ['volid', 'reviewed', 'obscure', 'pubdate', 'birthdate', 'gender', 'nation', 'allwords', 'logistic', 'author', 'title', 'pubname', 'actually', 'realclass']
    writer.writerow(header)
    for volid in IDsToUse:
        if volid not in logisticpredictions:
            continue
        metadata = metadict[volid]
        reviewed = metadata['reviewed']
        obscure = metadata['obscure']
        pubdate = metadata['pubdate']
        birthdate = metadata['birthdate']
        gender = metadata['gender']
        nation = metadata['nation']
        author = metadata['author']
        title = metadata['title']
        canonicity = metadata['canonicity']
        pubname = metadata['pubname']
        allwords = volsizes[volid]
        logistic = logisticpredictions[volid]
        realclass = classdictionary[volid]
        outrow = [volid, reviewed, obscure, pubdate, birthdate, gender, nation, allwords, logistic, author, title, pubname, canonicity, realclass]
        writer.writerow(outrow)
