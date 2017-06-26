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
		self.login_page = LoginPage(self.driver).open()
		self.login_page.login(common.USERNAME,common.PASSWORD)
		self.groups_page = Groups(self.driver).open()
		self.users_page = Users(self.driver)

		self.groups = []
		print('Welcome to Wasabi Users page tests')
	
	def test_createUser_with_console(self):
		self.users_page.open()
		print("Create user with CONSOLE access")

		self.users_page.createUser('bolak2','console')

		self.users_page.logOut()
		login_page = LoginPage(self.driver).open()
		file_page = login_page.login(common.USERNAME,'password','bolak2')

		self.assertTrue("file_manager" in self.driver.current_url,'Console user did not sign in, TEST FAIL')

		#Personoalized clean up, log back in to root main acount 
		self.users_page.logOut()
		self.login_page.login(common.USERNAME,common.PASSWORD) 

	
	def test_createUser_with_api(self):
		self.users_page.open()
		print("Create user with API access")

		accessKey , secretKey = self.users_page.createUser('bolak2','API')

		self.assertIsNotNone(accessKey, 'accessKey does not exist')
		self.assertIsNotNone(secretKey, 'secretKey does not exist')

	
	def test_createUser_with_group(self):
		self.users_page.open()
		print("Create user with console access and group 'group-1' ")

		self.groups_page.createGroup('group-1')

		self.users_page.createUser('bolak2','console','group-1')
		table = self.users_page.getUserGroups('bolak2')

		self.assertTrue("group-1" in table,'User does not have requested group, TEST FAIL')

	
	def test_createUser_with_policy(self):
		self.users_page.open()
		print("Create user with console access and polics 'WasabiFullAccess' ")

		self.users_page.createUser('bolak2','console','none','WasabiFullAccess')

		table = self.users_page.getGroupPermissions('bolak2')

		self.assertTrue('WasabiFullAccess' in table,'User does not have requested policy, TEST FAIL')

		self.groups_page.open()
		self.groups_page.deleteGroup('group-1')	
	
	
	def test_creat_many_users(self, count = 5):
		self.users_page.open()

		print("Create 5 users")
		for i in range(count):
			self.users_page.createUser('bolak'+str(i),'console')
		table = self.users_page.getUsers()

		self.assertTrue(len(table) == count,'Number of users does not match nuumber requested, TEST FAIL')


	
	def test_add_group_to_user(self):
		self.users_page.open()
		print('Add bolak2 to group group-1')

  		self.groups_page.createGroup('group-1')	

		self.users_page.open()
		self.users_page.createUser('bolak2','console','none')

		self.users_page.addUserToGroup('bolak2','group-1')

		table = self.users_page.getUserGroups('bolak2')

		self.assertTrue("group-1" in table,'group-1 does not exists, TEST FAIL')
		self.groups_page.open()
		self.groups_page.deleteGroup('group-1')	
	
			
	def test_delete_user_group(self):
		self.users_page.open()
		print('Remove bolak2 from group group-1')

  		self.groups_page.createGroup('group-1')	

		self.users_page.open()
		self.users_page.createUser('bolak2','console','group-1')

		self.users_page.deleteUserGroup('bolak2','group-1')

		table = self.users_page.getUserGroups('bolak2')

		self.assertTrue("group-1" not in table,'Group still exists, TEST FAIL')

		self.groups_page.open()
		self.groups_page.deleteGroup('group-1')	
	
	def test_add_policy_to_user(self):
		self.users_page.open()
		print('Add WasabiFullAccess to bolak2')

		self.users_page.createUser('bolak2','console')

		self.users_page.addUserPermission('bolak2','WasabiFullAccess')

		table = self.users_page.getGroupPermissions('bolak2')

		self.assertTrue("WasabiFullAccess" in table,'Policy not attachhed to user, TEST FAIL')

	def test_delete_policiy_to_user(self):
		self.users_page.open()
		print('Delete WasabiFullAccess policy for bolak2')

		self.users_page.createUser('bolak2','console','none','WasabiFullAccess')

		self.users_page.deleteUserPermission('bolak2','WasabiFullAccess')

		table = self.users_page.getGroupPermissions('bolak2')

		self.assertTrue("WasabiFullAccess" not in table,'User Policy not deleted, TEST FAIL')

	

	def test_change_user_name(self):
		self.users_page.open()
		print('Change user name bolak2 to bolak3')

		self.users_page.createUser('bolak2','console')
 		self.users_page.editUserName('bolak2','bolak3')
		print('changed bolak2 to bolak3')

		table = self.users_page.getUsers()		
		
		self.assertTrue("bolak3" in table,'User bolak3 does not exist, TEST FAIL')

		
	def tearDown(self):
		self.users_page.deleteAllUsers()

		#self.groups_page.deleteAllGroups()

		self.driver.close()

if __name__ == "__main__":
	unittest.main()
