from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from groups import Groups
from users import Users
command_executor = "http://127.0.0.1:4444/wd/hub"
import time
import common
import base

class GroupTest(unittest.TestCase):

	def setUp(self):
		self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
		self.driver.get(common.URL)
		login_page = LoginPage(self.driver).open()
		login_page.login(common.USERNAME,common.PASSWORD)
		self.users_page = Users(self.driver)
		self.groups_page = Groups(self.driver).open()
		print('Welcome to Wasabi Groups page tests')

	def test_create_group(self):
		print('Creating Group group-1')

		self.groups_page.createGroup('group-1')
	
		table = self.groups_page.getGroupList()

		self.assertTrue('group-1' in table,'group-1 does not exist, TEST FAIL')


	def test_delete_group(self):
		print('Delete Group group-1')

		self.groups_page.createGroup('group-1')

		self.groups_page.deleteGroup('group-1')
	
		table = self.groups_page.getGroupList()

		self.assertTrue("group-1" not in table,'group-1 does exist, TEST FAIL')



	def test_add_user_to_group(self):
		print('Add User bolak2 to group group-1')
		
		self.users_page.open()
		self.users_page.createUser('bolak2','console')

		self.groups_page.open()
		self.groups_page.createGroup('group-1')

		self.groups_page.addUsertoGroup('group-1','bolak2')

		table = self.groups_page.getGroupUsers('group-1')

		self.assertTrue("bolak2" in table,'bolak2 has not been added to group-1, TEST FAIL')

	

	def test_delete_group_user(self):
		print('Delete User bolak2 from group group-1')

		self.groups_page.createGroup('group-1')

		self.users_page.open()
		self.users_page.createUser('bolak2','console','group-1')

		self.groups_page.open()
		self.groups_page.deleteGroupUser('group-1','bolak2')

		table = self.groups_page.getGroupUsers('group-1')
		print(table)
		self.assertTrue("bolak2" not in table,'bolak2 has not been deleted from group-1, TEST FAIL')

	
	def test_add_policy_to_group(self):
		print('Add policy WasabiFullAcess to group group-1')

		self.groups_page.createGroup('group-1')

		self.groups_page.addPermissionToGroup('group-1','WasabiFullAccess')

		table = self.groups_page.getGroupPermissions('group-1')

		self.assertTrue("WasabiFullAccess" in table,'WasabiFullAcess is not in group-1, TEST FAIL')		


	
	
	def test_delete_group_policy(self):
		print('Delete policy WasabiFullAcess to group group-1')
		self.groups_page.createGroup('group-1')

		self.groups_page.addPermissionToGroup('group-1','WasabiFullAccess')

		self.groups_page.deleteGroupPermission('group-1','WasabiFullAccess')

		table = self.groups_page.getGroupPermissions('group-1')

		self.assertTrue("WasabiFullAccess" not in table,'WasabiFullAcess is not in group-1, TEST FAIL')

			
		

	def tearDown(self):
		self.groups_page.deleteAllGroups()
		self.users_page.deleteAllUsers()
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
