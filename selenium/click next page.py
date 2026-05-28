from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://quotes.toscrape.com")
time.sleep(2)
print("Title:", driver.title)

all_quotes = []

while True:

    quotes = driver.find_elements(By.CLASS_NAME, "quote")
    

    for quote in quotes:
        try:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            all_quotes.append(f"{text} - {author}")
        except Exception as e:
            continue

    print(f"Page scraped! Total quotes so far: {len(all_quotes)}")

    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
        next_button.click()
        time.sleep(2)
    except:
        print("last page reached!")
        break

print(f"Total quotes scraped: {len(all_quotes)}")

for quote in all_quotes:
    print(quote)
    print("----")
    
driver.quit
print("Done")