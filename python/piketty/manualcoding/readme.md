manualcoding
------------

Subdirectory for manual coding of snippets.

The main file here is manualcoding.py. It should be placed in the same directory with

twentyfivesnippets.tsv -- The source file of snippets.

unifiedficmetadata.csv -- The metadata for this collection.

codedsnippets.tsv -- The snippets already coded. The script will create a new file if no appropriate file is found. But you don't want it to do this, because there probably already is one somewhere.

The script asks you

Is this a quantifiable snippet or an error? (q or e)

If error, it doesn't ask more. Error could mean this isn't really money (a lot of prices and $ symbols are errors). Or it could mean this isn't at all quantifiable ('the moon looked like a silver dime') == not exactly a reference to money.

If it's quantifiable, it's going to ask you for the currency. Usually this will be pounds, dollars, or francs. Guineas or sixpence, etc. are 'pounds.' And you can just hit return for pounds, because that's most common.

Then it asks you for the face value. E.g., 'fifty guineas' has a face value of 52.5.

Then it asks for social context. If you want to add a context to our list, you can. But it will ask you to confirm this.

