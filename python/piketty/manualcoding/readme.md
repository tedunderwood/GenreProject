manualcoding
------------

Subdirectory for manual coding of snippets.

The main file here is **manualcoding.py**. It should be placed in the same directory with

**twentyfivesnippets.tsv** -- The source file of snippets.

**unifiedficmetadata.csv** -- The metadata for this collection.

**manualcoding2.py** is a version of the script for Py2.7.

The file **conversions.py** translates coded snippets into a csv file, which can then be visualized by the scripts in (/rplots)[https://github.com/tedunderwood/GenreProject/tree/master/python/piketty/rplots].

The file **context_distribution.py** plots the distribution of specific social context codes over time; it can also be used to assess the distribution of false positives, by plotting snippets coded as 'nonmonetary.

This should probably be in the parent dir, but we also have a couple of metadata files here: **badbooks.csv** are books that we decided were not fiction, or for other reasons needed to be excluded from the experiment (e.g. a character named Penny.) **remainingbooks.csv** are the volumes that remain from unifiedficmetadata.csv after the fifty 'bad books' were removed.

**codedsnippets.tsv** are the raw coded snippets.

**codedsnippets.csv** are produced by conversions.py. But not by the most recent version pushed up here.
