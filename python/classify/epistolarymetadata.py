# epistolarymetadata.py

# This module ingests metadata created by Clara Mount in the summer of 2014,
# and uses it to return information about genre in a group of novels. We
# are especially interested in the boundary between epistolary and
# non-epistolary fiction, which can be configured in a variety of ways.

import SonicScrewdriver as utils
import numpy as np

epindices, epcolumns, epmetadata = utils.readtsv("/Users/tunder/Dropbox/PythonScripts/classify/HathiGenreInfo-Epist.txt")

nonindices, noncolumns, nonmetadata = utils.readtsv("/Users/tunder/Dropbox/PythonScripts/classify/HathiGenreInfo-NonEpist2.txt")

def get_genrevector(volumeIDs, boundarydef):
	global epindices, nonindices

	n = len(volumeIDs)

	genrevector = np.zeros(n)

	if boundarydef == "nonepistolary / epistolary":

		for idx, volID in enumerate(volumeIDs):
			cleanID = utils.pairtreelabel(volID)

			if cleanID in epindices:
				genrevector[idx] = 1
			elif cleanID in nonindices:
				genrevector[idx] = 0
			else:
				print("Error, missing in metadata: " + cleanID)

	return genrevector





