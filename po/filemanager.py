from base import BasePage
import common
#from textbox import Textbox
from controls.text import Text
from controls.radiobutton import RadioButton
import time
from users import Users
from iam import Iam
from groups import Groups
from bucketcontent import BucketContent
import common
locators = {
    'iam_btn': "css=button[data-e2e='tn-overview']",
    'create_bucket': "css=button[data-e2e='bucket-cta']",
    'bucket_list_table_rows': 'css=.ReactVirtualized__Grid__innerScrollContainer .ReactVirtualized__Table__row',
    'bucket_list_table_colms':'css=div.ReactVirtualized__Table__rowColumn',
    'iam_links':'css=a[data-e2e="tn-overview"]',
    'option_button':'id=topNavOptions',
    'profile':'id=profile',
    'switch_role':'id=switchRoles',
    'logout':'id=logout',
    'users':"css=a[href='#/users']",
    'groups':"css=a[href='#/groups']",
    'acccess_key':"css=a[href='#/access_keys']",
    'policies':"css=a[href='#/policies']",
    'roles':"css=a[href='#/roles']",
    }

bucket_locators = {
    'bucketname': "name=Bucket",
    'versionradio': "css=input[name='Versioning']",
    'loggingradio': 'name=Logging',
    'nextbutton':'css=button[data-e2e="bucket-wiz-next"]',
    'createbucketbutton':'css=button[data-e2e="bucket-cta"]',
    }

class FileManagerPage(BasePage):
      url = common.URL + "file_manager"
      versioning = RadioButton(bucket_locators['versionradio'])
      logging = RadioButton(bucket_locators['loggingradio'])
      bucketname = Text(bucket_locators['bucketname'])

      def create_bucket(self,name,version,logging,region='',copybucket=''):
          if self.is_element_present("css=div[data-e2e='file-browser']"):
            self.find_element_by_locator(bucket_locators['createbucketbutton']).click()
          self.bucketname = name
          ##Todo Grab if there is error message on the bucket name
          ####
          try:
            self.find_element_by_locator(bucket_locators['nextbutton']).click()
          except NoSuchElementException:
            pass
          self.versioning = version
          self.logging = logging
          self.find_element_by_locator(bucket_locators['nextbutton']).click()
          self.find_element_by_locator(bucket_locators['nextbutton']).click()
          self.wait_for_visible("css=div[data-e2e='file-browser']")
          time.sleep(2)

      def openBucket(self,bucketname):

        table = []
        header = ['bucket_name' , 'owner','created_on']
        for rows in self.find_elements_by_locator(locators['bucket_list_table_rows']):
            d = {}
            for index,colms in enumerate(rows.find_elements_by_locator(locators['bucket_list_table_colms'])):
                if(index == 1):
                  if colms.text == bucketname:
                     colms.click()
                     self.wait_for_visible("xpath=//div[contains(text(), '"+bucketname+"')]")
                     time.sleep(5)
                     return BucketContent(self.driver)
      
      def getBucketList(self):
        table = []
        header = ['bucket_name' , 'owner','created_on']
        for rows in self.find_elements_by_locator(locators['bucket_list_table_rows']):
            d = {}
            for index,colms in enumerate(rows.find_elements_by_locator(locators['bucket_list_table_colms'])):
                if(index >0):
                  col_text = colms.text
                  d[header[index-1]] = col_text
            table.append(d)
        return table
      def deleteBucket(self,bucketname):
        pass
      def wait_until_loaded(self):
        self.wait_for_available(locators['create_bucket'])
        return self
      def open(self):
        self.driver.get(self.url)
        return self.wait_until_loaded()
      def clickIam(self):
          self.find_elements_by_locator(locators['iam_links']).click()
          return Iam(self.driver)
      def clickUsers(self):
          self.find_elements_by_locator(locators['users']).click()
          return Users(self.driver)
      def clickGroups(self):
          self.find_elements_by_locator(locators['groups']).click()
          return Groups(self.driver)
      def clickAccessKeys(self):
          self.find_elements_by_locator(locators['acccess_key']).click()
          return Keys(self.driver)
      def clickPolicies(self):
          self.find_elements_by_locator(locators['policies']).click()
          return Policies(self.driver)
      def clickRoles(self):
          self.find_elements_by_locator(locators['roles']).click()
          return Roles(self.driver)
      def selectProfile(self):
          self.find_elements_by_locator(locators['option_button']).click()
          try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="menu"]')))
          except TimeoutException:
            print("ERROR:Page took too long to load and sign up")
          self.find_elements_by_locator(locators['profile']).click()
          return UserDetail(self.driver)
      def switchRole(self):
          self.find_elements_by_locator(locators['option_button']).click()
          try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="menu"]')))
          except TimeoutException:
            print("ERROR:Page took too long to load and sign up")
          self.find_elements_by_locator(locators['switch_role']).click()
          return SwitchRole(self.driver)
      def logout(self):
          self.find_elements_by_locator(locators['option_button']).click()
          try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="menu"]')))
          except TimeoutException:
            print("ERROR:Page took too long to load and sign up")
          self.find_elements_by_locator(locators['logout']).click()

