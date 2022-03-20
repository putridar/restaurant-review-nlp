import os
import pickle
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
import scrape
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/scrape',methods = ['POST', 'GET'])
def get_result():
    result = ''
    if request.method == 'POST':
        name = request.get_json().get('name')
        result = scrape.run(name)
    else:
        result = request.args.get('name')
    return jsonify(str(result))

if __name__ == "__main__":
  app.run(debug=True)
