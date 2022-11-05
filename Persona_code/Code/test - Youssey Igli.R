#Question 1

#PACKAGES
install.packages("wordcloud")
install.packages("RColorBrewer")
install.packages("wordcloud2")
install.packages("tm")
#install.packages('devtools')
#devtools::install_github("lchiffon/wordcloud2")

#LOAD
library(wordcloud)
library(RColorBrewer)
library(wordcloud2)
library(tm)

#data <- read.delim("drawdown.txt")
data <- readLines("drawdown.txt")
docs <- Corpus(VectorSource(data))

#cleaning the txt file, tm_map to replace
toSpace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "/")
docs <- tm_map(docs, toSpace, "@")
docs <- tm_map(docs, toSpace, "\\|")

docs <- tm_map(docs, content_transformer(tolower)) #convert words to lower case
docs <- tm_map(docs, removeNumbers) #remove numbers
docs <- tm_map(docs, removePunctuation) #remove punctuations
docs <- tm_map(docs, stripWhitespace)
docs <- tm_map(docs, removeWords, stopwords("english"))

dtm <- TermDocumentMatrix(docs)
matrix <- as.matrix(dtm)
words <- sort(rowSums(matrix), decreasing = TRUE)
df <- data.frame(word = names(words), freq = words)
#print(length(df))
#print(nrow(df))
#newdf <- df[8:nrow(df)]

#newdf <- df[8:nrow(df), ]
#print(head(newdf, 10))

set.seed(1234)
#wordcloud(words = df$word, freq = df$freq,  min.freq = 1,
#max.words = 200, random.order = FALSE, rot.per = 0.35,
#colors = brewer.pal(8, "Dark2"))
#wordcloud(words = newdf$word, freq = newdf$freq,  min.freq = 1,
#max.words = 3, random.order = FALSE, rot.per = 0.35,
#colors = brewer.pal(8, "Dark2"))
wordcloud(words = df$word, freq = df$freq,  min.freq = 1,
max.words = 150, random.order = FALSE, rot.per = 0.35, scale=c(6,.3),
colors = brewer.pal(8, "Dark2"))

#Question 2
docs2 <- tm_map(docs, removeWords, c("can", "energy", "carbon", "percent", "emissions", "one", "will", "word", "water"))
dtm2 <- TermDocumentMatrix(docs2)
matrix2 <- as.matrix(dtm2)
words2 <- sort(rowSums(matrix2), decreasing = TRUE)
df2 <- data.frame(word = names(words2), freq = words2)
wordcloud(words = df2$word, freq = df2$freq,  min.freq = 1,
max.words = 150, random.order = FALSE, rot.per = 0.35, scale=c(4,.3),
colors = brewer.pal(8, "Dark2"))

#Question 3
wordcloud2(df2, size = 0.6, shape = "star")