# Corrected plot
# Corrects the ratio of money references / fiction words for
# predicted false negatives and false positives.

library(ggplot2)
library(dplyr)

rollingmean <- function(avector, window) {
  # Calculates a new vector created by taking a rolling average
  # of avector at every point using a window that is ± window
  # in size, assuming that enough points are available.
  
  veclen = length(avector)
  
  newvec = numeric()
  map = seq(veclen)
  # We use map to generate a Boolean vector without the requirement
  # to test for overruns of the endpoints with if statements.
  
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

fnr <- data.frame(falsenegs = filtered$ratio * falsenegrate)
filtered <- cbind(filtered, fnr)
# q<- ggplot(filtered, aes(x = date, y = corrected)) + geom_point() + geom_smooth()
# plot(q)
falsepos <- read.csv('~/Dropbox/GenreProject/python/piketty/manualcoding/nonmonetary_dist.csv')
falsepos <- arrange(falsepos, desc(year))
fp <- numeric(201)
idx = 0
for (i in 1750:1950) {
  idx = idx + 1
  for (j in seq(1,21)) {
    yearfloor = falsepos$year[j]
    if (yearfloor< i) {
      rate = falsepos$errorsnips[j] / falsepos$allsnips[j]
      break
    }  
  }
  fp[idx] <- filtered$ratio[idx] * rate
}
correction <- data.frame(corrected = filtered$ratio + filtered$falsenegs - fp)
filtered <- cbind(filtered, correction)

moveavg = rollingmean(filtered$corrected, 12)

#plot(filtered$date, filtered$corrected)
# par(new = T)
# plot(filtered$date, moveavg*10000, type='l', lwd=4, ylim = c(0, max(moveavg*10000)))

novels = data.frame(date = c(1799,1813,1874,1925), freq = c(0.77, 2.21, 5.4, 1.83))
lf <- data.frame(date = filtered$date[1:200], freq = moveavg[1:200] * 10000)
q <- ggplot(lf, aes(x = date, y = freq)) + geom_line(size = 3, colour = 'cornflowerblue') + scale_y_continuous('', breaks = c(0,1,2,3,4,5), limits = c(0, 5.45)) + scale_x_continuous('') +
  geom_point(data = novels, size = 4) + theme(text = element_text(size = 20))
plot(q)