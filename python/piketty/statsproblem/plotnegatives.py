#plotnegatives

import numpy as np
import matplotlib.pyplot as plt

falseneg = np.zeros(11)
allneg = np.zeros(11)

with open('falsenegatives.tsv') as f:
    for line in f:
        if len(line) <3:
            continue
        else:
            fields = line.split('\t')
            date = int(fields[0])
            decade = int((date-1750) / 20)

            allneg[decade] += 1
            if fields[1] == 'pos':
                falseneg[decade] += 1

y = falseneg / allneg
x = [o for o in range(1750, 1970, 20)]
plt.scatter(x, y)
plt.show()

