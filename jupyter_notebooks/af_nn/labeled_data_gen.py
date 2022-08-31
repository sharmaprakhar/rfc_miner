import string
import nltk
# nltk.download()
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import re
import sys
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from os import listdir
from os.path import isfile, join


from functools import total_ordering
import numpy as np
from os import listdir
from os.path import isfile, join
import re
from collections import defaultdict
import subprocess



# get total number of unique symbols
def get_max_line(file):
    with open(file, 'r') as fh:
        lines = fh.readlines()
        _max = 0
        for l in lines:
            cur = l.strip()
            if len(cur)>_max:
                _max = len(cur)
                max_line = cur
    return max_line, _max


# m1, _max1 = get_max_line('pos_seq.txt')
# m2, _max2 = get_max_line('neg_seq.txt')

# max_feature_length = max(_max1, _max2)

# steps:
    # 1: get max vocab length
    # 2: convert each line in neg and pos seq to a feature vector. vector Length = vocab
    # 3: 

def get_char_vocab():
    max_set = set()
    # onlyfiles = [join('../rfcs', f) for f in listdir('../rfcs') if isfile(join('../rfcs', f))]
    onlyfiles = ['../rfcs/mqtt.txt']
    for r in onlyfiles:
        with open(r,  encoding="utf8", errors='ignore') as rfh:
            lines = rfh.readlines()
            for l in lines:
                l = l.lower()
                l = set(l)
                max_set = max_set.union(l)
    return max_set

vocab = get_char_vocab()
print(list(vocab))