import json
import xmltodict
import requests
from .. import tools

settings = None
npaper   = None

class FoxNews:
    def __init__(self):
        self.name = "fox_news"
        self.rss_feeds = [
            {'name/category': 'recent', 'url': 'https://moxie.foxnews.com/google-publisher/latest.xml'},
             {'name/category': 'World', 'url': 'https://moxie.foxnews.com/google-publisher/world.xml'},
             {'name/category': 'US', 'url': 'https://moxie.foxnews.com/google-publisher/us.xml'},
              {'name/category': 'Politics', 'url': 'https://moxie.foxnews.com/google-publisher/politics.xml'},
               {'name/category': 'Science', 'url': 'https://moxie.foxnews.com/google-publisher/science.xml'},
                {'name/category': 'Health', 'url': 'https://moxie.foxnews.com/google-publisher/health.xml'},
                 {'name/category': 'Sports', 'url': 'https://moxie.foxnews.com/google-publisher/sports.xml'},
                  {'name/category': 'Travel', 'url': 'https://moxie.foxnews.com/google-publisher/travel.xml'},
                   {'name/category': 'Tech', 'url': 'https://moxie.foxnews.com/google-publisher/tech.xml'},
                    {'name/category': 'OPINION', 'url': 'https://moxie.foxnews.com/google-publisher/opinion.xml'}
        ]

        self.article_feed = []

    def export_serialized_feed(self):
        global settings
        if settings.get('indent_exports'):
            _w = open("articles/"+self.name+".json","w")
            _w.write(json.dumps(self.article_feed, indent=4))
            _w.close()
            return

        _w = open("articles/"+self.name+".json","w")
        _w.write(json.dumps(self.article_feed))
        _w.close()

    def get_news(self):
        
        global settings
        
        for feed in self.rss_feeds:
            if feed.get('name/category').lower() not in settings['news']['ignored_categories']:
                self.article_feed += self.fetch_feed(feed.get('url'))

    def fetch_feed(self, link):
        feed_resp = xmltodict.parse(requests.get(link).text).get('rss').get('channel').get('item')
        items = []
        for article in feed_resp:

            article_obj = {
                "title": article.get('title'),
                "description": article.get('description'),
                "content": npaper.fetch(article.get('guid').get('#text')),#tools.strip_tags(article.get('content:encoded')),
                "link": article.get('guid').get('#text'),
                "publish_date": article.get('pubDate'),
                "entities": []
            }
            keep_article = True

            for category in article.get('category'):
                if category.get('@domain').count('dc.source') > 0:
                    if category.get('#text').count('Fox News') == 0:
                        keep_article = False

                if category.get('@domain').count('taxonomy') > 0:
                    if category.get('#text').count('/') > 0:
                        subcategories = category.get('#text').split("/")
                        for subcategory in subcategories:
                            if article_obj['entities'].count(subcategory) == 0:
                                article_obj['entities'].append(subcategory)
            if keep_article:
                items.append(article_obj)
        return items

class CNN:
    def __init__(self):
        self.name = "cnn"
        self.rss_feeds = [
                {"name/category":"topstories", "url":"http://rss.cnn.com/rss/cnn_topstories.rss"},
                {"name/category":"World", "url":"http://rss.cnn.com/rss/cnn_world.rss"},
                {"name/category":"us", "url":"http://rss.cnn.com/rss/cnn_us.rss"},
                {"name/category":"Business", "url":"http://rss.cnn.com/rss/money_latest.rss"},
                {"name/category":"Politics", "url":"http://rss.cnn.com/rss/cnn_allpolitics.rss"},
                {"name/category":"tech", "url":"http://rss.cnn.com/rss/cnn_tech.rss"},
                {"name/category":"Health", "url":"http://rss.cnn.com/rss/cnn_health.rss"},
                {"name/category":"Entertainment", "url":"http://rss.cnn.com/rss/cnn_showbiz.rss"},
                {"name/category":"Travel", "url":"http://rss.cnn.com/rss/cnn_travel.rss"},
                {"name/category":"recent", "url":"http://rss.cnn.com/rss/cnn_latest.rss"},
            ]
        self.article_feed = []

    def export_serialized_feed(self):
        global settings
        if settings.get('indent_exports'):
            _w = open("articles/"+self.name+".json","w")
            _w.write(json.dumps(self.article_feed, indent=4))
            _w.close()
            return

        _w = open("articles/"+self.name+".json","w")
        _w.write(json.dumps(self.article_feed))
        _w.close()

    def get_news(self):
        global settings
        
        for feed in self.rss_feeds:
            if feed.get('name/category').lower() not in settings['news']['ignored_categories']:
                self.article_feed += self.fetch_feed(feed.get('url'))



    def fetch_feed(self, link):
        feed_resp = xmltodict.parse(requests.get(link).text).get('rss').get('channel').get('item')
        f = open('test.json',"w")
        f.write(json.dumps(feed_resp, indent=4))
        f.close()
        items = []
        for article in feed_resp:

            article_obj = {
                "title": article.get('title'),
                "description": article.get('description'),
                "content": npaper.fetch(article.get('link')),
                "link": article.get('link'),
                "publish_date": article.get('pubDate'),
                "entities": []
            }
            keep_article = True

            for category in article.get('category'):
                if category.get('@domain').count('dc.source') > 0:
                    if category.get('#text').count('Fox News') == 0:
                        keep_article = False

                if category.get('@domain').count('taxonomy') > 0:
                    if category.get('#text').count('/') > 0:
                        subcategories = category.get('#text').split("/")
                        for subcategory in subcategories:
                            if article_obj['entities'].count(subcategory) == 0:
                                article_obj['entities'].append(subcategory)
            if keep_article:
                items.append(article_obj)
        return items

sources = [
        FoxNews(),
        CNN()
    ]

