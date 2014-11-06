reception
---------

Scripts used for research on reception, especially the social stratification of genres and styles.

**Current (lame) workflow:**

run select_poetry_corpus, pointing it to Jordan's metadata.

copy the ids from poemeta1899 to create a list of volids, poe1899.txt
rsync that up to /code/collect
run this:

python3 collect.py /projects/ichass/usesofscale/poetry/ poe1899.txt .poe.tsv none /projects/ichass/usesofscale/sampletexts/

rsync the sampletexts folder back down to a subfolder in reception

then run test_boundary, pointing it at the folder and at poemeta1899
