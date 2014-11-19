money = read.csv('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/codedsnippets.csv', stringsAsFactors = F)
money$logval <- as.numeric(money$logval)
money$normval <- as.numeric(money$normval)
money$nominalval <- as.numeric(money$nominalval)

plot(density(log10(money$nominalval), adjust = 0.4), xlab = "Log base 10 of money face value", ylab = 'Density function', main = 'Distribution of references to money across powers of ten')
polygon(density(log10(money$nominalval), adjust = 0.4), col = 'cornflowerblue')