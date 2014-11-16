money = read.csv('/Users/tunder/Dropbox/GenreProject/python/piketty/manualcoding/snippetsandvols.csv', stringsAsFactors = F)
money$logval <- as.numeric(money$logval)
money$normval <- as.numeric(money$normval)
money$nominalval <- as.numeric(money$nominalval)
themeans = numeric()
db <- data.frame(y = numeric(), x = factor())
for (floor in seq(1750, 1930, 20)) {
  ceiling = floor + 20
  newvalues = money$normval[money$date >= floor & money$date < ceiling]
  newframe = data.frame(y = newvalues, x = as.factor(rep(floor, length(newvalues))))
  db = rbind(db, newframe)
}
# barplot(themeans, main = "Rich & Ted's 424 snippets, median (reference / wage)", ylab = "nominal value in £", names.arg = c('1750', '60', '70', '80', '90', '1800', '10', '20', '30', '40', '50', '60', '70', '80', '90', '1900', '10', '20', '30', '40'))

boxplot(db$y ~ db$x, range = 0.5, outline = F)