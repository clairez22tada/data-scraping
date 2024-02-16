import sys
import csv
import json
from mycsv import *

def csv2json():
    headers, data = readcsv(getdata())
    d = {"headers": headers}
    data_list=[]
    for row in data:
        row_d = {}
        for i in range(len(headers)):
            row_d[headers[i]] = row[i]
        data_list.append(row_d)

    d["data"]=data_list
    json_output=json.dumps(d)
    print(json_output)

csv2json()