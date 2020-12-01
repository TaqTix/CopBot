import unittest
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from login_details import PASSWORD, USERNAME

global DELAY
DELAY = 30

class SnkrsAndroidTest():
    def __init__(self):
        desired_caps = {} 
        desired_caps['platformName'] = 'Android' 
        desired_caps['platformVersion'] = '11' 
        desired_caps['deviceName'] = 'Pixel 4' 
        desired_caps['noReset'] = 'true' 
        desired_caps['appPackage'] = 'com.nike.snkrs' 
        desired_caps['appActivity'] = 'com.nike.snkrs.feed.activities.TheWallActivity'

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.wait = WebDriverWait(self.driver, DELAY)
        
    # def tearDown(self):
    #     self.driver.quit()

    def test_snkrsLogin(self):
        try:
            loginBtn = self.wait.until(EC.visibility_of_element_located((By.ID, "com.nike.snkrs:id/loginButton")))
        except Exception as e:
            print("Couldnt find login button", str(e))
        else:
            loginBtn.click()

        try:
            # emailInput = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "android.widget.EditText")))
            emailInput = self.driver.find_element_by_class_name("android.widget.EditText")
        except Exception as e:
            print("Couldnt find email input", str(e))
        else:
            emailInput.send_keys(USERNAME)

        try:
            passwordInput = self.driver.find_element_by_android_uiautomator('new UISelector().textContains("Password")')
        except Exception as e:
            print("Couldnt find password input")
        else:
            passwordInput.send_keys(PASSWORD)

        try:
            SignInBtn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "android.widget.Button")))
        except Exception as e:
            print("Couldnt click sign in button")
        else:
            SignInBtn.click()

if __name__ == '__main__':
    SnkrsAndroidTest()