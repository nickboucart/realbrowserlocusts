# Real Browser support for Locust.io load testing

This python package provides different Locusts that represent real browsers. This package is a thin wrapper around (parts of) Selenium Webdriver.


Installation via pip

    pip install realbrowserlocusts

Once installed, simple make a locustfile.py as per usual, but instead of inheriting your locust from HttpLocust, instantiate a FirefoxLocust, ChromeLocust or PhantomJSLocust as you which.

These locusts expose a self.client object, that is actually a selenium.webdriver, it will understand all the usual methods. The client also exposes a self.client.waitUntil method, that is similar to selenium's WebDriverWait, with the differences that these waits, their timing and success/failure are logged to locust.

An example locust scenario that uses real browser could be

    from realbrowserlocusts import FirefoxLocust, ChromeLocust, PhantomJSLocust
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC


    from locust import TaskSet, task


    class LocustUserBehavior(TaskSet):

        @task(1)
        def searchForLocust(self):
            self.client.get("http://locust.io/")
            self.client.waitUntil(EC.visibility_of_element_located((By.XPATH, '//a[text()="Documentation"]')), "documentation link is visible")
            self.client.find_element_by_xpath('//a[text()="Documentation"]').click()
            self.client.waitUntil(EC.visibility_of_element_located((By.XPATH, '//h1[text()="Locust Documentation"]')), "documentation is visible")


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
