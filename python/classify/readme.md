classify
========

Worked example of text classification using sklearn, on a dataset of epistolary and nonepistolary novels gathered by Clara Mount in the summer of 2014.

The /data folder holds word counts already extracted from the volumes. The volumes included in this folder are only a subset of the full corpus described under /metadata.

The main class is logistic.py, which imports bagofwords, epistolarymetadata, and SonicScrewdriver to do its job. To run this on your own machine you'll need to provide the path to the data folder in dialogue with logistic.py. But you'll also need to go into epistolarymetadata and alter the paths to metadata to reflect the paths to those files on your own machine. I haven't packaged that part neatly.

All of this is unfortunately written in Python 3, so if you're accustomed to py2.7, you may not even want to try to run it, but rather just use it as a model.
