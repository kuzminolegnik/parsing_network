from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import json
import time

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe', options=options)
driver.get('https://www.mvideo.ru/')

assert "М.Видео" in driver.title

el_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@data-init, 'ajax-category-carousel')][2]"))
)

action = ActionChains(driver)
action.move_to_element(el_container)
action.perform()

el_next = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@data-init, 'ajax-category-carousel')][2]//a[contains(@class, 'next-btn')]"))
)

while el_next.is_displayed():
    el_next.click()
    time.sleep(1)

el_items = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.XPATH,
         "/html/body/div[1]/div/div[3]/div[10]/div/div[2]/div/div/div/div[1]/div/ul//a[contains(@class, 'sel-product-tile-title')]"))
)

data = [json.loads(item.get_attribute('data-product-info')) for item in el_items]

client = MongoClient('mongodb://localhost:27017/')
db_mongo = client.lesson7
collection = db_mongo['mvideo']
collection.delete_many({})
collection.insert_many(data)

driver.close()
