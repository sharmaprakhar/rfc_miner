from os import listdir, symlink
from os.path import isfile, join
import re

# onlyfiles = [join('rfcs', f) for f in listdir('rfcs') if isfile(join('rfcs', f))]

# symbols = ['#', '|', '=']
symbols = ['#', '|', '=', '----', '->', '<-']

def explore(idx, lines):
    num_lines = len(lines)-1
    i = idx
    while i>0:
        i-=1
        if lines[i]=='\n':
            start = i+1
            break
    i = idx
    while i<num_lines:
        i+=1
        if lines[i]=='\n':
            end = i
            break
    return start, end

def prune(lines):
    # function to remove lines with pure text in them
    # prune blocks that beginwith 'rule'
    # TO DO : prune blocks that begin with 'Note:'
    if 'rule' in lines[0]:
        return False
    t = ' '.join(lines)
    # remove punctuations
    to_rem = [' ', ',', '.']
    for s in to_rem:
        t = t.replace(s,'')
    # ratio of symbols and alpha numeric characters
    alphas = 0
    syms = 0
    for i in t:
        if i.isalpha():
            alphas += 1
        else:
            syms += 1
    # symbols less than 10%
    if syms/(alphas+syms)<0.10:
        return False
    return True

def check_underscores(line):
    return re.match('^\s*-+\s*', line)

def check_proximity(prev_end, this_start):
    if this_start-prev_end<=4:
        return True
    return False


# onlyfiles = ['../rfcs/rfc{}.txt'.format(str(rfc)) for rfc in [2616, 1035, 6066, 959, 1772, 
#                                                               2131, 1001, 7530, 5321, 3977, 
#                                                               793, 768, 792, 826, 1661, 
#                                                               951, 791, 2460, 7426]]
onlyfiles = ['../rfcs/rfc{}.txt'.format(str(rfc)) for rfc in [1001]]

for r in onlyfiles:
    # extract from RFC
    artfcts = set()
    artifacts = []
    artifact_idx = []
    with open(r, 'r') as fh:
        lines = fh.readlines()
        for i,l in enumerate(lines):
            for s in symbols:
                if s in l:
                    if check_underscores(l):
                        continue
                    # block bounds
                    start, end = explore(i, lines)
                    # include after pruning: y/n?
                    should_inc = prune(lines[start:end])
                    if should_inc:
                        cand = ''.join(lines[start:end])
                        if cand not in artfcts:
                            artfcts.add(cand)
                            artifacts.append(cand)

    
    # write to artifact file
    with open('artifacts/artifact{}.txt'.format(r[-8:-4]), 'a+') as fh:
        for a in artifacts:
            fh.write('\n')
            fh.write(a)
            fh.write('\n')
            fh.write('##################################################################################\n')