install.packages("wordcloud")
library(wordcloud)
install.packages("wordcloud2")
library(wordcloud2)
install.packages("RColorBrewer")
library(RColorBrewer)
install.packages("tm")
library(tm)

text <- readLines("drawdown.txt")
docs <- Corpus(VectorSource(text))

toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "-")
docs <- tm_map(docs, toSpace, "“")
docs <- tm_map(docs, toSpace, "”")
docs <- tm_map(docs, toSpace, "•")
docs <- tm_map(docs, toSpace, "@")
docs <- tm_map(docs, toSpace, "©")
docs <- tm_map(docs, toSpace, "’")
docs <- tm_map(docs, toSpace, "• ")
docs <- tm_map(docs, toSpace, "'")

docs <- tm_map(docs,removeNumbers)
docs <- tm_map(docs,removePunctuation)
docs <- tm_map(docs,stripWhitespace)
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeWords, stopwords("english"))

dtm <- TermDocumentMatrix(docs) 
matrix <- as.matrix(dtm) 
words <- sort(rowSums(matrix),decreasing=TRUE) 
df <- data.frame(word = names(words),freq=words)

set.seed(1234)
wordcloud(words = df$word, freq = df$freq,
          min.freq = 50, max.words=150, random.order=FALSE, 
          rot.per=0.35, colors=brewer.pal(8, "Dark2"))

df2 <- tail(df,-9) 


wordcloud(words = df2$word, freq = df2$freq,
          scale = c(2,0.2),
          min.freq = 50, max.words=150, random.order=FALSE, 
          rot.per=0.35, colors=brewer.pal(8, "Dark2"))


df3 <- df[c(0:150),]
wordcloud2(data=df3,size=0.2,shape='star')