from __future__ import absolute_import, unicode_literals
from selenium.webdriver.common.by import By
from base import BasePage
import common
#from textbox import Textbox
import time
from filemanager import FileManagerPage
class LoginPage(BasePage):
  
  url = common.URL
  USERNAME = (By.NAME,'AccountName')
  PASSWORD = (By.NAME,'Password')
  LOGIN_BTN = (By.XPATH,"//span[contains(text(), 'Sign In')]")

  def setUsername(self, username):
      self.set_textbox(LoginPage.USERNAME, username)
  
  def setPassword(self, password):
      self.set_textbox(LoginPage.PASSWORD, password)
  
  def submit(self):
      self.driver.find_element(*LoginPage.LOGIN_BTN).click()
      return FileManagerPage(self.driver)