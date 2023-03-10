import newspaper
import os

publishers = []
class News:
    def __init__(self) -> None:
        pass

    def fetch(self, link):
        article = newspaper.Article(link)
        article.download()
        article.parse()
        article_data = self.get_article_data(article)

    def get_article_data(self, article):

        data = {
            "authors": article.authors,
            "text": article.text,
            "publish_date": article.publish_date
        }

        article.nlp()

def init(settings):
    global publishers
    if "articles" not in os.listdir():
        os.mkdir("articles")
    return News()

