import joblib
from bertopic import BERTopic

# phrases is the dataframe that is after sentiment analysis
# Topic 0 : place
# Topic 1 : fnb
# Topic 2 : price
# Topic 3 : service
def predict_topic(phrases, model):
    lst_topics = []
    sentences = phrases['Sentence']
    for i in sentences:
        idx = model.find_topics(i, top_n = 1)[0][0]
        if idx in [1,4,5,8,9]:
            lst_topics.append("Food and Beverage")
        elif (idx == 0) or (idx == 2):
            lst_topics.append("Place")
        elif idx == 6:
            lst_topics.append("Service")
        else:
            lst_topics.append("Price")
    df = phrases.copy()
    df['Topic'] = lst_topics
    return df