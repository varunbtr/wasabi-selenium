from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from base import BasePage

locators = {
    'create_folder': 'id=create-folder',
    'upload_wizard': 'id=upload-wizard',
    'upload_file':'id=upload-file',
    'upload_folder':'id=upload-folder',
    'input_upload':"css=.Flex .Box Input[type='file']",
    'start_upload':'id=start-upload',
    'clear_files':'id=clear-files',

}
class BucketContent(BasePage):
  def uploadfile(self,file_name):
        self.find_element_by_locator(locators['upload_wizard']).click()
        #self.find_element_by_locator(locators['upload_file']).click()
        inputfield = self.find_elements_by_locator(locators['input_upload'])[1]
        inputfield.send_keys(file_name)
        self.sleep(2)
        self.find_element_by_locator(locators['start_upload']).click()
        
  def uploadfolder(self,folder_name):
        self.find_element_by_locator(locators['upload_wizard']).click()
        inputfield = self.find_elements_by_locator(locators['input_upload'])[0]
        inputfield.send_keys(folder_name)
        self.sleep(2)
	self.find_element_by_locator(locators['start_upload']).click()
           
