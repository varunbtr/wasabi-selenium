from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from base import BasePage
from controls.radiobutton import RadioButton 
import common

locators = {
    'bucketname': "name=Bucket",
    'versionradio': "name=Versioning",
    'loggingradio': 'name=Logging',
    'nextbutton':'css=button[data-e2e="bucket-wiz-next"]',
    'createbucketbutton':'css=button[data-e2e="bucket-cta"]',
    }
class CreateBucketWiz(BasePage):
      url = common.URL + 'overview'
      versioning = RadioButton(locators['versionradio'])
      logging = RadioButton(locators['loggingradio'])

      def createBucket(self,name,version,logging,region='',copybucket=''):
          if not self.find_elements_by_locator('css=.custom-scroll').Displayed:
            self.find_elements_by_locator(locators['createbucketbutton']).click()
          self.set_textbox(LoginPage.USERNAME, username)
          self.find_elements_by_locator(locators['nextbutton']).click()
          self.versioning = version
          self.logging = logging
          self.find_elements_by_locator(locators['nextbutton']).click()