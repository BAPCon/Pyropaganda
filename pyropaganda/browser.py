from . import chrome_version
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver.v2 as uc
from win32.win32gui import GetWindowText, GetForegroundWindow
import win32com.client as comctl
import math
import random
import json
from datetime import datetime
import pyautogui
import time
from ctypes import windll
from win32 import win32gui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Browser:
    def __init__(self, settings):

        self.settings_dict = settings
        self.idle_movements = False
        self.avg_ms_delay = settings.get('avg_ms_delay')
        self.max_ms_delay = settings.get('max_ms_delay')
        self.mouse_status = [datetime.now(), True]
        self.organic_movements = [0, 0, json.loads(open('organic_movements.json','r').read())]

        if settings.get('check_drivers'):
            chrome_version.init()
        if settings.get('start_immediately'):
            self.start()
        self.wsh = None

        self.youtube_account = settings.get('youtube_account')


    def delay(self, use_average=False, sleep=True):
        if use_average:
            v = random.randint(int(.85*self.avg_ms_delay), int(1.15*self.avg_ms_delay))/1000
        else:
            v = (random.randint(int(.2*self.avg_ms_delay), int(1.35*self.avg_ms_delay))
                +
                random.randint(0, self.max_ms_delay)
                )/2000
        if sleep:
            time.sleep(v)
        return v
        

    def medium_delay(self):
        self.delay();self.delay();self.delay();self.delay();self.delay();

    def long_delay(self):
        self.medium_delay()
        self.medium_delay()
        self.delay()
        self.delay()

    def start(self):
        options = Options()
        options.add_argument('--profile-directory=Default')
        options.headless = True

        options.add_argument('--user-data-dir=C:/Temp/ChromeProfile')
        #driver = webdriver.Chrome(chrome_options=options)
        
        self.driver = uc.Chrome()#chrome_options=options)
        self.driver.delete_all_cookies()
        
        self.wait = WebDriverWait(self.driver, 20)

    def organic_move_loop(self):
        while False:
            if self.mouse_status[1] and self.idle_movements:
                if (datetime.now()-self.mouse_status[0]).total_seconds() > 1.5:
                    pyautogui.moveRel(xOffset=self.organic_movements[2][self.organic_movements[0]][0], yOffset=self.organic_movements[2][self.organic_movements[0]][1], duration=random.randint(0,50)/5000)
                    self.organic_movements[0] += 1
                    self.organic_movements[1] += 1
                    if self.organic_movements[1] >= 50 or self.organic_movements[0] >= len(self.organic_movements[2]):
                        self.organic_movements[0] = random.randint(0, len(self.organic_movements[2])-1)
                        self.organic_movements[1] = 0
                        time.sleep((5+random.randint(1, 130))/2)

    def move_mouse(self, final_target, final_exact=False):
        self.mouse_status[1] = False
        self.mouse_status[0] = datetime.now()
        run_time = 1
        _pos = [pyautogui.position().x, pyautogui.position().y]
        move_points = []
        i = 0
        try:
            _breakpoint = 0

            while _pos != final_target:
                _distance = math.sqrt(pow(final_target[0] - _pos[0], 2) + pow(final_target[1] - _pos[1], 2))*.1
                
                
                weight = random.randint(1, 5)


                __x = (_pos[0]*weight +final_target[0])/(weight+1) + (random.randint(0, int(_distance)*2) - int(_distance))
                __y = (_pos[1]*weight +final_target[1])/(weight+1) + (random.randint(0, int(_distance)*2) - int(_distance))
                if _distance <= 1:
                    move_points.append([final_target[0], final_target[1], min(_distance,20)/20])
                    _pos = final_target
                    break
                else:
                    move_points.append([(__x+final_target[0])/2, (__y+final_target[1])/2, min(_distance,20)/20])

                _pos = [move_points[-1][0], move_points[-1][1]]

                _breakpoint += 1
            npoints = []
            mpindex = 0
            total_time = 0
            #exec(open('run.txt','r').read())
            while mpindex < len(move_points)-1:
                offset= 0
                if mpindex < 5 and len(move_points)> 5:
                    offset =+random.randint(0,(10-mpindex)*2)-10-mpindex
                npoints.append([
                    (move_points[mpindex][0]+move_points[mpindex+1][0]+offset)/2,
                    (move_points[mpindex][1]+move_points[mpindex+1][1]+offset)/2,
                    (move_points[mpindex][2]+move_points[mpindex+1][2])/2
                ])
                total_time += (move_points[mpindex][2]+move_points[mpindex+1][2])/2
                mpindex += 2

            time_multipler = 1
            if total_time > run_time:
                mntime = (run_time+total_time+run_time)/3
                time_multipler = (mntime/total_time)
            start = datetime.now()
            for mp in npoints[:-2]:
                pyautogui.moveTo(mp[0], mp[1], (mp[2]/3)*time_multipler)
            pyautogui.moveTo(npoints[-2][0], npoints[-2][1], npoints[-2][2]/5)
            if final_exact:
                pyautogui.moveTo(final_target[0], final_target[1], npoints[-1][2]/7)
            else:
                pyautogui.moveTo(npoints[-1][0], npoints[-1][1], npoints[-1][2]/7)

            self.mouse_status[1] = True
            self.mouse_status[0] = datetime.now()
        except Exception as e:
            print(e)

    def maximize_window(self):
        self.set_visible()
        self.driver.maximize_window()

    def debug_exec(self, text):
        try:
            exec(text)
        except Exception as e:
            print(e)

    def key_series(self, key_list, release=True):
        """
        Procedurally calls key followed by delay.

        ------------------

        If release == True then each key called will be released in reverse order at end of each section.

            [
                ['ctrl', 'c'], #   KEYS RELEASED
                ['ctrl', 'v']  #   KEYS RELEASED AGAIN
            ]

        ------------------

        If key is up, and then called again it will be let go.

            ['ctrl', 's', 'ctrl', 's'] will press and then release ctrl+s

        ------------------
        """

        __aks = []
        if isinstance(key_list[0], str):
            key_list = [key_list]

        for item in key_list:

            for item_kp in item:

                if item_kp.count("delay|") > 0:
                    for i in range(0, int(item_kp.split('|')[1])):
                        self.delay()
                else:
                    self.delay()
                    if __aks.count(item_kp) > 0:
                        pyautogui.keyUp(item_kp)
                    else:
                        pyautogui.keyDown(item_kp)
                        __aks.append(item_kp)

            if release:
                for _ak in __aks:
                    self.delay()
                    pyautogui.keyUp(_ak)
    def type(self, text):
        """
        Procedurally calls key followed by delay.

        ------------------

        If release == True then each key called will be released in reverse order at end of each section.

            [
                ['ctrl', 'c'], #   KEYS RELEASED
                ['ctrl', 'v']  #   KEYS RELEASED AGAIN
            ]

        ------------------

        If key is up, and then called again it will be let go.

            ['ctrl', 's', 'ctrl', 's'] will press and then release ctrl+s

        ------------------
        """
        
        pyautogui.typewrite(text, interval=self.delay(sleep=False))


    def set_visible(self):
        pass

    def opensite(self, url):
        self.driver.get(url)
        
    def scroll_down(self):
        from selenium.webdriver.common.action_chains import ActionChains

        N = 25  # number of times you want to press TAB

        actions = ActionChains(self.driver) 
        for _ in range(N):
            actions = actions.send_keys(Keys.TAB)
        actions.perform()

        actions = ActionChains(self.driver) 
        for _ in range(3):
            actions = actions.send_keys(Keys.TAB)
        actions.perform()

        actions = ActionChains(self.driver) 
        for _ in range(2):
            actions = actions.send_keys(Keys.TAB)
        actions.perform()


    def login_youtube(self):
        self.set_visible()
        print('a')
        if self.driver.current_url.count('accounts.google.com/v3/signin') > 0:
            pass
        else:
            self.opensite('https://accounts.google.com/ServiceLogin?service=youtube')
        try:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'input[type=email]'))).click()
        except:
            pass
        email_input = self.driver.find_element(By.CSS_SELECTOR,'input[type=email]')
        print('b')
        for letter in self.youtube_account.get('email'):
            email_input.send_keys(letter)
            self.delay()
        print('c')
        # Click next
        self.medium_delay()
        self.set_visible()
        print('d')
        pyautogui.press('enter')
        self.medium_delay()
        time.sleep(6)
        print('e')
        # Type password
        password_input = self.driver.find_element(By.CSS_SELECTOR,'input[type=password]')
        for letter in self.youtube_account.get('password'):
            password_input.send_keys(letter)
            self.delay()
        print('f')
        pyautogui.press('enter')

        self.medium_delay()
        print('g')
        self.logged_in_youtube = True

    def move_mouse_range(self, coords):
        #[[654, 1112], [91, 108]]
        self.move_mouse([ random.randint(coords[0][0], coords[0][1]), random.randint(coords[1][0], coords[1][1]) ])

    def youtube_results(self, scrl=0):
        links = []
        while scrl > 0:
            ng = min(random.randint(10, 42) * -1, scrl)
            if ng > 0:
                ng = ng * -1
            pyautogui.scroll(ng)
            scrl += ng
            scrl -= 1
            if random.randint(0,5) == 0:
                elems = self.driver.find_elements(By.ID, "video-title")
                time.sleep(random.randint(.5,11))
        elems = self.driver.find_elements(By.ID, "video-title")
        for elem in elems:
            label = elem.get_attribute('aria-label')
            link = elem.get_attribute('href')
            if label != None and link != None:
                links.append({
                    'title': label,
                    'link': link,
                    "element": elem
                })
        return links
        

    def youtube_search(self, query, existing_results=False):
        self.set_visible()
        if not existing_results:
            self.opensite('https://www.youtube.com/results?search_query='+query)
        
        self.tmp_links = self.youtube_results()
        
        self.set_visible()
        self.tmp_links[0]['element'].click()
        self.medium_delay()
        time.sleep(14)
        self.youtube_close_ads()
        self.youtube_close_ads()
        #self.driver.find_element(By.ID, 'simplebox-placeholder').click()

    def close_ads(self):
        ad_close = self.driver.find_elements(By.CSS_SELECTOR,'button')
        for ac in ad_close:
            try:
                if ac.get_attribute('class').count('ytp-ad-skip-button') > 0:
                    ac.click()
            except: pass
    
        ad_close = self.driver.find_elements(By.CSS_SELECTOR,'button')
        for ac in ad_close:
            try:
                if ac.get_attribute('aria-label').count('Dismiss') > 0:
                    ac.click()
            except: pass
        ad_close = self.driver.find_elements(By.CSS_SELECTOR,'button')
        for ac in ad_close:
            try:
                if ac.get_attribute('class').count('ytp-ad-overlay-close-button') > 0:
                    ac.click()
            except: pass
            try:
                if ac.get_attribute('aria-label').count('Skip trial') > 0:
                    ac.click()
            except: pass

    def video_details(self):
        time.sleep(.5)
        td = self.driver.find_element(By.CSS_SELECTOR,'span[class=ytp-time-duration]')
        time_duration_list = td.get_attribute('innerHTML').split(':')
        time_duration_list.reverse()
        time_duration = 0
        description = ""
        views = 0

        mult = 1
        for tdl in time_duration_list:
            time_duration += int(tdl) * mult
            mult *= 60

        show_more = self.driver.find_element(By.ID, "description-inline-expander")
        description = show_more.text

        return {
            "description": description,
            'views': views,
            'duration': time_duration,
            'link': self.driver.current_url
        }
    class YoutubeVideo:
        def __init__(self, details, play_button, current_time_method, set_visible, browser):
            for key in details:
                setattr(self, key, details[key])

            self.play_button = play_button
            self.current_time_method = current_time_method
            self.set_visible = set_visible
            self.driver = browser.driver
            self.browser = browser

        def watch_for(self, duration):
            gdp = 0
            while gdp < duration:
                print('watching: ', gdp, '/', duration)
                time.sleep(1)
                if self.link != self.driver.current_url:
                    return
                gdp += 1
            
        def get_duration_percentage(self):
            return self.current_time_method()/self.duration
        
        def pause(self):
            if self.play_button.get_attribute('data-title-no-tooltip').lower() != "play":
                self.play_button.click()

        def play(self):
            if self.play_button.get_attribute('data-title-no-tooltip').lower() == "play":
                self.play_button.click()

        def comment(self, comment):
            self.set_visible()
            try:
                self.comment_box = self.driver.find_element(By.ID, 'simplebox-placeholder')
                self.comment_box.click()
            except: pass
            time.sleep(1.5)
            if self.driver.current_url.count('accounts.google.com/v3/signin'):
                self.browser.login_youtube()
                time.sleep(9)

            comment_input = self.driver.find_element(By.ID,"contenteditable-root")

            entering_comment_actions = ActionChains(self.driver)

            entering_comment_actions.move_to_element(comment_input)
            entering_comment_actions.click()

            for letter in comment:
                entering_comment_actions.send_keys(letter)
                wait_time = random.randint(0,1000)/1000
                entering_comment_actions.pause(wait_time)

            entering_comment_actions.perform()

            time.sleep(1)

            send_comment_buttons = self.driver.find_elements(By.CSS_SELECTOR,"button")
            for button in send_comment_buttons:
                if button.get_attribute('aria-label') == "Comment":
                    button.click()
                    return

            

            


    def build_video(self):
        self.wait.until(EC.visibility_of_element_located((By.ID,'description-inline-expander')))
        details = self.video_details()
        play_button = None
        #ytp-play-button ytp-button
        ad_close = self.driver.find_elements(By.CSS_SELECTOR,'button')
        for ac in ad_close:
            try:
                if ac.get_attribute('class').count('ytp-play-button') > 0:
                    play_button = ac
            except: pass

        return self.YoutubeVideo(details, play_button, self.current_time, self.set_visible, self)

    def current_time(self):
        #ytp-time-current
        td = self.driver.find_element(By.CSS_SELECTOR,'span[class=ytp-time-current]')
        time_duration_list = td.get_attribute('innerHTML').split(':')
        time_duration_list.reverse()
        time_duration = 0
        mult = 1
        for tdl in time_duration_list:
            time_duration += int(tdl) * mult
            mult *= 60
        return time_duration

    def open_youtube(self):
        self.opensite('https://www.youtube.com')
        