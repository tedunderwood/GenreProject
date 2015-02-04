python
======

This folder contains groups of python modules used in the genre project, mostly on the Taub campus cluster.

classify
--------
Just an example of regularized logistic regression for text classification. This works on volume-level bags of words that are generated *after* volumes have already been divided by genre at the page level. Contains some data and metadata for a sample application identifying epistolary novels.

collect
-------
Scripts that extract counts for specified words from the folders produced by /extract below.

extract
-------
A utility that extracts pages matching specified genre(s) from specified volume(s), and aggregates feature counts -- either all features or specified words/phrases.

utilities
---------
Some random python utilities.

piketty
-------
Code for a collaborative project with Hoyt Long and Richard So.

piketty2
--------
Continuation of the piketty project.

reception
---------
Code for modeling reception and audience.
