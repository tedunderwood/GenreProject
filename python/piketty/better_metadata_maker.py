import SonicScrewdriver as utils
import os, sys, csv

def all_nonalphanumeric(astring):
    nonalphanum = True
    for character in astring:
        if character.isalpha() or character.isdigit():
            nonalphanum = False
            break
    return nonalphanum

def count_alphanum_tokens(filepath):
    wordcount = 0
    with open(filepath, encoding = 'utf-8') as f:
        for line in f:
            line = line.replace('-', ' ')
            line = line.replace('—', ' ')
            words = line.split()
            for word in words:
                if not all_nonalphanumeric(word):
                    wordcount += 1
    countstring = str(wordcount)
    return countstring

outtable = list()

sourcedir = "/Volumes/TARDIS/work/US_NOVELS_1923-1950/"
metafile = os.path.join(sourcedir, "US_NOVELS_1923-1950_META.txt")

with open(metafile, newline='', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for fields in reader:
        idcode = fields[0]
        title = fields[2]
        author = fields[3] + ', ' + fields[4]
        date = fields[8]
        filename = idcode + '.txt'
        filepath = os.path.join(sourcedir, filename)
        if os.path.isfile(filepath):
            wordcount = count_alphanum_tokens(filepath)
        else:
            print("Missing file: " + filepath)
            sys.exit(0)
        newrow = [idcode, date, wordcount, author, title]
        outtable.append(newrow)

rows, columns, table = utils.readtsv('/Users/tunder/Dropbox/GenreProject/metadata/topicmodelingsample.tsv')

sourcedir = "/Volumes/TARDIS/work/moneytexts/"

for row in rows:
    filename = utils.pairtreefile(row) + ".fic.txt"
    filepath = os.path.join(sourcedir, filename)
    if os.path.isfile(filepath):
        wordcount = count_alphanum_tokens(filepath)
    else:
        print("Missing file: " + filepath)
        sys.exit(0)

    idcode = table["HTid"][row]
    date = str(utils.simple_date(row, table))
    author = table["author"][row]
    title = table["title"][row]
    newrow = [idcode, date, wordcount, author, title]
    outtable.append(newrow)

outfile = '/Users/tunder/Dropbox/GenreProject/metadata/unifiedficsample.csv'
with open(outfile, mode='w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    for row in outtable:
        writer.writerow(row)

