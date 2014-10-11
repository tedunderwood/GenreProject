collect
-------

Python scripts used to run queries on a database after it has already passed through the filtering process described in the /extract repo (parallel to this one, also under GenreProject/python).

In particular,

PostExtractionSubset.py  selects particular words from a list of volumes

PostExtractionCollectByYear.py  then gathers those wordcounts-by-volume into a list of wordcounts-by-year

ToRtable.py then munges that list of wordcounts-by-year into a form that can be imported to R as a plottable data frame. 
