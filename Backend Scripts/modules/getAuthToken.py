# https://gist.github.com/sonya75/c343129a02281568da4c488d83fb09fe
# trying to make code i found publicly work;
import requests,uuid
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
global MAX_RETRIES
MAX_RETRIES = 10

def ChromeLoginGetAuthToken():
    driver = setupHeadlessChrome(mobile=False)
    driver.wait = WebDriverWait(driver, 30, 0.01)
    driver.get("http://www.nike.com/launch")
    # ((By.XPATH, f'//button[contains(text(), "{self.size}")]'
    # "//button[text()[contains(.,'"+shoe_size_type+"')]]"
    # sizeBtn = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
    # sizeBtn = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
    # sizeBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
    # Click login button on nav bar;

    loginBtn=False
    retries = 0
    while(loginBtn==False and retries < MAX_RETRIES):
        try:
            login_text = 'Log In'
            driver.wait.until(EC.visibility_of_element_located((By.XPATH, f"//button[text()[contains(.,'{login_text}')]]")))
            loginBtn= driver.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{login_text}')]")))
            loginBtn.click()
        except Exception as err:
            retries += 1
            print("Couldnt find or click login button, Retrying", MAX_RETRIES, "times", str(err))
        else:
            loginBtn=True
    retries = 0
    # try to SEND KEYS to EMAIL INPUT;
    emailEntered=False
    while(emailEntered == False and retries < MAX_RETRIES):
        try:
            email_input = driver.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-componentname='emailAddress']")))
            email_input = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@data-componentname='emailAddress']")))
            
        except Exception as err:
            retries += 1
            print("Couldn't send keys: email address, Retrying", MAX_RETRIES, "times") # need to add retry loop;
        else:
            email_input.send_keys(USERNAME)
            emailEntered = True
            print()
            print()
            print()
            print()
            print("Entered Username")
            print()
            print()
            print()
    retries = 0
    # try to SEND KEYS TO PASSWORD INPUT
    passwordEntered=False
    while(passwordEntered==False and retries < MAX_RETRIES):
        try:
            password_input = driver.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-componentname='password']")))
        except Exception as err:
            retries += 1
            print("Couldn't send keys: Password, Retrying", MAX_RETRIES, "times") # need to add retry loop;
        else:
            passwordEntered=True
            password_input.send_keys(PASSWORD)
            print("Entered Password")
            print()
            print()
            print()
    retries = 0
    # try to CLICK SUBMIT BUTTON & GRAB SESSION COOKIES;
    submitBtnClicked=False
    while(submitBtnClicked==False and retries < MAX_RETRIES):
        try:
            submitBtn = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="SIGN IN"]'))) 
        except Exception as err:
            retries += 1
            print("Couldn't Click Submit Btn: Retrying:", MAX_RETRIES, "times") # need to add retry loop;
            print("Error Msg:", str(err))
        else:
            #click submit button; tried using selenium & kept getting ssl errors;
            # going to try loading cookies into session;
            # time.sleep(3)
            # submitBtn.click()
            # submitBtnClicked=True
            cookies = driver.get_cookies()
            cookies_dict = {}
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expires'] = cookie.pop('expiry')
            print()
            print(len(cookies))
            print()
            print()
            print()
            print()
            print()
            print()
            print("Driver Cookies List: ", driver.get_cookies())
            print()
            print()
            print()
            print()
            print()
            print("_abck:", cookies['_abck'])
            print()
            print()
            print()
            print()
            print()
            print("bm_sz:", cookies['bm_sz'])
            print()
            print()
            print()
            print()
            print()
            s = requests.session()
            for cookie in cookies:
                if 'httpOnly' in cookie:
                        httpO = cookie.pop('httpOnly')
                        cookie['rest'] = {'httpOnly': httpO}
                if 'expiry' in cookie:
                    cookie['expires'] = cookie.pop('expiry')
                if 'sameSite' in cookie:
                    cookie['sameSite'] = int(cookies['sameSite'])
                s.cookies.set(**cookie)
            
            print()
            print()
            print()
            print()
            print()
            print("Session Cookies: ", s.cookies)

            print()
            print()
            print()
            print()
            print() 
            
            print("Driver Cookies: ", cookies)
            print() 
            print() 
            print() 
            print() 
            print()

            # def set_cookies(cookies, s):
                

                # return s

            #print("Access Token: ", driver.get_cookie('access_token'))
            for request in driver.requests:
                if request.response:
                    print(request.url)
                    print(request.response.status_code)
                    if request.response.json() is not None:
                        print(request.response.json())
                    else:
                        print("NO JSON FOUND")
                    # print(
                    #     request.url,
                    #     request.response.status_code,
                    #     #request.response.headers['Content-Type'],
                    #     request.response
                    #     #if request.response.json is not none: request.response.json,
                    # )
    
            

    retries = 0    
    print()
    print()
    print()
    print()
    cookies=driver.get_cookies()
    print("Cookies After Login: ", cookies)
    print()
    print()
    print()
    print()
    print()
    print(cookies)
    # value="SIGN IN" INPUT
    # data-componentname='emailAddress'
    # data-componentname='password'
    time.sleep(100)

    cookies = driver.get_cookies()
    print(type(cookies))
    sess=requests.session()
    for cookie in cookies:
        sess.cookies.set(cookie['name'], cookie['value'])
    uid=str(uuid.uuid4())
    # sess.cookies["NIKE_COMMERCE_COUNTRY"]="US"
    # sess.cookies["NIKE_COMMERCE_LANG_LOCALE"]="en_US"
    # sess.cookies["nike_locale"]="us/en_us"
    print(sess.cookies)
    print()
    print()
    print()
    print()
    print()

    login_json = {'keepMeLoggedIn':True, 'client_id':'HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH','ux_id':'com.nike.commerce.nikedotcom.web','grant_type':'password','username': USERNAME,'password': PASSWORD}
    
    sess.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
    # e=sess.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=login_json,verify=False,timeout=30).json()
    d=dict()
    d=getAppExpVersionsDict()
    e=sess.post('https://unite.nike.com/login?appVersion='+d.get('APPVERSION')+'&experienceVersion='+d.get('EXPVERSION')+'&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false&visit=1&visitor='+uid,json=login_json, verify=False,timeout=30)#.json()
    print(e.status_code)
    token=e["access_token"]
    print(token)
    ee=sess.get("https://unite.nike.com/auth/slcheck_cookies/v1?appVersion=417&experienceVersion=352&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false&visit=1&visitor="+uid+"&atgSync=true&uxId=com.nike.commerce.nikedotcom.web&cookieType=N",headers={"Origin":"https://www.nike.com","Referer":"https://www.nike.com/us/en_us/","Authorization":("Bearer "+token),"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
    ee=sess.post("https://secure-store.nike.com/nikestore/html/services/orders/orderReturnHistory",headers={"X-Requested-With":"XMLHttpRequest","Origin":"https://secure-store.nike.com","Content-Type":"application/x-www-form-urlencoded","Referer":"https://secure-store.nike.com/common/content/endpoint.html","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},data="lang_locale=en_US&country=US&deviceType=desktop")
    ee=sess.post("https://secure-store.nike.com/nikestore/html/services/orders/orderReturnHistory",headers={"X-Requested-With":"XMLHttpRequest","Origin":"https://secure-store.nike.com","Content-Type":"application/x-www-form-urlencoded","Referer":"https://secure-store.nike.com/common/content/endpoint.html","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},data="lang_locale=en_US&country=US&deviceType=desktop")
    print(ee.text)

if __name__ == '__main__':
    ChromeLoginGetAuthToken()