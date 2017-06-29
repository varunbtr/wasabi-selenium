from __future__ import absolute_import, unicode_literals
#from selenium.webdriver.common.by import By
#from selenium.common.exceptions import (
#    ElementNotVisibleException,
#    InvalidElementStateException,
#    ElementNotSelectableException
#)
import time
from selenium.common.exceptions import NoAlertPresentException,TimeoutException

#TODO create WaitForElementError class
from errors import WaitForElementError

class BasePage(object):
    url = None
    timeout_seconds = 20
    sleep_interval = .25

    def __init__(self, driver):
        self.driver = driver
    def navigate(self):
        self.driver.get(self.url)
     @property
    def referrer(self):
        return self.driver.execute_script('return document.referrer')

    def sleep(self, seconds=None):
        if seconds:
            time.sleep(seconds)
        else:
            time.sleep(self.sleep_interval)

    def find_element_by_locator(self, locator):
        return self.driver.find_element_by_locator(locator)

    def find_elements_by_locator(self, locator):
        return self.driver.find_elements_by_locator(locator)
    def is_element_present(self,locator):
        return self.driver.is_element_present(locator)
    def wait_for_available(self, locator):
        for i in range(self.timeout_seconds):
            if self.driver.is_element_available(locator):
                break
            self.sleep()
        else:
            raise TimeoutException(msg='Wait for available timed out')
        return True

    def wait_for_visible(self, locator):
        for i in range(self.timeout_seconds):
            if self.driver.is_visible(locator):
                break
            self.sleep()
        else:
            raise TimeoutException(msg='Wait for available timed out')
        return True

    def wait_for_hidden(self, locator):
        for i in range(self.timeout_seconds):

            if self.driver.is_visible(locator):
                self.sleep()
            else:
                break
        else:
            raise WaitForElementError('Wait for hidden timed out')
        return True

    def wait_for_alert(self):
        for i in range(self.timeout_seconds):
            try:
                alert = self.driver.switch_to_alert()
                if alert.text:
                    break
            except NoAlertPresentException as nape:
                pass
            self.sleep()
        else:
            raise NoAlertPresentException(msg='Wait for alert timed out')
        return True

    def _dispatch(self, l_call, l_args, d_call, d_args):
        pass