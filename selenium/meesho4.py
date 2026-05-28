import time
import random
import undetected_chromedriver as uc
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------- HUMAN DELAY ---------------- #

def human_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))


# ---------------- CHROME SETUP ---------------- #

options = uc.ChromeOptions()

options.add_argument("--start-maximized")

options.add_argument(
    "user-agent=Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/120 Safari/537.36"
)

driver = uc.Chrome(options=options)

# ---------------- SCRAPER ---------------- #

try:
    driver.get("https://www.shopsy.in/0pm/~cs-nu9s0gaud4/pr?sid=0pm&collection-tab-name=Earphones+&bu=SHOPSY_EXCLUSIVE&pageCriteria=default") # Example category page
    human_delay(5, 8)

    # Scrolling logic...
    # (Insert your scrolling loop here)

    product_list = []
    
    # On Meesho, products are usually inside <div> elements with specific styles.
    # We look for the "ProductCard" container to keep Name and Price linked.
    cards = driver.find_elements(By.TAG_NAME, "div, span")

    for card in cards:
        try:
            # Finding name and price RELATIVE to the card
            # Product names are often in 'p' tags with specific font sizes
            name = card.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/span[1]").text
            
            # Prices are usually in 'h5' tags or bold 'p' tags
            price = card.find_element(By.XPATH, "//div[@class='sc-46489703-1 drgEeC']//div[2]//div[1]//div[1]//div[3]//div[1]//div[1]//div[1]//div[2]//div[2]//div[1]//div[2]//div[2]").text 
            
            if name and price:
                product_list.append({
                    "product_name": name,
                    "price": price
                })
        except:
            continue # Skip if a card is an ad or missing data

    # Save to JSON
    with open("meesho_data.json", "w", encoding="utf-8") as f:
        json.dump(product_list, f, indent=4, ensure_ascii=False)

    print(f"Successfully saved {len(product_list)} products to meesho_data.json")

finally:
    # Using quit() inside 'finally' is safer
    driver.quit()