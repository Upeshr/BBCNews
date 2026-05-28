import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

def scrape_maps_with_details(search_query, max_results=5):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--lang=en")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    
    
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
        
    try:
        driver.get("https://www.google.com/maps")
            
            # 1. Search
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ucc-1']")))
        search_box.send_keys("restaurants kathmandu")
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)
            
            # 2. Identify the Left Results Feed Panel
        try:
            feed_panel = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
        except Exception:
            print("Could not find the results panel.")
            return

        print("Gathering initial listings...")
            # Scroll slightly to load at least a few items
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", feed_panel)
        time.sleep(3)
            
            # Pull the clickable cards from the left panel
        cards = feed_panel.find_elements(By.XPATH, './/a[contains(@href, "/maps/place/")]')
        cards = cards[:max_results]  # Limit to your target count
        print(f"Found {len(cards)} listings to investigate.")
            
        results = []

            # 3. Loop through individual cards to open the Right Detail Panel
        for index, card in enumerate(cards):
            try:
                print(f"\nProcessing item {index + 1}...")
                    
                    # Scroll the card into view within the left panel so it's clickable
                driver.execute_script("arguments[0].scrollIntoView(true);", card)
                time.sleep(1)
                    
                    # Get the name from the card before clicking
                business_name = card.get_attribute("aria-label")
                    
                    # Click the card to open the right-side information panel
                card.click()
                print(f"Clicked: '{business_name}'. Waiting for right detail panel...")
                    
                    # Give the right panel 3-4 seconds to load its dynamic contents completely
                time.sleep(3.5)
                    
                    # 4. Extract data from the Right Panel using reliable attribute markers
                phone = "N/A"
                website = "N/A"
                address = "N/A"
                    
                    # Scrape Address (Looks for a button containing data-item-id="address")
                try:
                    address_element = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "address")]')
                    address = address_element.get_attribute("aria-label").replace("Address: ", "").strip()
                except:
                    pass

                    # Scrape Phone Number (Looks for a button containing data-item-id="phone:tel:")
                try:
                    phone_element = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "phone:tel:")]')
                    phone = phone_element.get_attribute("aria-label").replace("Phone: ", "").strip()
                except:
                    pass
                    
                    # Scrape Website (Looks for an anchor tag containing data-item-id="authority")
                try:
                    web_element = driver.find_element(By.XPATH, '//a[contains(@data-item-id, "authority")]')
                    website = web_element.get_attribute("href").strip()
                except:
                    pass
                    
                print(f"-> Got Address: {address}")
                print(f"-> Got Phone: {phone}")
                print(f"-> Got Website: {website}")
                    
                results.append({
                    "Name": business_name,
                    "Address": address,
                    "Phone": phone,
                    "Website": website
                })
                    
            except Exception as card_error:
                print(f"Error reading listing details: {card_error}")
                continue
            
            # 5. Save the compiled records
        if results:
            with open("google_maps_detailed_leads.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            print("\n🎉 Scraping complete! Data saved to 'google_maps_detailed_leads.csv'")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    # Keeping max_results small (5) for rapid testing; increase as needed
    scrape_maps_with_details("Consulting firms in New York", max_results=20)