from . import chrome_version
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



class Browser:
    def __init__(self, initialize = True):
        if initialize:
            chrome_version.init()
        self.driver = webdriver.Chrome("drivers/chromedriver")