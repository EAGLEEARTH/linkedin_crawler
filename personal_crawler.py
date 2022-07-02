import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from linkedin_scraper import actions
import sqlite3
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException


load_dotenv()

sqliteConnection = sqlite3.connect('linkedin.db')
cursor = sqliteConnection.cursor()
print("Database created and Successfully Connected to SQLite")
driver = webdriver.Chrome()

email = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
time.sleep(15)


adres_selector = "div.pb2.pv-text-details__left-panel > span.break-words"
name_selector = "h1.ember-view span, h1.text-heading-xlarge"
pozisyon_selector = "p.org-top-card-summary__tagline.t-16.t-black, div.text-body-medium.break-words"
sirket_link_selector = "section > div.pvs-list__outer-container > ul.pvs-list li.artdeco-list__item:nth-child(1) div.pvs-entity div > a[data-field='experience_company_logo']"
sriket_adı_selector = "div[aria-label='Current company'], section > div.pvs-list__outer-container > ul.pvs-list li.artdeco-list__item:nth-child(1) div.pvs-entity div > a[data-field='experience_company_logo'] span.hoverable-link-text > span[aria-hidden='true'],div.mt2.relative div.inline-show-more-text,div#experience + div +div ul li:nth-child(1) span.mr1.t-bold  span:nth-child(1)"
personal_email_selector = "section.pv-contact-info__contact-type.ci-email a"
personal_web_site_selector = "section.pv-contact-info__contact-type.ci-websites a"
profile_link_selector = "div.pv-contact-info__ci-container a"
contact_info_close_selector = "document.querySelector('button.artdeco-modal__dismiss').click();"
contact_info_click_selector = "document.querySelector('a#top-card-text-details-contact-info').click();"
phone_number = "section.pv-contact-info__contact-type.ci-phone li > span.t-14.t-black.t-normal"
got_to_sirket = "document.querySelector('section > div.pvs-list__outer-container > ul.pvs-list li.artdeco-list__item:nth-child(1) div.pvs-entity div > a[data-field=\"experience_company_logo\"]').click();"
go_to_abput = "document.querySelector('ul.org-page-navigation__items li.org-page-navigation__item a[href*=\"about\"]').click();"
company_web_site = "div.org-grid__content-height-enforcer section.artdeco-card a[href*='http']"
company_tel = "div.org-grid__content-height-enforcer section.artdeco-card a[href*='tel']"
company_Industry_seelctor = "section.org-top-card.artdeco-card div.org-top-card-summary-info-list > div.org-top-card-summary-info-list__info-item"
company_adress_seelctor = "section.org-top-card.artdeco-card div.org-top-card-summary-info-list > div.inline-block > div:nth-child(1)"


company_check = "section.artdeco-empty-state h2"


def click_func(selector):
    time.sleep(5)
    try:
        result = driver.find_element(By.CSS_SELECTOR,selector)
        if result:
            result.click
            time.sleep(5)
    except:
        print("Not click")


def execute_script_func(selector):
    driver.execute_script(selector)
    time.sleep(5)


def text_element_check(selector):
    try:
        result = driver.find_element(By.CSS_SELECTOR,selector).text
        if result:
            return result
        else:
            result="Notfound"
            return result
    except:
        print("Notfound")


def find_attribute_href(selector):
    try:
        result = driver.find_element(By.CSS_SELECTOR,selector)
        return result.get_attribute("href")
    except:
        print("Notfound")


def attribute_finds_elemtens(selector):
    try:
        result_list = []
        result = driver.find_elements(By.CSS_SELECTOR,selector)
        if result:
            for i in result:
                result_list.append(i.get_attribute("href"))
            
            return result_list
        else:
            result = "Notfound"
            return result
    except:
        print("Notfound")


def text_elemenst_find(selector):
    try:
        result_list = []
        result = driver.find_elements(By.CSS_SELECTOR,selector)
        if result:
            for i in result:
                result_list.append(i.text())
            
            return result_list
        else:
            result = "Notfound"
            return result
    except:
        print("Not found")


def join_func(params):
    if params != "NotFound":
        result = ",".join(params)
    else:
        params = "Notfound"
    return result


def personal_link_list():
    link_list = []
    with open('personal_list.txt') as f:
        lines = f.readlines()
        for i in lines:
            link_list.append(i)
    return link_list


link_list = personal_link_list()

for i in link_list:
    driver.get(i)
    time.sleep(15)
    delay = 1
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")


    name = text_element_check(name_selector)
    pozisyon = text_element_check(pozisyon_selector)
    sirket_linkedin_link = find_attribute_href(sirket_link_selector)
    sriket_adı  = text_element_check(sriket_adı_selector)
    adres = text_element_check(adres_selector)

    #contact_info_click = click_func(contact_info_click_selector)
    execute_script_func(contact_info_click_selector)

    profile_link= find_attribute_href(profile_link_selector)
    website_list = attribute_finds_elemtens(personal_web_site_selector)
    website_list = join_func(website_list)

    email_list = attribute_finds_elemtens(personal_email_selector)
    email_list = join_func(email_list)
    telefon_list = text_elemenst_find(phone_number)
    telefon_list = join_func(telefon_list)

    #contact_info_close_click = click_func(contact_info_close_selector)
    execute_script_func(contact_info_close_selector)
    driver.execute_script(
                "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
    )

    time.sleep(5)
    execute_script_func(got_to_sirket)
    time.sleep(8)
    try:
        is_company = text_element_check(company_check)
    except:
        is_company = False

    time.sleep(5)

    print("is company****",is_company)
    if is_company:

        get_company_web_site = "Notfound"
        get_company_tel = "Notfound"
        company_ındustry = "Notfound"
        company_adress = "Notfound"
        
    else:
        execute_script_func(go_to_abput)
        time.sleep(3)

        get_company_web_site = find_attribute_href(company_web_site)
        get_company_tel = find_attribute_href(company_tel)
        company_ındustry = text_element_check(company_Industry_seelctor)
        company_adress = text_element_check(company_adress_seelctor)
        if company_adress in "follo":
            company_adress = "Notfound"
        else:
            company_adress=company_adress

    print(name,adres,telefon_list, pozisyon,sirket_linkedin_link,
    sriket_adı,profile_link,website_list,email_list,get_company_web_site,get_company_tel,company_ındustry,company_adress)


    try:
        sqlite_select_Query = """INSERT into personal_list 
        (Personal_Name, Personal_Adress,Personal_Phone, Personal_Title,
        Personal_Linkedin_Link,Company_Name,Company_Linkedin_link,Personal_Website,
        Personal_Email,Company_Web_Site,Company_Phone,Company_Industry,Company_Adress)
        VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')
        """.format(name,adres,telefon_list,pozisyon,profile_link,sriket_adı,sirket_linkedin_link,website_list,email_list,get_company_web_site,get_company_tel,company_ındustry,company_adress)
        cursor.execute(sqlite_select_Query)
        sqliteConnection.commit()
        print("İnsert Done")
        time.sleep(2)
    except:
        print("İnsert Not Done")
driver.close()