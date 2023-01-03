import pyropaganda
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#pyropaganda.check_feeds()
import pyautogui
import requests
from bs4 import BeautifulSoup
import random
import time
import threading
from pynput.mouse import Listener


on_move_exec = ""
on_click_exec = """def on_move(x, y):
    global on_move_exec
    exec(on_move_exec)

def on_click(x, y, button, pressed):
    #print(x, y, button, pressed)
    global on_click_exec
    exec(on_click_exec)


def on_scroll(x, y, dx, dy):
    pass

def run_mouse():
    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()


t = threading.Thread(target=run_mouse)
t.start()"""


t = threading.Thread(target=pyropaganda.browser.organic_move_loop)
t.start()




pyropaganda.browser.start()

pyropaganda.browser.maximize_window()
print('loading!')
#pyropaganda.browser.login_youtube()
pyropaganda.browser.opensite('https://www.youtube.com/watch?v=KhJzEEBqBq4')
try:
    video = pyropaganda.browser.build_video()
except Exception as e:
    print(e)
print('Done loading!')
exec(open('run.txt','r').read())
while True:
    print('runnning loop!')
    try:
        res = input('Enter command:/n')
        exec(exec(open('run.txt','r').read()))
    except:
        pass