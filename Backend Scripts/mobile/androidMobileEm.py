import unittest
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from login_details import PASSWORD, USERNAME
# class PlaystoreLocators: 
#     PLAYSTORE_PACKAGE_NAME = 'com.android.vending' 
#     SEARCH_BAR_BOX = (By.ID, PLAYSTORE_PACKAGE_NAME+':id/search_bar_hint') 
#     SEARCH_BAR_BOX_TEXT_INPUT = (By.ID, PLAYSTORE_PACKAGE_NAME+':id/search_bar_text_input') 
#     COCCOC_BROWSER_ITEM_SEARCH_RESULT = (By.XPATH, '//android.widget.FrameLayout[contains(@content-desc, "Cốc Cốc Browser")]') 
#     INSTALL_BUTTON = (By.ID, PLAYSTORE_PACKAGE_NAME+':id/right_button') 
#     OPEN_BUTTON = (By.XPATH, '//android.widget.Button[contains(@text, "Open")][@clickable="true"]')

# class PlayStoreElements:

#     def find_search_box_playstore(self, driver: webdriver.Remote, ):
#         return self.wait_for_element(driver=driver).until(
#             EC.visibility_of_element_located(PlaystoreLocators.SEARCH_BAR_BOX))

#     def find_search_box_text_input(self, driver: webdriver.Remote, ):
#         return self.wait_for_element(driver=driver).until(EC.presence_of_element_located(PlaystoreLocators.SEARCH_BAR_BOX_TEXT_INPUT))

#     def find_coccoc_browser_item_search_result(self, driver: webdriver.Remote, ):
#         return self.wait_for_element(driver=driver).until(EC.presence_of_element_located(PlaystoreLocators.COCCOC_BROWSER_ITEM_SEARCH_RESULT))

#     def find_install_button(self, driver: webdriver.Remote, ):
#         return self.wait_for_element(driver=driver).until(EC.presence_of_element_located(PlaystoreLocators.INSTALL_BUTTON))

#     def find_open_button(self, driver: webdriver.Remote, ):
#         return self.wait_for_element(driver=driver, timeout=80).until(EC.presence_of_element_located(PlaystoreLocators.OPEN_BUTTON))
global DELAY
DELAY = 30

class SnkrsAndroidTest(unittest.TestCase):

    def setup(self):
        desired_caps = {} 
        desired_caps['platformName'] = 'Android' 
        desired_caps['platformVersion'] = '11' 
        desired_caps['deviceName'] = 'Pixel 4' 
        desired_caps['noReset'] = 'true' 
        desired_caps['appPackage'] = 'com.nike.snkrs' 
        desired_caps['appActivity'] = 'com.nike.snkrs.feed.activities.TheWallActivity'

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.wait = WebDriverWait(self.driver, DELAY)
        
    def tearDown(self):
        self.driver.quit()

    def test_storeBtnClick(self):
        # 
        #   CLICKING STORE BUTTON FROM HOME SCREEN (JUST TURNED ON)
        #
        try:
            storeBtn = self.driver.find_element_by_android_uiautomator('new UISelector().textContains("Play Store")')
        except Exception as e:
            print("Coudlnt find play store button", str(e))
            self.driver.quit()
        else:
            storeBtn.click()
        
    
    
        try:
            #storeBtn = self.driver.find_element_by_android_uiautomator('new UISelector().textContains("Sign In")')
            signinBtn = self.wait.until(EC.visibility_of_element_located('new UISelector().textContains("Sign In")'))
        except:
            print("couldnt see button")
        else:
            sBtn  = self.driver.find_element_by_class_name("android.widget.Button")
        try:
            email_input = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "android.widget.EditText")))
        except:
            print("couldnt find email_input")
        else:
            email_input.send_keys(USERNAME)
            sBtn.click()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SnkrsAndroidTest)
    unittest.TextTestRunner(verbosity=2).run(suite)