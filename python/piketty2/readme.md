piketty2
========

This cleverly-named repo is basically a second take on the workflow in [/piketty](https://github.com/tedunderwood/GenreProject/tree/master/python/piketty), with a few minor adjustments.

Adjustments include:

* simplify the snippet-extraction process by ditching the whole "contextual model"; instead we'll control false positives and negatives through manual sampling of snippets.

* include a few more trigger conditions that identify a snippet as "signifying money," especially number words followed by "a year," because "hundred a year" or "thousand a year" are important cases where a specific amount of money is mentioned sans explicit currency. Also add rubles.

* wordcounter.py => tokenizer.py (mostly through simplification)

* fifteenwordsnippets.py => extract_snippets.py