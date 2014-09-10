extract
------

Ted Underwood and Mike Black.
Version 1 / Sept 10, 2014

Extract.py is the top-level script guiding the workflow. In its full generality,
it's designed to:

* extract a particular set of features
* from pages matching a particular genre or set of genres
* in a particular set of volumes

The primary function of this top-level script is to parse command-line options and coordinate
the work done in other modules.

Allowable command-line options include

 -g or -genre    A genre or comma-separated list of genres to fetch.
 -id             A specified volume to fetch.
 -idfile         Path to a file listing multiple volume IDs.
 -index          Overrides default index for prediction files.
 -root           Overrides default rootpath.
 -wordlist       Overrides default feature set (all features.)
 -phraselist     Defines a list of two-word phrases to be extracted. At present we don't
                 provide for longer phrases. Default is, no such list.
 -rh             Remove running headers from the selected volumes.
 -o              Output folder. Otherwise defaults to output folder in PathDictionary.
 -v              Verbose.
 -sub            Make subdirectories for the top-level HathiTrust domains within the
                 output folder.

The only options that are mandatory are the ones providing volumes to process, and genre(s) to
select. All the other options have default settings.

This script assumes there is a file PathDictionary.txt in its directory; it needs a path to
the folder containing parsing rules.
