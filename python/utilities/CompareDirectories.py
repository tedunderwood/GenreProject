# CompareDirectories

dir1 = input('Name of first directory?')
dir2 = input('Name of second directory?')

import os
import sys

dir1list = set(os.listdir(dir1))
dir2list = set(os.listdir(dir2))

symmdiff = dir1list.symmetric_difference(dir2list)

if len(symmdiff) > 0:
    print(symmdiff)
    print("Those files are present in one but not the other.")

shared = dir1list.intersection(dir2list)
for filename in shared:
    fullpath1 = os.path.join(dir1, filename)
    with open(fullpath1, encoding = 'utf-8') as file:
        filelines1 = file.readlines()

    fullpath2 = os.path.join(dir2, filename)
    with open(fullpath2, encoding = 'utf-8') as file:
        filelines2 = file.readlines()

    firstonly = set(filelines1) - set(filelines2)
    if len(firstonly) > 0:
        print("THESE LINES IN", fullpath1,"and not", fullpath2)
        for line in firstonly:
            print(line)
    else:
        print("No lines in", fullpath1,"and not", fullpath2)

    secondonly = set(filelines2) - set(filelines1)
    if len(secondonly) > 0:
        print("THESE LINES IN", fullpath2,"and not", fullpath1)
        for line in secondonly:
            print(line)
    else:
        print("No lines in", fullpath2,"and not", fullpath1)

