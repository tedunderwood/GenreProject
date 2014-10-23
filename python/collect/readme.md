collect
-------

Python scripts used to run queries on a database after it has already passed through the filtering process described in the /extract repo (parallel to this one, also under GenreProject/python).

In particular,

collect.py selects particular volumes (and filters for a particular list of words if needed) and organizes them in a folder for download. Designed to be used for classification.

PostExtractionSubset.py  selects particular words from a list of volumes and bundles them in a single flat file. Designed to be used for wordcounting.

PostExtractionCollectByYear.py  then gathers those wordcounts-by-volume into a list of wordcounts-by-year

ToRtable.py then munges that list of wordcounts-by-year into a form that can be imported to R as a plottable data frame.

 
