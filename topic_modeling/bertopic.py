from bertopic import BERTopic
import pickle

#load pkl in a list
def load_corpus(pkl_path):
    rfc_dict = pickle.load(open( 'rfc_pkl.pkl', "rb" ))
    return list(rfc_dict.values())

# pkl is saved as a list of strings

def create_bert_topics(rfc_pickle_path):
    cleaned_rfcs = load_corpus(rfc_pickle_path)
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(cleaned_rfcs)
    return topic_model