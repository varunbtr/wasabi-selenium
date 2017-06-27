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
from controls.autocomplete import AutoComplete
import time

LOCATORS = {
	'menu': 'class=iconContainer-0-7',
	'iam_btn': "css=button[data-e2e='tn-overview']",
	'create_bucket': "css=button[data-e2e='bucket-cta']",
	'GROUPS_LIST_TABLE_ROWS': 'css=.ReactVirtualized__Grid__innerScrollContainer .ReactVirtualized__Table__row',
	'GROUPS_LIST_TABLE_COLMS': 'css=.ReactVirtualized__Table__rowColumn',
	'option_button':'id=topNavOptions',
	'profile':'id=profile',
	'switch_role':'id=switchRoles',
	'logout':'id=logout',

	'users':"css=a[href='#/users']",
	'groups':"css=a[href='#/groups']",
	'acccess_key':"css=a[href='#/access_keys']",
	'policies':"css=a[href='#/policies']",
	'roles':"css=a[href='#/roles']",

	'create_group': "css=button[data-e2e='group-cta']",
	'group_name' : 'name=GroupName',
	'save_group': 'css=form div.Flex button',

	'group_btn': 'id=group-',
	'delete_btn': 'css=div.Flex div.Box button',

	'delete_confirm_btn':'css=button[data-e2e="confirmBtn"]',

	'group_users': 'id=group-users',
	'add_user_to_group':'id=add-user-to-group',	
	'USER_BUBBLES': "css=div[aria-hidden='false'] .Flex .Box",
	'USER_SVG': "css=div[aria-hidden='false'] .Flex .Box span",

	'group_permissions': 'id=group-permissions',
	'add_policy_to_group': "css=div[aria-hidden='false'] input",
	'PERMISSION_BUBBLES': "css=div[aria-hidden='false'] .Flex .Box",
	'PERMISSION_SVG': "css=div[aria-hidden='false'] .Flex .Box span"
	}

class Groups(BasePage):
	url = common.URL + '#/groups'
	table = []
	header = ['Name','Path','ARN','Created on']
	groupName = Text(LOCATORS['group_name'])	
	userName = AutoComplete(LOCATORS['add_user_to_group'])
	permissionName = AutoComplete(LOCATORS['add_policy_to_group'])	


	def wait_until_loaded(self):
		self.wait_for_available(LOCATORS['create_group'])
		return self


	def open(self):
		self.driver.get(self.url)
		return self.wait_until_loaded()

	#Functions
	def createGroup(self, groupname):
		self.open()

		if self.driver.is_visible(LOCATORS['group_btn']+groupname):
			print("group exists")
			return

		self.wait_for_available(LOCATORS['create_group'])
		self.find_element_by_locator(LOCATORS['create_group'])	.click()
		self.groupName = groupname
		self.find_element_by_locator(LOCATORS['save_group']).click()
		self.wait_for_available(LOCATORS['group_btn']+groupname)

		print( groupname + ' created')
	

	def deleteGroup(self, groupname):
		self.checkGroupTable()

		if self.driver.is_element_available(LOCATORS['group_btn']+groupname):
			self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()
			self.find_element_by_locator(LOCATORS['delete_btn']).click()

			# Sometimes it fails to delete because of policies, this will make thh ecode try again
			if self.driver.is_visible(LOCATORS['delete_confirm_btn']):
				self.find_element_by_locator(LOCATORS['delete_confirm_btn']).click()

			self.wait_for_available(LOCATORS['create_group'])

		else:
			print(groupname + " does not exist")




	def deleteAllGroups(self):
		#self.checkGroupTable()

		while self.driver.is_visible(LOCATORS['GROUPS_LIST_TABLE_ROWS']):
			self.find_elements_by_locator(LOCATORS['GROUPS_LIST_TABLE_ROWS'])[0].click()
			self.wait_for_visible(LOCATORS['delete_btn'])
			self.find_element_by_locator(LOCATORS['delete_btn']).click()

			# Sometimes it fails to delete because of policies, this will make the code try again
			if self.driver.is_visible(LOCATORS['delete_confirm_btn']):
					self.find_element_by_locator(LOCATORS['delete_confirm_btn']).click()

			self.wait_for_available(LOCATORS['create_group'])

		else:
			print("All groups deleted")


	def selectGroup(self,groupname):
		self.checkGroupTable()

		self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()


	def getGroupList(self):
		self.checkGroupTable()

		table = []
		for rows in self.find_elements_by_locator(LOCATORS['GROUPS_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(LOCATORS['GROUPS_LIST_TABLE_COLMS'])
			col_text = colms[0].text
			table.append(col_text)
		return table


	def findGroup(self,groupname):
		self.checkGroupTable()

		header = ['Name' , 'Path','ARN','Created on']
		for rows in self.find_elements_by_locator(LOCATORS['GROUPS_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(LOCATORS['GROUPS_LIST_TABLE_COLMS'])
			col_text = colms[0].text
			if col_text == groupname:
				return colms[0]
				break
			else:
				raise TimeoutException('Failed to locate user '
					'value {!r}'.format(attr_val))

	#Group Users Page
	def addUsertoGroup(self,groupname,username):
		self.checkGroupTable()
		if self.driver.is_element_available(LOCATORS['group_btn']+groupname):
			self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()
			self.find_element_by_locator(LOCATORS['group_users']).click()
			self.wait_for_available(LOCATORS['add_user_to_group'])

			#Enter User
			self.userName = username 

		else:
			print(groupname + " does not exist")
	
		#Return to groups page
		Groups(self.driver).open()


	def deleteGroupUser(self,groupname,username):
		self.checkGroupTable()

		if self.driver.is_element_available(LOCATORS['group_btn']+groupname):
			self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()
			self.find_element_by_locator(LOCATORS['group_users']).click()
			self.wait_for_available(LOCATORS['add_user_to_group'])

			#Search for User
			index = 0
			for bubbles in self.find_elements_by_locator(LOCATORS['USER_BUBBLES']):
				#print(bubbles.text)
				if bubbles.text == username :
					self.find_elements_by_locator(LOCATORS['USER_SVG'])[index].click()
					print("Deleted")
					Groups(self.driver).open()
					return
				index+=1
			print("User does not exist")

		else:
			print(groupname + " does not exist")
	
		#Return to groups page
		Groups(self.driver).open()

	
	def getGroupUsers(self,groupname):
		self.checkGroupTable()

		if self.driver.is_element_available(LOCATORS['group_btn']+groupname):
			self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()
			self.find_element_by_locator(LOCATORS['group_users']).click()
			self.wait_for_available(LOCATORS['add_user_to_group'])

			table = []
			for colms in self.find_elements_by_locator(LOCATORS['USER_BUBBLES']):
				table.append(colms.text)
		
		
		else:
			print(groupname + " does not exist")
	
		#Return to groups page
		Groups(self.driver).open()
		return table
	

	#Group Permissions Page
	def addPermissionToGroup(self,groupname,permission):
		self.checkGroupTable()

		if self.driver.is_element_available(LOCATORS['group_btn']+groupname):
			self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()
			self.find_element_by_locator(LOCATORS['group_permissions']).click()
			self.wait_for_available(LOCATORS['add_policy_to_group'])
		
			#Add permission 
			self.permissionName = permission
			print("permission added")

		else:
			print(groupname + " does not exist")
	
		#Return to groups page
		Groups(self.driver).open()
	

	def deleteGroupPermission(self,groupname,permission):
		self.checkGroupTable()

		if self.driver.is_element_available(LOCATORS['group_btn']+groupname):
			self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()
			self.find_element_by_locator(LOCATORS['group_permissions']).click()
			self.wait_for_available(LOCATORS['add_policy_to_group'])

			#Search for permission
			index = 0
			for bubbles in self.find_elements_by_locator(LOCATORS['PERMISSION_BUBBLES']) :
				if bubbles.text == permission :
					self.find_elements_by_locator(LOCATORS['PERMISSION_SVG'])[index].click()
					print("Deleted")
					Groups(self.driver).open()
					return
				index+=1
			print("Permission does not exist")

		else:
			print(groupname + " does not exist")
	
		#Return to groups page
		Groups(self.driver).open()
	

	def getGroupPermissions(self,groupname):
		self.checkGroupTable()

		if self.driver.is_element_available(LOCATORS['group_btn']+groupname):
			self.find_element_by_locator(LOCATORS['group_btn']+ groupname).click()
			self.find_element_by_locator(LOCATORS['group_permissions']).click()
			self.wait_for_available(LOCATORS['add_policy_to_group'])

			table = []
			for bubbles in self.find_elements_by_locator(LOCATORS['PERMISSION_BUBBLES']) :
				table.append(bubbles.text)
			return table

		else:
			print(groupname + " does not exist")
	
		#Return to groups page
		Groups(self.driver).open()


	#Check if any groups on the table 
	def checkGroupTable(self):
		self.open()
		try: 
			self.wait_for_available(LOCATORS['GROUPS_LIST_TABLE_ROWS'])
		except TimeoutException:
			print("table has no groups")







