# Protocol RFC processing utilities

This repo contains APIs to process protocol RFCs. The capabilities of this code include the following:

1. Topic modeling on a set of RFCs using:
    > Latent Dirichlet Allocation
    > BERTopic (BERT based topic modeling)

2. Clustering of similar RFCs using:
    > Making a disjoint set forest using explicit connections from within RFCs
    > pairwise cosine similarity using tf-idf (term frequency, inverse document frequency)

3. Artifact extraction from RFCs using the following methodologies:
    > heuristic (symbol based): using key-symbols to extract diagrams, figures, callflows, message structures, tables, captions etc.
    > classifying each line of an RFC as 'natural language text' or 'artifact', thus aiding in artifact extraction
    > classifying each line of an RFC as a class from a predecided set of classes

# API:

The base class provides two class objects: 

**artifactExtractor**: provides APIs for extraction of protocol RFC artifacts. We identify the following major classes of artifacts:<br />
    &emsp; 1. Natural language text<br />
    &emsp; 2. C-Struct definition<br />
    &emsp; 3. Message structure<br />
    &emsp; 4. Data flow diagrams<br />
    &emsp; 5. Topology diagrams<br />
    &emsp; 6. Tables<br />
    &emsp; 7. State diagrams<br />
    &emsp; 8. Client-server comminucation diagrams<br />
    &emsp; 9. Protocol layer diagrams<br />
    &emsp; 10. Captions<br />
    &emsp; 11. RFC page headers<br />
    &emsp; 12. Table of contents<br />
    &emsp; 13. Lexical specifications<br />

**topicModel**: provides APIs for the following functionalities:<br />
    &emsp; 1. Cluster a given set of RFCs using explicit connection information inside RFCs<br />
    &emsp; 2. Create a pairwise RFC similarity matrix for 'soft-clustering' into groups<br />
    &emsp; 3. Perform topic modeling on RFCs using two major topic modeling techniques:<br />
        &emsp;&emsp; a. Latent Dirichlet Allocation<br />
        &emsp;&emsp; b. BERT model based topic modeling (BERTopic)<br />

### To run the n-way clasifier:<br />
    &emsp; python main.py --rfcs rfcs/ --extraction_method 'nway'

### To run the symbol based classifier:<br />
    &emsp; python main.py --rfcs rfcs/ --extraction_method 'symbol_based'

### To run the tfidf vectorizer:<br />
    &emsp; python main.py --rfcs rfcs/ --topic_method tfidf

### To run the lda topic mode;:<br />
    &emsp; python main.py --rfcs rfcs/ --topic_method lda

Acknowledgements: This research was funded by a grant from the Office of Naval Research (ONR). 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Office_of_Naval_Research_Official_Logo.png/640px-Office_of_Naval_Research_Official_Logo.png" width="200">