coded = read.table('/Users/tunder/Dropbox/GenreProject/python/piketty/coded.tsv',sep = '\t', stringsAsFactors = F, quote='')
wage = c(rep(17,50), rep(29,50), rep(30, 25), rep(45,25), rep(53, 10), rep(70,6), rep(107, 4), rep(180,20), rep(206,5), rep(316,6))
yearstoplot = integer(0)
logstoplot = numeric(0)
for (i in 1:400) {
  if (coded$V4[i] > 0) {
    yrindex = coded$V1[i] - 1749
    # column one contains the year for each snippet
    logval = log((coded$V4[i] / wage[yrindex]), 10)
    # column 4 contains the money value. The line above
    # calculates log10(nominal value / nominal wage)
    yearstoplot <- c(yearstoplot, coded$V1[i])
    logstoplot <- c(logstoplot, logval)
  }
}

df <- data.frame(x = yearstoplot, y = logstoplot)
q <- ggplot(df, aes(x = x, y = y))
q <- q +geom_point() + geom_smooth() + scale_x_continuous(' ') + scale_y_continuous("log10 of money referenced / avg annual wage\n") + theme(text = element_text(size = 18))
plot(q)

# wage[yrindex]