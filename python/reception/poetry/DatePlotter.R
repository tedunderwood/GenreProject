l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/datepredictions.csv')
l$nation[l$nation != 'us'] <- 'uk'
for (i in 1:700) {
  if(l$birthdate[i] < 1700) l$birthdate[i] <- l$pubdate[i] - 42.69
}

p <- ggplot(l, aes(x = birthdate, y = prediction, color = reviewed, shape = reviewed)) +
  geom_point() + scale_colour_manual(values= c('gray20','indianred2')) +
  theme(text = element_text(size = 16)) +
  geom_smooth() +
  scale_y_continuous('Predicted date.\n') + 
  ggtitle('A model trained on 1820-89 makes predictions about 1900-19.\n') + scale_x_continuous("")
plot(p)