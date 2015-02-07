from collections import Counter

with open('anovasnippets.tsv', encoding = 'utf-8') as f:
    filelines = f.readlines()

snipcounter = Counter()

for line in filelines:
    fields = line.split('\t')
    snipcounter[fields[0]] += 1

for key, value in snipcounter.items():
    print(key + " : " + str(value))

