import csv

birth = dict()
birth['elite'] = list()
birth['vulgar'] = list()

with open('/Users/tunder/Dropbox/GenreProject/metadata/richficmeta1899.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            birthday = int(row['birthdate'])
        except:
            continue
        if birthday > 1700:
            birth[row['class']].append(birthday)

for key, value in birth.items():
    print(key)
    print(sum(value) / len(value))
