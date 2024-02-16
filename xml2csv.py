import sys
import untangle
import xmltodict
import csv

def xml2csv():
    with open(sys.argv[1]) as f:
        s = f.read()
    d = xmltodict.parse(s)
    csv_output=d['file']['headers']
    for row in d['file']['data']['record']:
        csv_output+='\n'+','.join(row.values())
    print(csv_output)

xml2csv()
