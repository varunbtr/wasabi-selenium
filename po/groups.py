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

locators = {
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

	'group_users': 'id=group-users',
	'add_user_to_group':'id=add-user-to-group',	
	'USERS_LIST_SPANS': 'css=div[aria-hidden="false"] span',
	'USERS_LIST_DELETE': 'css=div[aria-hidden="false"] svg',
	'group_svg': "css=div[tabindex='0']",

	'group_permissions': 'id=group-permissions',
	'add_policy_to_group': '',
	'PERMISSION_LIST_TABLE_ROWS': 'css=.Flex .Box',
	}

class Groups(BasePage):
	url = common.URL + '#/groups'
	table = []
	header = ['Name','Path','ARN','Created on']
	groupName = Text(locators['group_name'])	
	userName = AutoComplete(locators['add_user_to_group'])
	permissionName = Text(locators['add_user_to_group'])	


	def wait_until_loaded(self):
		self.wait_for_available(locators['create_group'])
		return self


	def open(self):
		self.driver.get(self.url)
		return self.wait_until_loaded()

	#Functions for groups page
	def createGroup(self, groupname):
		#Need an if Statement to check if a group with the given name already exists
		self.find_element_by_locator(locators['create_group'])	.click()
		self.groupName = groupname
		self.find_element_by_locator(locators['save_group']).click()
	

	def deleteGroup(self, groupname):
		self.find_element_by_locator(locators['group_btn']+ groupname).click()
		self.find_element_by_locator(locators['delete_btn']).click()
		print(groupname + "Deleted")


	def selectGroup(self,groupname):
		self.find_element_by_locator(locators['group_btn']+ groupname).click()


	def getGroupList(self):
		table = []
		header = ['Name' , 'Path','ARN','Created on']
		for rows in self.find_elements_by_locator(locators['GROUPS_LIST_TABLE_ROWS']):
			d = {}
			index = 0
			for colms in rows.find_elements_by_locator(locators['GROUPS_LIST_TABLE_COLMS']):
				print(colms.text)
				d[header[index]] = colms.text
				index+=1
			table.append(d)
		print(table)
		return table


	def findGroup(self,groupname):
		header = ['Name' , 'Path','ARN','Created on']
		for rows in self.find_elements_by_locator(locators['GROUPS_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(locators['GROUPS_LIST_TABLE_COLMS'])
			col_text = colms[0].text
			if col_text == groupname:
				return colms[0]
				break
			else:
				raise TimeoutException('Failed to locate user '
					'value {!r}'.format(attr_val))

	#Users
	def addGrouptoUser(self,groupname,username):
		self.find_element_by_locator(locators['group_btn']+ groupname).click()
		self.find_element_by_locator(locators['group_users']).click()
		self.userName = username
		#figure out how to enter user name in to AddUserToGroup text box 

		#Return to user page
		Groups(self.driver).open()

	def deleteGroupUser(self,group,user):
		self.find_element_by_locator(locators['group_btn']+ groupname).click()
		self.find_element_by_locator(locators['group_users']).click()

		time.sleep(2)
		# Use get from span to find the group then use that index to click on its svg
		self.find_elements_by_locator(locators['group_svg'])[0].click()

		#Return to user page
		Groups(self.driver).open()

	'''
	def getGroupUsers(self,group):
		self.find_element_by_locator(locators['group_users'])
		# Varun: retrieve text using getText()
		print("test")

		#iterate through the list of users bubbles
		
		d = {}
		for colms in self.find_element_by_locator(locators['group_users']):
			print("here") 
			col_text = colms.getText(colms)
			print(col_text)
			d[header[index]] = col_text
		print(d)
		return d	
	'''

	#Permisions
	'''
	#def setGroupPermissions(self,permission):
		self.find_element_by_locator(locators['group_btn']+ groupname).click()
		self.find_element_by_locator(locators['group_permissions']).click() 

		#Enter it 
		self.permissionName = permission

		#Click on droping text box 

	def deleteGroupPermission(self):
		self.find_element_by_locator(locators['group_btn']+ groupname).click()
		self.find_element_by_locator(locators['group_permissions']).click()

		time.sleep(2)
		# Use get from span to find the group then use that index to click on its svg
		self.find_elements_by_locator(locators['group_svg'])[0].click()

		#Return to user page
		Groups(self.driver).open()


	#def getGroupPermissions(self,permission):
		self.find_element_by_locator(locators['group_btn']+ groupname).click()
		self.find_element_by_locator(locators['group_permissions']).click()
		#retrieve spans containing group permsions - loop through the table of spans 	
	'''


