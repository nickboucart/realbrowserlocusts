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


#class LocustUser(FirefoxLocust):
#class LocustUser(ChromeLocust):
class LocustUser(PhantomJSLocust):

    host = "not really used"
    wait_for_action_finished = 30 #in seconds
    min_wait = 100
    max_wait = 1000
    task_set = LocustUserBehavior
