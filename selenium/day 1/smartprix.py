import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    return uc.Chrome(options=options)

def pause(a=2, b=5):
    time.sleep(random.uniform(a, b))

def incremental_scroll(driver:uc.Chrome, scroll_pause=3):
    last_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    no_change_count = 0

    while True:
        # gradual scrolling
        for _ in range(8):
            driver.execute_script(
                "window.scrollBy(0, 300);"
            )
            pause(0.5, 1.5)

        # wait for new content to load
        time.sleep(scroll_pause)

        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        print("Old:", last_height)
        print("New:", new_height)

        if new_height == last_height:
            no_change_count += 1
            print(f"No change: {no_change_count}")

            # stop only after 3 failed checks
            if no_change_count >= 3:
                print("Reached end of page.")
                break
        else:
            no_change_count = 0

        last_height = new_height

driver = None
try:
    driver = setup_driver()
    driver.get("https://www.smartprix.com/mobiles")
    pause(5, 7)
    incremental_scroll(driver)

    # data = driver.page_source
    # print(data)
    # with open("smartprix.html", "w", encoding= "utf-8") as file:
    #     file.write(data)
    #     pause()

except Exception as e:
    print("Error:", e)

finally:
    if driver:
        try:
            driver.quit()
        except Exception:
            pass