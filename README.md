# Real Browser support for Locust.io load testing

This python package provides different Locusts that represent real browsers. This package is a thin wrapper around (parts of) Selenium Webdriver.


Installation via pip

    pip install realbrowserlocusts

Once installed, simple make a locustfile.py as per usual, but instead of inheriting your locust from HttpLocust, instantiate a FirefoxLocust, ChromeLocust, HeadlessChromeLocust or PhantomJSLocust as you which.

These locusts expose a self.client object, that is actually a selenium.webdriver, it will understand all the usual methods. The client also exposes a self.client.wait object, that is a selenium's WebDriverWait. A last method that is exposed by the client is the self.client.timed_event_for_locust method, that can be used to group a number of browser actions togehter, and time them in locust.

An example locust scenario that uses real browser could be:

```python
from realbrowserlocusts import FirefoxLocust, ChromeLocust, PhantomJSLocust
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from locust import TaskSet, task


class LocustUserBehavior(TaskSet):

    def open_locust_homepage(self):
        self.client.get("http://locust.io/")
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[text()="Documentation"]')), "documentation link is visible")

    def click_through_to_documentation(self):
        self.client.find_element_by_xpath('//a[text()="Documentation"]').click()
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[text()="Locust Documentation"]')), "documentation is visible")

    @task(1)
    def homepage_and_docs(self):
        self.client.timed_event_for_locust("Go to", "homepage", self.open_locust_homepage)
        self.client.timed_event_for_locust("Click to", "documentation", self.click_through_to_documentation)


class LocustUser(FirefoxLocust):
#class LocustUser(ChromeLocust):
#class LocustUser(PhantomJSLocust):

    host = "not really used"
    timeout = 30 #in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 1000
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior
```

### Using proxy with Chrome browser

To use proxy server while testing with Chrome browser, use LOCUST_BROWSER_PROXY environment variable, for example:

```
export LOCUST_BROWSER_PROXY=socks5://localhost:8899
```

It can be helpful especially while tests development.