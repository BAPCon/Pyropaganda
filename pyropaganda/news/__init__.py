from . import domestic
from . import npaper
import os

publishers = []

def init(settings):
    global publishers
    domestic.settings = settings
    domestic.npaper   = npaper
    publishers += domestic.sources
    if "articles" not in os.listdir():
        os.mkdir("articles")