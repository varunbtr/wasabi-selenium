from selenium.common.exceptions import (
   ElementNotVisibleException,
   InvalidElementStateException,
   ElementNotSelectableException,
   TimeoutException
)
import base
import common
from base import BasePage
from controls.text import Text
import time

locators = {
    'create_btn': "css=button[data-e2e='group-cta']",
    'group_name' : 'name=GroupName',
    'GROUPS_LIST_TABLE_ROWS': 'css=.ReactVirtualized__Grid__innerScrollContainer .ReactVirtualized__Table__row',
    'GROUPS_LIST_TABLE_COLMS': 'css=.ReactVirtualized__Table__rowColumn',
    'refresh_btn' : 'class=material-icons',
    'menu' : "css=button[data-e2e='topNav']",
    'save_group' : 'css=form div.Flex button',
    }

class Groups(BasePage):
    url = common.URL + 'groups'
    table = []
    header = ['Name','Path','ARN','Created on']
    groupName = Text(locators['group_name'])        #So do I make the create bucket page its own class ?
    
    def wait_until_loaded(self):
        self.wait_for_available(locators['create_btn'])
        return self

    def open(self):
        self.driver.get(self.url)
        return self.wait_until_loaded()

    def createGroup(self, groupname):
        self.find_element_by_locator(locators['create_btn']).click()
        self.groupName = groupname
        self.find_element_by_locator(locators['save_group']).click()

    def Refresh(self):
        self.find_element_by_locator(locators['refresh_btn']).click()


    def getGroupList(self):
        for rows in self.find_element_by_locator(locators['GROUPS_LIST_TABLE_ROWS']):
            d = {}
            for index, colms in self.find_element_by_locator(locators['GROUPS_LIST_TABLE_COLMS']):
                if(index >0):
                    col_text = colms.getText(colms)
                    d[header[index]] = col_text
            table.append(d)
        return table


    def findGroup(self,groupname):
        header = ['User Name' , 'Path','ARN','Created on']
        for rows in self.find_element_by_locator(locators['GROUPS_LIST_TABLE_ROWS']):
            colms = self.find_element_by_locator(locators['GROUPS_LIST_TABLE_COLMS'])
            col_text = colms[0].getText(colms[0])
            if col_text == groupname:
                return colums[0]
                break
            else:
                raise TimeoutException('Failed to locate user '
                    'value {!r}'.format(attr_val))
    
    
    #def getGroupUsers(self,username):
    #def setGroupUsers(self,username):
    #def getGroupPermissions(self,permission):
    #def setGroupPermissions(self,permission):