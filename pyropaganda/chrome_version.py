#
# Programmatically detect the version of the Chrome web browser installed on the PC.
# Compatible with Windows, Mac, Linux.
# Written in Python.
# Uses native OS detection. Does not require Selenium nor the Chrome web driver.
#__init__.py

import os
import re
from sys import platform as pf
import platform
from . config import hcolors
import requests
import subprocess
from zipfile import ZipFile


chrome_driver_link = "https://chromedriver.storage.googleapis.com/?delimiter=/&prefix="


def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""

def extract_version_registry(output):
    try:
        google_version = ''
        for letter in output[output.rindex('DisplayVersion    REG_SZ') + 24:]:
            if letter != '\n':
                google_version += letter
            else:
                break
        return(google_version.strip())
    except TypeError:
        return

def extract_version_folder():
    # Check if the Chrome folder exists in the x32 or x64 Program Files folders.
    for i in range(2):
        path = 'C:\\Program Files' + (' (x86)' if i else '') +'\\Google\\Chrome\\Application'
        if os.path.isdir(path):
            paths = [f.path for f in os.scandir(path) if f.is_dir()]
            for path in paths:
                filename = os.path.basename(path)
                pattern = '\d+\.\d+\.\d+\.\d+'
                match = re.search(pattern, filename)
                if match and match.group():
                    # Found a Chrome version.
                    return match.group(0)

    return None

def get_chrome_version():
    version = None
    install_path = None

    try:
        if pf == "linux" or pf == "linux2":
            # linux
            install_path = "/usr/bin/google-chrome-stable"
        elif pf == "darwin":
            # OS X
            install_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
        elif pf == "win32":
            # Windows...
            try:
                # Try registry key.
                stream = os.popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
                output = stream.read()
                version = extract_version_registry(output)
            except Exception as ex:
                # Try folder path.
                version = extract_version_folder()
    except Exception as ex:
        print(ex)

    version = os.popen(f"{install_path} --version").read().strip('Google Chrome ').strip() if install_path else version

    return version

def driver_name():
    _platform_filenames =  {
        "linux":"chromedriver_linux64.zip",
        "linux2":"chromedriver_linux64.zip",
        "darwin":"chromedriver_mac64.zip",
        "darwinSC":"chromedriver_mac_arm64.zip",
        "win32":"chromedriver_win32.zip"
    }
    if pf != "darwin":
        return _platform_filenames.get(pf)
    
    if get_processor_name().count("Intel") == 0:
        return _platform_filenames.get('darwinSC')
    
    return _platform_filenames.get('darwin')

def check_drivers():
    if "drivers" not in os.listdir():
        try:
            os.mkdir('drivers')
        except: pass

    return "chromedriver" in os.listdir("drivers")

def init():
    if not check_drivers():
        _version = get_chrome_version()
        try:
            print(hcolors.OKBLUE+"Fetching chromedriver for version: "+_version)
            _version = _version.split('.')
            resp = requests.get(chrome_driver_link+_version[0])
            _target_driver_version = resp.text.split('<Prefix>')[-1].split('</Prefix>')[0]
            _driver_download = requests.get('https://chromedriver.storage.googleapis.com/'+_target_driver_version+driver_name())
            _wb = open('driver_download.zip',"wb")
            _wb.write(_driver_download.content)
            _wb.close()

            with ZipFile("driver_download.zip", 'r') as zObject:
                zObject.extractall(
                    path="drivers")

            os.remove("driver_download.zip")
            print(hcolors.OKGREEN+"Success for version: "+".".join(_version))

        except:
            print(hcolors.WARNING+"Chrome not found on system, install Chrome or set Chrome path in settings.json")
            return
