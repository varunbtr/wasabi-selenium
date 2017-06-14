from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    ElementNotVisibleException,
    InvalidElementStateException,
    ElementNotSelectableException,
    TimeoutException
)
import base
import common
from base import BasePage
from controls.text import Text
import time
import driver
import base 

locators = {
	'menu': 'class=iconContainer-0-7',
	'iam_btn': "css=button[data-e2e='tn-overview']",
	'create_bucket': "css=button[data-e2e='bucket-cta']",
	'USERS_LIST_TABLE_ROWS': 'css=.ReactVirtualized__Grid__innerScrollContainer .ReactVirtualized__Table__row',
	'USERS_LIST_TABLE_COLMS': 'css=.ReactVirtualized__Table__rowColumn',
	'option_button':'id=topNavOptions',
	'profile':'id=profile',
	'switch_role':'id=switchRoles',
	'logout':'id=logout',

	'users':"css=a[href='#/users'] span",
	'groups':"css=a[href='#/groups']",
	'acccess_key':"css=a[href='#/access_keys']",
	'policies':"css=a[href='#/policies']",
	'roles':"css=a[href='#/roles']",

	'user': 'id=user-',
	'create_user': "css=button[data-e2e='user-cta']",

	'programmatic': 'name=ApiAccess',
	'console': 'ConsoleAccess',
	'console_password': 'name=Password',
	'next': 'css=.custom-scroll .Box button',	
	'next2': 'css =.custom-scroll .Box button',	# doesnt work [2]

	'user_settings':'id=user-settings',
	'user_name' : 'name=UserName',
	'user_path': 'name=Path',
	'update': "css=button[type='submit']",

	'user_groups': 'id=user-groups',
	'add_user_to_group': 'id=add-user-to-group',
	'GROUPS_LIST': "css=div[aria-hidden='false'] span",
	'group_svg': "css=div[tabindex='0']",

	'user_console': 'id=user_console',

	'user_api': 'id=user-api',

	'user_permission': 'user-permissions',
	'attach_policy': '',
	}

class Users(BasePage):
	url = common.URL + '#/users'
	consolePassword = Text(locators['console_password'])
	userName = Text(locators['user_name'])
	userToGroup = Text(locators['add_user_to_group'])

	def wait_until_loaded(self):
		self.wait_for_available(locators['create_user'])
		return self


	def open(self):
		self.driver.get(self.url)
		return self.wait_until_loaded()

	
	def createUser(self,user,API):
		self.find_element_by_locator(locators['create_user']).click()

		self.userName = user

		#With API
		if(API == 1):
			self.find_element_by_locator(locators['programmatic']).click()
		#Console
		else:
			self.find_element_by_locator(locators['console']).click()
			consolePassword = "password"
			print("console")
		self.find_elements_by_locator(locators['next'])[1].click()
		print("next")
		time.sleep(2)

		self.find_element_by_locator(locators['next2']).click()		#invalid locator
		print("next")
		time.sleep(2)
		

	def selectUser(self,user):
		self.find_element_by_locator(locators['user']+user).click()
		
	#Once you pick a group 

	#Settings
	def editUserName(self,user,newName ):
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_settings']).click()
		self.userName = "clear()"
		self.userName = newName
		time.sleep(2)

		#refresh the page
		self.find_element_by_locator(locators['user_settings']).click()
		time.sleep(2)
		#press next 
		self.find_element_by_locator(locators['update']).click()

		#Return to user page
		return Users(self.driver).open()
				

	#Groups
	'''
	def setUserToGroup(self,user,newGroup):
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_groups']).click()
		self.userToGroup = newGroup
		#figure out how to select a text box 
	'''
	def deleteGroup(self,user):
		#Click on box with name of user
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_groups']).click()
		time.sleep(2)

		# Use get from span to find the group then use that index to click on its svg
		self.find_elements_by_locator(locators['group_svg'])[0].click()

		#Return to user page
		Users(self.driver).open()
		

	'''
	def getGroups(self,user):
		#Click on box with name of user
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_groups']).click()
		time.sleep(2)

		print(locators['GROUPS_LIST'])
		#iterate through the list of users
		
		#somethhings wrong with these bubbles
		d = {}
		print(self.find_elements_by_locator(locators['user_groups']))
		print(len(self.find_elements_by_locator(locators['user_groups'])))
		for colms in self.find_elements_by_locator(locators['user_groups']):
			print(colms) 
			#col_text = colms.get(colms)
			#print(col_text)
			#print(col_text)
			#d[header[index]] = col_text
		#print(d)

		#Return to user page
		Users(self.driver).open()
		return d
	'''

	#Console Access
	#API Access

	#Permisions
	'''
	#def setGroupPermissions(self,permission):
		#click on permisions tab
		self.find_element_by_locator(locators['group_permissions']).click()
		#Check to see if permsion is in the list 
		#if so click on it 

		#if not enter it 
		self.permissionName = permission + "/n"

	def deleteGroupPermission(self):
		#click on permisions tab
		self.find_element_by_locator(locators['group_permissions']).click()
		#click on span with permision we are looking for


	#def getGroupPermissions(self,permission):
		#click on permisions tab
		self.find_element_by_locator(locators['group_permissions']).click()
		#retrieve spans containing group permsions - loop through the table of spans 	
	'''



