from doctest import DocFileSuite
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

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/scrape',methods = ['POST', 'GET'])
def get_result():
    result = ''
    if request.method == 'POST':
        name = request.get_json().get('name')
        # get dataframe that contains reviews from google
        df = scrape.run(name)
        # get wordcount
        wc = wordcount.get_wordcount(df)
        # get sentiment analysis and topic modelling result
        sa = sentiment.get_sentiment(df)
        print('Sentiment Analysis - done')
        tm = topic.predict_topic(sa, model)
        print('Topic modelling - done')
        # aggregate result
        final_result = {0:{'Food and Beverage': 0, 'Place': 0, 'Price':0, 'Service': 0}, 1:{'Food and Beverage': 0, 'Place': 0, 'Price':0, 'Service': 0}}
        for x in tm:
            curr = tm[x]
            final_result[curr[0]][curr[1]] += 1
        result = {'wordcount': wc, 'result': final_result}
    else:
        result = request.args.get('name')
    return jsonify(result)

if __name__ == "__main__":
  app.run(debug=True)
