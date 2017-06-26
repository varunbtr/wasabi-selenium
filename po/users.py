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

locators = {
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
	consolePassword = Text(locators['console_password'])
	userName = Text(locators['user_name'])
	UserNameText = AutoComplete(locators['add_newUser_to_group'])
	addPolicyToGroup = AutoComplete(locators['add_policy_to_group'])
	userToGroup = AutoComplete(locators['add_user_to_group'])

	def wait_until_loaded(self):
		self.wait_for_available(locators['create_user'])
		return self


	def open(self):
		self.driver.get(self.url)
		return self.wait_until_loaded()

	def createUser(self,user,user_type ='API',newGroup='none',userPolicy='none'):
		self.open()

		if self.driver.is_visible(locators['user']+user):
			print("user exists")
			return
 
		self.find_element_by_locator(locators['create_user']).click()

		if self.driver.is_visible(locators['create_another_user_btn']):
			self.find_element_by_locator(locators['create_another_user_btn']).click()

		#Details
		self.userName = user
		if (user_type == 'API'):
			self.find_element_by_locator(locators['programmatic']).click()
			#print('API')
		else:
			self.find_element_by_locator(locators['console']).click()
			self.consolePassword = "password"
			self.find_element_by_locator(locators['password_reset_box']).click()
			#print("console")
		self.find_elements_by_locator(locators['next'])[-1].click()

		#Group
		self.wait_for_hidden(locators['programmatic'])
		self.wait_for_visible(locators['create_a_new_group_btn'])
		if newGroup == 'none':
			print("no group")
		else: 
			self.wait_for_visible(locators['add_newUser_to_group'])
			self.UserNameText = newGroup
			#if group doesnt exist create new group, a warning catcher would help
		self.find_elements_by_locator(locators['next'])[-1].click()

		#Policy
		self.sleep(1)
		if userPolicy == 'none':
			print("no policy")
		else:
			self.wait_for_visible(locators['add_newUser_to_group'])
			self.UserNameText = userPolicy

		self.find_elements_by_locator(locators['next'])[-1].click()
			
		#Review
		self.find_elements_by_locator(locators['next'])[-1].click()

		if user_type == 'console':
			#Return to user page
			self.wait_for_visible(locators['check_success'])
			self.wait_for_visible(locators['close_review'])
			self.find_element_by_locator(locators['close_review']).click()
			self.wait_for_visible(locators['user']+user)
			print('user '+ user +' created')
			return 

		#Get access keys for API
		self.wait_for_visible(locators['show_secret_key'])
		self.find_element_by_locator(locators['show_secret_key']).click()
		accessKey = self.find_elements_by_locator(locators['access_key'])[0].text
		secretKey = self.find_elements_by_locator(locators['access_key'])[1].text

		#Return to user page
		self.find_elements_by_locator(locators['close_btn'])[-1].click()
		self.wait_for_visible(locators['user']+user)
		print('user '+ user +' created')
		return  accessKey , secretKey
		

	def selectUser(self,user):
		self.find_element_by_locator(locators['user']+user).click()


	def deleteUser(self,user):
		self.open()
		try: 
			self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
			if self.driver.is_element_available(locators['user']+user):
				self.find_element_by_locator(locators['user']+user).click()
				self.wait_for_visible(locators['delete_user_button'])
				self.find_element_by_locator(locators['delete_user_button']).click()

				#when in pop up screen
				self.wait_for_visible(locators['confirm_delete'])
				while self.driver.is_visible(locators['confirm_delete']):			#janky fix
					self.find_element_by_locator(locators['confirm_delete']).click()
				self.wait_for_hidden(locators['confirm_delete'])

				# Sometimes it fails to delete because of policies, this will make thh ecode try again
				if self.driver.is_visible(locators['create_user']):
					#self.wait_for_visible(locators['create_user'])
					print(user + ' deleted')
				else:
					print("DELETE BUTTON ERROR")
					self.deleteUser(user)

			else:
				print(user + " does not exist")
	        except TimeoutException:
			print("table empty") 

	def deleteAllUsers(self):
		self.open()
		try: 
			self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])

			while self.driver.is_visible(locators['USERS_LIST_TABLE_ROWS']):
				self.find_elements_by_locator(locators['USERS_LIST_TABLE_ROWS'])[0].click()
				self.wait_for_visible(locators['delete_user_button'])
				self.find_element_by_locator(locators['delete_user_button']).click()

				#when in pop up screen
				self.wait_for_visible(locators['confirm_delete'])
				while self.driver.is_visible(locators['confirm_delete']):			#janky fix
					self.find_element_by_locator(locators['confirm_delete']).click()
				self.wait_for_hidden(locators['confirm_delete'])

				# Sometimes it fails to delete because of policies, this will make thh ecode try again
				if self.driver.is_visible(locators['create_user']):
					continue
				else:
					Users(self.driver).open()
					print("DELETE BUTTON ERROR")
					self.deleteAllUsers()

			else:
				print("All users deleted")

	        except TimeoutException:
			print("table has no users")
	

	def findUser(self,user):
		header = ['Name' , 'Path','ARN','Created on']
		for rows in self.find_elements_by_locator(locators['USERS_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(locators['USERS_LIST_TABLE_COLMS'])
			col_text = colms[0].text
			print col_text
			if col_text == user:
				return colms[0]
				break
			else:
				raise TimeoutException('Failed to locate user '
					'value {!r}'.format(attr_val))	

	def getUsers(self):
			table = []
			for rows in self.find_elements_by_locator(locators['USERS_LIST_TABLE_ROWS']):
				colms = rows.find_elements_by_locator(locators['USERS_LIST_TABLE_COLMS'])
				col_text = colms[0].text
				table.append(col_text)
			return table
				
	
	'''SETTINGS FUNCTIONS'''
	def editUserName(self,user,newName ):
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_settings']).click()

		#Enter text
		self.userName = "clear()"
		self.userName = newName
		#refresh the page
		self.find_element_by_locator(locators['user_settings']).click()


		#press next 
		self.find_element_by_locator(locators['update']).click()

		#Return to user page
		Users(self.driver).open()
				

	'''GROUP PAGE FUNCTIONS'''
	def addUserToGroup(self,user,newGroup):
		self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
		if self.driver.is_element_available(locators['user']+user):
			self.find_element_by_locator(locators['user']+user).click()
			self.find_element_by_locator(locators['user_groups_page']).click()

			#Enter text
			self.wait_for_available(locators['add_user_to_group'])
			self.userToGroup = newGroup
			print("User added")
		else:
			print(user + " does not exist")
	
		#Return to user page
		Users(self.driver).open()
				

		
	
	def deleteUserGroup(self,user,group):
		self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
		if self.driver.is_element_available(locators['user']+user):
			self.find_element_by_locator(locators['user']+user).click()
			self.find_element_by_locator(locators['user_groups_page']).click()
			self.wait_for_available(locators['add_user_to_group'])

			#Search for Group
			index = 0
			for bubbles in self.find_elements_by_locator(locators['GROUPS_BUBBLES']):
				if bubbles.text == group :
					self.find_elements_by_locator(locators['GROUPS_SVG'])[index].click()
					print("Deleted")
					Users(self.driver).open()
				index+=1
			print("User does not exist")

		else:
			print(user + " does not exist")
	
		#Return to user page
		Users(self.driver).open()
		

	
	def getUserGroups(self,user):
		self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
		if self.driver.is_element_available(locators['user']+user):
			self.find_element_by_locator(locators['user']+user).click()
			self.find_element_by_locator(locators['user_groups_page']).click()
			self.wait_for_available(locators['add_user_to_group'])

			#Return table of group users
			table = []
			for bubbles in self.find_elements_by_locator(locators['GROUPS_BUBBLES']):
				table.append(bubbles.text)
		
		else:
			print(user + " does not exist")

		return table	
	

	'''CONTROL ACCESS FUNCTIONS'''
	'''API ACCESS FUNCTIONS'''

	'''PERMISSION FUNCTIONS'''
	
	def addUserPermission(self,user,permission):
		self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
		if self.driver.is_element_available(locators['user']+user):
			self.find_element_by_locator(locators['user']+user).click()
			self.find_element_by_locator(locators['user_permission_page']).click()
			self.wait_for_available(locators['add_policy_to_group'])

			#Enter permission
			self.addPolicyToGroup = permission
			print("permission added")

		else:
			print(user + " does not exist")

		Users(self.driver).open()
	
	def deleteUserPermission(self,user,permission):
		self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
		if self.driver.is_element_available(locators['user']+user):
			self.find_element_by_locator(locators['user']+user).click()
			self.find_element_by_locator(locators['user_permission_page']).click()
			self.wait_for_available(locators['add_policy_to_group'])

			#Search for permission
			index = 0
			for bubbles in self.find_elements_by_locator(locators['PERMISSION_BUBBLES']) :
				if bubbles.text == permission :
					self.find_elements_by_locator(locators['PERMISSION_SVG'])[index].click()
					Users(self.driver).open()
					return
				index+=1
			print("Permission does not exist")

		else:
			print(user + " does not exist")

		Users(self.driver).open()


	def getGroupPermissions(self,user):
		self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
		if self.driver.is_element_available(locators['user']+user):
			self.find_element_by_locator(locators['user']+user).click()
			self.find_element_by_locator(locators['user_permission_page']).click()
			self.wait_for_available(locators['add_policy_to_group'])
		
			#Return table of group permissions
			table = []
			#self.wait_for_available(locators['PERMISSION_BUBBLES']
			for bubbles in self.find_elements_by_locator(locators['PERMISSION_BUBBLES']) :
				table.append(bubbles.text)
		else:
			print(user + " does not exist")
		Users(self.driver).open()
		return table


	#log out
	def logOut(self):
		self.find_element_by_locator(locators['options_button']).click()
		self.wait_for_available(locators['logout'])
		self.find_element_by_locator(locators['logout']).click()



