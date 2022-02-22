from selenium import webdriver

class email(self):
    def start(self):
        self.driver = webdriver.Chrome(executable_path='C:/Users/roman/AppData/Local/Programs/Python/Python310/Lib/site-packages/selenium/webdriver/chromium/chromedriver')
        self.driver.get('www.google.com')