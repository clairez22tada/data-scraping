import sys

def getdata():
    if len(sys.argv)==1: # if no file given, read from stdin
        data = sys.stdin.read()
    else:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
    return data.strip()

def readcsv(data):
    """
    Read CSV with header from data string and return a header list
    containing a list of names and also return the list of lists
    containing the data.
    """
    lines = data.split('\n')
    headers = lines[0].split(',')
    data = []
  
    for line in lines[1:]:
        data_row = line.split(',')
        data.append(data_row)

    return headers, data
    
