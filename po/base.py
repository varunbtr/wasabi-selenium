from __future__ import absolute_import, unicode_literals
#from selenium.webdriver.common.by import By
#from selenium.common.exceptions import (
#    ElementNotVisibleException,
#    InvalidElementStateException,
#    ElementNotSelectableException
#)
import time
from selenium.common.exceptions import NoAlertPresentException

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
    '''
    def set_textbox(self,locator, value):
        elem = self.driver.find_element(*locator)
        elem.send_keys(value)
    def get_textbox(self,locator):
        elem = self.driver.find_element(*locator)
        return elem.getText(elem)
    def get_radiobutton(self,locator):
        for elem in self.driver.find_elements(*locator):
            if elem.size() != 0:
                raise ElementNotVisibleException(self)
            if not elem.isEnabled():
                raise InvalidElementStateException(
                    '{} is disabled'.format(self))
            if elem.is_selected():
                retval = elem.get_attribute('value')
                retval = self.reverse_mappings.get(retval, retval)
                break
            else:
                retval = None
        return retval
    def set_radiobutton(self,locator,value):
        for elem in self.driver.find_elements(*locator):
            if elem.get_attribute('value') == attr_val:
                if not elem.is_selected():
                    elem.click()
                return elem
            else:
                raise ElementNotSelectableException('Failed to locate radio button with '
                    'value {!r}'.format(attr_val))
    '''
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

    def wait_for_available(self, locator):
        for i in range(self.timeout_seconds):
            if self.driver.is_element_available(locator):
                break
            self.sleep()
        else:
            raise WaitForElementError('Wait for available timed out')
        return True

    def wait_for_visible(self, locator):
        for i in range(self.timeout_seconds):
            if self.driver.is_visible(locator):
                break
            self.sleep()
        else:
            raise WaitForElementError('Wait for visible timed out')
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

'''class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute("value")
'''
