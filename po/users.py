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

	'table':'css=.ReactVirtualized__Table',
	'user': 'id=user-',
	'create_user': "css=button[data-e2e='user-cta']",

	'programmatic': 'name=ApiAccess',
	'console': 'name=ConsoleAccess',
	'console_password': 'name=Password',
	'next': 'css=.custom-scroll .Box button',


	'create_a_new_group_btn': 'css=.custom-scroll .Flex .Flex button',
	'add_newUser_to_group': 'css=.custom-scroll .Flex input',

	'show_secret_key': 'css=.Flex .Box._lr-hide a',
	'access_key':'css=.Flex .Box._lr-hide code',
	'secret_key':'css=.Flex .Box._lr-hide',
	'close_btn':'css=.Flex .Box button',
 
	'delete_user_button': 'css=.Flex .Box button span.material-icons',
	'confirm_delete':"css=button[data-e2e='confirmBtn']",

	'user_settings':'id=user-settings',
	'user_name' : 'name=UserName',
	'user_path': 'name=Path',
	'update': "css=button[type='submit']",

	'user_groups_page': 'id=user-groups',
	'add_user_to_group': "css=div[aria-hidden='false'] input",
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

	def createUser(self,user,Details='API',newGroup='none',userPolicy='none'):

		self.find_element_by_locator(locators['create_user']).click()

		#Details
		print('Details')
		self.userName = user
		if (Details == 'API'):
			self.find_element_by_locator(locators['programmatic']).click()
			print('API')
		else:
			self.find_element_by_locator(locators['console']).click()
			consolePassword = "password"
			print("console")
		self.find_elements_by_locator(locators['next'])[-1].click()

		#Group
		self.wait_for_hidden(locators['programmatic'])
		self.wait_for_visible(locators['create_a_new_group_btn'])
		print("Group")
		if newGroup == 'none':
			print("no group")
		else: 
			self.wait_for_visible(locators['add_newUser_to_group'])
			self.UserNameText = newGroup
			#if group doesnt exist create new group, a warning catcher would help
		self.find_elements_by_locator(locators['next'])[-1].click()

		#Policy
		self.sleep(1)
		print("Policy")
		if userPolicy == 'none':
			print("no policy")
		else:
			self.wait_for_visible(locators['add_newUser_to_group'])
			self.UserNameText = userPolicy

		self.find_elements_by_locator(locators['next'])[-1].click()
			
		#Review
		print("Review")
		self.find_elements_by_locator(locators['next'])[-1].click()

		#Get access keys 
		self.wait_for_visible(locators['show_secret_key'])
		self.find_element_by_locator(locators['show_secret_key']).click()
		accessKey = self.find_elements_by_locator(locators['access_key'])[0].text
		secretKey = self.find_elements_by_locator(locators['access_key'])[1].text
		print(accessKey)
		print(secretKey)

		#Return to user page
		self.find_elements_by_locator(locators['close_btn'])[-1].click()
		self.wait_for_visible(locators['user']+user)
		print('user '+ user +' created')
		return Users(self.driver).open()
		

	def selectUser(self,user):
		self.find_element_by_locator(locators['user']+user).click()


	def deleteUser(self,user):
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
				Users(self.driver).open()
				self.deleteUser(user)

		else:
			print(user + " does not exist")
	
		return Users(self.driver).open()


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

	#Settings
	def editUserName(self,user,newName ):
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_settings']).click()

		#Enter text
		self.userName = "clear()"
		self.userName = newName
		#refresh the page
		self.find_element_by_locator(locators['user_settings']).click()
		time.sleep(1)

		#press next 
		self.find_element_by_locator(locators['update']).click()

		#Return to user page
		return Users(self.driver).open()
				

	#Groups Page
	def addUserToGroup(self,user,newGroup):
		self.wait_for_available(locators['USERS_LIST_TABLE_ROWS'])
		if self.driver.is_element_available(locators['user']+user):
			self.find_element_by_locator(locators['user']+user).click()
			self.find_element_by_locator(locators['user_groups_page']).click()
			time.sleep(1)

			#Enter text
			self.userToGroup = newGroup
			print("User added")
		else:
			print(user + " does not exist")
	
		#Return to user page
		return Users(self.driver).open()
				

		
	
	def deleteUserGroup(self,user,group):
		time.sleep(1)
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_groups_page']).click()
		time.sleep(1)

		#Search for Group
		index = 0
		for bubbles in self.find_elements_by_locator(locators['GROUPS_BUBBLES']):
			if bubbles.text == group :
				self.find_elements_by_locator(locators['GROUPS_SVG'])[index].click()
				print("Deleted")
				time.sleep(1)
				return Users(self.driver).open()
			index+=1
		print("User does not exist")

		#Return to user page
		return Users(self.driver).open()
		

	
	def getUserGroups(self,user):
		time.sleep(1)
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_groups_page']).click()
		time.sleep(1)

		#Return table of group users
		table = []
		for bubbles in self.find_elements_by_locator(locators['GROUPS_BUBBLES']):
			table.append(bubbles.text)
		
		#Return to user page
		Users(self.driver).open()
		print(table)
		return Users(self.driver).open()	
	

	#Console Access
	#API Access

	#Permisions
	
	def addUserPermission(self,user,permission):
		time.sleep(1)
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_permission_page']).click()
		time.sleep(1)

		#Enter permission
		self.permissionName = permission
		print("permission added")

		#Return to user page
		Users(self.driver).open()
	
	def deleteUserPermission(self,user,permission):
		time.sleep(1)
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_permission_page']).click()
		time.sleep(1)

		#Search for permission
		index = 0
		for bubbles in self.find_elements_by_locator(locators['PERMISSION_BUBBLES']) :
			if bubbles.text == permission :
				self.find_elements_by_locator(locators['PERMISSION_SVG'])[index].click()
				print("Deleted")
				time.sleep(1)
				Users(self.driver).open()
				return
			index+=1
		print("Permission does not exist")

		#Return to user page
		Users(self.driver).open()


	def getGroupPermissions(self,user):
		time.sleep(1)
		self.find_element_by_locator(locators['user']+user).click()
		self.find_element_by_locator(locators['user_permission_page']).click()
		time.sleep(1)

		#Return table of group permissions
		table = []
		for bubbles in self.find_elements_by_locator(locators['PERMISSION_BUBBLES']) :
			table.append(bubbles.text)
		print(table)
		return(table)


