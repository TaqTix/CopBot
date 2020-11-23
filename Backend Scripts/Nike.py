#from seleniumwire import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import threading
import requests
import json

# This is for Nike.com/launch only & on a computer;

#GLOBAL VARS
delay = 15 #seconds -> Later, If the drops happen at specific times usually can have bot only check most
                   #frequently around then

class NikeBot:

    def __init__(self, url, size, username, password, guest_checkout):
        # only grabbing one username/password so that I can spawn multiple threads of this process for multiple profiles.
        self.url = str(url)
        self.size = str(size)
        self.username = str(username)
        self.password = str(password)
        self.guest_checkout = guest_checkout

    def setupHeadlessChrome(self, mobile=False):       
        # open webdriver, incognito & start maximized
        chrome_options = Options()
        # Setup chrome options for better performance / less issues with elements in the way
        # headless browser = No UI = Less Resources;
        chrome_options.add_argument('--headless')
        # incognito for no leftover cookies, will need to load cookies on after every request & refresh page to acutally send them
        chrome_options.add_argument('--incognito')
        # mobile user agent = Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1
        if mobile=False:
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        else:
            self.user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1'
        # user agent for desktop chrome browser (google search what is my user agent for yours)
        # self.user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        # disable infobars
        chrome_options.add_argument('disable-infobars')
        # disable extensions
        chrome_options.add_argument('--disable-extensions')
        # disable sandbox to Bypass OS security Model
        chrome_options.add_argument('--no-sandbox')
        # use maximzied when not using headless
        #chrome_options.add_argument('start-maximized')
        # chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--window-size=1500,800')
        # do not verify ssl
        chrome_options.add_argument('verify_ssl="False"')
        # ignore certificate errors
        chrome_options.add_argument('ignore-certificate-errors')
        # applicable to windows os only
        chrome_options.add_argument('--disable-gpu')
        if (mobile):
            Mobile emulation; not working for login, login using regular browser, grab session cookies & pass to mobile;
            mobile_emulation = { 
                "deviceName": "iPhone X"
                #"deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
                #"userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
        self.driver = webdriver.Chrome(executable_path='Backend Scripts\\chromedriver.exe', 
                            options=chrome_options) #, seleniumwire_options={'verify_ssl': False}
        # Modifying Headers for headless version
        # allow_origin = self.url.split("/")[2] # grabs just www.nike.com
        # self.driver.header_overrides = {
        #     'Access-Control-Allow-Origin': f'{allow_origin}',
        #     'SameSite': 'True',
        # } 
        self.session_id = self.driver.session_id
        #self.driver.implicitly_wait(1)
        self.wait = WebDriverWait(self.driver, delay)
        self.actions = ActionChains(self.driver)
        self.driver.set_page_load_timeout(delay)
        return self.driver

    def getLoginCookiesFromDriver(self):
        self.driver.get("https://www.nike.com/launch/")
        print()
        print()
        print()
        print("Cookies from Driver: ", self.driver.get_cookies())
        print()
        print()
        print()
        print()
        try: # ((By.XPATH, f'//button[contains(text(), "{self.size}")]'
            self.wait.until(EC.element_to_be_clickable((By.XPATH), '//button[contains(text()="Log In")]'))
        except Exception as err:
            print("Couldnt click login button", str(err))
        cookies = self.driver.get_cookies()
        cookie_file = open("Cookies_after_login.json", "w")
        json.dump(cookies, cookie_file)
        # cookie_file.write(json_cookies)
        print("Cookies After Login Page:", self.driver.get_cookies())
        print()
        print()
        print()
        print()
        print()
        BrowserCookies = self.driver.get_cookies()
        s = requests.Session()
        c = [s.cookies.set(c['name'], c['value']) for c in BrowserCookies]
        print("Session Cookies:", c)
        return s
        # s = requests.session()
        # # res = s.get("https://www.nike.com/launch")
        # # if res.status_code == 200:
        # res = s.get("https://www.nike.com/login")
        # if res.status_code == 200:
        #     cookies_list = s.cookies
        #     cookies_dict = s.cookies.get_dict()
            
        #     print("Cookies Dict: ", cookies_dict)
        #     print()
        #     print()
        #     print()
        #     print()

        #     print("cookies list: ", cookies_list)
        #     print()
        #     print()
        #     print()
        #     print()
        #     for cookie in cookies_list:
                
        #         driver.add_cookie(cookie)
        #     return driver
if __name__ == "__main__":
    url7 = 'https://www.nike.com/launch/t/adapt-auto-max-fireberry'
    nikeBot = NikeBot(url7, 'M 7.5', 'acrypto91@gmail.com', 'Charlie123!', False)
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"

    driver = nikeBot.setupHeadlessChrome()




    session = nikeBot.getLoginCookiesFromDriver()
    #session.headers.update({"Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"})
    global CLIENT_ID, UX_ID
    CLIENT_ID = 'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7'
    UX_ID = 'com.nike.commerce.snkrs.web'
    email = 'acrypto91@gmail.com'
    password = 'Charlie123!'  
    data = {
        'username:': email,
        'password:': password,
        'client_id': CLIENT_ID,
        'ux_id': UX_ID,
        'grant_type': 'password',
    }
    params = {
    'appVersion': '847',
    'experienceVersion': '847',
    'uxid': 'com.nike.commerce.snkrs.web',
    'locale': 'en_US',
    'backendEnvironment': 'identity',
    'browser': 'Google%20Inc.',
    'os': 'undefined',
    'mobile': 'false',
    'native': 'false',
    'visit': '1',
    'visitor': 'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7'
    }
    headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '170',
    'content-type': 'application/json',
    'origin': 'https://www.nike.com',
    'referer': 'https://www.nike.com/launch',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': user_agent,
    }
    json_data = json.dumps(data, indent=4)
    response = session.post("https://unite.nike.com/login?", headers=headers, data=json_data, params=params)
    print()
    print()
    print()
    print()
    print(response.status_code)
    

    print()
    print()
    print()
    print()
    # print("Cookies after hitting login page: ", driver.get_cookies())
    driver.close()
            

    # def main_loop(self):
    #     #will monitor the URL & select size (new function) & finally click add to cart
    #     self.driver.get(self.url)
    #     #Scroll Window to "height" to uncover Size & add-to-cart buttons just in case they are covered;
    #     #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     #Setup While Loop, will refresh page every 10seconds (we can make this much more effecient)
    #     # We could refresh every 10-15sec but only when close to the "drop"
    #     purchaseEnabled = False
    #     while(purchaseEnabled == False):
    #         try:
    #             purchaseBtn = self.wait.until(EC.element_to_be_clickable(
    #             (By.XPATH, '//button[@data-qa="add-to-cart"]')))
    #         except (TimeoutException, NoSuchElementException) as err:
    #             # Still need to update this section with wait commands;
    #             # possible resturctor not sure if else gets executed after exceptions are raised;
    #             # since in loop can just move else statement outside of loop.
    #             # needs to do timeoutexception and restart loop if button not clickable / enabled;
    #             print(f'+[main_loop]: {str(err)}')
    #             print(f'+[main_loop]: Sleeping 10 Seconds & Refreshing the Page.')
    #             time.sleep(10)
    #             self.driver.refresh()
    #             #time.sleep(1)
    #             body = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
    #             # self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
    #             body.send_keys(Keys.END)
    #             #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #             #time.sleep(1) #i havent found a better way to wait after running javascript 
    #         except ElementClickInterceptedException as err:
    #             self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
    #         except Exception as err:
    #             print("+[main_loop]: ", str(err))
            
    #         else:
    #             print("+[main_loop]: Purchase Button Clickable")
    #             if purchaseBtn.is_enabled(): # makes sure its enabled & clickable;
    #                 print("+[main_loop]: Purchase Button Enabled")
    #                 purchaseEnabled = True # exit loop
    #                 return self.select_size()
        

    # def select_size(self):
    #     try:
    #         sizeBtn = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
    #         sizeBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
    #         if (sizeBtn):
    #             try:
    #                 self.actions.move_to_element(sizeBtn).click(sizeBtn).perform()
    #                 # sizeBtn = self.wait.until(
    #                 #         lambda driver: driver.execute_script("arguments[0].scrollIntoView(true);", sizeBtn)
    #                 #     )
    #             except Exception as err:
    #                 print(f"+[select_size]: Error Moving To Size Element: {str(err)}")
    #             else:
    #                 print("+[select_size]: sizeBtn ready to be clicked -- taking screenshot")
    #                 # self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]'))).click()
    #                 self.driver.save_screenshot(f"{self.driver.service.process.pid}-show size clicked.png")
            
    #     except Exception as err:
    #         #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         self.close()
    #         return print(f"+[select_size]: Error Selecting Size, Is it available? {str(err)}")
    #     else:
    #         print("+[select_size]: Size Selected")
    #         return self.add_to_cart()

    # def add_to_cart(self):
    #     try:
    #         print("+[add_to_cart]: made it to add_to_cart")
    #         add2cartBtn = self.wait.until(EC.element_to_be_clickable(
    #             (By.XPATH, '//button[@data-qa="add-to-cart"]')))
    #         try:
    #             self.actions.move_to_element(add2cartBtn).click(add2cartBtn).perform()
    #         except Exception as err:
    #             print("+[add_to_cart]: error moving to add to cart button", str(err))
    #             self.driver.execute_script("arguments[0].scrollIntoView(true);", add2cartBtn)
    #             print("+[add_to_cart]: scrolled into view successful")
    #             self.wait.until(EC.element_to_be_clickable(
    #                 (By.XPATH, '//button[@data-qa="add-to-cart"]'))).click()
    #     except Exception as err:
    #         print(f'+[add-to-cart]: {err}')
    #         return self.close()
    #     else:
    #         return self.go_to_cart()

    # def go_to_cart(self):
    #     # click iframe popup that says checkout;
    #     print("+[go_to_cart]: made it to go_to_cart")
        
    #     try:
    #         self.driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
    #         self.driver.save_screenshot(f"{self.driver.service.process.pid} checkout-popup.png")
    #         self.wait.until(EC.element_to_be_clickable(
    #             (By.XPATH, '//button[contains(text(), "Checkout")]'))).click()
    #         print("+[go_to_cart]: cart button on pop-up found, clicking")

    #     except Exception as err:
    #         print(f"+[go_to_cart]: {str(err)}")
    #         return self.close()
    #     else:
    #         return self.check_out()
                
    # def close(self):
    #     return self.driver.close() # self.session_id

    # def check_out(self):
    #     # member or guest checkout;
    #     self.driver.save_screenshot(f"{self.driver.service.process.pid} checkout.png")
    #     if type(self.guest_checkout) is dict:
    #         print("+[check_out]: Going to guest checkout")
    #         return self.check_out_as_guest()
    #     else:
    #         return self.check_out_as_member()

    # def check_out_as_member(self):
    #     #We're on the page that ask's whether you want to login or checkout as guest now;
    #     print("+[check_out_as_member]: made it to check_out_as_member")
    #     try: #fill in username
    #         self.wait.until(EC.visibility_of_element_located(
    #             (By.XPATH, '//input[@data-componentname="emailAddress"]'))).send_keys(self.username)
    #         #self.driver.find_element_by_xpath('//input[@data-componentname="emailAddress"]').send_keys(self.username)
    #     except Exception as err:
    #         print(f"+[check_out_as_member]: Visibility of Email Input Element Not Found: {err}")
    #         return self.close()
    #     else:
    #         self.driver.find_element_by_xpath('//input[@data-componentname="password"]').send_keys(self.password)
    #         self.driver.save_screenshot(f"{self.driver.service.process.pid}-before clicking login.png")
    #         self.wait.until(EC.visibility_of_element_located(
    #             (By.XPATH, '//input[@value="MEMBER CHECKOUT"]'))).click()
    #         #self.driver.find_element_by_xpath('//input[@value="MEMBER CHECKOUT"]').click()
    #         self.driver.save_screenshot(f"{self.driver.service.process.pid}-after clicking login.png")
    #         return

    # def check_out_as_guest(self):
    #     #We're on the page that ask's whether you want to login or checkout as guest now;
    #     print("+[check_out_as_guest]: made it to checkout as guest")
    #     # print("PAGE SOURCE: ")
    #     # print(self.driver.page_source)
    #     try:
    #         guestCheckoutBtn = self.wait.until(EC.visibility_of_element_located(
    #                 (By.ID, 'qa-guest-checkout')))
            
    #     except TimeoutException as err:
    #         try:
    #             self.wait.until(EC.element_to_be_clickable(
    #                 (By.ID, 'qa-guest-checkout-mobile'))).click()
    #             # self.wait.until(EC.element_to_be_clickable(
    #             #     (By.XPATH, '//*[@id="qa-guest-checkout"'))).click()
    #         except Exception as err:
    #             print("+[check_out_as_guest]: TimeoutException: Neither regular or mobile guest checkout button was found", str(err))
    #             return self.close()
    #         else:
    #             print("+[check_out_as_guest]: WE FOUND THE MOBILE BUTTON")
            
    #     except Exception as err:
    #         print("+[check_out_as_guest]: ", str(err))
    #     else:
    #         guestCheckoutBtn.click()

    #         # guest_keys = {
    #         #     "FirstName" : "John",
    #         #     "LastName" : "Doe",
    #         #     "Address1" : "2400 harbor blvd",
    #         #     "Address2" : "apt 2",
    #         #     "City" : "costa mesa",
    #         #     "State" : "California",
    #         #     "Zip" :   "92626",
    #         #     "Email" : "nowaythisisarealnikeemail@gmail.com",
    #         #     "PhoneNumber" : "123456789",
    #         #     "CreditCardNumber": "1234567812345678",
    #         #     "ExpDate" : "0822",
    #         #     "CVC" : "682"
    #         # }

    #         #input first name
    #         self.wait.until(EC.visibility_of_element_located(
    #             (By.XPATH, '//input[@id="firstName"]'))).send_keys(self.guest_checkout['FirstName'])
            
    #         #input last name
    #         self.wait.until(EC.element_to_be_clickable(
    #             (By.XPATH, '//input[@id="lastName"]'))).send_keys(self.guest_checkout['LastName'])

    #         self.wait.until(EC.element_to_be_clickable(
    #             (By.XPATH, '//a[@id="addressSuggestionOptOut"]'))).click()

    #         #start to fill in address
    #         self.wait.until(EC.element_to_be_clickable(
    #             (By.XPATH, '//input[@id="address1"]'))).send_keys(self.guest_checkout['Address1'])
            
    #         #fill in city
    #         self.wait.until(EC.element_to_be_clickable(
    #             (By.XPATH, '//input[@id="city"]'))).send_keys(self.guest_checkout['City'])
        
    #         #select state from drop down
    #         myselect = Select(self.driver.find_element_by_id('state'))
    #         #select visible text / state
    #         myselect.select_by_visible_text(self.guest_checkout['State'])
            
    #         #enter zip code
    #         self.driver.find_element_by_xpath('//input[@id="postalCode"]').send_keys(self.guest_checkout['Zip'])
            
    #         #enter email address
    #         self.driver.find_element_by_xpath('//input[@id="email"]').send_keys(self.guest_checkout['Email'])
            
    #         #enter phone number
    #         self.driver.find_element_by_xpath('//input[@id="phoneNumber"]').send_keys(self.guest_checkout['PhoneNumber'])
    #         #screen shot to make sure info was entered
    #         self.driver.save_screenshot(f"{self.driver.service.process.pid}-entered everything but cc.png")
    #         #click continue after entering address
    #         # //*[@id="shipping"]/div/div[2]/form/div/div/div/div[2]/button
    #         print("+[check_out_as_guest]: trying to click save & continue")
    #         self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="shipping"]/div/div[2]/form/div/div/div/div[2]/button' ))).click()
    #         print("+[check_out_as_guest]: save & continue button clicked")
    #         #click continue to payment information
    #         try:
    #             # waited until shipping div was visible & then waited until the button was clickable and clicked it;
    #             self.wait.until(EC.visibility_of_element_located((By.ID, 'shipping')))
    #             button = self.wait.until(EC.element_to_be_clickable(
    #                 (By.XPATH, '//button[@class="js-next-step continuePaymentBtn mod-ncss-btn ncss-btn-accent ncss-brand mod-button-width pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg u-md-ib u-uppercase u-rounded fs14-sm"]')
    #             )).click()
    #             print("+[check_out_as_guest]: ContinuePaymentBtn is clicked")
    #         except Exception as err:
    #             print(f"+[check_out_as_guest]: Couldn't Find Continue Btn: {str(err)}")
    #             return self.close()
    #         else:
    #             try:
    #                 self.wait.until(EC.frame_to_be_available_and_switch_to_it(
    #                     (By.XPATH,"//iframe[@class='credit-card-iframe mt1 u-full-width prl2-sm']")))
    #             except Exception as err:
    #                 self.driver.save_screenshot(f"{self.driver.service.process.pid}-after clicking contBtn.png")
    #                 print(self.driver.page_source)
    #                 print("+[check_out_as_guest]: Couldn't switch to credit card iFrame --headless;")
    #             else:
    #                 ccNumField = self.wait.until(EC.visibility_of_element_located(
    #                     (By.XPATH, "//input[@id='creditCardNumber']"))).send_keys(self.guest_checkout['CreditCardNumber'])
    #             # self.wait.until(ccNumField)
    #             # self.wait.until(self.driver.execute_script("arguments[0].scrollIntoView(true);", ccNumField))
    #                 self.wait.until(EC.visibility_of_element_located(
    #                     (By.XPATH, "//input[@id='expirationDate']"))).send_keys(self.guest_checkout['ExpDate'])
    #                 self.wait.until(EC.visibility_of_element_located(
    #                     (By.XPATH, "//input[@id='cvNumber']"))).send_keys(self.guest_checkout['CVC'])
    #                 self.driver.save_screenshot(f"{self.driver.service.process.pid}-all done.png")
    #             print("+[check_out_as_guest]: all done")
    #             # time.sleep(25)
    #             return True

# if __name__ == '__main__':
#     url1 = 'https://www.nike.com/launch/t/air-max-triax-96-university-red/'
#     url2 = 'https://www.nike.com/launch/t/sb-dunk-high-paul-rodriguez/'  #no checkout button available until 1/21 @ 8am;
#     url3 = 'https://www.nike.com/launch/t/kyrie-7-creator'
#     url4 = 'https://www.nike.com/launch/t/air-jordan-1-high-black-gym-red/'
#     url5 = 'https://www.nike.com/launch/t/air-jordan-1-metallic-gold' #no checkout button until 11/30 @ 8am;
#     url6 = 'https://www.nike.com/launch/t/air-force-1-high-goretex-boot-wheat'
#     url7 = 'https://www.nike.com/launch/t/adapt-auto-max-fireberry'
#     url8 = 'https://www.nike.com/launch/t/air-force-1-high-gore-tex-boot-anthracite'
#     url9 = 'https://www.nike.com/launch/t/kybrid-s2-best-of'

#     size = 'M 10'
#     login_username = 'email@email.com' # email to login @ nike.com
#     login_temp_pass = 'Password!'        # password to login
#     #test1= NikeBot(url1, size, login_username, login_temp_pass, True )
#     # test2= NikeBot(url2, size, login_username, login_temp_pass )
#     guest_keys = {
#         "FirstName" : "John",
#         "LastName" : "Doe",
#         "Address1" : "2400 harbor blvd",
#         "Address2" : "apt 2",
#         "City" : "costa mesa",
#         "State" : "California",
#         "Zip" :   "92626",
#         "Email" : "nowaythisisarealnikeemail@gmail.com",
#         "PhoneNumber" : "1234567895",
#         "CreditCardNumber": "1234567812345678",
#         "ExpDate" : "0822",
#         "CVC" : "682"
#     }
#     #startTime to calculate checkout time length;
#     startTime = time.time()
#     #test3= NikeBot(url3, 'M 6.5', login_username, login_temp_pass, guest_keys )
#     #test3= NikeBot(url8, 'M 10', login_username, login_temp_pass, guest_keys )
#     # test3= NikeBot(url7, 'M 10', login_username, login_temp_pass, guest_keys )
#     # test3= NikeBot(url4, size, login_username, login_temp_pass )
#     test3= NikeBot(url8, size, login_username, login_temp_pass, guest_keys )
    

#     try:
#         #test1.main_loop()
#         test3.main_loop()
#     except:
#         #test1.close()
#         test3.close()
        
#     else:
#         #test1.close()
#         test3.close()
#     print("+[main]: Code Ran Successfully")
#     execTime = (time.time() - startTime)
#     print('+[main]: Execution Time in Seconds: ' + str(execTime))
    # test3.close()
    # test4.close()

    # test3= NikeBot(url3, 'M 7.5', login_username, login_temp_pass )
    # test3.main_loop()
    # test3.close()

    # test4= NikeBot(url4, size, login_username, login_temp_pass )
    # test4.main_loop()
    # test4.close()
    #test.close()