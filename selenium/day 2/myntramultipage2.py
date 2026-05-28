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
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--robot-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0(Window NT 10.0; Win64: x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return uc.Chrome(options=options)

def pause(a=2, b=5):
    time.sleep(random.uniform(a, b))

def human_scroll(driver:uc.Chrome):
    total_height = driver.execute_script("return document.body.scrollHeight")
    current_pos = 0
    print("Start scrolling....")

    while current_pos < total_height:
        total_height = driver.execute_script(" return document.body.scrollHeight")
        step = random.randint(300, 600)
        current_pos += step

        driver.execute_script(f"window.scrollTo({{top: {current_pos}, behavior: 'smooth'}});")
        pause(0.8, 1.5)

        try:
            next_btn = driver.find_element(By.XPATH, "//li[@class='pagination-next']")

            visible = driver.execute_script("""
                var elem = arguments[0];
                var bounding = elem.getBoundingClientRect();
                return (
                    bounding.top >= 0 &&
                    bounding.left >= 0 &&
                    bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    bounding.right <= (window.innerWidth || document.documentElement.clientWidth));
                """, next_btn)