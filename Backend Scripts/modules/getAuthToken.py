# https://gist.github.com/sonya75/c343129a02281568da4c488d83fb09fe
# trying to make code i found publicly work;
import requests,uuid
import urllib3
from urllib3.exceptions import InsecureRequestWarning,SubjectAltNameWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)
from getAppExpVersions import getAppExpVersionsDict
from login_details import USERNAME, PASSWORD
from setupHeadlessChrome import setupHeadlessChrome

def LoginGetAuthToken():
    driver = setupHeadlessChrome(mobile=False)
    driver.get("http://www.nike.com/launch")
     try: # ((By.XPATH, f'//button[contains(text(), "{self.size}")]'
            self.wait.until(EC.element_to_be_clickable((By.XPATH), '//button[contains(text()="Log In")]'))
        except Exception as err:
            print("Couldnt click login button", str(err))
    sess=requests.session()
    uid=str(uuid.uuid4())
    sess.cookies["NIKE_COMMERCE_COUNTRY"]="US"
    sess.cookies["NIKE_COMMERCE_LANG_LOCALE"]="en_US"
    sess.cookies["nike_locale"]="us/en_us"

    login_json = {'keepMeLoggedIn':True, 'client_id':'HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH','ux_id':'com.nike.commerce.nikedotcom.web','grant_type':'password','username': USERNAME,'password': PASSWORD}
    
    sess.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
    #e=sess.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=login_json,verify=False,timeout=30).json()
    d=dict()
    d=getAppExpVersionsDict()
    e=sess.post('https://unite.nike.com/login?appVersion='+d.get('APPVERSION')+'&experienceVersion='+d.get('EXPVERSION')+'&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false&visit=1&visitor='+uid,json=login_json, cookies=cookies, verify=False,timeout=30)#.json()
    print(e.status_code)
    token=e["access_token"]
    print(token)
    ee=sess.get("https://unite.nike.com/auth/slcheck_cookies/v1?appVersion=417&experienceVersion=352&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false&visit=1&visitor="+uid+"&atgSync=true&uxId=com.nike.commerce.nikedotcom.web&cookieType=N",headers={"Origin":"https://www.nike.com","Referer":"https://www.nike.com/us/en_us/","Authorization":("Bearer "+token),"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
    ee=sess.post("https://secure-store.nike.com/nikestore/html/services/orders/orderReturnHistory",headers={"X-Requested-With":"XMLHttpRequest","Origin":"https://secure-store.nike.com","Content-Type":"application/x-www-form-urlencoded","Referer":"https://secure-store.nike.com/common/content/endpoint.html","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},data="lang_locale=en_US&country=US&deviceType=desktop")
    ee=sess.post("https://secure-store.nike.com/nikestore/html/services/orders/orderReturnHistory",headers={"X-Requested-With":"XMLHttpRequest","Origin":"https://secure-store.nike.com","Content-Type":"application/x-www-form-urlencoded","Referer":"https://secure-store.nike.com/common/content/endpoint.html","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},data="lang_locale=en_US&country=US&deviceType=desktop")
    print(ee.text)

if __name__ == '__main__':
    getAuthToken()