money = read.csv('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/codedsnippets.csv', stringsAsFactors = F)
money$logval <- as.numeric(money$logval)
money$normval <- as.numeric(money$normval)
money$nominalval <- as.numeric(money$nominalval)
library(ggplot2)
library(scales)

themeans = numeric()
themedians = numeric()
for (center in seq(1750, 1950)) {
  ceiling = center + 12
  floor = center - 12
  moneyvector = money$normval[money$date >= floor & money$date < ceiling]
  newmean = mean(moneyvector, trim = 0.45)
  newmedian = median(moneyvector)
  themeans = c(themeans, newmean)
  themedians = c(themedians, newmedian)
}
themedians[1:13] <- themedians[13]
themedians[189:201] <-themedians[189]
themeans[1:13] <- themeans[13]
themeans[189:201] <-themeans[189]
# barplot(themeans, main = "Rich & Ted's 424 snippets, median (reference / wage)", ylab = "nominal value in £", names.arg = c('1750', '60', '70', '80', '90', '1800', '10', '20', '30', '40', '50', '60', '70', '80', '90', '1900', '10', '20', '30', '40'))

# ('1750', '1760', '1770', '1780', '1790', '1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900', '1910', '1920', '1930', '1940')
#plot(seq(1750,1950), themedians, type='l', lwd=2, ylim = c(min(themedians), max(themedians)), xlab = '', ylab = 'nominal value in £', main = 'Running median of nominal value, 25 yr window.')
#par(new = T)
df <- data.frame(x = seq(1750,1950), y = themeans)
q <- ggplot(df, aes(x=x, y=y)) +  geom_area(aes(y=y), fill='cornflowerblue') + scale_y_continuous("", labels =percent)
q <- q + theme(text = element_text(size = 20)) + scale_x_continuous('') + ggtitle('Running 25-year, 45% trimmed mean of \n references to money as a percent of annual wages\n') + theme(plot.title = element_text(size = 20, lineheight = 1.2))
plot(q)
#plot(seq(1750,1950), themeans, type='l', lwd=1, ylim = c(min(themeans), max(themeans)), xlab='', ylab = 'nominal value  in £', main = 'Running 45% trimmed mean of\n (reference to money / annual average wage), 25 yr window.')
#polygon(c(1750, seq(1750,1950), 1950), c(0,themeans,0), col = 'cornflowerblue')