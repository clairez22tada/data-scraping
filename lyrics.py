import sys
from bs4 import BeautifulSoup
import requests
import argparse
import numpy as np
import re


def get_content_soup_from_url(url):
    result = requests.get(url)
    content = result.text
    return BeautifulSoup(content, "lxml")


def clean_text(text):
    """Given a string of text return clean text
    Clean issues with text
    "1. Hola" --> "Hola" 
    "Hola." --> "Hola" 
    "Hola (L)" --> "Hola"
    "Hola (1790)"  --> "Hola"
    "Hola 1790"  --> "Hola"
    """
    # your coode here
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"[0-9]", "", text)
    text = text.replace(".", "")
    return text.strip()



def process_row(row):
    """ Inputs a row of a table and returns the song, album and url

    The input should follow this format:
        <tr valign="bottom">
        <td align="left">
        Ain't No Cure For Love </td>
        <td align="left">
        <a href="album9.html" style="text-decoration:none">I'm Your Man (L)</a> </td>
        </tr>
    Ouputs: three strings, as shown in the example
        "Ain't No Cure For Love", "I'm Your Man", "album9.html"

    To ensure cleanliness and avoid duplicates, the following actions are performed:
      -- remove "(L)"
      -- remove years
    from album names and song names
    """
    # your code here
    song = clean_text(row.find('td').text)
    album = clean_text(row.a.text)
    url = row.a["href"]
    return song, album, url


def get_albums():
    """ Scrape album names from 
    "https://www.leonardcohenfiles.com/songind.html"

    Return a list of unique names in alfabetical order
    To ensure cleanliness and avoid duplicates, the following actions are performed:
      -- remove "(L)"
      -- remove years
    """
     # your coode here
    url="https://www.leonardcohenfiles.com/songind.html"
    list_albums = []
    soup = get_content_soup_from_url(url)
    rows = soup.table.table.find_all("tr")
    for row in rows:
        album = process_row(row)[1]
        if album not in list_albums:
            list_albums.append(album)
    list_albums.sort()
    return list_albums


def get_songs():
    """ Scrape song urls from
    "https://www.leonardcohenfiles.com/songind.html"

    Return a list of unique names in alfabetical order
    Some cleaning to avoid duplicates:
      -- remove "(L)"
    """
     # your coode here
    url="https://www.leonardcohenfiles.com/songind.html"
    list_songs = []
    soup = get_content_soup_from_url(url)
    rows = soup.table.table.find_all("tr")
    for row in rows:
        song = process_row(row)[0]
        if song not in list_songs:
            list_songs.append(song)
    list_songs.sort()
    return list_songs

def get_lyric_url(): #get the urls for lyrics
    url="https://www.leonardcohenfiles.com/songind.html"
    list_url = []
    soup = get_content_soup_from_url(url)
    rows = soup.table.table.find_all("tr")
    for row in rows:
        u = process_row(row)[2]
        if u not in list_url:
            list_url.append("https://www.leonardcohenfiles.com/"+u)
    list_url.sort()
    return list_url
    
def scrape_lyrics_from_url(song, url):
    """ Given a song and a url return the lyric of the song
    
    Inputs:
       song: string example: "Bird on the Wire"
       url: 'https://www.leonardcohenfiles.com/album2.html'
    
    Return the text of the lyrics:
    
    Like a bird on the wire,
    like a drunk in a midnight choir
    I have tried in my way to be free.
    Like a worm on a hook, 
    ...
    
    """
     # your coode here
    result = requests.get(url)
    content = result.text
    soup=BeautifulSoup(content, "lxml")
    s = clean_text(song)
    lyric_dict={}
    for title in soup.find_all("h2"):
        try:
            lyric_dict[clean_text(title.text)]=clean_text(title.find_next("blockquote").text)
        except:
            pass
    if s in lyric_dict:
        return lyric_dict[s]
    else:
        return None


def get_lyrics(s):
    """ Given an input song scrape and return the lyric
    """
     # your coode here
    lyrics=None
    album_list=get_albums()
    songs_list=get_songs()
    url_list=get_lyric_url()
    s = clean_text(s)
    if s not in songs_list:
        return None
    for u in url_list:
        lyrics = scrape_lyrics_from_url(s, u)
        if lyrics is not None:
            return lyrics
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Generates a list of songs", action='store_true')
    parser.add_argument("-a", help="Generates a list of albums", action='store_true')
    parser.add_argument("-l", help="Print lyrics for a given song", type=str)
    args = parser.parse_args()
    if args.s:
        songs = get_songs()
        for song in songs:
            print(song)
    if args.a:
        albums = get_albums()
        for a in albums:
            print(a)
    if args.l:
        lyric = get_lyrics(args.l)
        if lyric is None:
            print("No lyric was found")
        else:
            print(lyric)
