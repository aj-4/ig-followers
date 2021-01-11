from selenium import webdriver
from time import sleep

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Edge()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        sleep(2)
        
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        # This is for the save log-in info 
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)
        # This is for the turn on notifications
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()

    def get_unfollowers(self):
        #self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            #.click()
        # Reaching the profile.
        self.driver.find_element_by_xpath("//section/nav/div[2]/div/div/div[3]/div/div[5]/span/img").click()
        sleep(1)
        self.driver.find_element_by_xpath("//section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]/div").click()
            
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        print("\nUsers that not following you back: \n")
        print(not_following_back)

    def _get_names(self):
        sleep(2)
        #sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView(true)')
        #sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

# You can get these two from an external file if you want 

username = '' # userneme here
password = '' # password here



my_bot = InstaBot(username, password)
my_bot.get_unfollowers()
