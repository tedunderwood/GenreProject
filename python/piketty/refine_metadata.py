# reads CorrectedMetadata.csv and removes vols
# marked as bad

import csv
badvols = list()

with open('manualcoding/correctedmetadata.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 5 and len(row[5]) > 0:
            newdate = int(row[5])
            if newdate < 100:
                badvols.append(row[0])

with open('badvolids.txt', mode='a', encoding='utf-8') as f:
    for vol in badvols:
        f.write(vol + '\n')

