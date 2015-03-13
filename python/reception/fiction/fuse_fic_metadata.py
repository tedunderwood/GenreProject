import csv

allrows = list()

with open('richficmeta1919.tsv', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')

    for row in reader:
        rowdict = dict()
        rowdict['docid'] = row[0]
        rowdict['recept'] = row[1]
        rowdict['date'] = row[2]
        rowdict['author'] = row[3]
        rowdict['title'] = row[4]
        rowdict['birth'] = ''

        allrows.append(rowdict)

with open('richficmeta1899.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        row['docid'] = row.pop('htid')
        row['recept'] = row.pop('class')
        row['date'] = row.pop('pubdate')
        row['birth'] = row.pop('birthdate')

        allrows.append(row)

fieldnames = ['docid', 'recept', 'date', 'author', 'title', 'birth']

with open('amplifiedficmeta.tsv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, extrasaction = 'ignore', delimiter = '\t')
    writer.writeheader()

    for row in allrows:
        writer.writerow(row)
