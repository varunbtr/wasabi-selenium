from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from filemanager import FileManagerPage
command_executor = "http://127.0.0.1:4444/wd/hub"
import time
import common
import base

class FileManagerTest(unittest.TestCase):

    def setUp(self):
        self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
        self.driver.get("https://localhost/console")
        login_page = LoginPage(self.driver).open()
        login_page.login(common.USERNAME,common.PASSWORD)

    def testgroups(self):
        filemanager_page = FileManagerPage(self.driver).open()
        bucketlist = filemanager_page.getBucketList()
        print bucketlist
        filemanager_page.openBucket('vbatratest')
        time.sleep(20)
        common.check_error(self)


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()