import newspaper


def fetch(link):
    article = newspaper.Article(link)
    article.download()
    article.parse()
    article_data = get_article_data(article)

def get_article_data(article):

    data = {
        "authors": article.authors,
        "text": article.text,
        "publish_date": article.publish_date
    }

    article.nlp()


bbc = newspaper.build('https://www.europarl.europa.eu/news/en', language='en')

for category in bbc.category_urls():
    print(category)

print("--------------------")

print(len(bbc.articles))
