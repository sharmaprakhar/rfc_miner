from functools import total_ordering
import numpy as np
from os import listdir
from os.path import isfile, join
import re
from collections import defaultdict
import subprocess

onlyfiles = [join('../rfcs', f) for f in listdir('../rfcs') if isfile(join('../rfcs', f))]

graph = defaultdict(list)
link_prefix = 'https://www.rfc-editor.org/rfc/'

def download_rfcs(to_download):
    for rfc in to_download:
        # write code to check if file not present
        try:
            cmd = 'curl {}rfc{}.txt --output rfc{}.txt'.format(link_prefix, rfc, rfc)
            # subprocess.call('mkdir new_dir', shell=True) # just do this once
            subprocess.call(cmd, shell=True)
        except:
            print('could not download RFC', rfc)

def extract_nums(line):
    regex= "\d{4}"
    match = re.findall(regex, line)
    if match and len(match)<10:
        return match
    return None

class disjoint_set_forest:
    def __init__(self, edges):
        self.parent = {}
        self.edges = edges
    
    def find(self, x):
        if self.parent[x]!=x:
            return self.find(self.parent[x])
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if py!=px:
            self.parent[py] = px
    
    # make a disjoint set forest with the graph
    def djf(self):
        for edge in self.edges:
            u,v = edge
            if u not in self.parent:
                self.parent[u] = u
            if v not in self.parent:
                self.parent[v] = v
            self.union(u,v)

def dfs(rfc, graph, rfc_set):
    # print(rfc)
    seen.add(rfc)
    rfc_set.add(rfc)
    if rfc not in graph:
        return rfc_set
    for n in graph[rfc]:
        if n not in seen:
            rfc_set = dfs(n, graph, rfc_set)
    return rfc_set

edges = []
total_rfc_set = set()
present = set()
for r in onlyfiles:
    node = r[-8:-4]
    present.add(node)
    with open(r,  encoding="utf8", errors='ignore') as rfh:
        line = rfh.readline()
        while line:
            if 'Obsoletes' in line:
                match = extract_nums(line)
                if match:
                    total_rfc_set.add(node)       
                    for n in match:
                        edges.append([node, n])
                        graph[node].append(n)
                        total_rfc_set.add(n)
                break
            line = rfh.readline()

# print('keys in one way directed graph: ', len(graph))
# print('number of edges (undirected)', len(edges))
# print('number of total unique rfcs', len(total_rfc_set))
# print('number of present unique rfcs', len(present))

# Download missing RFCs

to_download = []
for i in total_rfc_set:
    if i not in present:
        to_download.append(i)
        print(i)
download_rfcs(to_download)

# DFS based grouping

# graph = {'a': ['b'], 'd' : ['r'], 'c' : ['r', 'g'], 'k' : ['n', 'p'], 'e' : ['f'], 'f' : ['l'], 'l' : ['m']}
# masterset = []
# seen = set()
# for rfc in graph.keys():
#     if rfc not in seen:
#         masterset.append(dfs(rfc, graph, set()))


# Union Find based grouping

d = disjoint_set_forest(edges)
d.djf()
ans = set()
for i in total_rfc_set:
    ans.add(d.find(i))

print('number of disjoint sets :', len(ans))
# print('unique parents', ans)