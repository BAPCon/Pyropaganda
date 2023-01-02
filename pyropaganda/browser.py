from . import chrome_version
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



class Browser:
    def __init__(self, settings):
        self.settings_dict = settings
        if settings.get('check_drivers'):
            chrome_version.init()
        if settings.get('start_immediately'):
            self.start()
    def start(self):
        self.driver = webdriver.Chrome("drivers/chromedriver")