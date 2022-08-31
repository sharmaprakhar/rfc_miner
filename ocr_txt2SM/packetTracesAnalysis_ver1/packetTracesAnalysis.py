import dpkt

import numpy as np
import sklearn.cluster
import distance

import matplotlib.pyplot as plt

def label_bar(ax, bars, text_format, is_inside=True, **kwargs):
    """
    Attach a text label to each bar displaying its y value

    :param ax: Matplolib axes object
    :param bars: The histogram
    :param text_format: The format used for the labels
    :param is_inside: Are the labels inside the bars (True) or outside (False)
    """
    max_y_value = max(bar.get_height() for bar in bars)
    if is_inside:
        distance = max_y_value * 0.05
    else:
        distance = max_y_value * 0.01

    for bar in bars:
        if bar.get_height() < 100 :
          continue
        text = text_format.format(bar.get_height())
        text_x = bar.get_x() + bar.get_width() / 2
        if is_inside:
            text_y = bar.get_height() - distance
        else:
            text_y = bar.get_height() + distance

        ax.text(text_x, text_y, text, ha='center', va='bottom', **kwargs)


def histogram(dic):
    """
    Print a histogram of the lengths of the messages

    :param dic: A dictionary of data
    """
    x=list(dic.keys())
    y=list(dic.values())

    fig, ax = plt.subplots()
    bars = ax.bar(x,y, 10, color='r',)
    ax.set_title('Lengths of tcp data')
    value_format = "{:1}"  # displaying values as percentage with one fractional digit
    label_bar(ax, bars, value_format, is_inside=False, color="black")

    plt.show()

def clustering(packets, printClusters=False, printClustersContents=False):
    """
    Do the clustering using the Affinity Propagation algorithm and the Hamming distance

    :param packets: The packets to cluster (array)
    :param printClusters: If True, will print the clusters ( "- 12: [0 4 12]" with 12 the index of this cluster's exemplar and 0, 4 and 12 the cluster's content)
    :param printClustersContents: If True, will print the clusters content
    """
    pkts = np.asarray(packets) #So that indexing with a list will work

    lev_similarity = -1*np.array([[distance.hamming(p1,p2) for p1 in pkts] for p2 in pkts])
    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)

    #Print clusters
    if printClusters:
        for cluster_id in np.unique(affprop.labels_):
            exemplar = affprop.cluster_centers_indices_[cluster_id]
            cluster = np.unique(np.nonzero(affprop.labels_==cluster_id))
            cluster_str = np.array_str(cluster)
            print(" - *%s:* %s" % (exemplar, cluster_str))


    #Print clusters contents
    if printClustersContents:
        for cluster_id in np.unique(affprop.labels_):
            print('CLUSTER No: ', cluster_id)
            cluster = np.unique(pkts[np.nonzero(affprop.labels_==cluster_id)])
            cluster_str = "\n\n".join(cluster)
            print(cluster_str)



##Find text/bytes
def tokens_decompo(pkt):
    """
    Decompose the packet into tokens

    :param pkt: The packet to tonkenize
    """
    i=0
    tokens = []
    for i in range(len(pkt)):
        if i%2 == 0:
            if pkt[i] in ['2','3','4','5','6','7']:
                tokens.append('t')
            else:
                tokens.append('b')
    return(tokens)


def fields_from_message(tokenizedpkt):
    """
    Compute the message structure from a tokenized packet

    :param tokenizedpkt: a tokenized packet from which we will infer the message structure
    :return: An array of tuples (start, end) corresponing to the inferred fields
    """
    indices = [0]
    for i in range(1,len(tokenizedpkt)):
        if tokenizedpkt[i-1] != tokenizedpkt[i]:
            indices.append(i-1)
            indices.append(i)
    indices.append(len(tokenizedpkt)-1)
    fields = []
    for k in range(0, len(indices), 2):
        fields.append((indices[k],indices[k+1]))
    f = 1
    while f < len(fields):
        if fields[f][0] == fields[f][1]:
            i1 = fields.pop(f-1)[0]
            i2 = fields.pop(f)[1]
            fields[f-1] = (i1,i2)
        else:
            f += 1
    return fields


filename='wrccdc.2018.pcap'

# Some counters
counter=0
ipcounter=0
tcpcounter=0
udpcounter=0
httpcounter=0


tcppkts = {}
smalls=[]
statuses=[]
even = True #Packets are always doubled in the wrccdc file, so we take one 

for ts, pkt in dpkt.pcap.Reader(open(filename,'rb')):

    counter+=1
    eth=dpkt.ethernet.Ethernet(pkt) 
    
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
       continue

    ip=eth.data
    ipcounter+=1

    if ip.p==dpkt.ip.IP_PROTO_TCP: 
        tcpcounter+=1
        tcp = ip.data
        
        if tcp.sport == 80 and len(tcp.data) > 0:
            try:
                http = dpkt.http.Response(tcp.data)
                httpcounter+=1
                if http.status not in statuses:
                    statuses.append(str(http.status))
                if len(tcp.data.hex()) > 200:
                    if even:
                        smalls.append(tcp.data.hex()[:10])
                    even = not even
                
                if len(tcp.data.hex()) not in tcppkts:
                    tcppkts[len(tcp.data.hex())] = 1
                else:
                    tcppkts[len(tcp.data.hex())] += 1
            
            except:
                continue
           
  
        

    if ip.p==dpkt.ip.IP_PROTO_UDP:
       udpcounter+=1

print("Total number of packets in the pcap file: ", counter)
print("Total number of ip packets: ", ipcounter)
print("Total number of tcp packets: ", tcpcounter)
print("Total number of udp packets: ", udpcounter)
print("Total number of http packets: ", httpcounter)

print(statuses)

# sorted_by_value = sorted(tcppkts.items(), key=lambda kv: kv[1], reverse=True)
# print(sorted_by_value)
# To print the histogram of lengths: 
# histogram(tcppkts)


clustering(smalls, True, True)

print('\nWITH TOKENS\n')
tokens_pkts=[tokens_decompo(pkt) for pkt in smalls]
clustering(tokens_pkts, True)



print(tokens_pkts[7])
print(fields_from_message(tokens_pkts[7]))
