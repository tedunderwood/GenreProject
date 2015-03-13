# GatherTopicModelSample

# Given a list of file ids to gather, and a root directory,
# gathers them from the subdirectories of said root.

import sys, os
import SonicScrewdriver as utils
import shutil

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

extension = ".fic.tsv"

args = sys.argv

d = args[1]
# We assume that the root directory to collect is passed in as the first command-line
# argument.

slicepath = args[2]

with open(slicepath, encoding = 'utf-8') as f:
    filelines = f.readlines()
idstoget = set([x.strip() for x in filelines])

newdir = args[3]

if not os.path.exists(newdir):
    sys.exit(0)

subdirectories = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

successes = set()

for subdir in subdirectories:
    filelist = [o for o in os.listdir(subdir) if not o.startswith('.')]

    for filename in filelist:
        dirtyID = filename.replace(extension, '')
        dirtyID = dirty_pairtree(dirtyID)

        if not dirtyID in idstoget:
            continue

        oldpath = os.path.join(subdir, filename)
        newpath = os.path.join(newdir, filename)

        shutil.copyfile(oldpath, newpath)
        print(dirtyID)

        successes.add(dirtyID)

failures = idstoget - successes
print(failures)






