import sys, os, csv
import SonicScrewdriver as utils

metafile = '/Users/tunder/Dropbox/GenreProject/metadata/ficsampleimprovedmetadata.csv'

id2date = dict()
date2wordcount = dict()
dateset = set()
id2wordcount = dict()

with open('/Users/tunder/Dropbox/GenreProject/python/piketty/badvolids.txt', encoding = 'utf-8') as f:
    badids = [x.rstrip() for x in f.readlines()]

with open('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/falsepositives.tsv', encoding = 'utf-8') as f:
    filelines = f.readlines()

penalizedvols = dict()

for line in filelines:
    line = line.rstrip()
    fields = line.split('\t')
    penalizedvols[fields[0]] = float(fields[1])

with open(metafile, encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        # skip header
        if row[0] == "idcode":
            continue
        code = row[0]
        if code in badids:
            continue
        date = int(row[1])
        dateset.add(date)
        wordcount = int(row[3])

        id2date[code] = date
        utils.addtodict(date, wordcount, date2wordcount)
        id2wordcount[code] = wordcount

def pricesymbol(keyword):
    if keyword == '$':
        return True
    elif keyword == '£':
        return True
    elif keyword == '¢':
        return True
    elif keyword == 'Â£':
        return True
    else:
        return False

def priceinsnippet(snippet):
    if ' $ ' in snippet:
        return True
    elif ' £ ' in snippet:
        return True
    elif ' ¢ ' in snippet:
        return True
    elif ' Â£ ' in snippet:
        return True
    elif '22nd' in snippet or '22d' in snippet:
        return True
    elif '23rd' in snippet or '23d' in snippet:
        return True
    elif '2d' in snippet:
        return True
    elif '3d' in snippet:
        return True
    else:
        return False

date2moneycount = dict()
idnword2moneycount = dict()

datafile = '/Volumes/TARDIS/work/moneycontext/fifteenwords.tsv'

with open(datafile, encoding = 'utf-8') as f:
    for line in f:
        fields = line.split('\t')
        code = fields[0]
        if code in badids:
            continue
        volid = fields[0]
        if volid in penalizedvols:
            increment = 1 - penalizedvols[volid]
        else:
            increment = 1

        date = int(fields[1])
        if date not in dateset:
            print("Missing " + str(date))
        keyword = fields[2]
        category = fields[3]
        snippet = fields[4]
        if category == "money" and not pricesymbol(keyword) and not priceinsnippet(snippet):
            utils.addtodict(date, 1, date2moneycount)
            if code in idnword2moneycount:
                if keyword in idnword2moneycount[code]:
                    idnword2moneycount[code][keyword] += increment
                else:
                    idnword2moneycount[code][keyword] = increment
            else:
                idnword2moneycount[code] = dict()
                idnword2moneycount[code][keyword] = increment

datelist = list(dateset)
datelist.sort()

outfile = '/Users/tunder/Dropbox/GenreProject/python/piketty/model_filtered_money_v3.csv'

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

# outfile = '/Users/tunder/Dropbox/GenreProject/python/piketty/filtered_moneywords_by_vol.csv'

# with open(outfile, mode = 'w', encoding = 'utf-8') as f:
#     writer = csv.writer(f)
#     row = ['idcode', 'word', 'count']
#     writer.writerow(row)
#     for code, subdict in idnword2moneycount.items():
#         for word, count in subdict.items():
#             row = [code, word, str(count)]
#             writer.writerow(row)



