import os, csv

sourcefiles = ['ReviewedTitles1820-1839.csv', 'ReviewedTitles1840-1859_200.csv', 'ReviewedTitles1860-1879_200.csv', 'ReviewedTitles1880-1899_200.csv', 'ReviewedTitles1900-1919_200.csv']

sourcefolder = '/Users/tunder/Dropbox/ted/reception/reviewed/lists/'

allrows = list()

for afile in sourcefiles:
    filepath = os.path.join(sourcefolder, afile)
    with open(filepath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'aubirth' not in row:
                row['aubirth'] = ''
            if 'augender' not in row:
                row['augender'] = ''
            if 'national origin' not in row:
                row['national origin'] = ''

            for key, value in row.items():
                if value == '<blank>' or value == '?':
                    row[key] = ''

            allrows.append(row)

fields = ['HTid', 'date', 'recordid', 'OCLC', 'author', 'imprint', 'enumcron', 'title', 'pubrev', 'judge', 'impaud', 'yrrev', 'pubname', 'Jgenre', 'firstpub', 'aubirth', 'augender', 'national origin']

outfile = os.path.join(sourcefolder, 'ReviewedTitlesAll.csv')
with open(outfile, mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fields, extrasaction='ignore')
    writer.writeheader()
    for row in allrows:
        writer.writerow(row)







