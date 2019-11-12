from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from time import sleep
import secrets


class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def close_browser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://instagram.com")
        sleep(2)
        login_button = driver.find_element_by_xpath("//a[contains(text(), 'Log in')]")
        login_button.click()
        
        # driver.switch_to_window(driver.window_handles[-1])
        sleep(2)
        login_field = driver.find_element_by_xpath("//input[@name=\"username\"]")
        login_field.send_keys(self.username)
        pw_field = driver.find_element_by_xpath("//input[@name=\"password\"]")
        
        pw_field.send_keys(self.password)
        login_button = driver.find_element_by_xpath('//button[@type="submit"]')
        login_button.click()
        sleep(4)
        driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(1)
        driver.find_element_by_xpath("//a[contains(text(), '{}')]".format(self.username)).click()
        sleep(2)


    def crawl(self):
        self.open_users('followers')
        followers = self.scroll_and_get()
        self.open_users('following')
        following = self.scroll_and_get()
        not_following_back = [f for f in following if f not in followers]
        print('USERS NOT FOLLOWING BACK', not_following_back)

    
    def open_users(self, user_type):
        driver = self.driver
        driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(user_type)).click()
        sleep(2)
        dialog = driver.find_element_by_xpath("//div[contains(@role, 'dialog')]")
    
    def scroll_and_get(self):
        driver = self.driver
        dialog = driver.find_element_by_xpath("//div[contains(@role, 'dialog')]")
        scroll_box = driver.find_element_by_xpath("//div[contains(@role, 'dialog')]/*[last()]")
        sugs = driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]');
        driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(2)
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;', scroll_box)
        names = dialog.find_elements_by_tag_name('a')
        users = [name.text for name in names if name != ''][2:]
        sugs = driver.find_element_by_xpath('//html/body/div[3]/div/div[1]/div/div[2]/button').click()
        return list(users)

insta_bot = InstaBot(secrets.username, secrets.password)
insta_bot.login()
insta_bot.crawl()