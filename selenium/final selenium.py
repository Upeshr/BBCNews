import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def human_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

driver = setup_driver()

# ---------------- STEP 1: OPEN GOOGLE ----------------
driver.get("https://www.google.com/")
human_delay()

# ---------------- STEP 2: TYPE SEARCH ----------------
search_box = driver.find_element(By.NAME, "q")

search_query = "amazon smartphones"
search_box.send_keys(search_query)
human_delay(1, 2)

# ---------------- STEP 3: PRESS ENTER ----------------
search_box.send_keys(Keys.RETURN)
human_delay(3, 6)

# ---------------- STEP 4: CLICK FIRST RESULT ----------------
results = driver.find_elements(By.CSS_SELECTOR, "h3")

if results:
    results[0].click()

human_delay(3, 6)

# ---------------- STEP 5: SCROLL LIKE HUMAN ----------------
scroll_pause = random.uniform(1, 2)

for _ in range(5):
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(scroll_pause)

# ---------------- STEP 6: WAIT ----------------
print("Human-like browsing complete. Waiting...")
time.sleep(10)

driver.quit()