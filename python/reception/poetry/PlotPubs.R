l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/logisticpredictions.csv')
by_pub <- group_by(l, pubname)
pubs <- summarise(by_pub, date = mean(pubdate), prediction = mean(logistic))
pubs$pubname <- c('random', "Atlantic", "Blackwood's", "Contemporary", "Egotist", "Edinburgh", 
             'Fortnightly', "Graham's", "Macmillan's", "Poetry", "Quarterly", "Savoy", "Tait's", "The New Age", "Westminster","Yellow Book")

xmin <- min(pubs$date) - 10
xmax <- max(pubs$date) + 10
pubs$prediction[4] = pubs$prediction[4] - 0.01
pubs$prediction[3] = pubs$prediction[3] - 0.00
pubs$prediction[8] = pubs$prediction[8] + 0.01
pubs$prediction[5] = pubs$prediction[5] - 0.01
pubs$prediction[12] = pubs$prediction[12] - 0.008
plot(pubs$date, pubs$prediction, type='n', 
     ylab='Probability its choices would be reviewed elsewhere', 
     xlab = '', xlim = c(xmin, xmax))
text(pubs$date, pubs$prediction, labels = pubs$pubname)
model <- lm(prediction ~ date, data = pubs[-1, ])
intercept = coef(model)[1]
slope = coef(model)[2]
xs <- c(xmin, xmax)
ys <- (xs * slope) + intercept
lines(xs, ys, lty = 2)
