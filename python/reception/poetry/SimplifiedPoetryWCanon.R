l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/linearpredictions.csv')
l$birthdate[l$birthdate == 0] <- NA
model = glm(data = l, formula = as.integer(reviewed == 'rev') ~ logistic + pubdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
line = intercept + (slope * l$pubdate)
true = sum(l$logistic > line & l$reviewed == 'rev') + sum(l$logistic <= line & l$reviewed == 'not')
false = sum(l$logistic < line & l$reviewed == 'rev') + sum(l$logistic >= line & l$reviewed == 'not')
print(true / (true + false))
levels(l$actually) <- c('yes', "yes", 'no', 'no')
levels(l$reviewed) <- c('added', 'random', 'from reviews')
l$logistic[l$reviewed == 'added'] <- NA
levels(l$reviewed) <- c(NA, 'random', 'from reviews')
p <- ggplot(l, aes(x = pubdate, y = logistic, color = reviewed, shape = actually)) + geom_point() + geom_abline(intercept = intercept, slope = slope) + 
  scale_shape_discrete(name='anthologized\ntoday\n') +
  ggtitle("811 volumes of poetry, sorted\nby a linguistic model of distinction.\n") +
  scale_color_manual(name = "sample\n", values = c('gray68', 'dodgerblue3')) + theme(text = element_text(size = 18)) + scale_y_continuous('Predicted probability that\nvolume came from reviewed set\n', labels = percent) + scale_x_continuous("")
plot(p)