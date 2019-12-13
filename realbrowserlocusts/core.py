# pylint:disable=too-few-public-methods
""" Core Selenium wrapping functionality """
import time
from selenium.webdriver.support.ui import WebDriverWait
from locust import events
from locust.exception import StopLocust


def wrap_for_locust(request_type, name, func, *args, **kwargs):
    """
    Wrap Selenium activity function with Locust's event fail/success
    method

    :param request_type: the type of request
    :param name: name to be reported to events.request_*.fire
    :param func: callable to be timed and logged
    :return result: Result of the provided function if doesn't raise exception
    """
    try:
        start_time = time.time()
        result = func(*args, **kwargs)
    except Exception as event_exception:
        total_time = int((time.time() - start_time) * 1000)
        events.request_failure.fire(
            request_type=request_type,
            name=name,
            response_time=total_time,
            response_length=0,
            exception=event_exception
        )
        raise StopLocust()
    else:
        total_time = int((time.time() - start_time) * 1000)
        events.request_success.fire(
            request_type=request_type,
            name=name,
            response_time=total_time,
            response_length=0
        )
        return result


class RealBrowserClient(object):
    """
    Web Driver client with Locust functionality
    """

    def __init__(self, driver, wait_time_to_finish, screen_width,
                 screen_height, set_window=True):
        self.driver = driver
        if set_window:
            self.driver.set_window_size(screen_width, screen_height)
        self.wait = WebDriverWait(self.driver, wait_time_to_finish)

    @staticmethod
    def timed_event_for_locust(request_type, message, func, *args, **kwargs):
        """
        Use this method whenever you have a logical sequence of browser steps
        that you would like to time. Group these in a seperate, not @task
        method and call them using this method. These will show up in the
        locust web interface with timings

        Args:
            request_type (str): the type of request
            message (str): name to be reported to events.request_*.fire
            func (Function): callable to be timed and logged
            *args: arguments to be used when calling func
            **kwargs: Arbitrary keyword args used for calling func

        Returns:
            func(*args, **kwargs) if this function invocation does not raise
            an exception

        Raises:
            StopLocust: whenever func raises an exception, this exception is
            catched, logged to locust as a failure and a StopLocust exception
            is raised.
        """
        return wrap_for_locust(request_type, message, func, *args, **kwargs)

    def __getattr__(self, attr):
        """
        Forward all messages this client doesn't understand to it's webdriver
        """
        return getattr(self.driver, attr)
