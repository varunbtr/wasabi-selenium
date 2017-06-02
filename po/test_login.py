from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
command_executor = "http://127.0.0.1:4444/wd/hub"
class Login(unittest.TestCase):

    def setUp(self):
        self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
        self.driver.get("https://localhost/console")

    def test_user_login(self):
        login_page = LoginPage(self.driver).open()
        login_page.login('vbatra@ba.com','password')
        #filemanager_page = login_page.submit()
        #assert filemanager_page.is_title_matches(), "File Manager"

    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    unittest.main()