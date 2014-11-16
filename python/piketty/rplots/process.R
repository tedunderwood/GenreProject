#id of book; book author; booy year, book title;
#book tokens; book words (total number of words essentially)
#specific word counts

require(rCharts)

data <- read.csv(file="wordcount.csv",header=T,sep=",")
data$date <- factor(data$date)

name <- c('Year','Num.Books','Tokens','Words',names(data)[8:48])
wordsOverTime <- data.frame(matrix(NA, nrow=length(levels(data$date)), ncol=length(name)))
names(wordsOverTime) <- name

for (level in seq(1,length(levels(data$date)))){
    J <- data$date == levels(data$date)[level]
    wordsOverTime[level,1] <- levels(data$date)[level]
    wordsOverTime[level,2] <- sum(J)
    count = 3
    for(j in c(3,4,seq(8,48))){
        wordsOverTime[level, count] <- sum(data[[j]][J])
        count = count+1
    }
}

##Visualize Data with Time Series Chart
plot <- rCharts::Highcharts$new()
plot$title(text='Word Counts over Time')
plot$chart(type='line', zoomType='xy')
plot$xAxis(type='datetime',
           title=list(text="Year"),
           labels=list(rotation=-45),
           dateTimeLabelFormats=list(
               month='%Y'
           ))
plot$yAxis(type='linear',
           title=list(text="Word Count"))
plot$legend(enabled=TRUE)

##Select columns from 8 to 48
selection <- c(12,13,14,15,16,17,18,19,20,21,22,23)
value <- as.numeric(levels(data$date))
for (choice in selection){
    lst <- list()
    for (i in 1:length(value)){
        indx <- as.numeric(data$date) == i
        lst[[i]] <- list((value[i]-1970)*365*24*3600*1000, sum(data[[choice]][indx]))
    }
    nom <- names(data)[choice]
    plot$series(data = lst, name= nom)
}
plot