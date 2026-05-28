import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def human_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 ""(Windows NT 10.0; Win64; x64) ""AppleWebKit/537.36 ""Chrome/120 Safari/537.36")

# Note: undetected_chromedriver usually handles user-agents well on its own, 
# but keeping it doesn't hurt.
driver = uc.Chrome(options=options)

try:
    driver.get("https://www.meesho.com")
    
    # Wait for the body to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    human_delay(3, 5)

    actions = ActionChains(driver)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
    # Scroll down
        driver.execute_script("""window.scrollTo({top: document.body.scrollHeight,behavior: 'smooth'});""")

        human_delay(2, 4)

    # Mouse movement
        try:
            actions.move_by_offset(random.randint(10, 50),random.randint(10, 50)).perform()

        except:
            pass

    # New page height
        new_height = driver.execute_script("return document.body.scrollHeight")

    # If no new content loaded -> stop
        if new_height == last_height:
            break

        last_height = new_height
        

        human_delay(1, 3)

    # Specific selector for product names (Targeting the actual product card text)
    # Note: Class names on Meesho change frequently; 'ProductDescription' is a common fragment
    products = driver.find_elements(By.TAG_NAME, "h3")
    price = driver.find_element(By.TAG_NAME, "h5")
    
    print(f"Scrape Complete. Total potential products identified: {len(products)}")
    
    for product in products: # Print first 10 for verification
        print(f"- {product.text}")
        print(f"- {price.text}")

finally:
    human_delay(5, 10)
    driver.quit()