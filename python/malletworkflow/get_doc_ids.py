#!/usr/bin/env python3

# Script tested in Python 3.3.4.

# This extracts a sequence of document ids from a text file that was used as input to
# Mallet. A wiser long-term approach would be to write your make_source script so that
# it  outputs this sequence of document labels in the *process* of producing the source
# text file.

# USAGE: python3 get_doc_ids.py sourcefile > targetfile

import sys

args = sys.argv

malletsource = args[1]

with open(malletsource, encoding = 'utf-8') as f:
    filelines = f.readlines()

docids = list()
for line in filelines:
    fields = line.split('\t')
    docid = fields[0]
    docids.append(docid)

for anid in docids:
    print(anid)
