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

quotes = driver.find_elements(By.CLASS_NAME, "quote")
print(f"Found {len(quotes)} quotes\n")
time.sleep(5)


for quote in quotes:
    try:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        print(f"Quote: {text}")
        print(f"Author: {author}\n")
        print("---")
    except Exception as e:
        continue

driver.quit
print("Done")