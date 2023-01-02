from bs4 import BeautifulSoup
import xmltodict
from googletrans import Translator, constants
import newspaper


translator = Translator()

def fetch_translate_article(url):
    global translator
    article = newspaper.Article(url)
    article.download()
    article.parse()
    translation = translator.translate(article.text)
    return translation.text

def get_rss_html(terms_in_links, file_path):
    rss_dirs = open(file_path,"r").read()
    feeds = []
    soup = BeautifulSoup(rss_dirs, 'html.parser')
    for link in soup.find_all('a'):
        h = False
        for term in terms_in_links:
            if link.get('href') != None:
                h = h or link['href'].lower().count(term) > 0
        if h:
            feeds.append('http'+link['href'].split('http')[1].replace('\\','').replace('\"',''))
    return [*set(feeds)]




countries = {
    "iran": {
        'news': ['https://iranpress.com/RSS|https://iranpress.com','https://en.mehrnews.com/rss-help|https://en.mehrnews.com',
        'https://www.tehrantimes.com/rss|https://www.tehrantimes.com/rss-homepage|https://www.tehrantimes.com/rss?pl=617|https://www.tehrantimes.com/rss/tp/696|https://www.tehrantimes.com/rss/tp/697|https://www.tehrantimes.com/rss/tp/698|https://www.tehrantimes.com/rss/tp/699|https://www.tehrantimes.com/rss/tp/700|https://www.tehrantimes.com/rss/tp/701|https://www.tehrantimes.com/rss/tp/702|https://www.tehrantimes.com/rss/tp/717||https://www.tehrantimes.com'],
        "nonenglish": [
            {
                "link": "https://www.entekhab.ir/fa/rss/allnews",
                "language": "fa"
            }
        ]
    },
    "russia": {
        'news': [
            'http://tass.com/rss/v2.xml',
            'https://www.rt.com/rss/',
            'https://www.rt.com/rss/russia/',
            'https://www.rt.com/rss/news/',
            'https://www.rt.com/rss/op-ed/',
            'https://www.rt.com/rss-feed/',
            'https://sputniknews.com/export/rss2/archive/index.xml'
        ],
        "nonenglish": [
            {
                "link": "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",
                "language": "ru"
            },
            {
                "link": "https://lenta.ru/rss",
                "language": "ru"
            },
            {
                "link": "https://ria.ru/export/rss2/archive/index.xml",
                "language": "ru"
            },
            {
                "link": "https://news.rambler.ru/rss/world/",
                "language": "ru"
            },
            {
                "link": "https://news.rambler.ru/rss/moscow_city/",
                "language": "ru"
            },
            {
                "link": "https://news.rambler.ru/rss/politics/",
                "language": "ru"
            },
            {
                "link": "https://news.rambler.ru/rss/army/",
                "language": "ru"
            },
            {
                "link": "https://news.rambler.ru/rss/articles/",
                "language": "ru"
            },
            {
                "link": "https://news.rambler.ru/rss/community/",
                "language": "ru"
            },
            {
                "link": "https://news.rambler.ru/rss/politics/",
                "language": "ru"
            },
            {
                "link": "https://tass.ru/rss/v2.xml",
                "language": "ru"
            },
            {
                "link": "https://russian.rt.com/rss",
                "language": "ru"
            }
        ]
    },
    "japan": {
        'news': ['https://newsonjapan.com/rss/top.xml','https://newsonjapan.com/html/newsdesk/Society_News/rss/index.xml','https://newsonjapan.com/html/newsdesk/Business_News/rss/index.xml','https://newsonjapan.com/html/newsdesk/Politics_News/rss/index.xml','https://newsonjapan.com/html/newsdesk/Technology_News/rss/index.xml',
            'https://www.japantimes.co.jp/feed',
            'https://japantoday.com/feed/atom',
            'https://english.kyodonews.net/rss/all.xml',
            'https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/topic/destination/japan/rss.xml',
            'https://japaninsides.com/category/news/feed/',
            'https://shingetsunewsagency.com/feed/',
            'https://japan.kantei.go.jp/index-e2.rdf'
        ],
        'nonenglish': [
            {
                'link': 'https://news.livedoor.com/topics/rss/top.xml',
                'language': 'ja'
            },
            {
                'link': 'https://news.livedoor.com/topics/rss/int.xml',
                'language': 'ja'
            },
            {
                'link': 'https://news.livedoor.com/topics/rss/eco.xml',
                'language': 'ja'
            },
            {
                'link': 'https://asia.nikkei.com/rss/feed/nar',
                'language': 'ja'
            },
            {
                'link': 'https://www.nhk.or.jp/rss/news/cat0.xml',
                'language': 'ja'
            },
            {
                'link': 'https://www.nhk.or.jp/rss/news/cat1.xml',
                'language': 'ja'
            },
            {
                'link': 'https://www.nhk.or.jp/rss/news/cat3.xml',
                'language': 'ja'
            },
            {
                'link': 'https://www.nhk.or.jp/rss/news/cat4.xml',
                'language': 'ja'
            },
            {
                'link': 'https://www.nhk.or.jp/rss/news/cat5.xml',
                'language': 'ja'
            },
            {
                'link': 'https://www.nhk.or.jp/rss/news/cat6.xml',
                'language': 'ja'
            },
            {
                'link': 'http://rss.asahi.com/rss/asahi/newsheadlines.rdf',
                'language':'ja'
            },
            {
                'link': '',
                'language':'ja'
            },
            {
                'link': '',
                'language':'ja'
            }
        ]
    },
    "un": {
        'news': [
            'https://news.un.org/feed/subscribe/en/news/all/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/health/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/un-affairs/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/law-and-crime-prevention/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/human-rights/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/humanitarian-aid/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/culture-and-education/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/economic-development/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/women/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml',
            'https://news.un.org/feed/subscribe/en/news/topic/migrants-and-refugees/feed/rss.xml',
            ''
        ],
        'nonenglish': []
    },
    "europe": {
        "news": [
            'https://feeds.feedburner.com/euronews/en/home/',
            'https://www.politico.eu/feed/',
            'https://en.trend.az/feeds/index.rss',
            'https://www.eureporter.co/feed/',
            'https://xml.euobserver.com/rss.xml',
            'https://feeds.thelocal.com/rss/es',
            'https://www.neweurope.eu/feed/',
            'https://www.rferl.org/z/645/rss/feeds/posts/default',
            'https://www.rferl.org/api/zbgvmtet_tmt',
            'https://news.un.org/feed/subscribe/en/news/region/europe/feed/rss.xml',
            'https://feeds.feedburner.com/TheBalticTimesNews',
            'https://www.europeantimes.news/feed/',
            'https://brusselsmorning.com/feed',
            'https://www.brusselstimes.com/feed'
        ],
        "nonenglish": []
    },
    "china": {
        'news': ['https://technode.com/feed/','http://feeds.bbci.co.uk/news/world/asia/china/rss.xml','https://thediplomat.com/category/china-power/feed/',
            'https://www.theguardian.com/world/china/rss',
            'https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/topic/destination/china/rss.xml',
            'https://china-environment-news.net/feed/',
            'http://china.timesofnews.com/feed',
            'https://chinaglobalsouth.com/feed/',
            'http://www.chinadaily.com.cn/rss/bizchina_rss.xml',
            '',
        ],
        'nonenglish': [
            {
                "link": "",
                "language": "cn"
            }
        ]
    }

}    

countries['russia']['nonenglish'].append({'link':get_rss_html(
    ["news.rambler.ru/rss"],
    'rss_html/Russia.mhtml'
),'language':'ru'})


#fw = open('test.txt','w')
#fw.write(json.dumps(xmltodict.parse(requests.get('https://www.europarl.europa.eu/rss/doc/top-stories/en.xml').text), indent=4))
