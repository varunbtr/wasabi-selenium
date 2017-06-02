from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from po.loginpage import LoginPage
class Login(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://localhost/console")

    def test_user_login(self):
        login_page = LoginPage(self.driver)
        login_page.login('vbatra@ba.com','password')
        #filemanager_page = login_page.submit()
        #assert filemanager_page.is_title_matches(), "File Manager"

    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    unittest.main()