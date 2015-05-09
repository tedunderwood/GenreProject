# namematcher.py

# does fuzzy matching on names and manually
# aligns near-misses

from difflib import SequenceMatcher
import SonicScrewdriver as utils
import csv

authornames = set()
allrows = list()

def forceint(astring):
    try:
        intval = int(astring)
    except:
        intval = 0

    return intval

existing = set()

with open('masterpoemeta.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        inferred = forceint(row['inferreddate'])
        firstpub = forceint(row['firstpub'])
        if inferred < firstpub:
            print(row['author'])
            print(row['docid'])
            print('inferred: ' + str(inferred))
            print('firstpub: ' + str(firstpub))
            date = int(input('Date of first publication: '))
            row['firstpub'] = str(date)
        if row['docid'] in existing:
            print('existing ' + row['docid'])
        existing.add(row['docid'])
        row['docid'] = utils.clean_pairtree(row['docid'])
        allrows.append(row)
        authornames.add(row['author'])

authornames = list(authornames)

synonyms = dict()

for name in authornames:
    for anothername in authornames:
        if name == anothername:
            continue

        if name in synonyms:
            if synonyms[name] == anothername:
                continue

        if anothername in synonyms:
            if synonyms[anothername] == name:
                continue

        m = SequenceMatcher(None, name, anothername)
        match = m.ratio()

        if match > 0.9:
            print(name + " | " + anothername + " | " + str(match))

            user = input('Are these synonymous? ')

            if not user.startswith('y'):
                continue

            user = input("Prefer 1) first or 2) second: ")
            if user == "1":
                synonyms[anothername] = name
            elif user == '2':
                synonyms[name] = anothername

with open('finalpoemeta.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()
    for row in allrows:
        author = row['author']
        if author in synonyms:
            row['author'] = synonyms[author]

        writer.writerow(row)
