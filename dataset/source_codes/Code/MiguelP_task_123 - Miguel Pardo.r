##################################################################
# TASK 1 (the Google Form doesn't allow to upload 3 different files)
##################################################################

library(wordcloud)
library(RColorBrewer)
library(wordcloud2)
library(tm)
library(png)
#Create a vector containing only the text
text <- readLines(file.choose())
# Create a corpus
docs <- Corpus(VectorSource(text))

tospace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, tospace, "/")
docs <- tm_map(docs, tospace, "@")
docs <- tm_map(docs, tospace, "\\|")
# Convert the text to lower case
docs <- tm_map(docs, content_transformer(tolower))
# Remove numbers
docs <- tm_map(docs, removeNumbers)
# Remove english common stopwords
docs <- tm_map(docs, removeWords, stopwords("english"))
# Remove your own stop word
# specify your stopwords as a character vector
#docs <- tm_map(docs, removeWords, c("blabla1", "blabla2"))
# Remove punctuations
docs <- tm_map(docs, removePunctuation)
# Eliminate extra white spaces
docs <- tm_map(docs, stripWhitespace)

#inspect(docs)

dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m), decreasing = TRUE)
d <- data.frame(word = names(v), freq = v)
#print(head(d, 20))

set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 70, scale = c(4.5, 0.5),
          max.words = Inf, random.order = FALSE, rot.per = 0.35,
          colors = brewer.pal(8, "Dark2"))

##################################################################
#TASK 2 (the Google Form doesn't allow to upload 3 different files)
##################################################################

#Create a vector containing only the text
text <- readLines(file.choose())
# Create a corpus
docs <- Corpus(VectorSource(text))

tospace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, tospace, "/")
docs <- tm_map(docs, tospace, "@")
docs <- tm_map(docs, tospace, "\\|")
# Convert the text to lower case
docs <- tm_map(docs, content_transformer(tolower))
# Remove numbers
docs <- tm_map(docs, removeNumbers)
# Remove english common stopwords
docs <- tm_map(docs, removeWords, stopwords("english"))
# Remove your own stop word
# specify your stopwords as a character vector
docs <- tm_map(docs, removeWords, c("can", "energy", "carbon",
        "percent", "emissions", "one", "will", "word", "water"))
# Remove punctuations
docs <- tm_map(docs, removePunctuation)
# Eliminate extra white spaces
docs <- tm_map(docs, stripWhitespace)

#inspect(docs)

dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m), decreasing = TRUE)
d <- data.frame(word = names(v), freq = v)
#print(head(d, 20))

set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 3, scale = c(3.5, 0.5),
          max.words = 200, random.order = FALSE, rot.per = 0.35,
          colors = brewer.pal(8, "Dark2"))

##################################################################
#TASK 2 (the Google Form doesn't allow to upload 3 different files)
##################################################################

set.seed(1234)
wordcloud2(data = d, size = 0.3, shape = "star", color = "random-dark")