import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return uc.Chrome(options=options)

def pause(a=2, b=5):
    time.sleep(random.uniform(a, b))

def incremental_scroll(driver:uc.Chrome, max_click=2):
    load_more_count = 0
    
    while load_more_count < max_click:
        # 1. Scroll down until the bottom or near where the button should be
        print("Scrolling to find the button...")
        for _ in range(10):
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(0.8) # Quick human-like scrolls
        
        # 2. Wait for the button to be AT LEAST present in the DOM
        print(f"Waiting for Load More button to appear...")
        try:
            # This waits up to 10 seconds for the button to exist
            wait = WebDriverWait(driver, 10)
            load_more_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='sm-load-more']")))
            
            # Scroll the button into view specifically
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_btn)
            pause(2, 3)

            print(f"Clicking Load More ({load_more_count + 1}/{max_click})...")
            driver.execute_script("arguments[0].click();", load_more_btn)
            
            load_more_count += 1
            pause(4, 6) # CRITICAL: Give it time to actually load the new data
            
        except Exception as e:
            print("Button didn't appear or timed out. Checking if we reached the end.")
            # Check if height changed; if not, we are actually at the end
            break

    print("Finished scrolling and clicking.")

driver = None
try:
    driver = uc.Chrome()
    driver.get("https://www.smartprix.com/scooters/electric-fuel")
    pause(3, 5)
    incremental_scroll(driver, max_click=2)
    pause(5, 7)

except Exception as e:
    print("Error:", e)


finally:
    if driver:
        try:
            print("Cleaning up browser...")
            driver.quit()
        except OSError:
            # This catches [WinError 6] and just ignores it
            pass
        except Exception as e:
            print(f"Final cleanup error: {e}")        