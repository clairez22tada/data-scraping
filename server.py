# Launch with
#
# python app.py

from flask import Flask, render_template
import sys
import pickle

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    ## YOUR CODE HERE
    return render_template("articles.html", articles=articles)

@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filenzxt so our URLs follow that.
    """
    ## YOUR CODE HERE
    article = [a for a in articles if a[0]==topic and a[1]==filename]
    text_list = article[0][3].split("\n")
    recs = recommended[(topic, filename)]
    return render_template("article.html", title=article[0][2], paragraphs = text_list, recs=recs)


f = open('articles.pkl', 'rb')
articles = pickle.load(f)
f.close()

f = open('recommended.pkl', 'rb')
recommended = pickle.load(f)
f.close()

# you may need more code here or not


# for local debug
if __name__ == '__main__':
    app.run(debug=True)

