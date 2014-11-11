import random

datafile = '/Volumes/TARDIS/work/moneycontext/fifteenwords.tsv'

def appendtodict(key, value, dictionary):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

snippetsbyyear = dict()
dateset = set()
with open(datafile, encoding = 'utf-8') as f:
    for line in f:
        fields = line.split('\t')

        date = int(fields[1])
        category = fields[3]
        snippet = fields[4]

        if category == 'notmoney':
            appendtodict(date, snippet, snippetsbyyear)
            dateset.add(date)

ctr = 0
with open('falsenegatives.tsv', mode = 'a', encoding = 'utf-8') as f:
    for date in dateset:
        snip = random.sample(snippetsbyyear[date], 1)[0]
        print(date)
        print(snip)
        user = input('True negative? ')
        if user == 'n':
            category = 'pos'
        else:
            category = 'neg'

        outline = str(date) + '\t' + category + '\t' + snip
        f.write(outline)

        print(ctr)
        ctr += 1
        print()



