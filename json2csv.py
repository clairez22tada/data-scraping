import sys
import json
import csv

def json2csv():
    with open(sys.argv[1]) as f:
        d=json.load(f)
    csv_output = ""
    csv_output += ",".join(d["headers"])+"\n"
    for row in d["data"]:
        csv_output += ",".join(row.values())+"\n"
    csv_output=csv_output.rstrip()
    print(csv_output)

json2csv()
