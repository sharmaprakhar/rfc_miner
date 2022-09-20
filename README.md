Protocol RFC processing utilities

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

How To Run:

The base class provides two class objects: 

artifactExtractor: provides APIs for extraction of protocol RFC artifacts. We identify the following major classes of artifacts:
    1. Natural language text<br />
    2. string definition<br />
    3. message structure<br />
    4. data flow diagrams<br />
    5. topology diagrams<br />
    6. tables<br />
    7. state diagrams<br />
    8. client-server comminucation diagrams<br />
    9. protocol layer diagrams<br />
    10. captions<br />
    11. headers<br />
    12. table of contents<br />
    13. lexical specifications<br />

topic_model: provides APIs for the following functionalities:
    1. Cluster a given set of RFCs using explicit connection information inside RFCs<br />
    2. Create a pairwise RFC similarity matrix for 'soft-clustering' into groups<br />
    3. Carry out topic modeling on RFCs using two major topic modeling techniques:<br />
        a. Latent Dirichlet Allocation<br />
        b. BERT model based topic modeling (BERTopic)<br />

To run the n-way clasifier:<br />
    &emsp; python main.py --rfcs rfcs/ --extraction_method 'nway'

To run the symbol based classifier:<br />
    &emsp; python main.py --rfcs rfcs/ --extraction_method 'symbol_based'

To run the tfidf vectorizer:<br />
    &emsp; python main.py --rfcs rfcs/ --topic_method tfidf

To run the lda topic mode;:<br />
    &emsp; python main.py --rfcs rfcs/ --topic_method lda


