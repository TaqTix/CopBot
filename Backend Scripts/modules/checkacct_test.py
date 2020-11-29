import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from setupHeadlessChrome import setupHeadlessChrome
from selenium.webdriver.support import expected_conditions as EC

global USERNAME, PASSWORD
USERNAME = 'acrypto91@gmail.com'
PASSWORD = 'Charlie123!'



driver = setupHeadlessChrome(mobile=True, proxy=True, headless=False)

driver.get("https://www.nike.com/launch")



# sess=requests.session()
# m_login_data = {'keepMeLoggedIn':True, 'client_id':'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7','ux_id':'com.nike.commerce.snkrs.droid','grant_type':'password','username':USERNAME,'password':PASSWORD}
# sess.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
# e=sess.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=m_login_data,verify=False,timeout=30)
# print(e.status_code) # 401 unauthorized; probably a problem with cookies;
# TOKEN=e.json()["access_token"]
# print("Token: ", TOKEN)
# ee=sess.get("https://idn.nike.com/user/accountsettings",headers={"Authorization":("Bearer "+TOKEN)})

#print "{0}, Number: {1}\n".format(v[0],ee.json().get("verifiedphone")),


