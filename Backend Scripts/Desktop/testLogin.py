from setupheadlesschrome import setupHeadlessChrome
from selenium.webdriver.common.action_chains import ActionChains


driver = setupHeadlessChrome(headless=False)
driver.get("https://www.nike.com/launch")


dLoginDict = {}
for cookie in dLoginCookies:
    type(cookie)
    dLoginDict.update({cookie['name']:cookie['value']})


passInput = driver.find_element_by_xpath('//input[@data-componentname="password"]').send_keys("Charlie123!")

emailInput = driver.find_element_by_xpath('//input[@data-componentname="emailAddress"]').send_keys("acrypto91@gmail.com")