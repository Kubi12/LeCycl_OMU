library(RColorBrewer)
library(wordcloud)
library(tm)
library(SnowballC)
library(wordcloud2) 

#-------------Exercice 1--------------------------------------------------------

#Load text
txt = readLines("drawdown.txt")
corpus = Corpus(VectorSource(txt))

#Cleaning text
corpus = tm_map(corpus, removePunctuation)                 #Remove punctuation
corpus = tm_map(corpus, removeNumbers)                     #Remove number
corpus = tm_map(corpus, stripWhitespace)                   #Remove useless blank
corpus = tm_map(corpus, content_transformer(tolower))      #To lower
corpus = tm_map(corpus, removeWords, stopwords("english")) #Remove stopwords
#corpus = tm_map(corpus, removeWords, c("the"))            #Remove 'the' it seem's not be in stopword
#corpus = tm_map(corpus, stemDocument)                     #Stemming

#Create the matrix
dtm = TermDocumentMatrix(corpus)
m = as.matrix(dtm)
v = sort(rowSums(m),decreasing=TRUE)
d = data.frame(word = names(v),freq=v)

#Cloud plot
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


#-------------Exercice 2--------------------------------------------------------

#Load text
txt = readLines("drawdown.txt")
corpus = Corpus(VectorSource(txt))

#Cleaning text
corpus = tm_map(corpus, removePunctuation)                 #Remove punctuation
corpus = tm_map(corpus, removeNumbers)                     #Remove number
corpus = tm_map(corpus, stripWhitespace)                   #Remove useless blank
corpus = tm_map(corpus, content_transformer(tolower))      #To lower
corpus = tm_map(corpus, removeWords, stopwords("english")) #Remove stopwords
corpus = tm_map(corpus, removeWords, c("can", "energy", "carbon", "percent", 
                                      "emissions", "one", "will", "word",
                                      "water", "The")) #Remove words

#Create the matrix
dtm = TermDocumentMatrix(corpus)
m = as.matrix(dtm)
v = sort(rowSums(m),decreasing=TRUE)
d = data.frame(word = names(v),freq=v)

#Cloud plot
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))


#-------------Exercice 3--------------------------------------------------------

#Load text
txt = readLines("drawdown.txt")
corpus = Corpus(VectorSource(txt))

#Cleaning text
corpus = tm_map(corpus, removePunctuation)                 #Remove punctuation
corpus = tm_map(corpus, removeNumbers)                     #Remove number
corpus = tm_map(corpus, stripWhitespace)                   #Remove useless blank
corpus = tm_map(corpus, content_transformer(tolower))      #To lower
corpus = tm_map(corpus, removeWords, stopwords("english")) #Remove stopwords
corpus = tm_map(corpus, removeWords, c("can", "energy", "carbon", "percent", 
                                       "emissions", "one", "will", "word",
                                       "water", "The")) #Remove words

#Create the matrix
dtm = TermDocumentMatrix(corpus)
m = as.matrix(dtm)
v = sort(rowSums(m),decreasing=TRUE)
d = data.frame(word = names(v),freq=v)

#Cloud plot
wordcloud2(d, size = 0.2, shape = 'star')
