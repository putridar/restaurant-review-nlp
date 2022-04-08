from bertopic import BERTopic

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