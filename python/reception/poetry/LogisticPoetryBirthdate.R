l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/logisticpredictions.csv')
l$birthdate[l$birthdate < 1700] <- NA
l$reviewed[l$reviewed == 'addedbecausecanon'] <- NA
model = glm(data = l, formula = as.integer(reviewed == 'rev') ~ logistic + birthdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
line = intercept + (slope * l$birthdate)
true = sum(l$logistic > line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic <= line & l$reviewed == 'not', na.rm = TRUE)
false = sum(l$logistic < line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic >= line & l$reviewed == 'not', na.rm = TRUE)
print(true / (true + false))
levels(l$reviewed) = c('random', 'reviewed')
p <- ggplot(l, aes(x = birthdate, y = logistic, color = reviewed, shape = reviewed)) + 
  geom_point() + geom_abline(intercept = intercept, slope = slope) + scale_shape(name="actually") + 
  scale_color_manual(name = "actually", values = c('gray64', 'red3')) + 
  theme(text = element_text(size = 16)) + 
  scale_y_continuous('Predicted probability of coming from reviewed set\n', labels = percent) + 
  ggtitle('700 volumes of poetry.\n') + scale_x_continuous("")
plot(p)