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

locators = {
	'menu': 'class=iconContainer-0-7',
	'iam_btn': "css=button[data-e2e='tn-overview']",
	'create_bucket': "css=button[data-e2e='bucket-cta']",
	'option_button':'id=topNavOptions',
	'profile':'id=profile',
	'switch_role':'id=switchRoles',
	'logout':'id=logout',

	'bucketname': "name=Bucket",
	'versionradio': "name=Versioning",
	'loggingradio': 'name=Logging',
	'nextbutton':'css=button[data-e2e="bucket-wiz-next"]',

	'users':"css=a[href='#/users']",
	'groups':"css=a[href='#/groups']",
	'acccess_key':"css=a[href='#/access_keys']",
	'policies':"css=a[href='#/policies']",
	'roles':"css=a[href='#/roles']",

	'alias_btn': 'css=.Flex span.material-icons',
	'input_alias': 'css=.Flex input',
	'save_alias': 'css=.Flex button',
	}

class Overview(BasePage):
	url = common.URL + '#/overview'
	BucketName = Text(locators['bucketname'])
	inputAlias = Text(locators['input_alias'])
	#versioning = RadioButton(locators['versionradio'])
	#logging = RadioButton(locators['loggingradio'])



	def wait_until_loaded(self):
		self.wait_for_available(locators['option_button'])
		return self


	def open(self):
		self.driver.get(self.url)
		return self.wait_until_loaded()


	def createBucket(self,bucketName):
		self.find_element_by_locator(locators['create_bucket']).click()
		self.BucketName = bucketName

		self.find_element_by_locator(locators['nextbutton']).click()

		self.find_element_by_locator(locators['nextbutton']).click()

		self.find_element_by_locator(locators['nextbutton']).click()
		print('done')
				

	
	def editAlias(self,alias):
		#click on alias
		time.sleep(1)
		self.find_elements_by_locator(locators['alias_btn'])[0].click()
		time.sleep(1)
		self.inputAlias = alias
		time.sleep(1)
		#click save
		self.find_element_by_locator(locators['save_alias']).click()



