import requests, uuid
import urllib3
from urllib3.exceptions import InsecureRequestWarning,SubjectAltNameWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)
from getAppExpVersions import getAppExpVersionsDict
from login_details import USERNAME, PASSWORD
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from setupHeadlessChrome import setupHeadlessChrome
import time
from selenium.webdriver.common.keys import Keys
from setupHeadlessChrome import setupHeadlessChrome
import json
import pprint
# post cookies to login;
# _abck - obtained from 
# Visitor Data {visit:1, visitor:uuid} Obtained from unite.com/s3/unite/mobile.html?.... 
#

driver = setupHeadlessChrome(mobile=True, proxy=False, headless=False)
print("getting Launch Page / will disable later to see if this step is even necessary;")
launchRes = driver.get("https://www.nike.com/launch")
print("+[Launch Page]: Driver Launch Page Cookies: ", type(driver.get_cookies()), driver.get_cookies())
print()
print()
print()
print()
print()
time.sleep(5)
test = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# print("getting mobile.html thru driver;")
# res = driver.get("https://unite.nike.com/s3/unite/mobile.html?mid=18959627270998287647537118415893677125?iOSSDKVersion=3.1.7&clientId=G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj&uxId=com.nike.commerce.snkrs.ios&view=none&locale=en_US&backendEnvironment=identity&corsOverride=https://unite.nike.com&osVersion=14.2")

loginRes = driver.get("https://www.nike.com/login")
try:
    email_input = driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-componentname="emailAddress"]')))
except Exception as e:
    print("Never found email input path")
    driver.quit()
else:
    email_input.send_keys("acrypto91@gmail.com")
try:
    pass_input = driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-componentname="password"]')))
except Exception as e:
    print("Never found password input path")
    driver.quit()
else:
    pass_input.send_keys("Charlie123!")
try:
    #//button[contains(text(), "{self.size}")]
    signInBtn = driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@value="SIGN IN"]')))
except Exception as e:
    print("sign in button not clickable", str(e))
    driver.quit()
else:
    time.sleep(10)
    signInBtn.click()
    # time.sleep(200)
    # exit()
time.sleep(5)
print(driver.title)
print()
print()
print()
print("NOW SAVE COOKIES BITCH")
exit()
#print(res.text)a
print()
print()
print()
print()
print()

driverCookiesList = driver.get_cookies()
print("Driver cookies: ", type(driverCookiesList))
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(driverCookiesList)
print()
print()
print()
print()
print()


# grab driver cookies with domain, to use to create CookieJar (session) cookies;

driverCookieDict = dict()
driverCookieSet = set()
newDriverCookieList = list()
for eaDict in driverCookiesList:
    for item in eaDict.items():
        # temp = {"domain": eaDict['domain'], "name": eaDict['name'], "value": eaDict['value']}
        temp = {eaDict['domain'], eaDict['name'], eaDict['value']}
        #driverCookieDict.update(temp)
        temp = tuple(temp)
        if temp not in driverCookieSet:
            driverCookieSet.add(temp)
            newDriverCookieList.append(temp)
# need to grab headers from response
# THIS IS WHERE I STOPPED WORKING & C/P From jupyter notebook;
# import re
# tempCookies = temp['Set-Cookie']
# print(tempCookies)
# # get anonId cookies;
# anonymousId = re.search('anonymousId=\S*', tempCookies)
# if anonymousId:
#     anonymousId.group()
#     print("\n\n\n")
#     anonymousId_value = anonymousId.split("=")[1]
#     print("Anonymous Id:", anonymousId_value)
#     print("\n\n\n")
# else:
#     print("didnt find Anonymous Id")
# # Get ak_bmsc cookies; everthing except anonid has domain of .nike.com
# ak_bmsc = re.search('ak_bmsc=\S*', tempCookies)
# if(ak_bmsc):
#     ak_bmsc_value = ak_bmsc.group()
#     ak_bmsc_value = ak_bmsc_value.split("=", 1)[1]
#     #print(ak_bmsc)
#     print("ak_bmsc:", ak_bmsc_value)
# else:
#     print("didnt find ak_bmsc")
# # get bm_mi

# # domain name value tuple in newDriverCookieList
# for tu in newDriverCookieList:
#     for domain,name,value in tu:
#         cookie_obj = requests.cookies.create_cookie(domain=domain,name=name,value=value)
#         #sess.cookies.set_cookie(cookie_obj)


print()
print()
print()
print()
print("Driver Cookie Set: ", driverCookieSet)
print()
print()
print()
# print("MY FUCKIN driverCookieDict: ", driverCookieDict)
# print(driverCookieDict.keys())
#del driverCookieDict['RT']

print()
print()
print()


# sess = requests.session()
# sess.headers.update({"User-Agent":'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1'})
# print("getting mobile.html through requests.session")
# resGet = sess.get("https://unite.nike.com/s3/unite/mobile.html?mid=18959627270998287647537118415893677125?iOSSDKVersion=3.1.7&clientId=G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj&uxId=com.nike.commerce.snkrs.ios&view=none&locale=en_US&backendEnvironment=identity&corsOverride=https://unite.nike.com&osVersion=14.2")


print("+[Mobile.html]: Session Get Headers: ", pp.pprint(resGet.headers))
# cookies_test = [
#     for c in sess.cookies:
#         if c.name is not None
#     {"name": c.name, "value": c.value, "domain":c.domain, "expires": c.expiry, "httpOnly":c.httpOnly}
    
# ]]
print()
print()
print()
print()
print()
print("+[Mobile.html]: Session Cookie Jar: ", sess.cookies)
print(resGet.status_code)
print()
print()
print()
print()
sCookies = sess.cookies.get_dict()
print("+[Mobile.html]: Session Cookies Dict: ", pp.pprint(sCookies))
print(type(sCookies))
#sess.cookies.update()
print()
print()
print()
print()
print()



print("Attempting to login wiht request session post")
headers = {
    'Host': 'unite.nike.com',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-us',
    'X-Sec-Clge-Req-Type': 'ajax',
    'Content-Type': 'application/json',
    'Origin': 'https://unite.nike.com',
    #'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Connection': 'close',
    'Referer': 'https://unite.nike.com/s3/unite/mobile.html?mid=18959627270998287647537118415893677125?iOSSDKVersion=3.1.7&clientId=G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj&uxId=com.nike.commerce.snkrs.ios&view=none&locale=en_US&backendEnvironment=identity&corsOverride=https://unite.nike.com&osVersion=14.2'
}
# update session headers;
sess.headers.update(headers)
login_json={
    "username":"acrypto91@gmail.com",
    "password":"Charlie123!",
    "client_id":"G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj",
    "ux_id":"com.nike.commerce.snkrs.ios",
    "grant_type":"password"
}
# dict_keys(['RT', 'domain', 'neo_sample', 'NIKE_CART', 'ppd', 'anonymousId', 'dreamcatcher_sample', 'visitData', 
# 'ak_bmsc', 'bm_sv', '_abck', 'NIKE_COMMERCE_LANG_LOCALE', 
# 'NIKE_COMMERCE_COUNTRY', 'siteCatalyst_sample', 'CONSUMERCHOICE', 
# 'AMCVS_F0935E09512D2C270A490D4D%40AdobeOrg', 'AnalysisUserId', 
# 'AMCV_F0935E09512D2C270A490D4D%40AdobeOrg', 's_ecid', 
# 'bm_sz', 'geoloc'])\
print()
print()
print()
print("updating session cookies, printing")

# grab driver cookies with domain, to use to create CookieJar (session) cookies;

# driverCookieDict = dict()
# driverCookieSet = set()
# newDriverCookieList = list()
# for eaDict in driverCookiesList:
#     for item in eaDict.items():
#         # temp = {"domain": eaDict['domain'], "name": eaDict['name'], "value": eaDict['value']}
#         temp = {eaDict['domain'], eaDict['name'], eaDict['value']}
#         driverCookieDict.update(temp)
#         temp = tuple(temp)
#         if temp not in driverCookieSet:
#             driverCookieSet.add(temp)
#             newDriverCookieList.append(temp)
# need to grab headers from response
# THIS IS WHERE I STOPPED WORKING & C/P From jupyter notebook;
import re
tempCookies = temp['Set-Cookie']
print(tempCookies)
# get anonId cookies;
anonymousId = re.search('anonymousId=\S*', tempCookies)
if anonymousId:
    anonymousId.group()
    print("\n\n\n")
    anonymousId_value = anonymousId.split("=")[1]
    print("Anonymous Id:", anonymousId_value)
    print("\n\n\n")
else:
    print("didnt find Anonymous Id")
# Get ak_bmsc cookies; everthing except anonid has domain of .nike.com
ak_bmsc = re.search('ak_bmsc=\S*', tempCookies)
if(ak_bmsc):
    ak_bmsc_value = ak_bmsc.group()
    ak_bmsc_value = ak_bmsc_value.split("=", 1)[1]
    #print(ak_bmsc)
    print("ak_bmsc:", ak_bmsc_value)
else:
    print("didnt find ak_bmsc")
# get bm_mi

# # domain name value tuple in newDriverCookieList
# for tu in newDriverCookieList:
#     for domain,name,value in tu:
#         cookie_obj = requests.cookies.create_cookie(domain=domain,name=name,value=value)
#         #sess.cookies.set_cookie(cookie_obj)


# visitData = {"visitData": driverCookieDict['visitData']}
# visitDataDict = json.loads(driverCookieDict['visitData'])

# _abck = {"_abck": driverCookieDict['_abck']}
# s_ecid = {"s_ecid": driverCookieDict['s_ecid']}
# amcvs_f = {"AMCVS_F0935E09512D2C270A490D4D%40AdobeOrg": driverCookieDict['AMCVS_F0935E09512D2C270A490D4D%40AdobeOrg']}
# avcv_f = {"AMCV_F0935E09512D2C270A490D4D%40AdobeOrg":  driverCookieDict['AMCV_F0935E09512D2C270A490D4D%40AdobeOrg']}
# geoloc = {"geoloc": driverCookieDict['geoloc']}
# ak_bmsc = {"ak_bmsc": driverCookieDict['ak_bmsc']}
# bm_sv = {"bm_sv": driverCookieDict['bm_sv']}
# sess.cookies.update(s_ecid)
# sess.cookies.update(amcvs_f)
# sess.cookies.update(avcv_f)
# sess.cookies.update(geoloc)
# sess.cookies.update(ak_bmsc)
# sess.cookies.update(bm_sv)
# print("Session Cookies After Update Jar:", sess.cookies)
print()
print()
print()
print()
print()


print()
print()
print()
print()


#pRes = sess.post(f"https://unite.nike.com/login?appVersion=847&experienceVersion=847&uxid=com.nike.commerce.snkrs.ios&locale=en_US&backendEnvironment=identity&browser=Apple%20Computer%2C%20Inc.&os=undefined&mobile=true&native=true&visit={visitDataDict['visit']}&visitor={visitDataDict['visitor']}", json=login_json, verify=True, timeout=30)
print(sCookies.keys())
print(sCookies.values())
# for k,v in sCookies:
#     if not isinstance(v, str):
#         sCookies[k] =  str(v) 
# requests.utils.add_dict_to_cookiejar(sess.cookies,
#                                         pRes.content)

print("response: ", pRes.status_code)
if pRes.status_code == 403:
    print("forbidden")
elif pRes.status_code == 200:
    print("WE FUCKING DID IT, GET JSON RESPONSE DATA")
print("headers:", sess.headers)
print()
print()
print()
print("post cookies")
print(sess.cookies.get_dict())
print()
print()
print()
print()
print()