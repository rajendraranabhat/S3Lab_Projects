#Load libraries
library(NLP)
library(tm)

#Sanitize function
sanitize = function(input){
	corpus = Corpus(VectorSource(input))
	corpus = tm_map(corpus, content_transformer(tolower))
	corpus = tm_map(corpus,removePunctuation)
	corpus = tm_map(corpus, stripWhitespace)
	corpus = tm_map(corpus, removeWords,stopwords("english"))
	corpus = tm_ma(corpus, stemDocument, language="english")
	corpus
}