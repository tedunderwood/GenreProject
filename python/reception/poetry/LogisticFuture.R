library(scales)
l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/logisticpredictions.csv')
#l$birthdate[l$birthdate < 1700] <- NA
threshold = 1899
evalthreshold = 1889
l$reviewed[l$reviewed == 'addedbecausecanon'] <- NA
model = glm(data = filter(l, pubdate <= evalthreshold), formula = as.integer(reviewed == 'rev') ~ logistic + pubdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
#line = intercept + (slope * l$pubdate)
line = intercept + (slope * evalthreshold)
true = sum(l$pubdate > threshold & l$logistic > line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$pubdate > threshold & l$logistic <= line & l$reviewed == 'not', na.rm = TRUE)
false = sum(l$pubdate > threshold & l$logistic < line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$pubdate > threshold & l$logistic >= line & l$reviewed == 'not', na.rm = TRUE)
print(true / (true + false))
xend <- c(1816)
x = c(1889)
y = (intercept + (slope*x))
yend = (intercept + (slope*xend))
xend <- c(xend,1900)
yend <- c(yend, y)
x <- c(x,1919)
y <- c (y,y)
segments <- data.frame(xend,yend,x,y,colours = c('gray20, gray70', 'gray90'))

#levels(l$reviewed) = c('random', 'reviewed')
p <- ggplot() + 
  geom_point(data=l, aes(x = pubdate, y = logistic, color = reviewed, shape = reviewed)) + scale_colour_manual(values= c('gray20','cadetblue', 'gray60', 'indianred2')) +
  theme(text = element_text(size = 16)) +
  geom_segment(data = segments, aes(x=x, y=y, xend=xend, yend=yend, colour = colours)) + theme(legend.position="none") +
  scale_y_continuous('Probability of coming from reviewed set.\n', labels = percent, breaks = c(0.25,0.5,0.75)) + 
  ggtitle('A model trained on 1820-89 makes predictions about 1900-19.\n') + scale_x_continuous("")
plot(p)