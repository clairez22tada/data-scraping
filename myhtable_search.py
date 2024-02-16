# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    table = htable(4011)
    for i in range(len(files)):
        s = get_text(files[i])
        for w in words(s):
            if htable_get(table, w) is None:
                htable_put(table, w, set([i]))
            else:
                htable_get(table, w).add(i)
    return table 
    

def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    results = []
    for i in range(len(files)): 
        result = True
        for t in terms:
            if htable_get(index, t) is None:
                result = False
                break
            elif i not in htable_get(index, t):
                result = False
                break
        if result == True: 
            results.append(files[i])
    return results
