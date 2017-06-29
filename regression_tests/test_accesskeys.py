from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from groups import Groups
from users import Users
from accesskeys import Keys
command_executor = "http://127.0.0.1:4444/wd/hub"
import time
import common
import base

class KeyTest(unittest.TestCase):

	def setUp(self):
		self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
		self.driver.get(common.URL)
		login_page = LoginPage(self.driver).open()
		login_page.login(common.USERNAME,common.PASSWORD)
		self.users_page = Users(self.driver)
		self.groups_page = Groups(self.driver).open()
		self.key_page = Keys(self.driver).open()
		print('Welcome to Wasabi Access Keys page tests')

	def test_create_key(self):
		print("Create Key")

		accessKey , secretKey = self.key_page.createKey()

		table = self.key_page.getKeys()

		self.assertIsNotNone(accessKey in table, 'accessKey does not exist')

	def test_delete_key(self):
		print("Delete a specific key")

		accessKey , secretKey = self.key_page.createKey()
		accessKey , secretKey = self.key_page.createKey()

		self.key_page.deleteKey(accessKey)

		table = self.key_page.getKeys()
		self.assertIsNotNone(accessKey not in table, 'accessKey does exist')

	def test_get_user_key(self):
		print("get keys that belong to bolak2")	

		self.users_page.open()
		accessKey , secretKey = self.users_page.createUser('bolak2','API')

		self.key_page.open()
		table = self.key_page.getUserKeys('bolak2')

		self.assertIsNotNone(accessKey in table, 'accessKey does not exist')

	def test_delete_user_deletes_key(self):
		print("Check if deleting bolak2 deletes its key")	

		self.users_page.open()
		accessKey , secretKey = self.users_page.createUser('bolak2','API')
		self.users_page.deleteUser('bolak2')

		self.key_page.open()
		table = self.key_page.getKeys()

		self.assertIsNotNone(accessKey not in table, 'accessKey does exist')				
				
	

	def tearDown(self):
		self.key_page.deleteAllKeys()
		self.groups_page.deleteAllGroups()
		self.users_page.deleteAllUsers()
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
