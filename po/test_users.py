from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from users import Users
command_executor = "http://127.0.0.1:4444/wd/hub"
import time
import common
import base

class UsersTest(unittest.TestCase):

	def setUp(self):
		self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
		self.driver.get(common.URL)
		login_page = LoginPage(self.driver).open()
		login_page.login(common.USERNAME,common.PASSWORD)


	def testusers(self):
		users_page = Users(self.driver).open()
		time.sleep(2)

		users_page.editUserName('Alice','test')
		time.sleep(2)
		print("home")




	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
