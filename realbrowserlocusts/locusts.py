# pylint:disable=too-few-public-methods
""" Combine Locust with Selenium Web Driver """
import logging
from locust import Locust
from locust.exception import LocustError
from selenium import webdriver
from realbrowserlocusts.core import RealBrowserClient

_LOGGER = logging.getLogger(__name__)


class RealBrowserLocust(Locust):
    """
   This is the abstract Locust class which should be subclassed.
   """
    client = None
    timeout = 30
    screen_width = None
    screen_height = None

    def __init__(self):
        super(RealBrowserLocust, self).__init__()
        if self.screen_width is None:
            raise LocustError("You must specify a screen_width "
                              "for the browser")
        if self.screen_height is None:
            raise LocustError("You must specify a screen_height "
                              "for the browser")


class ChromeLocust(RealBrowserLocust):
    """
    Provides a Chrome webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(ChromeLocust, self).__init__()
        self.client = RealBrowserClient(
            webdriver.Chrome(),
            self.timeout,
            self.screen_width,
            self.screen_height
        )


class HeadlessChromeLocust(RealBrowserLocust):
    """
    Provides a headless Chrome webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(HeadlessChromeLocust, self).__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size={}x{}'.format(
            self.screen_width, self.screen_height
        ))
        options.add_argument('disable-gpu')
        driver = webdriver.Chrome(chrome_options=options)
        _LOGGER.info('Actually trying to run headless Chrome')
        self.client = RealBrowserClient(
            driver,
            self.timeout,
            self.screen_width,
            self.screen_height,
            set_window=False
        )


class FirefoxLocust(RealBrowserLocust):
    """
    Provides a Firefox webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(FirefoxLocust, self).__init__()
        self.client = RealBrowserClient(
            webdriver.Firefox(),
            self.timeout,
            self.screen_width,
            self.screen_height
        )


class PhantomJSLocust(RealBrowserLocust):
    """
    Provides a PhantomJS webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(PhantomJSLocust, self).__init__()
        self.client = RealBrowserClient(
            webdriver.PhantomJS(),
            self.timeout,
            self.screen_width,
            self.screen_height
        )
