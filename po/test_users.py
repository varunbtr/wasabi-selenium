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
	'''

	def test_createUser_with_console(self):
		users_page = Users(self.driver).open()
		print("Create user with CONSOLE access")

		users_page = users_page.deleteUser('bolak2')
		users_page = users_page.createUser('bolak2','console')
		users_page = users_page.logOut()
		login_page = LoginPage(self.driver).open()
		file_page = login_page.login(common.USERNAME,'password','bolak2')

		if "file_manager" in self.driver.current_url:
			print('success') 
		else:
			print('FAIL') 

	
	def test_createUser_with_api(self):
		users_page = Users(self.driver).open()
		print("Create user with API access")

		users_page = users_page.deleteUser('bolak2')
		users_page, accessKey , secretKey = users_page.createUser('bolak2','API')

		print(accessKey)
		print(secretKey)
		print('success')

	
	def test_createUser_with_group(self):
		users_page = Users(self.driver).open()
		print("Create user with console access and group 'group-1' ")

		users_page = users_page.deleteUser('bolak2')
		users_page = users_page.createUser('bolak2','console','group-1')
		users_page, table = users_page.getUserGroups('bolak2')

		print(table)
		if "group-1" in table:
			print('success') 
		else:
			print('FAIL') 

	
	def test_createUser_with_policy(self):
		users_page = Users(self.driver).open()
		print("Create user with console access and polics 'WasabiFullAccess' ")

		users_page = users_page.deleteUser('bolak2')
		users_page = users_page.createUser('bolak2','console','none','WasabiFullAccess')

		users_page,table = users_page.getGroupPermissions('bolak2')
		print(table)
		if 'WasabiFullAccess' in table:
			print('success')
		else:
			print('FAIL') 


	def test_deleteUser_with_no_users(self):
		users_page = Users(self.driver).open()
		users_page = users_page.deleteUser('bolak2')




	'''


		
	def test_deleteAllUsers(self):
		users_page = Users(self.driver).open()
		users_page = users_page.deleteAllUsers()

	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
