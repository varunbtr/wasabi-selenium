#from __future__ import absolute_import, unicode_literals
from base import BasePage
import common
#from textbox import Textbox
from controls.text import Text
import time
from filemanager import FileManagerPage
locators = {
    'username': 'name=AccountName',
    'password': 'name=Password',
    'login_btn': "xpath=//span[contains(text(), 'Sign In')]",
    }
class LoginPage(BasePage):
  username = Text(locators['username'])
  password = Text(locators['password'])
  url = common.URL
  
  def wait_until_loaded(self):
        self.wait_for_available(locators['username'])
        return self
  
  def open(self):
        self.driver.get(self.url)
        return self.wait_until_loaded()

  def login(self,username,password):
    self.username = username
    self.password = password
    login_btn = self.find_element_by_locator(locators['login_btn'])
    login_btn.click()
    common.check_error(self)
    return FileManagerPage(self.driver)
    