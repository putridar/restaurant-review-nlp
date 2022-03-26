import pandas as pd
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup

import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('brown')
nltk.download('punkt')
nltk.download('omw-1.4')

from nltk import sent_tokenize
from nltk.tokenize import word_tokenize

from string import punctuation
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import scripts.scrape as scrape

stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def get_wordcount(name):
    # get dataframe that contains reviews from google
    df = scrape.run(name)
    # For wordcloud
    wordLst = [] # for unigram
    wordLstBigram = [] # for bigram
    for sent in df['cleaned_text']: # customised based on df returned from scrape() function
        if (sent):
            wordLst.extend(nltk.word_tokenize(sent)) # Use extend bcs word tokenize return list
            wordLstBigram.extend(nltk.bigrams(nltk.word_tokenize(sent)))
    wordCount = nltk.FreqDist(wordLst)
    wordBigramCount = nltk.FreqDist(wordLstBigram)
    wordCountFinalLst = [[x, y] for x, y in wordCount.items()]
    wordBigramCountFinalLst = [[x, y] for x, y in wordBigramCount.items()]
    wordCountFinalLst.sort(key= lambda x: x[1], reverse=True)
    return wordCountFinalLst[:50]
