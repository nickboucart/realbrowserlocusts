from locust import Locust
from locust.exception import LocustError
from selenium import webdriver
from core import RealBrowserClient

class RealBrowserLocust(Locust):
    client = None
    timeout = 30
    screen_width = None
    screen_height = None

    def __init__(self):
        super(RealBrowserLocust, self).__init__()
        if self.screen_width is None:
            raise LocustError("You must specify a screen_width for the browser")
        if self.screen_height is None:
            raise LocustError("You must specify a screen_height for the browser")

class ChromeLocust(RealBrowserLocust):
    """
    This is the abstract Locust class which should be subclassed. It provides a Firefox webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(ChromeLocust, self).__init__()
        self.client = RealBrowserClient(webdriver.Chrome(), self.timeout, self.screen_width, self.screen_height)

class FirefoxLocust(RealBrowserLocust):
    """
    This is the abstract Locust class which should be subclassed. It provides a Firefox webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(FirefoxLocust, self).__init__()
        self.client = RealBrowserClient(webdriver.Firefox(), self.timeout, self.screen_width, self.screen_height)

class PhantomJSLocust(RealBrowserLocust):
    """
    This is the abstract Locust class which should be subclassed. It provides a PhantomJS webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(PhantomJSLocust, self).__init__()
        self.client = RealBrowserClient(webdriver.PhantomJS(), self.timeout, self.screen_width, self.screen_height)
