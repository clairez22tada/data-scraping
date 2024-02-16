import sys
from mycsv import *

headers, data = readcsv(getdata())

def csv2html(headers, data):
    html_output = """<html>\n<body>\n<table>\n<tr>"""

    for header in headers:
        html_output += f"<th>{header}</th>"
    html_output += "</tr>\n"

    for row in data:
        html_output += "<tr>"
        for item in row:
            html_output += f"<td>{item}</td>"
        html_output += "</tr>\n"

    html_output += """</table>\n</body>\n</html>"""

    print(html_output)

csv2html(headers,data)
