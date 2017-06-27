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
	'KEY_LIST_TABLE_ROWS': 'css=.ReactVirtualized__Grid__innerScrollContainer .ReactVirtualized__Table__row',
	'KEY_LIST_TABLE_COLMS': 'css=.ReactVirtualized__Table__rowColumn',
	'options_button':'id=topNavOptions',
	'profile':'id=profile',
	'switch_role':'id=switchRoles',
	'logout':'id=logout',

	'users':"css=a[href='#/users'] span",
	'groups':"css=a[href='#/groups']",
	'acccess_key':"css=a[href='#/access_keys']",
	'policies':"css=a[href='#/policies']",
	'roles':"css=a[href='#/roles']",

	'create_key':'css=.Flex .Box button',
	'close_btn':'css=.Flex .Box button',


	'show_secret_key': 'css=.Flex .Box._lr-hide a',
	'access_key':'css=.Flex .Box._lr-hide code',

	'delete_key':'css=.ReactVirtualized__Table__row button',
	'confirm_delete':"css= button[data-e2e='confirmBtn']",

	}


class Keys(BasePage):
	url = common.URL + '#/access_keys'


	def wait_until_loaded(self):
		self.wait_for_available(LOCATORS['create_key'])
		return self


	def open(self):
		self.driver.get(self.url)
		return self.wait_until_loaded()

	def createKey(self):
		self.open()

		self.find_element_by_locator(LOCATORS['create_key']).click()

		#Get access keys for API
		self.wait_for_visible(LOCATORS['show_secret_key'])
		self.find_element_by_locator(LOCATORS['show_secret_key']).click()
		accessKey = self.find_elements_by_locator(LOCATORS['access_key'])[0].text
		secretKey = self.find_elements_by_locator(LOCATORS['access_key'])[1].text

		accessKey = accessKey.split('\n')[0]
		secretKey = secretKey.split('\n')[0]

		self.find_elements_by_locator(LOCATORS['close_btn'])[-1].click()

		return accessKey , secretKey


	def deleteAllKeys(self):
		#self.checkKeysTable()

		while self.driver.is_visible(LOCATORS['KEY_LIST_TABLE_ROWS']):
			self.find_elements_by_locator(LOCATORS['delete_key'])[-1].click()
			
			self.wait_for_visible(LOCATORS['confirm_delete'])
			self.find_element_by_locator(LOCATORS['confirm_delete']).click()
			self.wait_for_visible(LOCATORS['create_key'])

		else:
			print("All keys deleted")

	def deleteKey(self,key):
		self.checkKeysTable()

		table = []
		index = 0
		for rows in self.find_elements_by_locator(LOCATORS['KEY_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(LOCATORS['KEY_LIST_TABLE_COLMS'])
			if colms[1].text == key:
				self.find_elements_by_locator(LOCATORS['delete_key'])[index].click()
				self.wait_for_visible(LOCATORS['confirm_delete'])
				self.find_element_by_locator(LOCATORS['confirm_delete']).click()
				self.wait_for_visible(LOCATORS['create_key'])
				time.sleep(10)
				return
			index +=1 
				
		print('No such key')

	
	def getKeys(self):
		self.checkKeysTable()

		table = []
		for rows in self.find_elements_by_locator(LOCATORS['KEY_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(LOCATORS['KEY_LIST_TABLE_COLMS'])
			col_text = colms[1].text
			table.append(col_text)
		return table


	def getUserKeys(self,username):
		self.checkKeysTable()

		table = []
		for rows in self.find_elements_by_locator(LOCATORS['KEY_LIST_TABLE_ROWS']):
			colms = rows.find_elements_by_locator(LOCATORS['KEY_LIST_TABLE_COLMS'])
			if colms[0].text == username:
				col_text = colms[1].text
				table.append(col_text)
		return table		


	'''
	def deactivateKey(self):
	'''
	

	#Check if groups on table
	def checkKeysTable(self):
		self.open()
		try: 
			self.wait_for_available(LOCATORS['KEY_LIST_TABLE_ROWS'])
		except TimeoutException:
			print("table has no keys")






