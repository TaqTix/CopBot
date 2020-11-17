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

startTime = time.time()

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
        
        # open webdriver, incognito & start maximized
        chrome_options = Options()
        # Setup chrome options for better performance / less issues with elements in the way
        # headless browser = No UI = Less Resources;
        # chrome_options.add_argument('--headless')
        # incognito for no leftover cookies
        chrome_options.add_argument('--incognito')
        # user agent for desktop chrome browser (google search what is my user agent for yours)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        # disable infobars
        chrome_options.add_argument('disable-infobars')
        # disable extensions
        chrome_options.add_argument('--disable-extensions')
        # disable sandbox to Bypass OS security Model
        chrome_options.add_argument('--no-sandbox')
        # use maximzied when not using headless
        #chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('--window-size=1920,1080')
        # do not verify ssl
        chrome_options.add_argument('verify_ssl="False"')
        # ignore certificate errors
        chrome_options.add_argument('ignore-certificate-errors')
        # applicable to windows os only
        chrome_options.add_argument('--disable-gpu')
        
        # https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
        self.driver = webdriver.Chrome(executable_path='Backend Scripts\\chromedriver.exe', 
                            options=chrome_options) #, seleniumwire_options={'verify_ssl': False}
        #Modifying Headers for headless version
        self.driver.header_overrides = {
            'Access-Control-Allow-Origin': f'{self.url}',
            'SameSite': 'True',
        }
        self.session_id = self.driver.session_id
        #self.driver.implicitly_wait(1)
        self.wait = WebDriverWait(self.driver, delay)
        self.actions = ActionChains(self.driver)
        
    def main_loop(self):
        #will monitor the URL & select size (new function) & finally click add to cart
        self.driver.get(self.url)
        #Scroll Window to "height" to uncover Size & add-to-cart buttons just in case they are covered;
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #Setup While Loop, will refresh page every 10seconds (we can make this much more effecient)
        # We could refresh every 10-15sec but only when close to the "drop"
        purchaseEnabled = False
        while(purchaseEnabled == False):
            try:
                purchaseBtn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa="add-to-cart"]')))
            except Exception as err:
                # Still need to update this section with wait commands;
                # possible resturctor not sure if else gets executed after exceptions are raised;
                # since in loop can just move else statement outside of loop.
                # needs to do timeoutexception and restart loop if button not clickable / enabled;

                print(f'+[main_loop]: {str(err)}')
                print(f'+[main_loop]: Sleeping 10 Seconds & Refreshing the Page.')
                time.sleep(10)
                self.driver.refresh()
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1) #i havent found a better way to wait after running javascript  
            else:
                print("Purchase Button Clickable")
                if purchaseBtn.is_enabled():
                    print("Purchase Button Enabled")
                    purchaseEnabled = True
                    return self.select_size()
        

    def select_size(self):

        try:
            sizeBtn = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
            sizeBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]')))
            if (sizeBtn):
                try:
                    self.actions.move_to_element(sizeBtn).click(sizeBtn).perform()
                    # sizeBtn = self.wait.until(
                    #         lambda driver: driver.execute_script("arguments[0].scrollIntoView(true);", sizeBtn)
                    #     )
                except Exception as err:
                    print(f"+[select_size]: Error Moving To Size Element: {str(err)}")
                else:
                    print("+[select_size]: sizeBtn ready to be clicked -- taking screenshot")
                    # self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{self.size}")]'))).click()
                    self.driver.save_screenshot(f"{self.driver.service.process.pid}-show size clicked.png")
            
        except Exception as err:
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.close()
            return print(f"+[select_size]: Error Selecting Size, Is it available? {str(err)}")
        else:
            print("+[select_size]: Size Selected")
            return self.add_to_cart()

    def add_to_cart(self):
        try:
            print("+[add_to_cart]: made it to add_to_cart")
            add2cartBtn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa="add-to-cart"]')))
            try:
                self.actions.move_to_element(add2cartBtn).click(add2cartBtn).perform()
            except Exception as err:
                print("+[add_to_cart]: error moving to add to cart button", str(err))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add2cartBtn)
                print("+[add_to_cart]: scrolled into view successful")
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@data-qa="add-to-cart"]'))).click()

            # if (add2cartBtn):
            #     print("add to cart btn clickable, scrolling & clicking...")
            #     try: 
            #         self.actions.move_to_element(add2cartBtn).perform()
            #     except Exception as err:
            #         print(f"+[add_to_cart]: Couldn't Move to Element: {str(err)}")
            #     else:
            #         add2cartBtn.click()
            #         self.driver.save_screenshot(f"{self.driver.service.process.pid} add2cartBtn clicked.png")
        except Exception as err:
            print(f'+[add-to-cart]: {err}')
            return self.close()
        else:
            return self.go_to_cart()

    def go_to_cart(self):
        # click iframe popup that says checkout;
        print("+[go_to_cart]: made it to go_to_cart")
        
        try:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
            self.driver.save_screenshot(f"{self.driver.service.process.pid} checkout-popup.png")
            # cart_button = self.wait.until(EC.frame_to_be_available_and_switch_to_it(
            #     (By.XPATH, '//button[contains(text(), "Checkout")]')))
            #if (cart_button): 
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Checkout")]'))).click()
            #self.actions.move_to_element(cart_button).perform()
            print("+[go_to_cart]: cart button found, clicking")

        except Exception as err:
            print(f"+[go_to_cart]: {str(err)}")
            return self.close()
        else:
            return self.check_out()
                
    def close(self):
        return self.driver.close() # self.session_id

    def check_out(self):
        # member or guest checkout;
        self.driver.save_screenshot(f"{self.driver.service.process.pid} checkout.png")
        #time.sleep(2) #time to let frame popup
        if type(self.guest_checkout) is dict:
            print("+[check_out]: Going to guest checkout")
            return self.check_out_as_guest()
        else:
            return self.check_out_as_member()

    def check_out_as_member(self):
        #We're on the page that ask's whether you want to login or checkout as guest now;
        print("+[check_out_as_member]: made it to check_out_as_member")
        try: #fill in username
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//input[@data-componentname="emailAddress"]'))).send_keys(self.username)
            #self.driver.find_element_by_xpath('//input[@data-componentname="emailAddress"]').send_keys(self.username)
        except Exception as err:
            print(f"Login Error: {err}")
            return self.close()
        else:
            self.driver.find_element_by_xpath('//input[@data-componentname="password"]').send_keys(self.password)
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-before clicking login.png")
            self.driver.find_element_by_xpath('//input[@value="MEMBER CHECKOUT"]').click()
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-after clicking login.png")
            return 

    def check_out_as_guest(self):
        #We're on the page that ask's whether you want to login or checkout as guest now;
        print("made it to checkout as guest")
                
        # print("PAGE SOURCE: ")
        # print(self.driver.page_source)
        #time.sleep(1000)
        #time.sleep(2)
        try:
            # self.wait.until(EC.presence_of_element_located(
            #     (By.XPATH, '//*[@id="qa-guest-checkout-mobile"]/span')))
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
            # time.sleep(30)
            # //*[@id="qa-guest-checkout"]
            # //*[@id="qa-guest-checkout"]
            #//*[@id="qa-guest-checkout-mobile"]/span
            # /html/body/div/div/div[3]/div[2]/div/div/div[1]/div[1]/div/button/span
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
            print("trying to click save & continue")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="shipping"]/div/div[2]/form/div/div/div/div[2]/button' ))).click()
            print("save & continue button clickable")
            #click continue to payment information
            try:
                self.wait.until(EC.visibility_of_element_located((By.ID, 'shipping')))
                
                
                #self.driver.execute_script("arguments[0].scrollIntoView(true);", contBtn)
                button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@class="js-next-step continuePaymentBtn mod-ncss-btn ncss-btn-accent ncss-brand mod-button-width pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg u-md-ib u-uppercase u-rounded fs14-sm"]')
                )).click()
                # self.wait.until(EC.frame_to_be_available_and_switch_to_it(
                #     (By.CLASS_NAME, 'ncss-row')))

                # button = self.wait.until(EC.visibility_of_element_located(
                #     (By.XPATH, '//button[@id="shipping"]/div/div[3]/div/button')))
                #//*[@id="shipping"]/div/div[3]/div/button
                
            #  contBtn.click()
                # button = self.wait.until(EC.element_to_be_clickable(
                #     (By.CLASS_NAME, 'js-next-step continuePaymentBtn mod-ncss-btn ncss-btn-accent ncss-brand mod-button-width pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg u-md-ib u-uppercase u-rounded fs14-sm')
                # ))
                print("button is clickable")
            # self.driver.find_element_by_class_name('js-next-step continuePaymentBtn mod-ncss-btn ncss-btn-accent ncss-brand mod-button-width pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg u-md-ib u-uppercase u-rounded fs14-sm').click()
            except Exception as err:
                print(f"+[check_out_as_guest]: Couldn't Find Continue Btn: {str(err)}")
                return self.close()

            # (By.XPATH, '//button[contains(text(), "Checkout")]')))
            #now entering credit card information
            # time.sleep(2)
            else:
                # button.click()
                
                # wait for cc frame & switch to it;
                # self.wait.until(EC.frame_to_be_available_and_switch_to_it(
                #     (By.XPATH,"//iframe[@class='credit-card-iframe mt1 u-full-width prl2-sm']"))) 
                #self.actions.move_to_element(cc_iframe).perform()
                
                #time.sleep(1)
                # print(self.driver.page_source)
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
                print("all done")
                # time.sleep(25)
                return True

if __name__ == '__main__':
    url1 = 'https://www.nike.com/launch/t/air-max-triax-96-university-red/'
    url2 = 'https://www.nike.com/launch/t/sb-dunk-high-paul-rodriguez/'  #no checkout button available until 1/21 @ 8am;
    url3 = 'https://www.nike.com/launch/t/kyrie-7-creator'
    url4 = 'https://www.nike.com/launch/t/air-jordan-1-high-black-gym-red/'
    url5 = 'https://www.nike.com/launch/t/air-jordan-1-metallic-gold' #no checkout button until 11/30 @ 8am;
    url6 = 'https://www.nike.com/launch/t/air-force-1-high-goretex-boot-wheat'
    size = 'M 10'
    login_username = 'email@email.com' # email to login @ nike.com
    login_temp_pass = 'Password!'        # password to login
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

    # test3= NikeBot(url3, 'M 6.5', login_username, login_temp_pass, guest_keys )
    test3= NikeBot(url6, 'M 6.5', login_username, login_temp_pass, guest_keys )
    # test4= NikeBot(url4, size, login_username, login_temp_pass )

    try:
        #test1.main_loop()
        test3.main_loop()
    except:
        #test1.close()
        test3.close()
        return False
    else:
        #test1.close()
        test3.close()
    print("Code Ran Successfully")
    execTime = (time.time() - startTime)
    print('Execution Time in Seconds: ' + str(execTime))
    # test3.close()
    # test4.close()

    # test3= NikeBot(url3, 'M 7.5', login_username, login_temp_pass )
    # test3.main_loop()
    # test3.close()

    # test4= NikeBot(url4, size, login_username, login_temp_pass )
    # test4.main_loop()
    # test4.close()
    #test.close()