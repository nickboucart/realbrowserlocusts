from locust import Locust
from real_browser_client import RealBrowserClient
from helper import PhantomJSLocustDriver

class PhantomJSLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides a PhantomJS webdriver that logs GET's and waits to locust
    """
    def __init__(self, *args, **kwargs):
        super(PhantomJSLocust, self).__init__(*args, **kwargs)
        self.client = RealBrowserClient(PhantomJSLocustDriver(), 30)
