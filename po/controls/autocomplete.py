import time
from selenium.webdriver.common.keys import Keys
    
class AutoComplete(object):
    def __init__(self,locator):
        self.locator = locator

    def __set__(self, instance, value):
        try:
            e = instance.element.find_element_by_locator(self.locator)
        except AttributeError:
            e = instance.driver.find_element_by_locator(self.locator)
        if value == "clear()":
            e.clear()
        else:
            e.send_keys(value)
            try:
                e = instance.element.find_element_by_locator("css=span[role='menuitem'] div")
            except AttributeError:
                e = instance.driver.find_element_by_locator("css=span[role='menuitem'] div")
            e.click()
            time.sleep(2)


    def __get__(self, instance, owner=None):
        try:
            e = instance.element.find_element_by_locator(self.locator)
        except AttributeError:
            e = instance.driver.find_element_by_locator(self.locator)
        text = None
        if e.tag_name in ["input", "textarea"]:
            text = e.get_attribute("value")
        else:
            text = e.text
        return text
