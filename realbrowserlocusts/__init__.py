# pylint:disable=undefined-all-variable
""" Expose RealBrowserLocust subclasses at package level """
from realbrowserlocusts.locusts import FirefoxLocust, PhantomJSLocust, \
    ChromeLocust, HeadlessChromeLocust

__all__ = [
    'FirefoxLocust',
    'PhantomJSLocust',
    'ChromeLocust',
    'HeadlessChromeLocust'
]

__version__ = "0.2"
