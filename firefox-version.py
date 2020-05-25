from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.instagram.com/")
        sleep(2)
        self.driver.find_element_by_css_selector("input[name=username]")\
            .send_keys(username)
        self.driver.find_element_by_css_selector("input[name=password]")\
            .send_keys(password)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div")\
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[text() = 'Not Now']")\
            .click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a")\
            .click()
        sleep(2)
        self.driver.find_element_by_css_selector("a[href*='following']")\
            .click()
        following = self._get_names()
        print('You are following {} accounts'.format(len(following)))

        self.driver.find_element_by_css_selector("a[href*='followers']")\
            .click()
        followers = self._get_names()
        print('You have {} followers'.format(len(followers)))
        not_following_back = [user for user in following if user not in followers]
        return not_following_back

    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']

        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        return names

    def unfollow(self, list):
        for account in list:
            self.driver.find_element_by_css_selector('input[placeholder="Search"]')\
                .send_keys(account)
            sleep(3)
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]")\
                    .click()
            except NoSuchElementException:
                self.driver.find_element_by_css_selector('input[placeholder="Search"]')\
                    .clear()
                print ('I couldn\'t unfollow this account:', account)
                continue
            sleep(2)
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button")\
                    .click()
            except NoSuchElementException:
                print ('I couldn\'t unfollow this account:', account)
                continue
            self.driver.find_element_by_xpath("//button[text()='Unfollow']")\
                .click()     


myUserName = input('What is your username?')
myPassword = input('What is your password?')

my_checkUnfollowers = InstaBot(myUserName, myPassword)

# FIND WHO IS NOT FOLLOWING YOU BACK
not_following_back = my_checkUnfollowers.get_unfollowers() 
print(not_following_back)

# UNFOLLOW THESE BASTARDS!!!
# my_checkUnfollowers.unfollow(not_following_back)