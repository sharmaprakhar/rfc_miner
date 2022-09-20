import sys
import os
import argparse
from rfc_clustering.rfc_cc import *
from rfc_clustering.tfidf import *
from topic_modeling.lda import *
from artifact_extraction.artifactExtractor import *
from artifact_extraction.data_utils import *
from artifact_extraction.models import *
from artifact_extraction.trainer import *
# from topic_modeling.bertopic import *
from demos import *

parser = argparse.ArgumentParser(description='Topic modeling and artifact extraction from protocol RFCs')
parser.add_argument('--rfcs', type=str, default='rfcs/',
                    help='directory containing RFC documents')
parser.add_argument('--extraction_method', type=str, default=None,
                    help='method for artifact extraction, default: None')
parser.add_argument('--topic_method', type=str, default=None,
                    help='method for topic modeling, default: None')
args = parser.parse_args()

class artifactExtractor:
    def __init__(self, rfcs):
        '''
        inputs: 
            rfcs: RFC directory
            extraction_method: sym, zero_one, n_way
        '''
        self.rfc_dir = rfcs
    
    def symbol_based(self):
        '''
        Symbol based artifact extraction. Writes artifacts 
        for each rfc from source rfc_dir to target savedir
        Input: rfc_dir (directory containing RFCs)
        savedir: 
        '''
        rep_rfcs_dir = 'artifact_extraction/rep_rfcs'
        extract_sym(rep_rfcs_dir)
    
    def zero_one(self):
        pass

    def n_way(self):
        import os
        p = 'jupyter_notebooks/af_nn/annotated_rfcs/'
        annot = os.listdir(p)
        annot.remove('mqtt.txt')
        annotated_rfcs = [os.path.join(p,x) for x in annot]
        # print(annotated_rfcs)
        leav = [os.path.join(p,'mqtt.txt')]
        # print(leav)
        context_window =  5
        run_nway(self.rfc_dir, annotated_rfcs, leav, context_window)

class topicModel:
    def __init__(self, rfcs):
        '''
        inputs: 
            rfcs: RFC directory
            modeler: one of LDA, BERTopic, union_find on explicit RFC connections
        '''
        self.sim_threshold = 0.6
        rfc_files = [f for f in listdir(rfcs) if isfile(join(rfcs, f))]
        if not os.path.exists('rfc_pkl.pkl'):
            print('pickled rfcs not found. Processing RFCs...')
            _ = clean_and_pkl(rfc_files)
    
    def tfidf(self):
        # set args at init
        print('running tfidf')
        tfidf(self.sim_threshold)

    def make_cc():
        # set args at init
        make_cc(dfs=True, uf=True, download=False)
    
    def run_lda(self, num_topics):
        build_and_run(num_topics)

    def bertopic(self, reduce=True, vis=True):
        '''
        currently need to provide pickle rfc file for topic modeling
        reduce=True automatically reduces the topics
        '''
        rfc_pickle_path = 'rfc_pkl.pkl'
        print('creating BERTopic model')
        topic_model = create_bert_topics(rfc_pickle_path)
        if vis:
            topic_model.get_topic_info()
            topic_model.get_topic(7)
            topic_model.visualize_topics()
            topic_model.visualize_barchart()
        if reduce:
            print('reducing topics')
            new_topics, new_probs = topic_model.reduce_topics(cleaned_rfcs, topics, probs, nr_topics="auto")


af = artifactExtractor('rfcs/')
tm = topicModel('rfcs/')
# if args.extraction_method=='nway':
    # af.n_way()
# if args.topic_method=='bertopic':
#     tm.bertopic()
# if args.topic_method=='tfidf':
#     tm.tfidf()
if args.topic_method=='lda':
    num_topics = 20
    tm.run_lda(num_topics)
if args.extraction_method=='symbol_based':
    af.symbol_based()