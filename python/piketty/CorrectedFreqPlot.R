# Corrected plot
#

library(ggplot2)

rollingmean <- function(avector, window) {
  veclen = length(avector)
  
  newvec = numeric()
  map = seq(veclen)
  for (idx in 1:veclen) {
    floor = idx - window
    ceiling = idx + window
    newmean = mean(avector[map >= floor & map <= ceiling])
    newvec <- c(newvec, newmean)
   
  }
  newvec
}


filtered <- read.csv('~/Dropbox/GenreProject/python/piketty/model_filtered_money_v3.csv')
falsenegs = read.csv('~/Dropbox/GenreProject/python/piketty/statsproblem/falsenegativesbyyear.csv')
model <- loess(rate ~ date, falsenegs)
falsenegrate <- predict(model)

fnr <- data.frame(corrected = filtered$ratio + (filtered$ratio * falsenegrate))
filtered <- cbind(filtered, fnr)
# q<- ggplot(filtered, aes(x = date, y = corrected)) + geom_point() + geom_smooth()
# plot(q)

moveavg = rollingmean(filtered$corrected, 12)

#plot(filtered$date, filtered$corrected)
# par(new = T)
# plot(filtered$date, moveavg*10000, type='l', lwd=4, ylim = c(0, max(moveavg*10000)))

novels = data.frame(date = c(1799,1813,1874,1925), freq = c(0.77, 2.21, 5.8, 2.03))
lf <- data.frame(date = filtered$date, freq = moveavg * 10000)
q <- ggplot(lf, aes(x = date, y = freq)) + geom_line(size = 3, colour = 'cornflowerblue') + scale_y_continuous('', limits = c(0, 5.9)) + scale_x_continuous('') +
  geom_point(data = novels, size = 3) + theme(text = element_text(size = 20))
plot(q)