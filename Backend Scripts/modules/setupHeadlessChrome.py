from selenium.webdriver.chrome.options import Options
from selenium import webdriver


global delay
delay = 30

def setupHeadlessChrome(mobile=False):       
    # open webdriver, incognito & start maximized
    chrome_options = Options()
    # Setup chrome options for better performance / less issues with elements in the way
    # headless browser = No UI = Less Resources;
    chrome_options.add_argument('--headless')
    # incognito for no leftover cookies, will need to load cookies on after every request & refresh page to acutally send them
    chrome_options.add_argument('--incognito')
    # mobile user agent = Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1
    if(mobile==False):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    else:
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1'
    # user agent for desktop chrome browser (google search what is my user agent for yours)
    # user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"
    chrome_options.add_argument(f'user-agent={user_agent}')
    # disable infobars
    chrome_options.add_argument('disable-infobars')
    # disable extensions
    chrome_options.add_argument('--disable-extensions')
    # disable sandbox to Bypass OS security Model
    chrome_options.add_argument('--no-sandbox')
    # use maximzied when not using headless
    #chrome_options.add_argument('start-maximized')
    # chrome_options.add_argument('--window-size=1920,1080')
    if(mobile):
        chrome_options.add_argument('--window-size=375,812')
    chrome_options.add_argument('--window-size=1500,800')
    # do not verify ssl
    chrome_options.add_argument('verify_ssl="False"')
    # ignore certificate errors
    chrome_options.add_argument('ignore-certificate-errors')
    # applicable to windows os only
    chrome_options.add_argument('--disable-gpu')
    if (mobile):
        #Mobile emulation; not working for login, login using regular browser, grab session cookies & pass to mobile;
        mobile_emulation = { 
            "deviceName": "iPhone X"
            #"deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            #"userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/86.0.4240.93 Mobile/15E148 Safari/604.1"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
    driver = webdriver.Chrome(executable_path='Backend Scripts\\chromedriver.exe', 
                        options=chrome_options) #, seleniumwire_options={'verify_ssl': False}
    # Modifying Headers for headless version
    # allow_origin = url.split("/")[2] # grabs just www.nike.com
    # driver.header_overrides = {
    #     'Access-Control-Allow-Origin': f'{allow_origin}',
    #     'SameSite': 'True',
    # } 
    # session_id = driver.session_id
    # #driver.implicitly_wait(1)
    # wait = WebDriverWait(driver, delay)
    # actions = ActionChains(driver)
    # driver.set_page_load_timeout(delay)
    return driver