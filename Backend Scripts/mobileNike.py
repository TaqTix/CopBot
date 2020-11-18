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
import os
from os import path
import pickle
from urllib.parse import urlparse
# if (path.exists(path.join(os.getcwd(), self.cookies_file_path))
if (path.exists(path.join(os.getcwd(), 'Backend Scripts/login_details.py'))):
    print("login file exists, importing")
    from login_details import USERNAME, PASSWORD, CVC

# This is for Nike.com/launch only & on a computer;

#GLOBAL VARS
delay = 15 #seconds -> Later, If the drops happen at specific times usually can have bot only check most
                   #frequently around then

class NikeBot:

    def __init__(self, url, size, username, password, cvc, guest_checkout):
        # only grabbing one username/password so that I can spawn multiple threads of this process for multiple profiles.
        self.url = str(url)
        self.size = str(size)
        self.username = str(username)
        self.password = str(password)
        self.cvc = str(cvc)
        self.guest_checkout = guest_checkout
        
        # open webdriver, incognito & start maximized
        self.chrome_options = Options()
        # Setup chrome options for better performance / less issues with elements in the way
        # headless browser = No UI = Less Resources;
        # self.chrome_options.add_argument('--headless')
        
        # incognito for no leftover cookies
        # self.chrome_options.add_argument('--incognito')
        
        # user agent for desktop chrome browser (google search what is my user agent for yours)
        # self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
        #chrome_options.add_argument(f'user-agent={self.user_agent}')
        # mobile_emulation = {

        # "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

        # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        # }

        # chrome_options = Options()

        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # driver = webdriver.Chrome(chrome_options = chrome_options)
        # Mobile Emulation for iOS device;
        mobile_emulation = {
            # device metrics for iPhone XS Max
        "deviceMetrics": { "width": 414, "height": 896, "pixelRatio": 3.0 },
            # user agent for iPhone XS Max with latest iOS as of 11/17/2020
            # Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1
            # user agent for iPhone XS Max up to date software (chrome);
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"
        }

        self.chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        # disable infobars
        self.chrome_options.add_argument('disable-infobars')
        # disable extensions
        self.chrome_options.add_argument('--disable-extensions')
        # disable sandbox to Bypass OS security Model 
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--disable-site-isolation-trials")
        # use maximzied when not using headless
        #chrome_options.add_argument('start-maximized')
        # chrome_options.add_argument('--window-size=1920,1080')
        # self.chrome_options.add_argument('--window-size=414,896') 
        # do not verify ssl
        self.chrome_options.add_argument('verify_ssl="False"')
        # ignore certificate errors
        self.chrome_options.add_argument('ignore-certificate-errors')
        # applicable to windows os only
        # chrome_options.add_argument('--disable-gpu')
        
        self.cookies_file_path = 'Backend Scripts/Cookies/nike_cookies.txt'

        # check violent python homework to figure out how to do this with all systems including linux; something about joining absolute path with relative path;
        if (path.exists(path.join(os.getcwd(), self.cookies_file_path)) == True):
            self.cookies = True
        else:
            self.cookies = False

        # https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
        self.driver = webdriver.Chrome(executable_path='Backend Scripts/chromedriver.exe', 
                            options=self.chrome_options) #, seleniumwire_options={'verify_ssl': False}
        # Modifying Headers for headless version
        self.driver.header_overrides = {
            'Access-Control-Allow-Origin': f'{self.url}',
            'SameSite': 'True',
        }
        self.session_id = self.driver.session_id
        #self.driver.implicitly_wait(1)
        self.wait = WebDriverWait(self.driver, delay)
        self.actions = ActionChains(self.driver)
    
    def main_loop(self):
        # checks for cookies first
        if (self.cookies) == False:
            print("+[main_loop]: logging in to get cookies")
            if(self.login_to_get_cookies()):
                print("+[main_loop]: got cookies & saved file")
            else:
                self.close()
                return print("+[main_loop]: login to get cookies failed")
      
            #will monitor the URL & select size (new function) & finally click add to cart
        self.driver.get(self.url)
        if (self.cookies) is not False:
            print("+[main_loop]: loading cookies")
            self.load_cookies()
        # looks for cookies might want this above, then close connection, reopen with cookies already; 

        #Scroll Window to "height" to uncover Size & add-to-cart buttons just in case they are covered;
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #Setup While Loop, will refresh page every 10seconds (we can make this much more effecient)
        # We could refresh every 10-15sec but only when close to the "drop"
        purchaseEnabled = False
        while(purchaseEnabled == False):
            try:
                
                purchaseBtn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa="add-to-cart"]')))
            except (TimeoutException, NoSuchElementException) as err:
                # needs to do timeoutexception and restart loop if button not clickable / enabled;
                print(f'+[main_loop]: {str(err)}')
                print(f'+[main_loop]: Sleeping 10 Seconds & Refreshing the Page.')
                time.sleep(10)
                self.driver.refresh()
                #time.sleep(1)
                body = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                # self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
                body.send_keys(Keys.END)
                #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #time.sleep(1) #i havent found a better way to wait after running javascript 
            except ElementClickInterceptedException as err:
                self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            except Exception as err:
                print("+[main_loop]: ", str(err))
            
            else:
                print("+[main_loop]: Purchase Button Clickable")
                if purchaseBtn.is_enabled(): # makes sure its enabled & clickable;
                    print("+[main_loop]: Purchase Button Enabled")
                    purchaseEnabled = True # exit loop
                    # print("we found the purchase button, moving to select size (after reprogram)")
                    return self.select_size()

    def login_to_get_cookies(self):
        parseUrl = urlparse(self.url)
        loginUrl = parseUrl.scheme + "://" + parseUrl.netloc + "/login"
        self.driver.get(loginUrl)
        print("+[login_to_get_cookies]: made it to login_to_get_cookies")
        try: #fill in username
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//input[@data-componentname="emailAddress"]'))).send_keys(self.username)
            #self.driver.find_element_by_xpath('//input[@data-componentname="emailAddress"]').send_keys(self.username)
        except Exception as err:
            print(f"+[login_to_get_cookies]: Visibility of Email Input Element Not Found: {err}")
            return self.close()
        else:
            self.driver.find_element_by_xpath('//input[@data-componentname="password"]').send_keys(self.password)
            # save screenshot for headless
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-after entering email and password.png")
            # Click Sign In Button
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//input[@value="SIGN IN"]'))).click()
            # save screenshot for headless;
            
            # self.driver.save_screenshot(f"{self.driver.service.process.pid}-after clicking login.png")
            # Create cookies file;
            #self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'title')))
            # Need to wait until page refreshes to pull cookies;
            
            while 'Login' in self.driver.title:
                print("sleeping for 1 second until page refresh to grab cookies ------------------------------------------")
                time.sleep(1)

            print("WE WAITED UNTIL PAGE REFRESH TO GRAB COOKIES")
            try:
                self.create_cookies()
            except Exception as err:
                print("Yeah hit the error")
            else:
                self.load_cookies()
                return True

    def create_cookies(self):
        # Create Cookie File (usually after login)
        with open(self.cookies_file_path, "wb") as writeFile:
            pickle.dump(self.driver.get_cookies(), writeFile)
            #filehandler.close()
        return True
    def load_cookies(self):
        # Load Cookie File;
        while not os.access(self.cookies_file_path, os.R_OK):
            print("Not Readable Yet")
            time.sleep(1)
        if(path.isfile(self.cookies_file_path)):
            print("+[load_cookies]: Cookie File Exists, Loading Cookies & Refreshing")

            with open(self.cookies_file_path, "rb") as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                #cookiesfile.close()
                self.driver.refresh() # neccessary to load cookies just loaded;

    def select_size(self):
        try:
            sizeBtn = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
            #sizeBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
            if (sizeBtn):
                try:
                    print("+[select_size]: trying to move to sizeBtn")
                    self.actions.move_to_element(sizeBtn).perform()
                    # sizeBtn = self.wait.until(
                    #         lambda driver: driver.execute_script("arguments[0].scrollIntoView(true);", sizeBtn)
                    #     )
                except Exception as err:
                    print(f"+[select_size]: Error Moving To Size Element: {str(err)}")
                # else:
                #     #print("+[select_size]: sizeBtn ready to be clicked -- taking screenshot")
                #     # self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]'))).click()
                #     # self.driver.save_screenshot(f"{self.driver.service.process.pid}-show size clicked.png")
            
        except Exception as err:
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.close()
            return print(f"+[select_size]: Error Selecting Size, Is it available? {str(err)}")
        else:
            sizeBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]'))).click()
            print("+[select_size]: Size Selected")
            return self.add_to_cart()

    def add_to_cart(self):
        print("+[add_to_cart]: Attempting to click add_to_cart button")
        try:
            add2cartBtn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa="add-to-cart"]')))
            try:
                self.actions.move_to_element(add2cartBtn).perform()
            except Exception as err:
                print("+[add_to_cart]: error moving to add to cart button", str(err))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add2cartBtn)
                print("+[add_to_cart]: scrolled into view successful")
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@data-qa="add-to-cart"]'))).click()
        except Exception as err:
            print(f'+[add-to-cart]: {err}')
            return self.close()
        else:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa="add-to-cart"]'))).click()
            
            # self.driver.save_screenshot(f"{self.driver.service.process.pid}-add to cart succesful.png")
            print("+[add_to_cart]: self.add_to_cart successful")
            return self.go_to_cart()
    def go_to_cart(self):
        # click iframe popup that says checkout;
        print("+[go_to_cart]: made it to go_to_cart")
        
        try:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
            self.driver.save_screenshot(f"{self.driver.service.process.pid} checkout-popup.png")
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Checkout")]'))).click()
            print("+[go_to_cart]: cart button on pop-up found, clicking")

        except Exception as err:
            print(f"+[go_to_cart]: {dir(err)}")
            return self.close()
        else:
            return self.check_out()
                
    def close(self):
        return self.driver.close() # self.session_id

    def check_out(self):
        # member or guest checkout;
        self.driver.save_screenshot(f"{self.driver.service.process.pid} checkout.png")
        if type(self.guest_checkout) is dict:
            print("+[check_out]: Going to guest checkout")
            return self.check_out_as_guest()
        else:
            print("+[check_out]: Going to member checkout")
            return self.check_out_as_member()

    def check_out_as_member(self):
        print("+[check_out_as_member]: Made it to checkout as member")
        time.sleep(5)
        # We're on page where we just need to fill in CVC and click 2 buttons to confirm order;
        #time.sleep(20)
        # self.driver.save_screenshot(f"{self.driver.service.process.pid} member checkout.png")
        cvc_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='cvNumber']")))
        cvc_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='cvNumber']"))).send_keys(self.cvc)
        self.driver.save_screenshot(f"{self.driver.service.process.pid} member checkout.png")
        time.sleep(35)
        return self.close()

    def check_out_as_guest(self):
        #We're on the page that ask's whether you want to login or checkout as guest now;
        print("+[check_out_as_guest]: made it to checkout as guest")
        # print("PAGE SOURCE: ")
        # print(self.driver.page_source)
        try:
            guestCheckoutBtn = self.wait.until(EC.visibility_of_element_located(
                    (By.ID, 'qa-guest-checkout')))
            
        except TimeoutException as err:
            try:
                self.wait.until(EC.element_to_be_clickable(
                    (By.ID, 'qa-guest-checkout-mobile'))).click()
                # self.wait.until(EC.element_to_be_clickable(
                #     (By.XPATH, '//*[@id="qa-guest-checkout"'))).click()
            except Exception as err:
                print("+[check_out_as_guest]: TimeoutException: Neither regular or mobile guest checkout button was found", str(err))
                return self.close()
            else:
                print("+[check_out_as_guest]: WE FOUND THE MOBILE BUTTON")
            
        except Exception as err:
            print("+[check_out_as_guest]: ", str(err))
        else:
            guestCheckoutBtn.click()

            # guest_keys = {
            #     "FirstName" : "John",
            #     "LastName" : "Doe",
            #     "Address1" : "2400 harbor blvd",
            #     "Address2" : "apt 2",
            #     "City" : "costa mesa",
            #     "State" : "California",
            #     "Zip" :   "92626",
            #     "Email" : "nowaythisisarealnikeemail@gmail.com",
            #     "PhoneNumber" : "123456789",
            #     "CreditCardNumber": "1234567812345678",
            #     "ExpDate" : "0822",
            #     "CVC" : "682"
            # }

            #input first name
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//input[@id="firstName"]'))).send_keys(self.guest_checkout['FirstName'])
            
            #input last name
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//input[@id="lastName"]'))).send_keys(self.guest_checkout['LastName'])

            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//a[@id="addressSuggestionOptOut"]'))).click()

            #start to fill in address
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//input[@id="address1"]'))).send_keys(self.guest_checkout['Address1'])
            
            #fill in city
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//input[@id="city"]'))).send_keys(self.guest_checkout['City'])
        
            #select state from drop down
            myselect = Select(self.driver.find_element_by_id('state'))
            #select visible text / state
            myselect.select_by_visible_text(self.guest_checkout['State'])
            
            #enter zip code
            self.driver.find_element_by_xpath('//input[@id="postalCode"]').send_keys(self.guest_checkout['Zip'])
            
            #enter email address
            self.driver.find_element_by_xpath('//input[@id="email"]').send_keys(self.guest_checkout['Email'])
            
            #enter phone number
            self.driver.find_element_by_xpath('//input[@id="phoneNumber"]').send_keys(self.guest_checkout['PhoneNumber'])
            #screen shot to make sure info was entered
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-entered everything but cc.png")
            #click continue after entering address
            # //*[@id="shipping"]/div/div[2]/form/div/div/div/div[2]/button
            print("+[check_out_as_guest]: trying to click save & continue")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="shipping"]/div/div[2]/form/div/div/div/div[2]/button' ))).click()
            print("+[check_out_as_guest]: save & continue button clicked")
            #click continue to payment information
            try:
                # waited until shipping div was visible & then waited until the button was clickable and clicked it;
                self.wait.until(EC.visibility_of_element_located((By.ID, 'shipping')))
                button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@class="js-next-step continuePaymentBtn mod-ncss-btn ncss-btn-accent ncss-brand mod-button-width pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg u-md-ib u-uppercase u-rounded fs14-sm"]')
                )).click()
                print("+[check_out_as_guest]: ContinuePaymentBtn is clicked")
            except Exception as err:
                print(f"+[check_out_as_guest]: Couldn't Find Continue Btn: {str(err)}")
                return self.close()
            else:
                try:
                    self.wait.until(EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH,"//iframe[@class='credit-card-iframe mt1 u-full-width prl2-sm']")))
                except Exception as err:
                    self.driver.save_screenshot(f"{self.driver.service.process.pid}-after clicking contBtn.png")
                    print(self.driver.page_source)
                    print("+[check_out_as_guest]: Couldn't switch to credit card iFrame --headless;")
                else:
                    ccNumField = self.wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//input[@id='creditCardNumber']"))).send_keys(self.guest_checkout['CreditCardNumber'])
                # self.wait.until(ccNumField)
                # self.wait.until(self.driver.execute_script("arguments[0].scrollIntoView(true);", ccNumField))
                    self.wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//input[@id='expirationDate']"))).send_keys(self.guest_checkout['ExpDate'])
                    self.wait.until(EC.visibility_of_element_located(
                        (By.XPATH, "//input[@id='cvNumber']"))).send_keys(self.guest_checkout['CVC'])
                    self.driver.save_screenshot(f"{self.driver.service.process.pid}-all done.png")
                print("+[check_out_as_guest]: all done")
                # time.sleep(25)
                print("+[main]: Code Ran Successfully")
                return True

if __name__ == '__main__':
    url1 = 'https://www.nike.com/launch/t/air-max-triax-96-university-red/'
    url2 = 'https://www.nike.com/launch/t/sb-dunk-high-paul-rodriguez/'  #no checkout button available until 1/21 @ 8am;
    url3 = 'https://www.nike.com/launch/t/kyrie-7-creator'
    url4 = 'https://www.nike.com/launch/t/air-jordan-1-high-black-gym-red/'
    url5 = 'https://www.nike.com/launch/t/air-jordan-1-metallic-gold' #no checkout button until 11/30 @ 8am;
    url6 = 'https://www.nike.com/launch/t/air-force-1-high-goretex-boot-wheat'
    url7 = 'https://www.nike.com/launch/t/adapt-auto-max-fireberry'
    url8 = 'https://www.nike.com/launch/t/air-force-1-high-gore-tex-boot-anthracite'
    url9 = 'https://www.nike.com/launch/t/kybrid-s2-best-of'

    size = 'M 10'
    login_username = USERNAME # email to login @ nike.com
    login_temp_pass = PASSWORD        # password to login
    cvc = CVC
    #test1= NikeBot(url1, size, login_username, login_temp_pass, True )
    # test2= NikeBot(url2, size, login_username, login_temp_pass )
    guest_keys = {
        "FirstName" : "John",
        "LastName" : "Doe",
        "Address1" : "2400 harbor blvd",
        "Address2" : "apt 2",
        "City" : "costa mesa",
        "State" : "California",
        "Zip" :   "92626",
        "Email" : "nowaythisisarealnikeemail@gmail.com",
        "PhoneNumber" : "1234567895",
        "CreditCardNumber": "1234567812345678",
        "ExpDate" : "0822",
        "CVC" : "682"
    }
    #startTime to calculate checkout time length;
    startTime = time.time()
    #test3= NikeBot(url3, 'M 6.5', login_username, login_temp_pass, guest_keys )
    #test3= NikeBot(url8, 'M 10', login_username, login_temp_pass, guest_keys )
    # test3= NikeBot(url7, 'M 10', login_username, login_temp_pass, guest_keys )
    # test3= NikeBot(url4, size, login_username, login_temp_pass )
    test3= NikeBot(url8, size, login_username, login_temp_pass, cvc, False )
    

    try:
        test3.main_loop()            
    except Exception as err:
        print("__main__: ", str(err))
        test3.close()
    else:
        test3.close()
        print("+[main]: Code Ran Successfully")
        execTime = (time.time() - startTime)
        print('+[main]: Execution Time in Seconds: ' + str(execTime))