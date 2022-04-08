from transformers import pipeline, AutoTokenizer
from transformers import AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import AutoConfig

def sentiment_analysis(sentence):
  
    finetuned_model = "potatobunny/results-bm"  # from huggingface repo
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', config=AutoConfig.from_pretrained(finetuned_model), padding=True, truncation=True)
    model = AutoModelForSequenceClassification.from_pretrained(finetuned_model)
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    results = classifier(sentence)
    return results

def get_sentiment(df):
    map_label = {'LABEL_1': 1, 'LABEL_0': 0}

    sentences = df['cleaned'].drop_duplicates().dropna().to_list()
    full_sentence = []
    for x in sentences:
        full_sentence.extend(x)

    full_sentence = [x for x in full_sentence if (x != '')]
    res = sentiment_analysis(full_sentence)
    final = {}
    for x in range(len(full_sentence)):
      final[full_sentence[x]] = [map_label[res[x]['label']]]
    return final