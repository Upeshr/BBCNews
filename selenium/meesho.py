import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def human_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))
#driver = uc.Chrome(options=Options)

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return uc.Chrome(options=options)

driver = setup_driver()
def incremental_scroll(driver, steps=5, step_dist=500, pause=2):
    """
    Scrolls incrementally and waits for content to load.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        print("Scrolling incrementally...")
        for _ in range(steps):
            # Using 'window.scrollBy' with a dictionary for smoother, more human-like movement
            driver.execute_script(f"window.scrollBy({{top: {step_dist}, left: 0, behavior: 'smooth'}});")
            human_delay(0.3, 0.8)

        # Critical: Wait for the site to fetch new data and expand the DOM
        print("Waiting for new content...")
        time.sleep(pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # Try one last 'nudge' in case the loader is stuck
            driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                print("Reached end of page.")
                break
        
        last_height = new_height

driver = setup_driver()
driver.get("https://www.smartprix.com/mobiles/")
for _ in range(14):
     
    driver.execute_script("window.scrollBy(0, 400);")
    human_delay(1, 3)
data = driver.page_source
print(data)
human_delay()







driver.quit()