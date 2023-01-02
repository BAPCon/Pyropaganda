import pyropaganda
import xmltodict
import requests
import newspaper
import json
import nltk
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
from spacy import tokenizer
nlp = spacy.load('en_core_web_sm')
 

feeds = ['https://www.rt.com/rss/russia/',
            'https://www.rt.com/rss/news/'
        ]
articles = []

for feed in feeds:
    for article in xmltodict.parse(requests.get(feed).text).get('rss').get('channel').get('item'):
        
        articlenp = newspaper.Article(article.get('link'))
        articlenp.download()
        articlenp.parse()
        text = articlenp.text
        doc = nlp(text)
        sentences = list(doc.sents)
        ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
        
        articles.append({
            'title': article.get('title'),
            'link': article.get('link'),
            'keywords': ents
        })

        f = open('ukraine_articles.json',"w")
        f.write(json.dumps(articles, indent=4))
        f.close()


        




    

