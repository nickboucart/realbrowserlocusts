# pylint:disable=undefined-all-variable
from realbrowserlocusts.locusts import FirefoxLocust, PhantomJSLocust, \
    ChromeLocust
""" Expose RealBrowserLocust subclasses at package level """
__all__ = [
    'FirefoxLocust',
    'PhantomJSLocust',
    'ChromeLocust'
]

__version__ = "0.2"
