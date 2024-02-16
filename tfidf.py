import sys

import spacy
from lxml import etree
from collections import Counter
import string
import zipfile
import os
import numpy as np
import re

"""
pytest -v

test_tfidf.py::test_gettext PASSED                                                              [ 14%]
test_tfidf.py::test_tokenize PASSED                                                             [ 28%]
test_tfidf.py::test_tokenize_2 PASSED                                                           [ 42%]
test_tfidf.py::test_doc_freq PASSED                                                             [ 57%]
test_tfidf.py::test_compute_tfidf_i PASSED                                                      [ 71%]
test_tfidf.py::test_compute_tfidf PASSED                                                        [ 85%]
test_tfidf.py::test_summarize PASSED                                                            [100%]
"""

def gettext(xmlfile) -> str:
    """
    Parse xmltext and return the text from <title> and <text> tags
    """
    # your code here
    tree = etree.parse(xmlfile)
    root = tree.getroot()
    text=""
    for ti in tree.findall("title"):
        text+=" ".join(i.strip() for i in ti.itertext() if i.strip()!="")
    text+=" "
    for te in tree.findall("text"):
        text+=" ".join(i.strip() for i in te.itertext() if i.strip()!="" )
    return text

def tokenize(text, nlp) -> list:
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. 
      1. Normalize to lowercase. Strip punctuation, numbers, and `\r`, `\n`\, `\t`. 
      2. Replace multiple spaces for a single space.
      3. Tokenize with spacy.
      4. Remove stopwords with spacy.
      5. Remove tokens with len <= 2.
      6. Apply lemmatization to words using spacy.
    """
    text = text.lower()
    text = re.sub('[' + string.punctuation + '0-9\\r\\t\\n]', ' ', text)
    text =" ".join(text.split()) #remove tabs, multiple spaces
    doc = nlp(text)
    l = []
    for token in doc:
        if token.is_stop or len(token)<3:
            continue
        token = token.lemma_
        l.append(token)
    return l

def doc_freq(tok_corpus):
    """
    Returns a dictionary of the number of docs in which a word occurs.
    Input:
       tok_corpus: list of list of words
    Output:
       df: dictionary df[w] = # of docs containing w 
    """
    # your code here
    df={}
    for words in tok_corpus:
        for word in set(words):
            df[word]=df.get(word,0)+1
    return df
        

def compute_tfidf_i(tok_doc: list, doc_freq: dict, N: int) -> dict:
    """ Returns a dictionary of tfidf for one document
        tf[w, doc] = counts[w, doc]/ len(doc)
        idf[w] = np.log(N/(doc_freq[w] + 1))
        tfidf[w, doc] = tf[w, doc]*idf[w]
    """
    # your code here
    tfidf = {}
    for w in tok_doc:
        tfidf[w] = tfidf.get(w,0)+1/len(tok_doc)
        
    for w in tfidf:
        idf=np.log(N/(doc_freq[w] + 1))
        tfidf[w] *= idf
    return tfidf

def compute_tfidf(tok_corpus:list, doc_freq: dict) -> dict:
    """Computes tfidf for a corpus of tokenized text.

    Input:
       tok_corpus: list of tokenized text
       doc_freq: dictionary of word to set of doc indeces
    Output:
       tfidf: list of dict 
               tfidf[i] is the dictionary of tfidf of word in doc i.
    """
    # your code here
    N = len(tok_corpus)
    return [compute_tfidf_i(tok_doc, doc_freq, N) for tok_doc in tok_corpus]

def summarize(xmlfile, doc_freq, N,  n:int) -> list:
    """
    Given xml file, n and the tfidf dictionary 
    return up to n (word,score) pairs in a list. Discard any terms with
    scores < 0.01. Sort the (word,score) pairs by TFIDF score in reverse order.
    if words have the same score, they should be sorted in alphabet order.
    """
    # your code here
    nlp = spacy.load("en_core_web_sm")
    tfidf = compute_tfidf_i(tokenize(gettext(xmlfile),nlp),doc_freq, N)
    top_n = sorted([(k,v) for k,v in tfidf.items() if v>=0.01],
                   key=lambda x: (-x[1], x[0]))[:n]
    return top_n

    
