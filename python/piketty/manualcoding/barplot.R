money = read.csv('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/normalbyvol.csv', stringsAsFactors = F)
money$logval <- as.numeric(money$logval)
money$normval <- as.numeric(money$normval)
themeans = numeric()
for (floor in seq(1750, 1900, 50)) {
  ceiling = floor + 50
  newmean = median(money$normval[money$date >= floor & money$date < ceiling])
  themeans = c(themeans, newmean)
}
barplot(themeans, main = "Ted & Hoyt's 300 volumes, median(moneyreference / wage)", names.arg = c('1750-99', '1800-49', '1850-99', '1900-49'))