money = read.csv('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/normalbyvol.csv', stringsAsFactors = F)
money$logval <- as.numeric(money$logval)
themeans = numeric()
for (floor in seq(1750, 1900, 50)) {
  ceiling = floor + 50
  newmean = mean(money$logval[money$date >= floor & money$date < ceiling])
  themeans = c(themeans, newmean)
}
barplot(themeans, main = "Hoyt/Ted's 300 volumes, mean log(moneyreference / wage)", names.arg = c('1750-99', '1800-49', '1850-99', '1900-49'))