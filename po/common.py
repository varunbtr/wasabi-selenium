from gui_exceptions import GuiInputError
from selenium.common.exceptions import (
   InvalidElementStateException,
   NoSuchElementException,
   StaleElementReferenceException,
   TimeoutException,
)
import base
import time

URL = 'https://localhost/console#/'


def check_error(self):
    try:
        elem = self.driver.find_element_by_locator("css=div[data-e2e='snackBar'] span")
        time.sleep(2)
        print(elem.text)
    except NoSuchElementException:
        pass
    else:
        error_text = elem.text

    if error_text:
        raise GuiInputError(error_text)