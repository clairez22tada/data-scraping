import sys
from mycsv import *

headers, data = readcsv(getdata())

def csv2xml(headers,data):
    xml_output = '''<?xml version="1.0"?><file><headers>'''
    
    xml_output+=','.join(headers)
    xml_output+='</headers>\n<data>\n'
    
    for row in data:
        xml_output+='<record>'
        for i in range(len(headers)):
            h = headers[i].replace(' ', '_')
            xml_output+=f'<{h}>'+ row[i]+f'</{h}>'
        xml_output+='</record>\n'
    
    xml_output+='</data>\n</file>'
    print(xml_output)

csv2xml(headers,data)
