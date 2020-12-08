from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os
from os import path

global delay, DRIVERRELDIR, PROXY
delay = 30
DRIVERRELDIR = 'chromedriver.exe'



def setupHeadlessChrome(mobile=False, proxy=False, headless=True):       
    # open webdriver, incognito & start maximized
    chrome_options = Options()
    # Setup chrome options for better performance / less issues with elements in the way
    # headless browser = No UI = Less Resources;
    if(headless):
        chrome_options.add_argument('--headless')

    # incognito for no leftover cookies, will need to load cookies on after every request & refresh page to acutally send them
    # chrome_options.add_argument('--incognito')
    # mobile user agent = Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1
    if(mobile==False):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        # disable infobars
        chrome_options.add_argument('disable-infobars')
        # disable extensions
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument(f'user-agent={user_agent}')
    else:
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1'

    # user agent for desktop chrome browser (google search what is my user agent for yours)
    # user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"
    
    
    # disable sandbox to Bypass OS security Model
    # chrome_options.add_argument('--no-sandbox')
    # use maximzied when not using headless
    # chrome_options.add_argument('start-maximized')
    # adds dir for cookies 
    # chrome_options.add_argument("--user-data-dir=chrome_profile_dir")

    if(mobile):
        chrome_options.add_argument('--window-size=375,812')
    else:
        chrome_options.add_argument('start-maximized')
    # do not verify ssl
    # chrome_options.add_argument('verify_ssl="False"')
    # ignore certificate errors
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--auto-open-devtools-for-tabs")

    burp_proxy="127.0.0.1:8080"
    if(proxy):
        chrome_options.add_argument(f'--proxy-server={burp_proxy}')
    
    if (mobile):
        #Mobile emulation; not working for login, login using regular browser, grab session cookies & pass to mobile;
        mobile_emulation = { 
            #"deviceName": "iPhone X"
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"
    
           }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        # applicable to windows os only
        chrome_options.add_argument('--disable-gpu')

    # https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
    #print(os.path.abspath(os.getcwd())) 
    #print(os.path.relpath(__file__))
    # make sure this works on other PC's join current working dir to relative path of chromedirver;
    curDir = os.getcwd()
    driver_rel_dir = DRIVERRELDIR
    driver_dir = os.path.join(curDir, driver_rel_dir)
    # print(driver_dir)
    driver = webdriver.Chrome(executable_path=driver_dir, 
                        options=chrome_options)
    driver.wait = WebDriverWait(driver, delay)
    driver.actions = ActionChains(driver)
    
    return driver

if __name__ == '__main__':
    setupHeadlessChrome(mobile=True, proxy=False, headless=False)