manualcoding
------------

Subdirectory for manual coding of snippets.

The main file here is **manualcoding.py**. It should be placed in the same directory with

**twentyfivesnippets.tsv** -- The source file of snippets.

**unifiedficmetadata.csv** -- The metadata for this collection.

**manualcoding2.py* is a version of the script for Py2.7.

The file **conversions.py** translates coded snippets into a csv file, which can then be visualized by **barplot.R**.

The file **context_distribution.py** plots the distribution of specific social context codes over time; it can also be used to assess the distribution of false positives, by plotting snippets coded as 'nonmonetary.'
