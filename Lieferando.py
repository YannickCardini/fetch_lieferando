from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Lieferando(object):

    def __init__(self):
        url = "https://www.lieferando.de/lieferservice/essen/dahme-spreewald-schoenefeld-12529"
        self.loadDriver()
        self.driver.get(url)

    def loadDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")
        # options.add_argument("--start-maximized")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=options)
 
    def loadListRestaurants(self):

        #Wait all restaurants are loaded
        ul_xpath = '//*[@id="page"]/div[4]/section/div[1]/div/div[4]/div[2]/ul'
        WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, ul_xpath)))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.scroll_to_botoom()

        ul = self.driver.find_element(by=By.XPATH, value=ul_xpath)
        lis = ul.find_elements(by=By.TAG_NAME, value='li')
        for li in lis:
            print("Title:"+ li.get_attribute("class"))

    def scroll_to_botoom(self):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height