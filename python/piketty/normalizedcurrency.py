import sys, os, csv
import SonicScrewdriver as utils

metafile = '/Users/tunder/Dropbox/GenreProject/metadata/unifiedficsample.csv'

id2date = dict()
date2wordcount = dict()
dateset = set()

with open(metafile, encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        # skip header
        if row[0] == "idcode":
            continue
        code = row[0]
        date = int(row[1])
        dateset.add(date)
        wordcount = int(row[2])

        id2date[code] = date
        utils.addtodict(date, wordcount, date2wordcount)

date2moneycount = dict()

datafile = '/Volumes/TARDIS/work/moneycontext/fifteenwords.tsv'

with open(datafile, encoding = 'utf-8') as f:
    for line in f:
        fields = line.split('\t')
        date = int(fields[1])
        if date not in dateset:
            print("Missing " + str(date))
        category = fields[3]
        if category == "money":
            utils.addtodict(date, 1, date2moneycount)

datelist = list(dateset)
datelist.sort()

outfile = '/Users/tunder/Dropbox/GenreProject/python/piketty/model_filtered_money.csv'

with open(outfile, mode='w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    row = ['date', 'money', 'total', 'ratio']
    writer.writerow(row)
    for date in datelist:
        strdate = str(date)
        total = str(date2wordcount[date])
        money = str(date2moneycount[date])
        ratio = date2moneycount[date] / date2wordcount[date]
        strratio = ('%.6f' % ratio)
        row = [strdate, money, total, strratio]
        writer.writerow(row)



