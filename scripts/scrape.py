import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer
from transformers import AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import AutoConfig

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
import sentiment_analysis as sentiment
import topic_model as topic
import joblib

model = joblib.load('use_bert_topic.pkl')

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
    # clean the full text
    df['cleaned_text'] = df['text'].apply(lambda review: process_text(review))
    return df

def run(name):
    links = scrape(name + " singapore food review")
    df = get_text(links)
    df = clean_text(df)
    return df

def sentiment_analysis(sentence):
  
    finetuned_model = "potatobunny/results-bm"  # from huggingface repo
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', config=AutoConfig.from_pretrained(finetuned_model), padding=True, truncation=True)
    model = AutoModelForSequenceClassification.from_pretrained(finetuned_model)
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    results = classifier(sentence)
    return results

def get_sentiment(df):
    map_label = {'LABEL_1': 1, 'LABEL_0': 0}

    # df = df.drop_duplicates().dropna()
    sentences = df['cleaned'].drop_duplicates().dropna().to_list()
    full_sentence = []
    for x in sentences:
        full_sentence.extend(x)

    full_sentence = [x for x in full_sentence if (x != '')]
    # df['Sentence'] = full_sentence
    res = sentiment_analysis(full_sentence)
    final = {}
    for x in range(len(full_sentence)):
      final[full_sentence[x]] = [map_label[res[x]['label']]]
    # final_df['Sentiment'] = res
    # final_df['Sentiment'] = final_df['Sentiment'].apply(lambda x: map_label[x['label']])
    return final

# phrases is the dataframe that is after sentiment analysis
# Topic 0 : place
# Topic 1 : fnb
# Topic 2 : price
# Topic 3 : service
def predict_topic(sentences, model):
    lst_topics = {}
    for i in sentences:
        idx = model.find_topics(i, top_n = 1)[0][0]
        topics = ''
        if idx in [1,4,5,8,9]:
            topics = "Food and Beverage"
        elif (idx == 0) or (idx == 2):
            topics = "Place"
        elif idx == 6:
            topics = "Service"
        else:
            topics = "Price"
        lst_topics[i] = [sentences[i][0], topics]
    return lst_topics

def run_analysis(df):
    sa = get_sentiment(df)
    print('Sentiment Analysis - done')
    tm = predict_topic(sa, model)
    print('Topic modelling - done')
    final_result = {0:{'Food and Beverage': 0, 'Place': 0, 'Price':0, 'Service': 0}, 1:{'Food and Beverage': 0, 'Place': 0, 'Price':0, 'Service': 0}}
    for x in tm:
        curr = tm[x]
    #     # print(curr[0])
        final_result[curr[0]][curr[1]] += 1
    return final_result
    


    
