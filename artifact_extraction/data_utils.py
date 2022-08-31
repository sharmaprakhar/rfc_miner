from functools import total_ordering
import numpy as np
from os import listdir
from os.path import isfile, join
import re
from collections import defaultdict
import subprocess
import string

'''
ALL CHARACTERS IN CURRENT RFCs

# {'ϔ': 0, 's': 1, 'j': 2, '\x0c': 3, 'ß': 4, 'k': 5, 'ϋ': 6, '}': 7, '7': 8, ')': 9, 'l': 10, '>': 11, 
#  'ꮪ': 12, 'w': 13, 'v': 14, ']': 15, '1': 16, 'ⅳ': 17, '\x08': 18, '♦': 19, 'y': 20, '!': 21, '/': 22, 
#  '|': 23, '$': 24, ',': 25, 'ς': 26, '_': 27, 'z': 28, 'ꭲ': 29, '*': 30, 't': 31, '4': 32, '¹': 33, 
#  '[': 34, 'σ': 35, '∞': 36, 'b': 37, 'a': 38, '+': 39, '(': 40, '9': 41, '\u1680': 42, 'h': 43, '?': 44, 
#  'ı': 45, 'm': 46, '0': 47, '"': 48, 'ꮢ': 49, ':': 50, '໐': 51, 'u': 52, '6': 53, '%': 54, 'å': 55, 
#  'é': 56, '3': 57, '£': 58, 'p': 59, '#': 60, '.': 61, 'ü': 62, '8': 63, '@': 64, 'g': 65, 'i': 66, 
#  'x': 67, 'ዐ': 68, '０': 69, '5': 70, 'd': 71, '\\': 72, '2': 73, 'ſ': 74, 'ꮅ': 75, 'π': 76, 'e': 77, 
#  '-': 78, '<': 79, ';': 80, '=': 81, '&': 82, 'ﬁ': 83, '~': 84, '\ufeff': 85, 'r': 86, '\t': 87, 
#  '\x00': 88, 'ꮛ': 89, '€': 90, 'n': 91, '{': 92, '\n': 93, '`': 94, 'а': 95, ' ': 96, 'o': 97, 'c': 98, 
#  '^': 99, 'q': 100, "'": 101, 'f': 102}
'''

window = 5

label_dict = { 'onr_rfcclass_nlt' : 0, 'onr_rfcclass_strdef' : 1, 'onr_rfcclass_msgStructure' : 2,
'onr_rfcclass_dataflow' : 3,
'onr_rfcclass_topologyDiag' : 4,
'onr_rfcclass_table' : 5,
'onr_rfcclass_stateTD' : 6,
'onr_rfcclass_cs' : 7,
'onr_rfcclass_protocolLayerDiag' : 8,
'onr_rfcclass_caption' : 9,
'onr_rfcclass_headers' : 10,
'onr_rfcclass_toc' : 11,
'onr_rfcclass_lex_spec' : 12 }

def plot_current_loss_profile(train_loss_list, val_loss_list):
    plt.plot(range(len(train_loss_list)), train_loss_list, label='train')
    plt.plot(range(len(val_loss_list)), val_loss_list, label='val')
    plt.legend(loc='upper right')
    plt.show()

def split_and_create_loaders(data):
    X_train, X_test, y_train, y_test = train_test_split(data, Y, test_size=0.33, random_state=42)
    print('train sequences: ', X_train.shape[0])

    train_dataset = TensorDataset(torch.Tensor(X_train), torch.Tensor(y_train)) 
    test_dataset = TensorDataset(torch.Tensor(X_test), torch.Tensor(y_test))

    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                                        batch_size=batch_size, 
                                                        shuffle=True)
                
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                                        batch_size=batch_size, 
                                                        shuffle=False)
    return train_loader, test_loader

def get_max_line(rfc_dir):
    # get max line in RFCs
    onlyfiles = [join(rfc_dir, f) for f in listdir(rfc_dir) if isfile(join(rfc_dir, f))]
    length_max = []
    for r in onlyfiles:
        with open(r,  encoding="utf8", errors='ignore') as rfh:
            lines = rfh.readlines()
            for l in lines:
                length_max.append([l, len(l)])
    #ascending
    length_max = sorted(length_max, key=lambda x:x[1], reverse=True)
    print('maximum line length in an RFC:', length_max[2][1])
    return length_max[2][1]

def get_char_vocab(rfc_dir, predecided=True):
    '''
    vocab is the set of all chars in RFCs
    predecided=True returns a subset of the vocab most appropriate for modeling
    consisting of lowercase alphabets, digits and chosen special characters

    input: rfc_dir (directory containing all RFCs)
    predecided=True returns a subset of total vocab

    returns: vocab and length of vocab
    '''
    # special charcters used in current modeling
    specials = ['}', ')', '>', ']', '!', '/', '|', '$', ',', '_', '*', '?', 
           '"', ':', '%', '@', '.', '#', '\\', '\t', '~', '&', '=', ';',
            '<', '-', '{', ' ', '^', "'"]

    if not predecided:
        max_set = set()
        onlyfiles = [join(rfc_dir, f) for f in listdir(rfc_dir) if isfile(join(rfc_dir, f))]
        for r in onlyfiles:
            with open(r,  encoding="utf8", errors='ignore') as rfh:
                lines = rfh.readlines()
                for l in lines:
                    l = l.lower()
                    l = set(l)
                    max_set = max_set.union(l)
        
        return max_set, len(max_set)
    
    allowed = list(string.ascii_lowercase) + [str(x) for x in range(10)] + specials + 'unk'
    return allowed, len(allowed)

def char_to_idx(allowed):
    '''
    returns a mapping from chars to idx and 
    from idx to char
    '''
    char_to_idx = {}
    idx_to_char = {}
    for i,e in enumerate(allowed):
        # allowed chars get an integer
        # all others get unknown (idx = len(allowed))
        char_to_idx[e] = i
        idx_to_char[i] = e
    return char_to_idx, idx_to_char



def create_samples(file, _maxlen):
    '''
    read each line, strip it, convert line to list of integers (indexes) usign char_to_idx
    join the resulting vector to master array
    return array

    input: _maxlen: maximum length line in all rfc documents (output of get_max_line)
    '''
    data = []
    with open(file, 'r') as fh:
        lines = fh.readlines()
        for l in lines:
            if l=='\n':
                continue
            l = l.lower()
            l = l.strip()
            cur_len = len(l)
            # convert to arr of integers
            curseq = []
            for c in l:
                try:
                    curseq.append(char_to_idx[c])
                except:
                    curseq.append(len(allowed))
            # pad sequences shorter than _maxlen
            pad = _maxlen - cur_len
            for _ in range(pad):
                curseq.append(len(allowed))
            data.append(curseq)
    return np.array(data)