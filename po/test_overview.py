from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from overview import Overview
command_executor = "http://127.0.0.1:4444/wd/hub"
import time
import common
import base

class OverviewTest(unittest.TestCase):

	def setUp(self):
		self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
		self.driver.get(common.URL)
		login_page = LoginPage(self.driver).open()
		login_page.login('testing+ali@wasabi.com','password')

	def testoverview(self):
		overview_page = Overview(self.driver).open()

		overview_page.editAlias('temp3')

		time.sleep(2)

		print("Overview")
		
		#common.check_error(self)

	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
