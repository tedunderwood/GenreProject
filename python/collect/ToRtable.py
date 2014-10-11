# mungeforR.py

with open("/Volumes/TARDIS/work/forandrew/emotions_by_year.tsv", encoding = 'utf-8') as f:
    filelines = f.readlines()

yeardict = dict()

for line in filelines:
    line = line.rstrip()
    fields = line.split('\t')
    year = fields[0]
    word = fields[1]
    if word == "total#words":
        word = "total"
    count = fields[2]

    if year in yeardict:
        yeardict[year][word] = count
    else:
        yeardict[year] = dict()
        yeardict[year][word] = count

rbg = ['desire', 'pleasure', 'chafe', 'total']
with open("/Volumes/TARDIS/work/forandrew/emotiontable.tsv", mode = 'w', encoding = 'utf-8') as f:
    f.write('year\tdesire\tpleasure\tchafe\ttotal\n')
    for year, subdict in yeardict.items():
        outstring = year
        for word in rbg:
            if word in subdict:
                outstring = outstring + '\t' + subdict[word]
            else:
                print(year)
                print(word)
                outstring = outstring + '\t' + '0'
        outstring = outstring + '\n'
        f.write(outstring)
