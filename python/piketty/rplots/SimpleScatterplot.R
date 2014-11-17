# Simple money plot
# 
# This produces simply a scatterplot of the counts
# produced by counting prices and currency words,
# after filtering by our model of context to
# get rid of occurrences of 'pounds,' 'crowns,'
# and 'sovereigns,' etc, that are not monetary.
#
# It's not yet corrected for errors.
library(ggplot2)
filtered <- read.csv('~/Dropbox/GenreProject/python/piketty/model_filtered_money_v3.csv')
q <- ggplot(filtered, aes(x = date, y = ratio * 10000)) + geom_point() + geom_smooth() + 
  scale_y_continuous('references to money / 10000 words\n') + scale_x_continuous('') + theme(text = element_text(size = 20)) + ggtitle('Number of references to money in fiction\nper ten thousand words, raw yearly count\n')
plot(q)