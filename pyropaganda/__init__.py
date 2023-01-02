from . import config
from .browser import Browser
from . import news
from .telegram import Telegram
from.translate import Translate
print("Loading/Initializing:")

settings        = config.load_settings()               ; print(config.hcolors.OKBLUE+"\tSettings loaded")
browser         = Browser(settings.get('browser'))     ; print(config.hcolors.OKBLUE+"\tBrowser loaded")
telegram_client = Telegram(settings.get('telegram'))   ; telegram_client.print_status()
translate_client = Translate()
news_client     = news.init(settings)                  ; print(config.hcolors.OKBLUE+"\tNews loaded")

    


