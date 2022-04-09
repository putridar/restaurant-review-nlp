# Restaurant Reviews Analysis with Sentiment Analysis and Topic Modelling

## Project setup
1. Type ```git clone https://github.com/putridar/restaurant-review-nlp.git``` in your terminal/command prompt
3. Type ```cd restaurant-review-nlp```
4. Run ```conda install -c conda-forge hdbscan```
5. Run ```pip install -r requirements.txt``` to install dependencies
6. Run ```npm install```
7. Run ```python -m nltk.downloader stopwords vader_lexicon brown punkt omw-1.4```
8. Download use_bert_topic.pkl from [here](https://drive.google.com/file/d/17hFihWhLlxL1VeO67fPqjEU3FyNCWi5S/view?usp=sharing) and put it inside the restaurant-review-nlp folder
9. Run ```npm start --fix```

If error persist, stop the program (Ctrl + C) and run ```npm start --fix``` again

Navigate to http://localhost:8080/ to see the result

Note: Use Python 3.7.x to run, and it might take a while to run when your first time running it, since it needs to download some packages first
