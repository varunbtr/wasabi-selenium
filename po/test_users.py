from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from groups import Groups
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

		users_page = users_page.deleteUser('bolak2')
		#users_page = users_page.deleteUser('bolak3')
		#users_page = users_page.deleteUser('bolak4')

		users_page = users_page.createUser('bolak2','API','1','WasabiFullAccess')
		#users_page = users_page.createUser('bolak3','API','2','WasabiFullAccess')
		#users_page = users_page.createUser('bolak4','API','none' ,'WasabiFullAccess')

		users_page = users_page.addUserToGroup('bolak2','2')

		group_page = Groups(self.driver).open()
		temp = group_page.getGroupUsers('2')
		print(temp)

		users_page = Users(self.driver).open()
		users_page = users_page.deleteUser('bolak2')
		users_page = users_page.deleteUser('bolak3')
		users_page = users_page.deleteUser('bolak4')



	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
