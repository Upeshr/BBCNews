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
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0(Windows NT 10.0: Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return uc.Chrome(options=options)

def pause(a=2, b=5):
    time.sleep(random.uniform(a, b))


def human_scroll_to_next(driver):
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    current_pos = 0
    step = 400  # How many pixels to move per "flick"
    
    print("Starting human-like crawl...")

    while current_pos < total_height:
        # 1. Update total height in case more products loaded
        total_height = driver.execute_script("return document.body.scrollHeight")
        
        # 2. Scroll to the next position
        current_pos += step
        driver.execute_script(f"window.scrollTo(0, {current_pos});")
        
        # 3. CRITICAL: A real pause to let the browser draw the images
        time.sleep(random.uniform(0.7, 1.2)) 
        
        # 4. Check if the "Next" button is visible yet
        try:
            next_btn = driver.find_element(By.XPATH, "//li[@class='pagination-next']")
            
            # Check if button is within the current viewport
            is_visible = driver.execute_script("""
                var elem = arguments[0];
                var bounding = elem.getBoundingClientRect();
                return (
                    bounding.top >= 0 &&
                    bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)
                );
            """, next_btn)

            if is_visible:
                print("Found 'Next' button in view! Stopping scroll.")
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_btn)
                return True # Exit function
        except:
            pass # Keep scrolling if not found
            
    print("Reached the bottom.")
    return False

driver = None       
if __name__ == "__main__":
    driver = setup_driver()
    try:
        driver.get("https://www.myntra.com/men-tshirts?f=Brand%3ARoadster&rf=Price%3A100.0_500.0_100.0%20TO%20500.0")
        pause(5, 7)
        human_scroll_to_next(driver)
        pause(3, 5)
        print("Now on the next page!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if driver:
            print("Closing browser safely...")
            try:
                driver.close()
                driver.quit()
            except OSError:
                pass
        print("Session ended.")
        # FORCE EXIT: This prevents Python 3.14 from triggering the deallocator error
        os._exit(0)