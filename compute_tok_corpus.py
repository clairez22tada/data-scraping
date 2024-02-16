from tfidf import *
import os
import pickle

"""
1. Get a list of all xml_files in the corpus (~/data/reuters-vol1-disk1-subset).
2. Get a list of texts for all files xml_files.
3. Get a list of tokenized text (list of list of tokens).
4. Save the tokenized corpus in ~/data/tok_corpus.pickle.
"""
directory = sys.argv[1]
pickle_file = os.path.expanduser("~/data/tok_corpus.pickle")
# your code here
nlp = spacy.load("en_core_web_sm")
file_paths = [os.path.join(directory, file) for file in os.listdir(directory)]
text_corpus = [gettext(f) for f in file_paths]
tok_corpus=[]
c=0
for text in text_corpus:
    tok_corpus.append(tokenize(text, nlp))
    c+=1
    if c%100==0:
        print(c)
with open(pickle_file, 'wb') as f:
    pickle.dump(tok_corpus, f)