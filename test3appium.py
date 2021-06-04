import unittest
import os

from appium import webdriver
from time import sleep

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Test1Appium(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['app'] = PATH('contactmanager.apk')
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'Genymotion Cloud'
        desired_caps['udid'] = 'localhost:10000'  # do uzupelnia gdyby nie byl staly
        desired_caps['appPackage'] = 'com.example.android.contactmanager'
        desired_caps['appActivity'] = 'com.example.android.contactmanager.ContactManager'

        # polaczenie z Appium
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(2)

    def tearDown(self):
        self.driver.quit()

    def testFormularzUnicode(self):
        self.driver.is_app_installed('com.example.android.contactmanager')
        self.driver.find_element_by_id('com.example.android.contactmanager:id/addContactButton').click()
        textfields = self.driver.find_elements_by_class_name('android.widget.EditText')
        textfields[0].send_keys('Иоа́нн Иоа́ннович')
        textfields[1].send_keys('123456789')
        textfields[2].send_keys('Иоа́нн.Иоа́ннович@mail.ru')
        sleep(2)

        # printy dydaktycznie
        print(textfields[0])
        print(textfields[0].text)

        # asercja
        self.assertEqual('Иоа́нн Иоа́ннович', textfields[0].text)
        self.assertEqual('123456789', textfields[1].text)
        self.assertEqual('Иоа́нн.Иоа́ннович@mail.ru', textfields[2].text)


if __name__ == 'main':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test1Appium)
    unittest.TextTestRunner(verbosity=2).run(suite)