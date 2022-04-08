import os
import pickle
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import sys
sys.path.append('./scripts')
import numpy as np
import wordcount
from flask import Flask, jsonify, request
import scrape
import sentiment_analysis as sentiment
import topic_model as topic
import pandas as pd
import joblib

model = joblib.load('use_bert_topic.pkl')

import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('brown')
nltk.download('punkt')
nltk.download('omw-1.4')

df = scrape.run('mcdonalds')
wc = wordcount.get_wordcount(df)
sa = sentiment.get_sentiment(df)
print('Sentiment Analysis - done')
tm = topic.predict_topic(sa, model)
print('Topic modelling - done')
final = tm.groupby(['Sentiment','Topic']).count().reset_index().sort_values(by='Topic')
final_result = {0:[], 1:[]}
for x in range(len(final)):
    curr = final.iloc[x]
    final_result[curr['Sentiment']].append(curr['Sentence'])
result = {'wordcount': wc, 'result': final_result}