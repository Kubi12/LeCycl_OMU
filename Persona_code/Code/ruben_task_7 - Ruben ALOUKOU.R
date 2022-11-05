install.packages("RColorBrewer")
install.packages("wordcloud")
install.packages("wordcloud2")
install.packages("tm")

library(RColorBrewer)
library(wordcloud)
library(wordcloud2)
library(tm)

text<-read.table(drawdown.txt) 
#oubli des quote et des paramètres
text <-read.table("drawdown.txt", sep="\t", header=TRUE)
docs <- Corpus(VectorSource(text))

docs <- docs %>%
  tm_map(removeNumbers) %>%
  tm_map(removePunctuation) %>%
  tm_map(stripWhitespace)
#mauvaise écriture des fonctions

docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, removePunctuation)
docs <- tm_map(docs, stripWhitespace)
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeWords, stopwords("english"))

dtm <- TermDocumentMatrix(docs) 
matrix <- as.matrix(dtm) 
words <- sort(rowSums(matrix),decreasing=TRUE) 
df <- data.frame(word=names(words), freq=words)

set.seed(1234) # for reproducibility

wordcloud(words=df$word, 
          freq=df$freq, 
          min.freq=1,           
          max.words=100, 
          random.order=FALSE, 
          rot.per=0.35,            
          colors=brewer.pal(8, "Dark2"))

docs <- tm_map(docs, removeWords, c("can", "energy", "carbon", "percent", "emissions", "one", "will", "word", "water"))

dtm <- TermDocumentMatrix(docs) 
matrix <- as.matrix(dtm) 
words <- sort(rowSums(matrix),decreasing=TRUE) 
df <- data.frame(word = names(words),freq=words)

set.seed(1234)
wordcloud(words=df$word, 
          freq=df$freq, 
          min.freq = 1,           
          max.words=100, 
          random.order=FALSE, 
          rot.per=0.35,           
          colors=brewer.pal(8, "Dark2"))

set.seed(1234)
wordcloud2(data=df, size=0.7, shape="star")
#does not work beacause ???

head(df, 20)