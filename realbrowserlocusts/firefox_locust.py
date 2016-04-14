from locust import Locust
from real_browser_client import RealBrowserClient
from helper import FirefoxLocustDriver

class FirefoxLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides a Firefox webdriver that logs GET's and waits to locust
    """
    def __init__(self, *args, **kwargs):
        super(FirefoxLocust, self).__init__(*args, **kwargs)
        self.client = RealBrowserClient(FirefoxLocustDriver(), 30)
