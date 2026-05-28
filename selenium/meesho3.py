import time
import random
import undetected_chromedriver as uc

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

    driver.get("https://www.meesho.com/")

    # Wait for products to appear
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

    human_delay(3, 5)

    actions = ActionChains(driver)

    body = driver.find_element(By.TAG_NAME, "body")

    # Store unique products
    all_products = set()

    # ---------------- SCROLLING ---------------- #

    for i in range(25):

        print(f"\nScrolling {i+1}/25")

        # Keyboard scroll
        body.send_keys(Keys.PAGE_DOWN)

        # JS scroll
        driver.execute_script(
            "window.scrollBy(0, 1200);"
        )

        # Small random mouse movement
        try:
            actions.move_by_offset(
                random.randint(5, 40),
                random.randint(5, 40)
            ).perform()

        except:
            pass

        human_delay(2, 4)

        # Debug scroll position
        position = driver.execute_script(
            "return window.pageYOffset"
        )

        print(f"Scroll Position: {position}")

        # ---------------- SCRAPE PRODUCTS ---------------- #

        products = driver.find_elements(By.TAG_NAME, "p")
        prices = driver.find_elements(By.TAG_NAME, "h5")

        print(f"Visible Products: {len(products)}")

        for product, price in zip(products, prices):

            name = product.text.strip()
            cost = price.text.strip()

            if name:

                all_products.add(
                    f"{name} ---> {cost}"
                )

    # ---------------- FINAL OUTPUT ---------------- #

    print("\n\n=========== FINAL PRODUCTS ===========\n")

    for item in all_products:
        print(item)

    print(f"\nTotal Unique Products: {len(all_products)}")


finally:

    human_delay(5, 8)

    driver.quit()