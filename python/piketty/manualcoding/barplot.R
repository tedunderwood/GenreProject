money = read.csv('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/allsnippets.csv', stringsAsFactors = F)
money$logval <- as.numeric(money$logval)
money$normval <- as.numeric(money$normval)
money$nominalval <- as.numeric(money$nominalval)
themeans = numeric()
for (floor in seq(1750, 1925, 25)) {
  ceiling = floor + 26
  newmean = median(money$logval[money$date >= floor & money$date < ceiling])
  themeans = c(themeans, newmean)
}
# barplot(themeans, main = "Rich & Ted's 424 snippets, median (reference / wage)", ylab = "nominal value in £", names.arg = c('1750', '60', '70', '80', '90', '1800', '10', '20', '30', '40', '50', '60', '70', '80', '90', '1900', '10', '20', '30', '40'))

# ('1750', '1760', '1770', '1780', '1790', '1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900', '1910', '1920', '1930', '1940')
library(ggplot2)
library(scales)
db <- data.frame(x = as.factor(c('1750-74', '1775-99', '1800-24', '1825-49', '1850-74', '1875-99', '1900-24', '1925-49')), y = themeans)
q <- ggplot(db, aes(x=x, y = y)) + geom_bar(stat = 'identity', fill = 'cornflowerblue') + xlab(' ') + scale_y_continuous("") + 
  theme(text = element_text(size = 18)) + ggtitle("Median reference to money in fiction\n")
plot(q)