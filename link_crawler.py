import os
from selenium.webdriver.common.by import By
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
from dotenv import load_dotenv


load_dotenv()

sqliteConnection = sqlite3.connect('linkedin.db')
cursor = sqliteConnection.cursor()
print("Database created and Successfully Connected to SQLite")
driver = webdriver.Chrome()

email = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

actions.login(driver, email, password) 


go_to_link = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22101452733%22%5D&origin=FACETED_SEARCH&sid=AAr"

driver.get(go_to_link)

time.sleep(10)

personal_link_selector = "ul.reusable-search__entity-result-list.list-style-none   li div.entity-result:not([data-chameleon-result-urn*='headless'])  a.app-aware-link.scale-down"
click_selector = "document.querySelector('button[aria-label=\"Next\"]:not([class*=\"disabled\"])').click();"


#marketing  textile Australia contact email "gmail" "yahoo" site:linkedin.com

for i in range(0,100):
    time.sleep(10)
    driver.execute_script(
                "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
    )
    f = open("personal_list.txt", "a")
    result = driver.find_elements(By.CSS_SELECTOR,personal_link_selector)
    for k in result:
        href = k.get_attribute("href")
        f.write("{0}\n".format(href))
    f.close()
    time.sleep(5)
    driver.execute_script(click_selector)
    time.sleep(10)


