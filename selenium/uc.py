import undetected_chromedriver as uc
import time
import random
import json
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver



# ── Config ──────────────────────────────────────────────────────────────────
TARGET_URL = "https://books.toscrape.com/"


OUTPUT_FILE = "scraped_data.json" # or .csv



# ── Driver Setup ─────────────────────────────────────────────────────────────

def create_driver():

    options = uc.ChromeOptions()



# Non-headless (visible browser)

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

# Randomize window size slightly to appear more human

    width = random.randint(1200, 1920)
    height = random.randint(800, 1080)
    options.add_argument(f"--window-size={width},{height}")

    driver = uc.Chrome(options=options, version_main=148)
# Override navigator properties to reduce fingerprinting

    driver.execute_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined});Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});""")

    return driver

# ── Human-like Delays ────────────────────────────────────────────────────────
def random_delay(min_sec=1.5, max_sec=4.5):
    """Random sleep to mimic human reading/thinking time."""
    time.sleep(random.uniform(min_sec, max_sec))

def micro_delay():
    """Tiny delay between actions."""
    time.sleep(random.uniform(0.1, 0.5))

# ── Human-like Mouse Scrolling ───────────────────────────────────────────────
def human_scroll(driver, scrolls=None):
    """Scroll the page in random increments, like a human would."""
    if scrolls is None:
        scrolls = random.randint(3, 7)


    for _ in range(scrolls):
        scroll_amount = random.randint(200, 600)
        direction = random.choice([1, 1, 1, -1]) # bias toward scrolling down
        driver.execute_script(f"window.scrollBy(0, {direction * scroll_amount});")
        time.sleep(random.uniform(0.4, 1.2))

def scroll_to_element(driver, element):
    """Smoothly scroll an element into view."""
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",element)

    micro_delay()

# ── Human-like Mouse Movement ────────────────────────────────────────────────
def move_mouse_randomly(driver):
    """Move mouse to a random position on the page."""
    action = ActionChains(driver)
    x_offset = random.randint(-200, 200)
    y_offset = random.randint(-100, 100)
    action.move_by_offset(x_offset, y_offset).perform()
    micro_delay()



# ── Core Scraping Logic ──────────────────────────────────────────────────────

def scrape_page(driver, url):
    driver.get(url)
    print(url)
    random_delay(2, 5) # Wait for page to load naturally

    # Simulate human behavior on page load
    human_scroll(driver, scrolls=random.randint(2, 4))
    move_mouse_randomly(driver)
    random_delay(1, 3)

    # Wait for a key element (adjust selector as needed)
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(wait)
    except Exception as e:
        print(f"Page load timeout: {e}")
        return []

    results = []

# ── YOUR SCRAPING LOGIC HERE ─────────────────────────────────────────
# Example: scrape article titles and links

    items = driver.find_elements(By.CSS_SELECTOR, "h3 a") # adjust selector
    for item in items:
        try:
            scroll_to_element(driver, item)
            micro_delay()

            data = {
                "title": item.text.strip(),
                "url": item.get_attribute("href"),
                }
            results.append(data)
            random_delay(0.3, 0.8) # small pause between reads
        except Exception as e:
            print(f"Error extracting item: {e}")
            continue
# ─────────────────────────────────────────────────────────────────────
    return results

# ── Save Data ────────────────────────────────────────────────────────────────
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} records to {filename}")

def save_csv(data, filename):
    if not data:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} records to {filename}")

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    driver = create_driver()
    all_data = []
    try:
# Single page example — loop over URLs for multi-page
        data = scrape_page(driver, TARGET_URL)
        all_data.extend(data)
        # Add delay between pages if paginating
        # for page_url in page_urls:
        # data = scrape_page(driver, page_url)
        # all_data.extend(data)
        # random_delay(3, 8) # longer pause between pages

    except Exception as e:
        print(f"Scraping error: {e}")
    finally:
        driver.quit()

# Save results
    if OUTPUT_FILE.endswith(".csv"):
        save_csv(all_data, OUTPUT_FILE)
    else:
        save_json(all_data, OUTPUT_FILE)

if __name__ == "__main__":
    main()