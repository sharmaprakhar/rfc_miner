from os import listdir, symlink
from os.path import isfile, join
import re

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
    # prune blocks that begin with 'rule'
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
            if i.isdigit() or i.islower():
                alphas += 1
        else:
            syms += 1
    # symbols less than 10%
    # print(syms/(alphas+syms))
    if syms/(alphas+syms)<0.10:
        return False
    return True

def check_hyphons(line):
    return re.match('^\s*-+\s*$', line)

def check_proximity(prev_end, this_start):
    if this_start-prev_end<=4:
        return True
    return False

def include_fig_caption(end, lines):
    for i in range(5):
        if 'Figure' in lines[end+i]:
            # print('found figure at:', end+i)
            # # while lines[i]!='\n':
            # #     i+=1
            # print('returning:', end+i+1)
            return end+i+1
    return False

def extract_sym(rfc_dir, savedir):
    symbols = ['#', '|', '=', '----', '->', '<-', '!']
    onlyfiles = [join(rfc_dir, f) for f in listdir(rfc_dir) if isfile(join(rfc_dir, f))]

    for r in onlyfiles:
        # extract from RFC
        artfcts = set()
        artifacts = []
        artifact_idx = []
        with open(r, 'r') as fh:
            lines = fh.readlines()
            i=0
            while i<len(lines):
                # print('!!! current i:', i)
                l = lines[i]
                line_flag = False
                for s in symbols:
                    # if symbol found in line, process the block and skip to the end
                    # start checking symbols at the end (break)
                    if s in l:
                        if check_hyphons(l):
                            # print('check underscores True')
                            continue
                        start, end = explore(i, lines)
                        # include after pruning: y/n?
                        should_inc = prune(lines[start:end])
                        isfig = include_fig_caption(end, lines)
                        if isfig: end = isfig # include keyword figure
                        # if abs(end-start)<2: should_inc=False #ignore single lines: doesnt work very well
                        if should_inc:
                            line_flag = True
                            i=end+1
                            # merge two nearby aftifacts. Nearness threshold decided inside check_proximity
                            if len(artifact_idx)>0 and check_proximity(artifact_idx[-1][1], start):
                                to_rem = artifacts.pop()
                                # print('artifact being removed:\n', to_rem)
                                artfcts.discard(to_rem)
                                prev_start, prev_end = artifact_idx.pop()
                                cand = ''.join(lines[prev_start:end])
                                # print('artifact being added:\n', cand)
                                start = prev_start
                            else:
                                cand = ''.join(lines[start:end])
                                # print('artifact just being added:\n', cand)
                            if cand not in artfcts:
                                artfcts.add(cand)
                                artifacts.append(cand)
                                artifact_idx.append([start, end])
                        # break because even if a single symbol hits, the whole block will be taken care of
                        break
                if not line_flag:
                    i+=1
            
    
        # write to artifact file
        with open(join(savedir, 'artifact{}.txt'.format(r[-8:-4])), 'a+') as fh:
            for a in artifacts:
                fh.write('\n')
                fh.write(a)
                fh.write('\n')
                fh.write('##################################################################################\n')