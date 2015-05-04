library(ggplot2)
library(scales)
l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/logisticpredictions.csv')
l$birthdate[l$birthdate == 0] <- NA
model = glm(data = l, formula = as.integer(reviewed == 'rev') ~ logistic + pubdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
line = intercept + (slope * l$pubdate)
true = sum(l$logistic > line & l$reviewed == 'rev') + sum(l$logistic <= line & l$reviewed == 'not')
false = sum(l$logistic < line & l$reviewed == 'rev') + sum(l$logistic >= line & l$reviewed == 'not')
print(true / (true + false))
levels(l$actually) <- c('Norton', 'Norton', 'random', 'reviewed')
p <- ggplot(l, aes(x = pubdate, y = logistic, color = actually, shape = actually)) + geom_point() + 
  geom_smooth(method="lm", size = 2) + 
  scale_shape_discrete(name='') +
  ggtitle("710 volumes of poetry.\n") +
  scale_color_manual(name = "", values = c('indianred3', 'gray70', 'cadetblue', 'gray80')) +
  theme(text = element_text(size = 18)) + 
  scale_y_continuous('Predicted probability of coming from reviewed set\n', labels = percent) + 
  scale_x_continuous("")
plot(p)