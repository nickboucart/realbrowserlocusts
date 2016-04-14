from helper import wrapForLocust as wrap
from selenium.webdriver.support.ui import WebDriverWait

class RealBrowserClient(object):

    def __init__(self, driver, wait_time_to_finish):
        self.driver = driver
        self.driver.set_window_size(1120, 550)
        self.wait = WebDriverWait(self.driver, wait_time_to_finish)

    def waitUntil(self, method, message=""):
        return wrap("Wait for", message, self.wait.until, method, message)

    def __getattr__(self, attr):
        """Forward all messages this client doesn't understand to it's webdriver"""
        return getattr(self.driver, attr)
