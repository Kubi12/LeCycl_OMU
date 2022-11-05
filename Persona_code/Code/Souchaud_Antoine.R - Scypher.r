 # We can use the print() function
print("Hello World!")
#[1] "Hello World!"
# Quotes can be suppressed in the output
print("Hello World!", quote = FALSE)
#[1] Hello World!
# If there are more than 1 item, we can concatenate using paste()
print(paste("How", "are", "you?"))
#[1] "How are you?"

#ap <- available.packages()
#View(ap)
#"tm" %in% rownames(ap)


library(tm)
library(wordcloud2)
library(readr)
library(dplyr)

#ap <- available.packages()
#View(ap)
#"tm" %in% rownames(ap)

getSources()

text1 <- readLines("./drawdown.txt")

cor <- Corpus(VectorSource(text1))

cor <- tm_map(cor, content_transformer(tolower))

#cor <- tm_map(cor, removeNumbers())


#cor <- tm_map(cor, removeWords(), stopwords("english"))
cor <- tm_map(cor, removeNumbers)

cor <- tm_map(cor, removeWords, stopwords("english"))

cor <- tm_map(cor, removePunctuation)

cor <- tm_map(cor, stripWhitespace)

tdm <- TermDocumentMatrix(cor)

m <- as.matrix(tdm)

v <- sort(rowSums(m), decreasing = TRUE)

d <- data.frame(word = names(v), freq = v)

df <- data.frame(word = names(v), freq = v)

#wordcloud(d$word, d$freq)
wordcloud2(d)


#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
# Wordcloud2 for social media responses on COVID-19 pandemic

# step-by-step approach to word cloud generation

# step 1: load libraries NLP, tm, RColorBrewer, SnowballC, wordcloud, 
#         stringr, wordcloud2
# step 2: input text data file pandemic_30052020.csv
# step 3: clean the text data with tm and stringr functions
# step 4: make corpus and dtm (document-term-matrix)
# step 5: generate word cloud 

#---------------------------------------------------
# load the required packages
# input data data pandemic_30052020

library(NLP)
library(tm)
library(RColorBrewer)
library(SnowballC)
library(wordcloud)
library(stringr)
library(wordcloud2)

# read in pandemic_30052020.csv as input file
#reviews <- read.csv(file.choose(), sep=",", header=T)

reviews <- readLines("./drawdown.txt")


abc <- as.matrix(reviews)
head(abc)
tail(abc)

#---------------------------------------------------

#text data cleaning

# stringr functions for removing symbols
abc <- str_remove_all(abc,"–")
abc <- str_remove_all(abc,"’")
abc <- str_remove_all(abc,"—")
abc <- str_remove_all(abc,"“")
abc <- str_remove_all(abc,"”")

# tm functions for text cleaning
abc<-removeNumbers(abc)
abc<-removePunctuation(abc)
abc<-tolower(abc)
abc<-removeWords(abc,c("now", "one", "will", "may", "says", "said", 
                       "also", "figure", "etc", "re", "can", "energy", "carbon", "percent", 
                       "emissions", "one", "will", "word", "water"))
stopwords<-c("the", "and", stopwords("en"))
abc<-removeWords(abc, stopwords("en"))
abc<-stripWhitespace(abc)
abc<-wordStem(abc)        #function from SnowballC

reviews <- abc
head(reviews)
tail(reviews)

#---------------------------------------------------

#A vector source interprets each element of the vector as a document
review.source<-VectorSource(reviews)

#form corpus from vector source
corpus<-Corpus(review.source)
inspect(corpus[1:10])

#make document-term-matrix
dtm<-TermDocumentMatrix(corpus)
inspect(dtm[51:60,10:20])

dtm2<-as.matrix(dtm)
frequency <- sort(rowSums(dtm2), decreasing=T)
head(frequency)
words<-names(frequency)

#---------------------------------------------------

#Visualization of the data
plot(frequency, col="darkblue")

df<- data.frame(names(frequency), frequency)

#visualization via wordcloud package
wordcloud2(df, size=0.4, widgetsize=c(1000,1000))
wordcloud2(df, size=0.1, shape="star", widgetsize=c(1000,1000))
wordcloud2(df, size=0.1, shape="diamond", widgetsize=c(800,800))