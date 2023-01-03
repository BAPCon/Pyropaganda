from . import config
from .browser import Browser
from . import news
from .telegram import Telegram
from.translate import Translate
import xmltodict
import requests
import newspaper
import json
import nltk
from bs4 import BeautifulSoup
import spacy
import random
import os
from spacy import displacy
from spacy import tokenizer
from operator import itemgetter
from datetime import datetime
import time

        




    


print("Loading/Initializing:")

settings        = config.load_settings()               ; print(config.hcolors.OKBLUE+"\tSettings loaded")
browser         = Browser(settings.get('browser'))     ; print(config.hcolors.OKBLUE+"\tBrowser loaded")
#telegram_client = Telegram(settings.get('telegram'))   ; telegram_client.print_status()
#translate_client = Translate()
#news_client     = news.init(settings)                  ; print(config.hcolors.OKBLUE+"\tNews loaded")
#nlp             = spacy.load('en_core_web_sm')
    

already_processed = None
detected_entities = []
target_feeds = None

cluster_threshold = settings.get('news').get('feeds').get('cluster_threshold')
max_article_per_feed = settings.get('news').get('feeds').get('per_feed')
summary_nlp = settings.get('news').get('feeds').get('use_summary')

save_frequency = settings.get('news').get('feeds').get('save_frequency_minutes') * 60
last_save = datetime.now()


def get_feed(url):
    global already_processed
    global max_article_per_feed
    global nlp
    __articles = []
    try:
        try:
            xml = xmltodict.parse(requests.get(url, timeout=6).text).get('rss').get('channel').get('item')
        except:
            return __articles
        for article in xml:
            if article.get('link') not in already_processed:
                already_processed.append(article.get('link'))
                articlenp = newspaper.Article(article.get('link'))
                articlenp.download()
                articlenp.parse()
                text = articlenp.text
                if summary_nlp:
                    articlenp.nlp()
                    doc = nlp(articlenp.summary)
                else:
                    doc = nlp(text)
                ents = []
                for e in doc.ents:
                    if e.label_ not in ['DATE', 'CARDINAL']:
                        ents.append({
                            'text': e.text,
                            'label': e.label_
                        })
                __articles.append({
                    'entities': ents,
                    'entity_count': len(ents),
                    'summary': articlenp.summary,
                    'text': articlenp.text,
                    'title': articlenp.title,
                    'authors': articlenp.authors,
                    'link': article.get('link'),
                    'alive': True,
                    'clustered': []
                })
                if len(__articles) >= max_article_per_feed:
                    return __articles
    except: pass
    return __articles

def check_feeds():
    global target_feeds
    global detected_entities
    global cluster_threshold
    global already_processed
    global save_frequency
    global last_save

    if already_processed == None:
        if 'processed_links_pp.csv' not in os.listdir():
            f = open('processed_links_pp.csv',"x")
            already_processed = []
        else:
            already_processed = open('processed_links_pp.csv',"r").read().split('\n')

    if target_feeds == None:
        target_feeds = []
        rss_feeds = json.loads(open('pyropaganda/datasets/rss_feeds_all.json','r').read())
        for country in rss_feeds:
            target_feeds += rss_feeds[country].get('news')
        while len(target_feeds) > settings.get('news').get('feeds').get('random_selection_size'):
            target_feeds.pop(random.randint(0, len(target_feeds)-1))

    __responses = []
    __clusters  = []
    __i = 0

    for feed in target_feeds:
        print(__i, "/", len(target_feeds))
        print('\t', len(__responses))
        __i += 1
        __responses += get_feed(feed)
    
    __responses = sorted(__responses, key=itemgetter('entity_count'), reverse=True)

    for response in __responses:
        for ent in response.get('entities'):
            exists = False
            for existing_ent in detected_entities:
                if existing_ent.get('text') == ent.get('text'):
                    existing_ent['count'] += 1
                    exists = True
                    break
            if not exists:
                detected_entities.append({
                    'count': 1,
                    'text': ent.get('text'),
                    'label': ent.get('label')
                })
    clustered_fail_point = 3
    clustered_count = 0
    while clustered_fail_point > 0:
        __clustered = False
        for a_index in range(0, len(__responses)):
            if __responses[a_index].get('alive'):
                for b_index in range(a_index+1, len(__responses)):
                    try:
                        if __responses[b_index].get('alive'):
                            common_entities = 0
                            for ent in __responses[b_index].get('entities'):
                                if ent in __responses[a_index]['entities']:
                                    common_entities += 1
                            if common_entities / len(__responses[b_index].get('entities')) >= cluster_threshold:
                                __responses[b_index]['alive'] = False
                                __responses[a_index]['clustered'].append(__responses[b_index])
                                __clustered = True
                                clustered_count += 1
                    except: pass
        if not __clustered:
            clustered_fail_point -= 1

    print(clustered_count, " were clustered")

    _ap = []
    for link in already_processed:
        if isinstance(link, str):
            _ap.append(link)

    _proc = open('processed_links_pp.csv',"w")
    _proc.write("\n".join(_ap))
    _proc.close()

    
    

    if (datetime.now() - last_save).total_seconds() >= save_frequency:
        _proc = open('processed_articles.json',"w")
        _proc.write(json.dumps(__responses, indent=4))
        _proc.close()
        last_save = datetime.now()

        



                

    
    
