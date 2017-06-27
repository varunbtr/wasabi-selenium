from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from overview import Overview
from groups import Groups
from users import Users
from accesskeys import Keys
command_executor = "http://127.0.0.1:4444/wd/hub"
import time
import common
import base

class OverviewTest(unittest.TestCase):

	def setUp(self):
		self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
		self.driver.get(common.URL)
		self.login_page = LoginPage(self.driver).open()
		self.login_page.login(common.USERNAME,common.PASSWORD)
		self.groups_page = Groups(self.driver).open()
		self.users_page = Users(self.driver)
		self.key_page = Keys(self.driver).open()
		self.overview_page = Overview(self.driver).open()
		print('Welcome to Wasabi Overview page tests')

	def test_alias(self):

		self.overview_page.editAlias('alias')

		self.users_page.logOut()
		self.login_page = LoginPage(self.driver).open()
		file_page = self.login_page.login('alias','password')

		self.assertTrue("file_manager" in self.driver.current_url,'Console user did not sign in, TEST FAIL')

		#Personoalized clean up, log back in to root main acount 
		self.users_page.open()
		self.users_page.logOut()
		self.login_page.login(common.USERNAME,common.PASSWORD) 


	def tearDown(self):
		#self.groups_page.deleteAllGroups()
		#self.users_page.deleteAllUsers()
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
