import os, sys, random

files = os.listdir('readable')
root = os.getcwd()

def isheader(line):
    header = True
    linelen = len(line)
    if linelen > 5:
        linelen = 5
    for i in range(linelen):
        char = line[i]
        if char.islower():
            header = False
            break

    return header


pagedict = dict()

for afile in files:
    path = os.path.join(root, 'readable/' + afile)
    with open(path, encoding = 'utf-8') as f:
        filelines = f.readlines()
    filelen = len(filelines)
    n = random.randrange(int(filelen * .35), int(filelen * .7))
    pagelines = list()
    pgct = 0
    while pgct < 2:
        line = filelines[n].strip()
        if line.startswith('<pb>'):
            if len(pagelines) > 8 or pgct < 1:
                pgct += 1
        elif pgct > 0:
            if len(line) > 2:
                if isheader(line):
                    print(line)
                else:
                    pagelines.append(line)

        n += 1

    newfile = afile.replace('.norm.txt', '.poe.txt')
    outpath = os.path.join(root, 'poems/' + newfile)
    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        for line in pagelines:
            f.write(line + '\n')







