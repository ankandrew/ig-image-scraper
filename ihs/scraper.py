import random
from time import sleep

from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .logger import Logger


class Scraper:
    URL = f'https://www.instagram.com/explore/tags'
    SLEEP_LOGIN_ENTER = 5
    WAIT_PAGE_LOAD = 4
    HUMAN_DELAY = 2

    def __init__(self,
                 login: dict = None,
                 driver_path: str = 'driver/chromedriver.exe',
                 url_save_path: str = 'log/urls.txt',
                 max_samples: int = None) -> None:
        self.login = login
        self.driver = webdriver.Chrome(driver_path)
        self.is_logged = False
        self.logger = Logger(url_save_path)
        if not max_samples:
            self.max_samples = float('inf')
        else:
            self.max_samples = max_samples

    def get_img_link(self, driver) -> set:
        most_recent = driver.find_elements_by_xpath("//h2[contains(text(), 'Most recent')]/following-sibling::div")
        # Filter displayed posts
        posts = most_recent[0]
        soup = BeautifulSoup(posts.get_attribute('innerHTML'), 'html.parser', parse_only=SoupStrainer('img'))
        return {link['src'] for link in soup if link.has_attr('src')}

    def __login(self) -> None:
        username_elem = self.driver.find_element_by_xpath("//input[@name='username']")
        username_elem.send_keys(self.login['username'])
        sleep(self.HUMAN_DELAY)
        password_elem = self.driver.find_element_by_xpath("//input[@name='password']")
        password_elem.send_keys(self.login['password'])
        sleep(self.HUMAN_DELAY)
        password_elem.send_keys(Keys.RETURN)
        sleep(self.SLEEP_LOGIN_ENTER)
        self.driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
        self.is_logged = True

    def scan(self, tag: str) -> None:
        self.driver.get(f'{self.URL}/{tag}/')
        # Wait for page to load
        sleep(self.WAIT_PAGE_LOAD)
        # If ig blocked our request it seems to be requiring logged user
        if self.driver.title == 'Login • Instagram' or 'login' in self.driver.current_url.lower():
            if self.login:
                self.__login()
            else:
                raise ValueError('IG blocked non-user from searching tags, so login must be provided!')
        # Re-visit tags sites (we may be re-directed to home page)
        if 'instagram' == self.driver.title.lower():
            self.driver.get(f'{self.URL}/{tag}/')
        img_set = self.get_img_link(self.driver)
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        counter = 0
        while True:
            if counter == 2:
                if self.login and not self.is_logged:
                    sleep(5)
                    self.__login()
                elif not self.is_logged:
                    print('Posts may be limited when not logging into an user!')
                    self.driver.execute_script("""document.querySelector("body").style.overflow="visible";""")
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(round(random.uniform(3, 4.3), 2))
            # Save new imgs
            img_set.update(self.get_img_link(self.driver))
            self.logger.log(img_set)
            if len(img_set) > self.max_samples:
                print(f'Finished scrapping. Asked for {self.max_samples}, got {len(img_set)}')
                return
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f'End of page (no more images). Scrapped {len(img_set)} urls')
                return
            last_height = new_height
            counter += 1
