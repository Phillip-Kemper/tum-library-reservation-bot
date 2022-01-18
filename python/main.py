import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import configparser

config = configparser.RawConfigParser()
config.read('private.properties')

name = config.get('Data', 'name')
kennung = config.get('Data', 'kennung')
mail = config.get('Data', 'mail')
morning_session = config.get('Data','morning_session') == 'True'
morning_session = 1 if morning_session else 2

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
tum_library_url = 'https://www.ub.tum.de/arbeitsplatz-reservieren'
browser.get(tum_library_url)

book_now_a_button = browser.find_element(By.XPATH, f'//*[@id="block-system-main"]/div/div/div[2]/table/tbody/tr[{morning_session}]/td[4]').find_element_by_tag_name('a')

book_now_a_button.send_keys(Keys.ENTER)
timeout = 5
try:
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="edit-submit"]'))
    WebDriverWait(browser, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print("Page loaded")

submit_button = browser.find_element(By.XPATH,'//*[@id="edit-submit"]')

browser.find_element(By.ID, "edit-field-tn-name-und-0-value").click()
browser.find_element(By.ID, "edit-field-tn-name-und-0-value").send_keys(name)
browser.find_element(By.ID, "edit-anon-mail").send_keys(mail)
browser.find_element(By.CSS_SELECTOR, ".form-type-radio:nth-child(1) > .option").click()
browser.find_element(By.ID, "edit-field-tum-kennung-und-0-value").click()
browser.find_element(By.ID, "edit-field-tum-kennung-und-0-value").send_keys(kennung)
checkbox = browser.find_element(By.CSS_SELECTOR, ".form-item-field-benutzungsrichtlinien-und > .option")
browser.execute_script("arguments[0].innerText = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'", checkbox)
checkbox.click()
browser.find_element(By.CSS_SELECTOR, ".form-item-field-datenschutzerklaerung-und > .option").click()

time.sleep(5)

submit_button.send_keys(Keys.ENTER)
