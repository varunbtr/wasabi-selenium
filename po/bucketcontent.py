from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from po.controls.checkbox import CheckBox
from .errors import ExpectedElementError, WaitForElementError
from .page import Page
from po.controls import Text
from po.common import common

locators = {
    'create_folder': 'id=create-folder',
    'upload_wizard': 'id=upload-wizard',
    'upload_file':'id=upload-file',
    'upload_folder':'id=upload-folder',
    'start_upload':'',
    'clear_files':'',


}
url = common.URL + 'overview'

class BucketContent(Page):
      url = common.URL + 'overview'
      BUCKET_NAME = (By.NAME,'Bucket')
      VERSION_RADIO = (By.NAME,'Versioning')
      LOGGING_RADIO = (By.NAME,'Logging')
      NEXT_BUTTON = (By.CSS,'button[data-e2e="bucket-wiz-next"]')
      CREATE_BUCKET_BTN = (By.CSS,'button[data-e2e="bucket-cta"]')

      def upload(self):
        self.driver.get(page_url)
        return self.wait_until_loaded()
      
      def createBucket(self,name,region='',copybucket='',version,logging):
          if not self.driver.findElement(By.CSS(".custom-scroll")).Displayed:
            self.driver.find_element(CREATE_BUCKET_BTN).click()
          self.set_textbox(LoginPage.USERNAME, username)
          self.driver.find_element(NEXT_BUTTON).click()
          self.set_radiobutton(VERSION_RADIO,version)
          self.set_radiobutton(LOGGING_RADIO,logging)
          self.driver.find_element(NEXT_BUTTON).click()