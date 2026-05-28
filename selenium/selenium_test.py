import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def human_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return webdriver.Chrome(options=options)

def human_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))

driver = setup_driver()

driver.get("https://quotes.toscrape.com/js/")

#wait for js content
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))
human_delay()

#scrape plus navigate
for page in range(10):                                                              
    print(f"\n----Page {page+1}----")

    quotes = driver.find_elements(By.CLASS_NAME, "quote")

    for q in quotes:
        text = q.find_element(By.CLASS_NAME, "text").text
        author = q.find_element(By.CLASS_NAME, "author").text
        print(text, "-", author)

        #scroll like human
    driver.execute_script("window.scrollTo(0, document.body.scrollHight);")

        #click next button
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
        next_btn.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

    except:
        print("no more page")
        break





input("Press Enter to quit...")
driver.quit()