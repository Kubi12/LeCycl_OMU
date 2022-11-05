install.packages("wordcloud")
library(wordcloud)


install.packages("RColorBrewer")
library(RColorBrewer)

install.packages("wordcloud2")
library(wordcloud2)

##loading the data
install.packages("tm")
library(tm)

#creating vector contatining text

#data = read("drawdown.txt")
#text <- data$text
data <- file.path("drawdown.txt")
#create a corpus
#docs <- Corpus(VectorSource(text))
docs <- Corpus(DirSource(text))
#Cleaning the data

docs <- docs %>%
  tm_map(removeNumbers) %>%
  tm_map(removePunctuation) %>%
  tm_map(stripWhitespace)
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeWords, stopwords("english"))
docs <- tm_map(docs, PlainTextDocument)

#Create the document-term-matrix

dtm <- TermDocumentMatrix(docs) 
matrix <- as.matrix(dtm) 
words <- sort(rowSums(matrix),decreasing=TRUE) 
df <- data.frame(word = names(words),freq=words)

#Generating the word cloud
wordcloud(words= df$word, freq = df$freq, min.freq = 1, max.words = 200, random.order = False, rot.per = 0.35, colors = brewer.pal(2, "Dark2"))

###############Excluding certain words from the wordcloud########################

docs <- tm_map(docs, removeWords, c("can", "energy", "carbon", "percent", "one", "will", "word", "water"))

dtm <- TermDocumentMatrix(docs) 
matrix <- as.matrix(dtm) 
words <- sort(rowSums(matrix),decreasing=TRUE) 
df <- data.frame(word = names(words),freq=words)

wordcloud(words= df$word, freq = df$freq, min.freq = 1, max.words = 200, random.order = False, rot.per = 0.35, colors = brewer.pal(2, "Dark2"))

####################Create a wordcloud in a star shape#################
wordcloud2(data = df, shape = 'star')