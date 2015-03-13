# namematcher.py

# does fuzzy matching on names and manually
# aligns near-misses

from difflib import SequenceMatcher

import csv

authornames = set()
allrows = list()

with open('amplifiedficmeta.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    fieldnames = reader.fieldnames

    for row in reader:
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

        if match > 0.85:
            print(name + " | " + anothername + " | " + str(match))

            user = input('Are these synonymous? ')

            if not user.lower().startswith('y'):
                continue

            user = input("Prefer 1) first or 2) second: ")
            if user == "1":
                synonyms[anothername] = name
            elif user == '2':
                synonyms[name] = anothername

with open('namefusedficmeta.tsv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, delimiter = '\t')
    writer.writeheader()
    for row in allrows:
        author = row['author']
        if author in synonyms:
            row['author'] = synonyms[author]

        writer.writerow(row)
