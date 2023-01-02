from .browser import Browser
from . import config
from . import news

settings = config.load_settings()
#browser = Browser()

news.init(settings)
    


