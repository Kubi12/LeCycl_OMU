datafile <- read_file("./drawdown.txt")
lower <- str_to_lower(datafile[1])
letter_space <- str_replace_all(lower, "[^\\w\\s]", "")
words <- split(letter_space, "\\s")
unique_words <- unique(words)
word_freq <- lapply(unique_words, function(x) (sum(grepl(x, words)) / length(words)))




test_sentences <- "Drawdown is a message grounded in science; it also is a testament to the growing stream of humanity who understands the enormity of the challenge we face, and is willing to devote their lives to a future of kindness, security, and regeneration. The young girl here is from the Borana Oromo people, who reside in the Nakuprat-Gotu Community Conservancy in northern Kenya. Her picture has been our talisman, calling us daily to the work that we do.
"
test_sentences2 <- "Drawdown is a message grounded in science; it also is a testament to the growing stream "


library(stringr)
lower <- str_to_lower(test_sentences2[1])
letter_space <- str_replace_all(lower[1], "[^\\w\\s]", "")
letter_space_shortened <- str_replace_all(letter_space[1], "[\\s]+", " ")
words <- str_split(letter_space_shortened[1], "\\s")
unique_words <- unique(words[[1]])
word_freq <- lapply(unique_words, function(x) (sum(grepl(x, words[[1]])) / length(words[[1]])))

library(stringr)
library(wordcloud)
library(readr)
datafile <- read_file("./drawdown.txt")
lower <- str_to_lower(datafile[1])
letter_space <- str_replace_all(lower[1], "[^\\w\\s]", "")
letter_space_shortened <- str_replace_all(letter_space[1], "[\\s]+", " ")
#words <- str_split(letter_space_shortened[1], "\\s")
#unique_words <- unique(words[[1]])
#word_freq <- lapply(unique_words, function(x) (sum(grepl(x, words[[1]])) / length(words[[1]])))
colors <- c("#58c59b", "#c58104", "#4545a0", "#62af53", "#beb200", "#ff00f2", "#222222")
wordcloud(lower, max.words = 150, random.order = FALSE, rot.per = .33, colors = colors)


#install.packages('name')
#install.packages("wordcloud")
#library(wordcloud)
#install.packages("RColorBrewer")
#library(RColorBrewer)
#install.packages("wordcloud2")
#library(wordcloud2)
#install.packages("tm")

library(tm)
library(wordcloud2)
library(wordcloud)
library(readr)
docs <- Corpus(VectorSource(datafile[1]))

docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, removePunctuation)
docs <- tm_map(docs, stripWhitespace)
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeWords, stopwords("english"))

dtm <- TermDocumentMatrix(docs)
matrix <- as.matrix(dtm)
words <- sort(rowSums(matrix), decreasing = TRUE)
df1 <- data.frame(word = names(words), freq = words)

# build wordcloud
set.seed(1234) # for reproducibility
wordcloud(words = df1$word,
    freq = df1$freq,
    min.freq = 1,
    max.words = 150,
    random.order = FALSE,
    rot.per = 0.35,
    colors = brewer.pal(8, "Dark2"))


# remove special words

#lower <- str_to_lower(datafile[1])
#letter_space <- str_replace_all(lower[1], "[^\\w\\s]", " ")
docs <- Corpus(VectorSource(datafile[1]))


letter_space <- str_replace_all(datafile[1], "[“–•]", " ")
docs <- Corpus(VectorSource(letter_space[1]))

docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, removePunctuation)
docs <- tm_map(docs, stripWhitespace)
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeWords, stopwords("english"))


docs <- tm_map(docs, removeWords, c("can", "energy", "carbon",
    "percent", "emissions", "one", "will", "world", "water"))
#    "percent", "emissions", "one", "will", "word", "water"))

docs <- tm_map(docs, removeWords, c("“", "–", "•", "'s"))

dtm <- TermDocumentMatrix(docs)
matrix <- as.matrix(dtm)
words <- sort(rowSums(matrix), decreasing = TRUE)
df <- data.frame(word = names(words), freq = words)


wordcloud2(df[1:150, ], size = 0.3, shape = "star")

wordcloud2(df[1:150, ])

