l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/linearpredictions.csv')
l$birthdate[l$birthdate < 1700] <- NA
l$reviewed[l$reviewed == 'addedbecausecanon'] <- NA
model = glm(data = l, formula = as.integer(reviewed == 'rev') ~ logistic + pubdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
line = intercept + (slope * l$pubdate)
true = sum(l$logistic > line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic <= line & l$reviewed == 'not', na.rm = TRUE)
false = sum(l$logistic < line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic >= line & l$reviewed == 'not', na.rm = TRUE)
print(true / (true + false))
#levels(l$reviewed) = c('random', 'reviewed')
p <- ggplot(l, aes(x = pubdate, y = logistic, color = reviewed, shape = reviewed)) + geom_point() + geom_abline(intercept = intercept, slope = slope) + scale_color_manual(values = c('dodgerblue4', 'indianred2')) + theme(text = element_text(size = 16)) + scale_y_continuous('Probability of being obscure\n', labels = percent) + ggtitle('Obscure and well-known works. 74.3% accurate.\n') + scale_x_continuous("")
plot(p)