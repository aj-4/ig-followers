from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from secrets import pw


class InstaBot:
	def __init__(self, username, pw):
		self.username = username
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		# self.driver = webdriver.Chrome(executable_path='C:\WebDrivers\chromedriver.exe')
		self.driver.get("https://instagram.com") #Launches instagram on chrome
		sleep(2)
		# self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[2]/p/a').click() #Clicks login
		sleep(2)
		self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
		.send_keys(username)
		self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
			.send_keys(pw)
		self.driver.find_element_by_xpath('//button[@type="submit"]')\
			.click()
		sleep(4)
		self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
			.click()
		sleep(2)
		self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
			.click()
		sleep(2)

	def get_unfollowers(self):
		self.driver.find_element_by_xpath("//a[contains(@href,'/_aaronjack')]")\
			.click()
		sleep(2)
		self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
			.click()
		following = self._get_names()
		self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
			.click()
		followers = self._get_names()
		not_following_back = [user for user in following if user not in followers]
		print(not_following_back)

	def _get_names(self):
		sleep(2)
		#scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
		scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div")
		last_ht, ht = 0, 1
		while last_ht != ht:
			last_ht = ht
			sleep(3)
			ht = self.driver.execute_script("""
				arguments[0].scrollTo(0, arguments[0].scrollHeight); 
				return arguments[0].scrollHeight;
				""", scroll_box)

		links = scroll_box.find_elements_by_tag_name('a')
		names = [name.text for name in links if name.text != '']
		# close button 
		self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
			.click()
		print("Counted: " + str(len(names)) )
		return names

my_bot = InstaBot('_aaronjack', pw)
my_bot.get_unfollowers()
