l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/alllinearpredictions.csv')
l$birthdate[l$birthdate == 0] <- NA
model = glm(data = l, formula = as.integer(reviewed == 'rev') ~ logistic + pubdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
line = intercept + (slope * l$pubdate)
true = sum(l$logistic > line & l$reviewed == 'rev') + sum(l$logistic <= line & l$reviewed == 'not')
false = sum(l$logistic < line & l$reviewed == 'rev') + sum(l$logistic >= line & l$reviewed == 'not')
print(true / (true + false))

p <- ggplot(l, aes(x = pubdate, y = logistic, color = actually, shape = actually)) + geom_point() + geom_abline(intercept = intercept, slope = slope) + 
  scale_shape_discrete(name='are\nactually\n') +
  ggtitle("740 volumes of poetry, sorted\nby a linguistic model of distinction.\n") +
  scale_color_manual(name = "are\nactually\n", values = c('indianred1', 'indianred3', 'gray65', 'dodgerblue4')) + theme(text = element_text(size = 18)) + scale_y_continuous('Predicted similarity to (all) reviewed volumes\n', labels = percent) + scale_x_continuous("")
plot(p)