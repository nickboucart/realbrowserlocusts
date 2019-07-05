# pylint:disable=too-few-public-methods
""" Combine Locust with Selenium Web Driver """
import logging
from os import getenv as os_getenv
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
        self.proxy_server = os_getenv("LOCUST_BROWSER_PROXY", None)


class ChromeLocust(RealBrowserLocust):
    """
    Provides a Chrome webdriver that logs GET's and waits to locust
    """

    timeout =  15 #in seconds in waitUntil thingies
    stop_timeout = 120
    min_wait = 1000
    max_wait = 2000
    screen_width = 1200
    screen_height = 800

    def teardown(self):
        try:
            gevent.sleep(5)  # let reports complete its job
            from locust.web import logger
            logger.warn('Shutting down all')
            runners.locust_runner.stop()
            runners.locust_runner.quit()
        finally:
            import gc
            from locust.web import logger
            logger.warn('Shutting down all')
            gevent.sleep(5)
            gevent.killall([obj for obj in gc.get_objects() if isinstance(obj, gevent.Greenlet)])
            os._exit(0)

    def __init__(self):
        super(ChromeLocust, self).__init__()
        options = webdriver.ChromeOptions()
        if self.proxy_server:
            _LOGGER.info('Using proxy: ' + self.proxy_server)
            options.add_argument('proxy-server={}'.format(self.proxy_server))
        self.client = RealBrowserClient(
            webdriver.Chrome(chrome_options=options),
            self.timeout,
            self.screen_width,
            self.screen_height
        )


class HeadlessChromeLocust(RealBrowserLocust):
    """
    Provides a headless Chrome webdriver that logs GET's and waits to locust
    """

    timeout =  15 #in seconds in waitUntil thingies
    stop_timeout = 120
    min_wait = 1000
    max_wait = 2000
    screen_width = 1200
    screen_height = 800

    def teardown(self):
        try:
            gevent.sleep(5)  # let reports complete its job
            from locust.web import logger
            logger.warn('Shutting down all')
            runners.locust_runner.stop()
            runners.locust_runner.quit()
        finally:
            import gc
            from locust.web import logger
            logger.warn('Shutting down all')
            gevent.sleep(5)
            gevent.killall([obj for obj in gc.get_objects() if isinstance(obj, gevent.Greenlet)])
            os._exit(0)

    def __init__(self):
        super(HeadlessChromeLocust, self).__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size={}x{}'.format(
            self.screen_width, self.screen_height
        ))
        options.add_argument('disable-gpu')
        if self.proxy_server:
            _LOGGER.info('Using proxy: ' + self.proxy_server)
            options.add_argument('proxy-server={}'.format(self.proxy_server))
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

    timeout =  15 #in seconds in waitUntil thingies
    stop_timeout = 120
    min_wait = 1000
    max_wait = 2000
    screen_width = 1200
    screen_height = 800

    def teardown(self):
        try:
            gevent.sleep(5)  # let reports complete its job
            from locust.web import logger
            logger.warn('Shutting down all')
            runners.locust_runner.stop()
            runners.locust_runner.quit()
        finally:
            import gc
            from locust.web import logger
            logger.warn('Shutting down all')
            gevent.sleep(5)
            gevent.killall([obj for obj in gc.get_objects() if isinstance(obj, gevent.Greenlet)])
            os._exit(0)

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
