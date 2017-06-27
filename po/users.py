#from driver import webdriver
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
#import driver
import base 
from controls.autocomplete import AutoComplete

LOCATORS = {
	'iam_btn': "css=button[data-e2e='tn-overview']",
	'create_bucket': "css=button[data-e2e='bucket-cta']",
	'USERS_LIST_TABLE_ROWS': 'css=.ReactVirtualized__Grid__innerScrollContainer .ReactVirtualized__Table__row',
	'USERS_LIST_TABLE_COLMS': 'css=.ReactVirtualized__Table__rowColumn',
	'options_button':'id=topNavOptions',
	'profile':'id=profile',
	'switch_role':'id=switchRoles',
	'logout':'id=logout',

	'users':"css=a[href='#/users'] span",
	'groups':"css=a[href='#/groups']",
	'acccess_key':"css=a[href='#/access_keys']",
	'policies':"css=a[href='#/policies']",
	'roles':"css=a[href='#/roles']",

	'table':'css=.ReactVirtualized__Table',
	'user': 'id=user-',
	'create_user': "css=button[data-e2e='user-cta']",

	'programmatic': 'name=ApiAccess',
	'console': 'name=ConsoleAccess',
	'console_password': 'name=Password',
	'password_reset_box':'name=PasswordResetRequired',
	'next': 'css=.custom-scroll .Box button',


	'create_a_new_group_btn': 'css=.custom-scroll .Flex .Flex button',
	'add_newUser_to_group': 'css=.custom-scroll .Flex input',

	'check_success':"xpath=//div[@class='custom-scroll']/div/div/div/div/div/div[@class='Flex']/div[@class='Box']/p",
	'close_review':"xpath=//div[@class='Flex']/span",

	'show_secret_key': 'css=.Flex .Box._lr-hide a',
	'access_key':'css=.Flex .Box._lr-hide code',
	'secret_key':'css=.Flex .Box._lr-hide',
	'close_btn':'css=.Flex .Box button',

	'create_another_user_btn':'css=.custom-scroll .Flex button',
 
	'delete_user_button': 'css=.Flex .Box button span.material-icons',
	'confirm_delete':"css=button[data-e2e='confirmBtn']",

	'user_settings':'id=user-settings',
	'user_name' : 'name=UserName',
	'user_path': 'name=Path',
	'update': "css=button[type='submit']",

	'user_groups_page': 'id=user-groups',
	'add_user_to_group': "id=add-user-to-group",
	'GROUPS_BUBBLES': "css=div[aria-hidden='false'] .Flex .Box span",
	'GROUPS_SVG': "css=div[aria-hidden='false'] .Flex .Box",

	'user_console': 'id=user_console',

	'user_api': 'id=user-api',

	'user_permission_page': 'id=user-permissions',
	'add_policy_to_group': "css=div[aria-hidden='false'] input",
	'PERMISSION_BUBBLES': "css=div[aria-hidden='false'] .Flex .Box",
	'PERMISSION_SVG': "css=div[aria-hidden='false'] .Flex .Box span",
	}

class Users(BasePage):
	url = common.URL + '#/users'
	consolePassword = Text(LOCATORS['console_password'])
	userName = Text(LOCATORS['user_name'])
	UserNameText = AutoComplete(LOCATORS['add_newUser_to_group'])
	addPolicyToGroup = AutoComplete(LOCATORS['add_policy_to_group'])
	userToGroup = AutoComplete(LOCATORS['add_user_to_group'])

	def wait_until_loaded(self):
		self.wait_for_available(LOCATORS['create_user'])
		return self


	def open(self):
		self.driver.get(self.url)
		return self.wait_until_loaded()

	def createUser(self,user,user_type ='API',newGroup='none',userPolicy='none'):
		self.open()

		if self.driver.is_visible(LOCATORS['user']+user):
			print("user exists, deleting existing user")
			self.deleteUser(user)
 
		self.find_element_by_locator(LOCATORS['create_user']).click()
		
		if self.driver.is_visible(LOCATORS['create_another_user_btn']):
			self.find_element_by_locator(LOCATORS['create_another_user_btn']).click()
		
		#Details
		self.userName = user
		if (user_type == 'API'):
			self.find_element_by_locator(LOCATORS['programmatic']).click()
			#print('API')
		else:
			self.find_element_by_locator(LOCATORS['console']).click()
			self.consolePassword = "password"
			self.find_element_by_locator(LOCATORS['password_reset_box']).click()
			#print("console")
		self.find_elements_by_locator(LOCATORS['next'])[-1].click()

		#Group
		self.wait_for_hidden(LOCATORS['programmatic'])
		self.wait_for_visible(LOCATORS['create_a_new_group_btn'])
		if newGroup == 'none':
			print("no group")
		else: 
			self.wait_for_visible(LOCATORS['add_newUser_to_group'])
			self.UserNameText = newGroup
			#if group doesnt exist create new group, a warning catcher would help
		self.find_elements_by_locator(LOCATORS['next'])[-1].click()

		#Policy
		self.sleep(1)
		if userPolicy == 'none':
			print("no policy")
		else:
			self.wait_for_visible(LOCATORS['add_newUser_to_group'])
			self.UserNameText = userPolicy

		self.find_elements_by_locator(LOCATORS['next'])[-1].click()
			
		#Review
		self.find_elements_by_locator(LOCATORS['next'])[-1].click()

		if user_type == 'console':
			#Return to user page
			self.wait_for_visible(LOCATORS['check_success'])
			self.wait_for_visible(LOCATORS['close_review'])
			self.find_element_by_locator(LOCATORS['close_review']).click()
			self.wait_for_visible(LOCATORS['user']+user)
			print('user '+ user +' created')
			return 

		#Get access keys for API
		self.wait_for_visible(LOCATORS['show_secret_key'])
		self.find_element_by_locator(LOCATORS['show_secret_key']).click()
		accessKey = self.find_elements_by_locator(LOCATORS['access_key'])[0].text
		secretKey = self.find_elements_by_locator(LOCATORS['access_key'])[1].text

		accessKey = accessKey.split('\n')[0]
		secretKey = secretKey.split('\n')[0]

		#Return to user page
		self.find_elements_by_locator(LOCATORS['close_btn'])[-1].click()
		self.wait_for_visible(LOCATORS['user']+user)
		print('user '+ user +' created')
		return  accessKey , secretKey
		

	def selectUser(self,user):
		self.checkUsersTable()

		self.find_element_by_locator(LOCATORS['user']+user).click()


	def deleteUser(self,user):
		self.checkUsersTable()

		if self.driver.is_element_available(LOCATORS['user']+user):
			self.find_element_by_locator(LOCATORS['user']+user).click()
			self.wait_for_visible(LOCATORS['delete_user_button'])
			self.find_element_by_locator(LOCATORS['delete_user_button']).click()

			#when in pop up screen
			self.wait_for_visible(LOCATORS['confirm_delete'])
			while self.driver.is_visible(LOCATORS['confirm_delete']):			#janky fix
				self.find_element_by_locator(LOCATORS['confirm_delete']).click()
			self.wait_for_hidden(LOCATORS['confirm_delete'])

			# Sometimes it fails to delete because of policies, this will make thh ecode try again
			if self.driver.is_visible(LOCATORS['create_user']):
				#self.wait_for_visible(LOCATORS['create_user'])
				print(user + ' deleted')
			else:
				print("DELETE BUTTON ERROR")
				self.deleteUser(user)
		else:
			print(user + " does not exist")

	def deleteAllUsers(self):
		#self.checkUsersTable()

		while self.driver.is_visible(LOCATORS['USERS_LIST_TABLE_ROWS']):
			self.find_elements_by_locator(LOCATORS['USERS_LIST_TABLE_ROWS'])[0].click()
			self.wait_for_visible(LOCATORS['delete_user_button'])
			self.find_element_by_locator(LOCATORS['delete_user_button']).click()

			#when in pop up screen
			self.wait_for_visible(LOCATORS['confirm_delete'])
			while self.driver.is_visible(LOCATORS['confirm_delete']):			#janky fix
				self.find_element_by_locator(LOCATORS['confirm_delete']).click()
			self.wait_for_hidden(LOCATORS['confirm_delete'])

			# Sometimes it fails to delete because of policies, this will make the code try again
			if self.driver.is_visible(LOCATORS['create_user']):
				continue
			else:
				Users(self.driver).open()
				print("DELETE BUTTON ERROR")
				self.deleteAllUsers()

		else:
			print("All users deleted")
	

	def findUser(self,user):
		header = ['Name' , 'Path','ARN','Created on']
		for rows in self.find_elements_by_locator(LOCATORS['USERS_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(LOCATORS['USERS_LIST_TABLE_COLMS'])
			col_text = colms[0].text
			print col_text
			if col_text == user:
				return colms[0]
				break
			else:
				raise TimeoutException('Failed to locate user '
					'value {!r}'.format(attr_val))	

	def getUsers(self):
		self.checkUsersTable()
	
		table = []
		for rows in self.find_elements_by_locator(LOCATORS['USERS_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(LOCATORS['USERS_LIST_TABLE_COLMS'])
			col_text = colms[0].text
			table.append(col_text)
		return table
				
	
	'''SETTINGS FUNCTIONS'''
	def editUserName(self,user,newName):
		self.checkUsersTable()

		self.find_element_by_locator(LOCATORS['user']+user).click()
		self.find_element_by_locator(LOCATORS['user_settings']).click()

		#Enter text
		self.userName = "clear()"
		self.userName = newName
		#refresh the page
		self.find_element_by_locator(LOCATORS['user_settings']).click()


		#press next 
		self.find_element_by_locator(LOCATORS['update']).click()

		#Return to user page
		Users(self.driver).open()
				

	'''GROUP PAGE FUNCTIONS'''
	def addUserToGroup(self,user,newGroup):
		self.checkUsersTable()

		if self.driver.is_element_available(LOCATORS['user']+user):
			self.find_element_by_locator(LOCATORS['user']+user).click()
			self.find_element_by_locator(LOCATORS['user_groups_page']).click()

			#Enter text
			self.wait_for_available(LOCATORS['add_user_to_group'])
			self.userToGroup = newGroup
			print("User added")
		else:
			print(user + " does not exist")
	
		#Return to user page
		Users(self.driver).open()
				

		
	
	def deleteUserGroup(self,user,group):
		self.checkUsersTable()

		if self.driver.is_element_available(LOCATORS['user']+user):
			self.find_element_by_locator(LOCATORS['user']+user).click()
			self.find_element_by_locator(LOCATORS['user_groups_page']).click()
			self.wait_for_available(LOCATORS['add_user_to_group'])

			#Search for Group
			index = 0
			for bubbles in self.find_elements_by_locator(LOCATORS['GROUPS_BUBBLES']):
				if bubbles.text == group :
					self.find_elements_by_locator(LOCATORS['GROUPS_SVG'])[index].click()
					print("Deleted")
					Users(self.driver).open()
				index+=1
			print("User does not exist")
	
		#Return to user page
		Users(self.driver).open()
		

	
	def getUserGroups(self,user):
		self.checkUsersTable()

		if self.driver.is_element_available(LOCATORS['user']+user):
			self.find_element_by_locator(LOCATORS['user']+user).click()
			self.find_element_by_locator(LOCATORS['user_groups_page']).click()
			self.wait_for_available(LOCATORS['add_user_to_group'])

			#Return table of group users
			table = []
			for bubbles in self.find_elements_by_locator(LOCATORS['GROUPS_BUBBLES']):
				table.append(bubbles.text)
		
		else:
			print(user + " does not exist")

		return table	
	

	'''CONTROL ACCESS FUNCTIONS'''
	'''API ACCESS FUNCTIONS'''

	'''PERMISSION FUNCTIONS'''
	
	def addUserPermission(self,user,permission):
		self.checkUsersTable()

		if self.driver.is_element_available(LOCATORS['user']+user):
			self.find_element_by_locator(LOCATORS['user']+user).click()
			self.find_element_by_locator(LOCATORS['user_permission_page']).click()
			self.wait_for_available(LOCATORS['add_policy_to_group'])

			#Enter permission
			self.addPolicyToGroup = permission
			print("permission added")

		else:
			print(user + " does not exist")

		Users(self.driver).open()
	
	def deleteUserPermission(self,user,permission):
		self.checkUsersTable()

		if self.driver.is_element_available(LOCATORS['user']+user):
			self.find_element_by_locator(LOCATORS['user']+user).click()
			self.find_element_by_locator(LOCATORS['user_permission_page']).click()
			self.wait_for_available(LOCATORS['add_policy_to_group'])

			#Search for permission
			index = 0
			for bubbles in self.find_elements_by_locator(LOCATORS['PERMISSION_BUBBLES']) :
				if bubbles.text == permission :
					self.find_elements_by_locator(LOCATORS['PERMISSION_SVG'])[index].click()
					Users(self.driver).open()
					return
				index+=1
			print("Permission does not exist")

		else:
			print(user + " does not exist")

		Users(self.driver).open()


	def getGroupPermissions(self,user):
		self.checkUsersTable()

		if self.driver.is_element_available(LOCATORS['user']+user):
			self.find_element_by_locator(LOCATORS['user']+user).click()
			self.find_element_by_locator(LOCATORS['user_permission_page']).click()
			self.wait_for_available(LOCATORS['add_policy_to_group'])
		
			#Return table of group permissions
			table = []
			for bubbles in self.find_elements_by_locator(LOCATORS['PERMISSION_BUBBLES']) :
				table.append(bubbles.text)
		else:
			print(user + " does not exist")
		Users(self.driver).open()
		return table


	#log out
	def logOut(self):
		self.wait_for_available(LOCATORS['options_button'])
		self.find_element_by_locator(LOCATORS['options_button']).click()
		self.wait_for_available(LOCATORS['logout'])
		self.find_element_by_locator(LOCATORS['logout']).click()

	#Check if groups on table
	def checkUsersTable(self):
		self.open()
		try: 
			self.wait_for_available(LOCATORS['USERS_LIST_TABLE_ROWS'])
		except TimeoutException:
			print("table has no groups")



