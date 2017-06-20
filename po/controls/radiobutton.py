class RadioButton(object):
    def __init__(self,locator):
        self.locator = locator

    def __set__(self, instance, value):
        try:
            e = instance.element.find_element_by_locator(self.locator)
        except AttributeError:
            for e in instance.driver.find_elements_by_locator(self.locator):
                if e.get_attribute('value') == value:
                    e.click()

    def __get__(self, instance, owner=None):
        try:
             e = instance.element.find_element_by_locator(self.locator)    
        except AttributeError:
            for e in instance.driver.find_elements_by_locator(self.locator):
                if e.is_selected():
                    retval = e.get_attribute('value')
                else:
                    retval = None
        return retval