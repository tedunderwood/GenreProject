money = read.csv('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/codedsnippets.csv', stringsAsFactors = F)
money$logval <- as.numeric(money$logval)
money$normval <- as.numeric(money$normval)
money$nominalval <- as.numeric(money$nominalval)
themeans = numeric()
for (center in seq(1750, 1950)) {
  ceiling = center + 25
  floor = center - 25
  newmean = mean(money$normval[money$date >= floor & money$date < ceiling], trim = 0.45)
  themeans = c(themeans, newmean)
}
# barplot(themeans, main = "Rich & Ted's 424 snippets, median (reference / wage)", ylab = "nominal value in £", names.arg = c('1750', '60', '70', '80', '90', '1800', '10', '20', '30', '40', '50', '60', '70', '80', '90', '1900', '10', '20', '30', '40'))

# ('1750', '1760', '1770', '1780', '1790', '1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900', '1910', '1920', '1930', '1940')
plot(seq(1750,1950), themeans, type='l', lwd=2, ylim = c(0, max(themeans)), xlab = '', ylab = 'nominal value in £', main = 'Running median of nominal value in 500 snippets, 41 yr window.')