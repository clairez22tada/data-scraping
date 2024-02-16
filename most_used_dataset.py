import sys
from bs4 import BeautifulSoup
import requests


# feel free to define other functions


def get_one_page(url):
    result = requests.get(url)
    content = result.text
    soup = BeautifulSoup(content, "lxml")
    heading = soup.find_all('h3', class_="dataset-heading")
    output = []
    for i in heading:
        u="https://catalog.data.gov"+i.a["href"]
        t=i.text.split("\n\n")[0].strip()
        pair=(t, u)
        output.append(pair)
    return output

def list_of_pairs(n):
    """ Get first n datasets

    Output: list of (dataset title, url)
    """
    ### Your coode here
    
    output = []
    num_pages = n//20+1
    for p in range(1,num_pages+1):
        url='https://catalog.data.gov/dataset?q=&sort=views_recent+desc&page='+str(p)
        output = output+get_one_page(url)
    return output[:n]

if __name__ == "__main__":
    n = int(sys.argv[1])
    pairs = list_of_pairs(n)
    for title, url in pairs:
        print(title, url)


