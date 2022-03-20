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

stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)

def scrape(q):
    q = urllib.parse.quote_plus(q)
    result = get_source("https://www.google.com/search?q=" + q)
    lst = list(result.html.absolute_links)
    exclude_domains = ('google.', 'https://google.', 'https://webcache.googleusercontent.', 'http://webcache.googleusercontent.', 'https://policies.google.',
                       'https://support.google.','https://maps.google.','https://www.instagram.','https://www.youtube.', 'facebook', 'tripadvisor')
    links = lst.copy()
    for url in lst:
        for domain in exclude_domains:
            if domain in url:
                try:
                  links.remove(url)
                except:
                  continue
                continue

    return links

def filter_text(txt):
    stop_words = ["inbox","©",":","=","@", "copyright", "cookies","..","\xa0","min","redirecting…","seconds…", "#", '()', "captcha",'redirect','anti-virus','malware','JavaScript','developer','technology','subscribe','learn more…','support us']
    if not txt or len(txt)<100:
        return False
    for x in stop_words:
        if x in txt.lower():
            return False
    return True

def get_text(links):
    result = []
    for url in links:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # soup = str(soup.find_all('div')).split('>')
        # main = url.split('/')
        # text = list(set(filter(lambda x:"<br" in x or "</p" in x, soup)))
        # text = list(filter(lambda x:filter_text(x), text))
        p = set(map(lambda x : x.get_text(), soup.find_all('p')))
        text = list(filter(lambda x:filter_text(x), p))
        result.extend(text)
    df = pd.DataFrame(result, columns = ['text'])
    return df

def process_text(text):
    # remove '\n' present in the raw reviews
    text = text.replace('\n', ' ')
    # lower text
    text = text.lower()
    # split sentence into words
    token = word_tokenize(text)
    # spelling error check
    # token = [checker(x) for x in token]
    # remove punctuation
    table = str.maketrans('', '', punctuation)
    stripped = [x.translate(table) for x in token]
    # remove remaining tokens that are not alphabetic
    word = [x for x in stripped if x.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    stop_words.remove('not')
    word = [x for x in word if not x in stop_words]
    # lemmatization
    lemmatized_output = [lemmatizer.lemmatize(x) for x in word]
    # join all words into one sentence
    result = " ".join(lemmatized_output)
    return result

def clean_text(df):
    df['review_splitted'] = df['text'].apply(sent_tokenize)
    df['cleaned'] = df['review_splitted'].apply(lambda reviews: [process_text(sentence) for sentence in reviews])
    return df

def is_positive(sentence):
    # Means positive sentiment if compound score greater than 0 (can tweak this threshold)
    return sia.polarity_scores(sentence)["compound"] > 0 

def polarity_score_list(lst, positive_reviews, negative_reviews, positive_reviews_bigram, negative_reviews_bigram):
    result = []

    for sent in lst:
        if (is_positive(sent) and sent):
            result.append("Positive")
            positive_reviews.extend(nltk.word_tokenize(sent))
            positive_reviews_bigram.extend(nltk.bigrams(nltk.word_tokenize(sent)))
        elif (sent):
            result.append("Negative")
            negative_reviews.extend(nltk.word_tokenize(sent))
            negative_reviews_bigram.extend(nltk.bigrams(nltk.word_tokenize(sent)))
        else:
            result.append([])
    return result,  positive_reviews, negative_reviews, positive_reviews_bigram, negative_reviews_bigram

def get_sentiment(df):
    positive_reviews = []
    negative_reviews = []

    positive_reviews_bigram = []
    negative_reviews_bigram = []
    
    df_review = pd.DataFrame()
    df_review["Text"] = df["text"]
    df_review["Review"] = df["cleaned"]
    df_review["Sentiment"] = df["cleaned"]
    df_review["Sentiment"] = df_review["Sentiment"].apply(lambda x: polarity_score_list(x, positive_reviews, negative_reviews, positive_reviews_bigram, negative_reviews_bigram)[0])
    return df_review, positive_reviews, negative_reviews, positive_reviews_bigram, negative_reviews_bigram

def get_top(positive_reviews, negative_reviews):
    positive_fd = nltk.FreqDist(positive_reviews)
    negative_fd = nltk.FreqDist(negative_reviews)

    common_set = set(positive_fd).intersection(negative_fd) # Remove common set

    for word in common_set:
        del positive_fd[word]
        del negative_fd[word]
    top_5_positive = {word for word, count in positive_fd.most_common(5)}
    top_5_negative = {word for word, count in negative_fd.most_common(5)}
    return top_5_positive, top_5_negative

def run(name):
    links = scrape(name + " singapore food review")
    df = get_text(links)
    df = clean_text(df)
    df, pos, neg, pos_bi, neg_bi = get_sentiment(df)
    pos, neg = get_top(pos, neg)
    return pos, neg
    


    
