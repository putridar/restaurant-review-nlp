from transformers import pipeline, AutoTokenizer
from transformers import AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import AutoConfig
import pandas as pd

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
    # final_df['Sentiment'] = res
    # final_df['Sentiment'] = final_df['Sentiment'].apply(lambda x: map_label[x['label']])
    return res

def run_analysis(df):
    sa = get_sentiment(df)
    # tm = topic.predict_topic(sa, model)
    # print('Topic modelling - done')
    # final = tm.groupby(['Sentiment','Topic']).count().reset_index().sort_values(by='Topic')
    # final_result = {0:{'Food and Beverage': 0, 'Place': 0, 'Price':0, 'Service': 0}, 1:{'Food and Beverage': 0, 'Place': 0, 'Price':0, 'Service': 0}}
    # for x in range(len(final)):
    #     curr = final.iloc[x]
    #     final_result[curr['Sentiment']][curr['Topic']] = curr['Sentence']
    return sa