import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from locust import Locust, events
from locust.exception import StopLocust


def wrapForLocust(request_type, name, func, *args, **kwargs):
    """
    Internall wrapper function that calls a given func with args and kwargs, and triggers locust events. The request type and name params for
    locusts events.request_success.fire are passed through from the params

    Args:
        request_type (str): the type of request
        name (str): name to be reported to events.request_*.fire
        func (Function): function to be timed and wrapped
        *args: arguments to be used when calling func
        **kwargs: Arbitrary keyword args used for calling func

    Returns:
        func(*args, **kwargs) if this function invocation does not raise an exception

    Raises:
        StopLocust: whenever func raises an exception, this exception is catched, logged to locust as a failure and a StopLocust exception is raised.
    """
    try:
        start_time = time.time()
        result = func(*args, **kwargs)
    except Exception as e:
        total_time = int((time.time() - start_time) * 1000)
        events.request_failure.fire(request_type=request_type, name=name, response_time=total_time, exception=e)
        raise StopLocust()
    else:
        total_time = int((time.time() - start_time) * 1000)
        events.request_success.fire(request_type=request_type, name=name, response_time=total_time, response_length=0)
        return result


class FirefoxLocustDriver(webdriver.Firefox):

    def get(self, url):
        return wrapForLocust("GET", url, super(FirefoxLocustDriver, self).get, url)

class PhantomJSLocustDriver(webdriver.PhantomJS):

    def get(self, url):
        return wrapForLocust("GET", url, super(PhantomJSLocustDriver, self).get, url)

class ChromeLocustDriver(webdriver.Chrome):

    def get(self, url):
        return wrapForLocust("GET", url, super(ChromeLocustDriver, self).get, url)

class RealBrowserClient(object):

    def __init__(self, driver, wait_time_to_finish, screen_width, screen_height):
        self.driver = driver
        self.driver.set_window_size(screen_width, screen_height)
        self.wait = WebDriverWait(self.driver, wait_time_to_finish)

    def waitUntil(self, method, message=""):
        return wrapForLocust("Wait for", message, self.wait.until, method, message)

    def __getattr__(self, attr):
        """Forward all messages this client doesn't understand to it's webdriver"""
        return getattr(self.driver, attr)
