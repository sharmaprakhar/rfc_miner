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
from bertopic import *


parser = argparse.ArgumentParser(description='Topic modeling and artifact extraction from protocol RFCs')
parser.add_argument('--rfcs', type=str, default='rfcs/',
                    help='directory containing RFC documents')
parser.add_argument('--extraction_method', type=str, default='sym',
                    help='method for artifact extraction, default: symbol based')
args = parser.parse_args()

class rfc_baseclass:
    def __init__(self):
        pass

class artifactExtractor:
    def __init__(rfcs, extraction_method):
        '''
        inputs: 
            rfcs: RFC directory
            extraction_method: sym, zero_one, n_way
        '''
        pass
    
    def symbol_based(self, rfc_dir, savedir):
        '''
        Symbol based artifact extraction. Writes artifacts 
        for each rfc from source rfc_dir to target savedir
        Input: rfc_dir (directory containing RFCs)
        savedir: 
        '''
        extract_sym(rfc_dir, savedir)
    
    def zero_one(self):
        pass

    def n_way(self):
        pass

class topic_model:
    def __init__(rfcs, modeler):
        '''
        inputs: 
            rfcs: RFC directory
            modeler: one of LDA, BERTopic, union_find on explicit RFC connections
        '''
        self.sim_threshold = 0.6
        rfc_files = [f for f in listdir(rfc_dir) if isfile(join(rfc_dir, f))]
        _ = clean_and_pkl(rfc_files)
    
    def tfidf():
        # set args at init
        tfidf(self.sim_threshold)

    def make_cc():
        # set args at init
        make_cc(dfs=True, uf=True, download=False)
    
    def run_lda():
        build_and_run()

    def bertopic(rfc_pickle_path, reduce=True, vis=False):
        '''
        currently need to provide pickle rfc file for topic modeling
        reduce=True automatically reduces the topics
        '''
        topic_model = create_bert_topics(rfc_pickle_path)
        if vis:
            topic_model.get_topic_info()
            topic_model.get_topic(7)
            topic_model.visualize_topics()
            topic_model.visualize_barchart()
        if reduce:
            new_topics, new_probs = topic_model.reduce_topics(cleaned_rfcs, topics, probs, nr_topics="auto")