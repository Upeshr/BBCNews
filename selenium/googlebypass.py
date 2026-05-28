import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

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

driver = setup_driver()

driver.get("https://www.google.com")
human_delay()
driver.execute_script("window.scrollBy(0, 400);")

time.sleep(20)

search_box = driver.find_element(By.NAME, "q")

search_query = "amazon smartphones"

for i in search_query:
    search_box.send_keys(i)
    time.sleep(random.uniform(0.2, 0.5))

human_delay()
search_box.send_keys(Keys.ENTER)
human_delay(4, 7)

driver.execute_script("window.scrollBy(0, 400);")
human_delay(2, 4)


link = driver.find_element(By.CSS_SELECTOR, "a[href*='amazon']")
link.click()



input("press any key to quit")
driver.quit()