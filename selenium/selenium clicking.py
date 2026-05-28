from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.get("https://easyautomationpractice.com")
driver.maximize_window()
time.sleep(1)

start = driver.find_element(By.XPATH, '//button[contains(., "Start Free Automation Journey")]')
start.click()

driver.execute_script("window.scrollBy(0, 700);")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Click Me!']").click()
time.sleep(1)

element = driver.find_element(By.XPATH, "//button[text()='Double Click Me!']")
actions = ActionChains(driver)
actions.double_click(element).perform()
driver.execute_script("window.scrollBy(0, 500);")


hover_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > main:nth-child(3) > div:nth-child(1) > div:nth-child(4) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > svg:nth-child(1) > path:nth-child(1)")))
actions.move_to_element(hover_element).perform()
print("Hover action performed successfully!")
time.sleep(1)


right_click_area = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".lucide.lucide-mouse-pointer.h-8.w-8.text-muted-foreground")))
actions.context_click(right_click_area).perform()
print("Right-click performed!")
time.sleep(1)
driver.execute_script("window.scrollBy(0, 700);")
time.sleep(1)


source_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > main:nth-child(3) > div:nth-child(1) > div:nth-child(4) > div:nth-child(5) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > svg:nth-child(1) > path:nth-child(4)")))
target_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='text-xs text-muted-foreground']")))
actions.click_and_hold(source_element).move_to_element(target_element).release().perform()
print("Drag and drop completed!")
time.sleep(1)

input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Click here and press spacebar']")))
actions.move_to_element(input_field).click().send_keys(Keys.SPACE).perform()
print("Spacebar pessed successfully!")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "input[placeholder='Focus me!']").click
time.sleep(1)
driver.execute_script("window.scrollBy(0, 600)")

input_to_focus = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Focus me!']")))
input_to_focus.click()
time.sleep(1)

paragraph = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".text-foreground.leading-relaxed.cursor-text.select-text")))
actions.move_to_element_with_offset(paragraph, 5, 5).click_and_hold().move_by_offset(200, 0).release().perform()
print("Text selection performed!")
time.sleep(1)
driver.execute_script("window.scrollBy(0, 500)")

long_press_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".lucide.lucide-timer.h-8.w-8.text-muted-foreground")))
actions.click_and_hold(long_press_element).pause(1).release().perform()
print("lomg press of 1 second performed!")
time.sleep(1)

triple_click_me = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium ring-offset-background transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 hover:scale-105 active:scale-95 border bg-background h-11 rounded-md px-8 border-accent text-accent hover:bg-accent hover:text-accent-foreground']")))
actions.click(triple_click_me).click(triple_click_me).click(triple_click_me).perform()

for i in range(3):
    actions.click(triple_click_me)
actions.perform()
time.sleep(1)
driver.execute_script("window.scrollBy(0, 300)")
time.sleep(1)

container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='h-32 overflow-y-auto bg-secondary border border-border rounded-lg p-4']")))
driver.execute_script("arguments[0].scrollTop += 150", container)
print("Internal scroll completed!")
time.sleep(1)

shape_lacator = [(By.CSS_SELECTOR, ".lucide.lucide-square.h-8.w-8"),
                 (By.CSS_SELECTOR, ".lucide.lucide-circle.h-8.w-8"),
                 (By.CSS_SELECTOR, ".lucide.lucide-star.h-8.w-8")]

for locator in shape_lacator:
    shape = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
    shape.click()
    print(f"Clicked: {locator[1]}")
print("Sequence completed!")
time.sleep(1)

rapid_clicking =WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Rapid Click!']")))
for i in range(5):
    actions.click(rapid_clicking)
actions.perform()
print("Rapid Clicking Perform!")
time.sleep(1)

pricese_clicking = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".lucide.lucide-target.h-6.w-6.text-primary.absolute")))
actions.click(pricese_clicking).perform()
print("Pricese clicked!")
driver.execute_script("window.scrollBy(0, 100)")



input("PRESS any key to quit")
driver.quit()
