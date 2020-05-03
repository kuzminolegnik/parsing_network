from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe', options=options)
driver.get('https://mail.ru/')

assert "Mail.ru" in driver.title

el_login = driver.find_element_by_xpath('//a[@id="PH_authLink"]')
el_login.click()

switch_frame = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[contains(@src, "https://account.mail.ru/login/")]'))
)

if not switch_frame:
    driver.close()

el_username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'username-formfield')]//input[@name='Login']"))
)

el_username.send_keys("study.ai_172@mail.ru")
el_username.send_keys(Keys.RETURN)

el_pass = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'password')]//input[@name='Password']"))
)

el_pass.send_keys("NewPassword172")
el_pass.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'dataset__items')]"))
)

links = []

while True:
    letters = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class, 'dataset__items')]/a[contains(@class, 'js-letter-list-item')]"))
    )
    new_links = list(set(links + [letters[i].get_attribute('href') for i in range(len(letters))]))
    # Поставил ограничение для теестов len(links) > 10
    if len(new_links) == len(links) or len(links) > 10:
        break

    links = new_links
    action = ActionChains(driver)
    action.move_to_element(letters[-1])
    action.perform()
    time.sleep(2)

data = []

for link in links:
    driver.get(link)

    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'thread__header')]"))
    ).text

    source = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'letter__author')]//span[contains(@class, 'letter-contact')]"))
    ).get_attribute('title')

    date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'letter__author')]//div[contains(@class, 'letter__date')]"))
    ).text

    description = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'letter__body')]"))
    ).text

    data.append({
        "title": title,
        "source": source,
        "date": date,
        "description": description
    })

client = MongoClient('mongodb://localhost:27017/')
db_mongo = client.lesson7
collection = db_mongo['mail']
collection.delete_many({})
collection.insert_many(data)

driver.close()
