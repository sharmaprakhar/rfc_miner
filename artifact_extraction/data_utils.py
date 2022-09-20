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

specials = ['\n', '}', ')', '>', ']', '!', '/', '|', '$', ',', '_', '*', '?', '"',
            ':', '%', '@', '.', '#', '\\', '\t', '~', '&', '=', ';', '<', '-', '{',
             ' ', '^', "'"]

def plot_current_loss_profile(train_loss_list, val_loss_list):
    plt.plot(range(len(train_loss_list)), train_loss_list, label='train')
    plt.plot(range(len(val_loss_list)), val_loss_list, label='val')
    plt.legend(loc='upper right')
    plt.show()

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

def get_char_vocab(rfc_dir, mode='minimal'):
    '''
    vocab is the set of all chars in RFCs
    predecided=True returns a subset of the vocab most appropriate for modeling
    consisting of lowercase alphabets, digits and chosen special characters

    input: rfc_dir (directory containing all RFCs)
    mode: what subset of characters to use

    returns: vocab and length of vocab
    '''
    # special charcters used in current modeling
    if mode=='raw':
        max_set = set()
        onlyfiles = [join(rfc_dir, f) for f in listdir(rfc_dir) if isfile(join(rfc_dir, f))]
        for r in onlyfiles:
            with open(r,  encoding="utf8", errors='ignore') as rfh:
                lines = rfh.readlines()
                for l in lines:
                    l = l.lower()
                    l = set(l)
                    max_set = max_set.union(l)
        
        return max_set
    elif mode=='subset':
        allowed = list(string.ascii_lowercase) + [str(x) for x in range(10)] + specials + 'unk'
        return allowed
    elif mode=='minimal':
        allowed = ['char'] + ['digit'] + specials
        return allowed

def make_maps(allowed):
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

def process_window(w):
    # print('w:',len(w)) 
    lst = []
    for k in w:
        lst.append([x for x in k])
    return lst

def make(onlyfiles):
    '''
    input: onlyfiles, a list of annotated RFCs
    returns: samples and labels
    '''
    samples = []
    labels = []
    for r in onlyfiles:
        print('processing :', r)
        with open(r,  encoding="utf8", errors='ignore') as rfh:
            lines = rfh.readlines()
            cur_tag = 'onr_rfcclass_nlt'
            cur_label = label_dict[cur_tag]
            for i,l in enumerate(lines):
                if l=='\n':
#                     print('yowzaa!!')
                    continue
                if 'onr_rfcclass' in l:
                    if 'onr_rfcclass_references_start' in l:
                        break
                    if l.startswith('<end_'):
                        cur_tag = 'onr_rfcclass_nlt'
                        cur_label = label_dict[cur_tag]
                        continue
                    else:
                        cur_tag = l.strip()[1:-1]
                        # print(cur_tag)
                        cur_label = label_dict[cur_tag]
                        continue
                if i<=window: # lines before the window'th line
                    lst = process_window(lines[i:i+window+1])
                    smpl = [['a' for _ in range(50)] for _ in range(window)] + lst
                    # print(len(smpl))
                    assert len(smpl)==2*window+1
                elif i==len(lines)-1:
                    lst = process_window(lines[i-window:i+1])
                    smpl = lst + [['a' for _ in range(50)] for _ in range(window)]
                    # print(len(smpl))
                    assert len(smpl)==2*window+1
                else:
                    smpl = process_window(lines[i-window:i+1]) + process_window(lines[i+1:i+window+1])
                    # print(len(smpl))
                    assert len(smpl)==2*window+1
                samples.append(smpl)
                labels.append(cur_label)
    for _ in range(window):
        samples.pop()
        labels.pop()
    return samples, labels

def handle_newlines(samples, length_max):
    '''
    each empty line is ['\n']. To be included as a sample, it needs to be 
    as long as length_max (uniform sample length)
    input: samples (array of context window samples)
    returns: processed samples array
    '''
    for i,e in enumerate(samples):
        for j,v in enumerate(e):
            if v==['\n']:
                samples[i][j]=['\n']*length_max
    return samples

def create_samples_subset(samples, char_to_idx, _maxlen, allowed):
    '''
    read each sample, convert line to list of integers (indexes) using char_to_idx
    join the resulting vector to master array, return array
    NOTE: this method uses a subset of all symbols in the RFCs to create samples
    e.g all digits and alphabets are given the same index, and a subset of specials is used
    '''
    data = []
    for s in samples:
        mini_data = []
        for line_list in s:
            ll = []
            cur_len = len(line_list)
            for char in line_list:
                if char.isalpha():
                    ll.append(char_to_idx['char'])
#                     ll.append(char_to_idx[char])
                elif char.isdigit():
                    ll.append(char_to_idx['digit'])
#                     ll.append(char_to_idx[digit])
                elif char in specials:
                    ll.append(char_to_idx[char])
#                     ll.append(char_to_idx['specials'])
                else:
                    ll.append(len(allowed))
            # pad sequences shorter than _maxlen
            pad = _maxlen - cur_len
            for _ in range(pad):
                ll.append(len(allowed))
            mini_data.append(ll)
        data.append(mini_data)
    return np.array(data)

def create_samples_full(file):
    '''
    read each line, strip it, convert line to list of integers (indexes) usign char_to_idx
    join the resulting vector to master array, return array
    NOTE: digits and alphabets are unique, subset of specials is used
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

def make_one_hot_single(allowed,X):
    vector_len = len(allowed)+1 # should be 67 in this case, added 1 for unknown
    big_mat = []
    for sample in X:
        mat = []
        for idx in sample:
            cand = np.zeros((vector_len))
            cand[idx] = 1 #(1x67)
            mat.append(cand)
        big_mat.append(np.array(mat))
        
    big_mat = np.array(big_mat)
    return big_mat

def make_one_hot_window(allowed, X):
    vector_len = len(allowed)+1
    big_mat = []
    for sample in X: # (5,82)
        mat = []
        for s in sample: # (82,)
            idx_mat = []
            for idx in s:
                cand = np.zeros((vector_len))
                cand[idx] = 1 #(1x33)
                idx_mat.append(cand)
            mat.append(idx_mat)
        big_mat.append(np.array(mat))
        
    big_mat = np.array(big_mat)
    return big_mat

def how_many(y):
    for i in range(13):
        print('label: {}, samples : {}'.format(i, y[y==i].shape[0]))