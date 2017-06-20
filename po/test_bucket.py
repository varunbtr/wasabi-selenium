import unittest
import time
import common
import base
import random
import string
from loginpage import LoginPage
from driver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from filemanager import FileManagerPage
command_executor = "http://127.0.0.1:4444/wd/hub"


class BucketTest(unittest.TestCase):

	def setUp(self):
		self.driver = WebDriver(desired_capabilities=DesiredCapabilities.CHROME,command_executor=command_executor)
		self.driver.get(common.URL)
		login_page = LoginPage(self.driver).open()
		login_page.login(common.USERNAME,common.PASSWORD)
		self.bucketname=""	
	
	def testUpload(self):
		self.bucketname = 'testbucket.'+''.join(random.choice(string.lowercase) for i in range(4))
		file_page = FileManagerPage(self.driver).open()
		file_page.create_bucket(self.bucketname,'suspend','suspend')
		bucket_content = file_page.openBucket(self.bucketname)
		bucket_content.uploadfile('/home/vbatra/wasabi-selenium/po/unittest')
		time.sleep(5)
		common.check_error(self)
		#group_page.findGroup('1')

		#group_page.deleteGroup('1')
		#time.sleep(2)
		#print(group_page.getGroupList())

		#group_page.selectGroup('1')

		#time.sleep(2)

		#group_page.addGroupUser('1','ali')
		#print('user added')

		#time.sleep(2)
		
		#common.check_error(self)

	def tearDown(self):
		#self.deleteBucket(self,self.bucketname)
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
