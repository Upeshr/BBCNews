import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControll")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return uc.Chrome(options=options)

def pause(a=2, b=5):
    time.sleep(a, b)

driver = setup_driver()

def incremental_scroll(driver:uc.Chrome, scroll_pause=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 500);")
            pause(0.5, 1.5)

        time.sleep(scroll_pause)  # ✅ inside function

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("Reached end of page.")
            break

        last_height = new_height

driver.get("")
incremental_scroll()

data = driver.page_source

with open("flipkart.html", "w", encoding="utf-8") as file:
    file.write(data)
pause()

driver.quit()