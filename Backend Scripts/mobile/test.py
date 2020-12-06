from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import threading
import os
from os import path
import pickle
from urllib.parse import urlparse
import requests
from selenium.webdriver.common.proxy import Proxy, ProxyType
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json

def cookiesDict(session):
    print(requests.utils.dict_from_cookiejar(session.cookies))
    return requests.utils.dict_from_cookiejar(session.cookies)

def save_driver(fileName, driver_info):
	with open(fileName, 'w') as fout:
		json.dump(driver_info, fout)

def openHeadlessChrome(url):
    #mobile emulation
    mobile_emulation = { 
			#"deviceName": "Apple iPhone 3GS"
			#"deviceName": "Apple iPhone 4"
			#"deviceName": "Apple iPhone 5"
			#"deviceName": "Apple iPhone 6"
			#"deviceName": "Apple iPhone 6 Plus"
			#"deviceName": "BlackBerry Z10"
			#"deviceName": "BlackBerry Z30"
			#"deviceName": "Google Nexus 4"
			# "deviceName": "Google Nexus 5"
			#"deviceName": "Google Nexus S"
			#"deviceName": "HTC Evo, Touch HD, Desire HD, Desire"
			#"deviceName": "HTC One X, EVO LTE"
			#"deviceName": "HTC Sensation, Evo 3D"
			#"deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black"
			#"deviceName": "LG Optimus G"
			#"deviceName": "LG Optimus LTE, Optimus 4X HD" 
			#"deviceName": "LG Optimus One"
			#"deviceName": "Motorola Defy, Droid, Droid X, Milestone"
			#"deviceName": "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2"
			#"deviceName": "Motorola Droid Razr HD"
			#"deviceName": "Nokia C5, C6, C7, N97, N8, X7"
			#"deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900"
			#"deviceName": "Samsung Galaxy Note 3"
			#"deviceName": "Samsung Galaxy Note II"
			#"deviceName": "Samsung Galaxy Note"
			#"deviceName": "Samsung Galaxy S III, Galaxy Nexus"
			#"deviceName": "Samsung Galaxy S, S II, W"
			#"deviceName": "Samsung Galaxy S4"
			#"deviceName": "Sony Xperia S, Ion"
			#"deviceName": "Sony Xperia Sola, U"
			#"deviceName": "Sony Xperia Z, Z1"
			#"deviceName": "Amazon Kindle Fire HDX 7″"
			#"deviceName": "Amazon Kindle Fire HDX 8.9″"
			#"deviceName": "Amazon Kindle Fire (First Generation)"
			#"deviceName": "Apple iPad 1 / 2 / iPad Mini"
			#"deviceName": "Apple iPad 3 / 4"
			#"deviceName": "BlackBerry PlayBook"
			#"deviceName": "Google Nexus 10"
			#"deviceName": "Google Nexus 7 2"
			#"deviceName": "Google Nexus 7"
			#"deviceName": "Motorola Xoom, Xyboard"
			#"deviceName": "Samsung Galaxy Tab 7.7, 8.9, 10.1"
			#"deviceName": "Samsung Galaxy Tab"
			#"deviceName": "Notebook with touch"
			
			# Or specify a specific build using the following two arguments
            "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
		    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
        }
    chrome_options = Options() #this is ChromeOptions

    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    # Setup chrome options for better performance / less issues with elements in the way
    # headless browser = No UI = Less Resources;
    # chrome_options.add_argument('--headless')
    # incognito for no leftover cookies
    chrome_options.add_argument('--incognito')
    # user agent for desktop chrome browser (google search what is my user agent for yours)
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    # disable infobars
    chrome_options.add_argument('disable-infobars')
    # disable extensions
    chrome_options.add_argument('--disable-extensions')
    # disable sandbox to Bypass OS security Model
    chrome_options.add_argument('--no-sandbox')
    # use maximzied when not using headless
    #chrome_options.add_argument('start-maximized')
    # chrome_options.add_argument('--window-size=1024,768')
    # do not verify ssl
    chrome_options.add_argument('verify_ssl="False"')
    # ignore certificate errors
    chrome_options.add_argument('ignore-certificate-errors')
    # applicable to windows os only
    chrome_options.add_argument('--disable-gpu')
    # setup chrome driver instance
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options )
    # incase we need actions
    driver.actions = ActionChains(driver)
    # incase we need wait commands
    driver.wait = WebDriverWait(driver, 20)
    #load url
    driver.get(url)
    return driver

def reloadWithCookies(driver, url):
    driver_info = {}
    driver_info = driver.get_cookies()
    for cookie in driver_info:
        driver.add_cookie(cookie)
    driver.get(url)  # refresh to load cookies;
    return driver

driver = openHeadlessChrome("https://www.nike.com/launch")
time.sleep(30)
    # res = driver.get("https://unite.nike.com/s3/unite/mobile.html")
print("driver get nike.com/launch taking screenshot")
# driver.save_screenshot("test.png")
# print(driver.get_cookies())
# cookies_list_launch = driver.get_cookies() #get cookies from launch page returns list
# not sure if its necessary to get them from launch page  or if login page will provide them;
print()
print()
print()
print()
print()
print("Launch Page Cookies: ")
# print(cookies_list_launch)
# cookies_list = [] #initialized to hold all the cookies in list; then convert to dict to use in requests;
# for cookie in cookies_list_launch:
#     cookies_list.append([cookie['name'],cookie['value']])
# cookies_dict = dict(cookies_list)
print()
print()
print()
#print(cookies_dict)
print("getting login page through driver for more cookies")
driver.get("https://www.nike.com/login")
cookies_list_login = driver.get_cookies()
# cookies_list = cookies_list_launch.append(cookies_list_login)
print()
print()
print()
print()
print()
#print("Cookies_List after appending")
url = "https://www.nike.com/login"
driver = reloadWithCookies(driver, url)

#driver.post("")

# for cookie in cookies_list_login:
#     cookies_list.append([cookie['name'],cookie['value']])
# login_cookie_dict = dict(cookies_list)
# print("updating cookies_dict with new cookies")
# cookies_dict.update(login_cookie_dict)
print()
print()
print()
print()
print()
print("printing new cookies after login page")
print(driver.get_cookies())
print()
print()
print()
# print(type(cookies_dict))
# print(cookies_dict)

# print("Type of cookies_dict")
# print(type(cookies_dict))
#res = driver.get("https://unite.nike.com/session.html")

# s = requests.session()
# print("attempting post to login")
# APPVERSION = '847'
# EXPVERSION = '847'
# email = 'acrypto91@gmail.com'
# password = 'Charlie123!'
# # res = s.post("https://unite.nike.com/loginWithSetCookie?appVersion={0}&experienceVersion={1}&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false".format(APPVERSION,EXPVERSION),json={"username":email,"password":password,"client_id":"HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH","ux_id":"com.nike.commerce.nikedotcom.web","grant_type":"password"},verify=False)
# # print("status code:", res.status_code)
# global USER_AGENT
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
# headers = {
# 'accept': '*/*',
# 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'en-US,en;q=0.9',
# 'content-length': '170',
# 'content-type': 'application/json',
# 'origin': 'https://www.nike.com',
# 'referer': 'https://www.nike.com/',
# 'sec-fetch-dest': 'empty',
# 'sec-fetch-mode': 'cors',
# 'sec-fetch-site': 'same-site',
# 'user-agent': USER_AGENT,
# }
# global CLIENT_ID, UX_ID
# CLIENT_ID = 'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7'
# UX_ID = 'com.nike.commerce.snkrs.web'
# data = {
#     'username:': email,
#     'password:': password,
#     'client_id': CLIENT_ID,
#     'ux_id': UX_ID,
#     'grant_type': 'password',
# }
# json_data = json.dumps(data, indent=4)
# uuid = uuid.uuid4()
# params = {
# 'appVersion': '847',
# 'experienceVersion': '847',
# 'uxid': 'com.nike.commerce.snkrs.web',
# 'locale': 'en_US',
# 'backendEnvironment': 'identity',
# 'browser': 'Google%20Inc.',
# 'os': 'undefined',
# 'mobile': 'false',
# 'native': 'false',
# 'visit': '1',
# 'visitor': uuid,
# }
# print(cookies_dict['AnalysisUserId'])

# res = s.post("https://unite.nike.com/login?", headers=headers, cookies=cookies_dict, data=json_data, params=params)
# print(res.status_code)
# print()
# print()
# print()
# print(s.params)
# print()
# print()
# print()
# print()
# print(s.cookies)

# client id = PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7
# res = s.post("https://unite.nike.com/login?", )
# res = s.get("https://www.nike.com/login", cookies=cookies_dict)




# cookies_list_login = driver.get_cookies()
# for cookie in cookies_list_login:
#     cookies_list.append([cookie['name'],cookie['value']])
# login_dict = dict(cookies_list) # turn list from above into dict;
# cookies_dict.update(login_dict) # update dict of previous cookies with new ones;
# print()
# print()
# print()
# print()
# print()
# print("type of cookies_dict after going to login page")

# print(type(cookies_dict))
# print(cookies_dict)

# print("Attempting to get login page")
# print()
# print()
# print()
# print()
# print()
# print("Getting cookies from login page")
# print(driver.get_cookies())
# cookies_list1 = driver.get_cookies()
# cookies_dict = []
# for cookie in cookies_list1:
#     cookies_dict.append([cookie['name'],cookie['value']])
# cookies_dict = dict(cookies_dict)
# print()
# print()
# print()
# print()
# print()
# print(cookies_dict)
# print(type(cookies_dict))

# # driver.add_cookie({'name' : 'CONSUMERCHOICE', 'value' : 'us/en_us'})
# # driver.add_cookie({"name" : "NIKE_COMMERCE_COUNTRY", "value" : "US"})
# # driver.add_cookie({"name" : "NIKE_COMMERCE_LANG_LOCALE", "value" : "en_US"})
# # driver.add_cookie({"name" : "nike_locale", "value" : "us/en_us"})
# #print(type(driver.get_cookies()))
# print()
# print()
# print()
# print()
# print()
# pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# s = requests.session()
# res = s.get("https://unite.nike.com/session.html", cookies=cookies_dict)
# print(type(s.cookies))
# print()
# print()
# print()
# print()
# print()
# print(s.cookies)
    # cookies_dict2 = []
    # for cookie in cookies_list:
    #     cookies_dict.append([cookie['name'],cookie['value']])
    # cookies_dict = dict(cookies_dict)
    # print(res.status_code)
    # print()
    # print()
    # print()
    # print()
    # print()
    # res = s.get("")
# res = driver.get("https://unite.nike.com/s3/unite/mobile.html?mid=52808542570411881128326486930296807267?iOSSDKVersion=3.1.7&clientId=G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj&uxId=com.nike.commerce.snkrs.ios&view=none&locale=en_US&backendEnvironment=identity&corsOverride=https://unite.nike.com&osVersion=14.1")

# while not os.path.exists("cookies.pkl"):
#     print("File not available sleeping 1 sec")
#     time.sleep(1)
# if os.path.isfile("cookies.pkl"):
#     cookies = pickle.load(open("cookies.pkl", "rb"))
#     for cookie in cookies:
#         driver.add_cookie(cookie)




# try:
#     wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="SIGN IN"]'))).click()
# except Exception as err:
#     print("Couldnt Click Login", str(err))

time.sleep(30)
driver.close()