import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

def setup_driver():
    options = Options()
    options.add_argument("--start-maximzed")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0(Windows NT 10.0; Win64; x65) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return uc.Chrome(options=options)

def pause(a=2, b=5):
    time.sleep(random.uniform(a, b))

def incremental_scroll(driver:uc.Chrome, max_click=2):
    load_more_count = 0

    while load_more_count < max_click:
        print("Scrolling to find the button....")

        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 500);")
            pause(0.8, 1.5)

        print("waiting for load more button to appear....")

        try:
            wait = WebDriverWait(driver, 10)
            load_more_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='sm-load-more']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_btn)
            pause(2, 3)

            print(f"Clicking load more({load_more_count}/{max_click})....")
            driver.execute_script("arguments[0].click():", load_more_btn)
            load_more_count += 1
            pause(4, 6)
        except Exception as e:
             print("Button didn't appear or timeout. Checking if we reachrd the end")
             break
        print("Finishing clicking and scrolling.")