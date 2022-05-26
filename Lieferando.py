from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import Restaurant
from pandas import DataFrame
import numpy as np

class Lieferando(object):

    def __init__(self,area):
        self.listRestaurantsURL = []
        self.listreviews = []
        self.areaSearched = area
        self.delay = 15
        url = "https://www.lieferando.de/lieferservice/essen/rinteln-31737"
        self.loadDriver()
        self.driver.get(url)

    def loadDriver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=options)
 
    def loadListRestaurantsURL(self):

        #Wait all restaurants are loaded
        ul_xpath1 = '//*[@id="page"]/div[4]/section/div[1]/div/div[2]/div[2]/ul'
        ul_xpath2 = '//*[@id="page"]/div[4]/section/div[1]/div/div[3]/div[2]/ul'
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, ul_xpath1)))
            ul_xpath = ul_xpath1
        except TimeoutException:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, ul_xpath2)))
            ul_xpath = ul_xpath2
       
        self.scroll_to_botoom()

        ul = self.driver.find_element(by=By.XPATH, value=ul_xpath)
        lis = ul.find_elements(by=By.TAG_NAME, value='li')
        for li in lis:
            a = li.find_element(by=By.TAG_NAME, value='a')
            self.listRestaurantsURL.append(a.get_attribute("href"))
        print("List URL restaurants:\n",self.listRestaurantsURL)

    def getRestaurantsData(self):

        if(len(self.listRestaurantsURL) < 1):
            self.loadListRestaurantsURL()
        
        info_xpath = '//*[@id="page"]/div[2]/section/div[1]/div[1]/section/div/div[1]/div[2]/div/span[1]'
        resto = Restaurant.Restaurant()

        for url in self.listRestaurantsURL:

            self.driver.get(url)
            nbrReviews = self.getNbrOfReviews()

            WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, info_xpath)))
            self.driver.find_element(by=By.XPATH,value=info_xpath).click()

            restaurantName, city, owner = self.getRestaurantInfo()
            print(restaurantName, nbrReviews, city, owner)
            resto.appendData(restaurantName, owner, city, nbrReviews)

        self.writeInExcel(resto)

    def writeInExcel(self,resto):
        df = DataFrame({'Restaurant ': resto.names, 'Contact': resto.owners, 'Area': resto.citys, 'Info': resto.reviews})
        df["Call"] = " "
        df["Outcome"] = " "
        df.to_excel("output/" + self.areaSearched + '.xlsx', sheet_name='sheet1', index=False)

    def getRestaurantInfo(self):

        # impressum_xpath = '//*[@id="restaurant-about-panel-info"]/div/div[6]/div[2]/div/div/div[1]'
        impressum_class = 'GcAXtd'
        self.scroll_to_botoom()
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, impressum_class)))
        impressum = self.driver.find_element(by=By.CLASS_NAME, value=impressum_class)
        divs = impressum.find_elements(by=By.TAG_NAME, value='div')

        restaurantName = divs[0].text
        city = ''.join(divs[len(divs)-2].text.split(' ')[1:])
        owner = ''.join(divs[len(divs)-1].text.split('Gesetzlicher Vertreter:'))

        return restaurantName, city, owner


    def getNbrOfReviews(self):
        
        reviews_xpath = '//*[@id="page"]/div[2]/section/div[1]/div[1]/section/div/div[2]/div/div[2]/span'
        reviews_xpath2 = '//*[@id="page"]/div[2]/section/div[1]/div[1]/section/div/div[2]/div/div[2]'
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, reviews_xpath)))
            review = self.driver.find_element(by=By.XPATH, value=reviews_xpath).text
        except TimeoutException:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, reviews_xpath2)))
            review = self.driver.find_element(by=By.XPATH, value=reviews_xpath2).text
        return self.parseReviws(review)

    def parseReviws(self,review):
        res = review.split(" ")[0]
        return res[1:] + " reviews"
        
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

    def kill(self):
        print("Destroying the webBrowser...")
        self.driver.quit()
        exit()