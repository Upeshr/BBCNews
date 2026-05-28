from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://www.myntra.com")
    page.wait_for_timeout(2000)

    #the range loop for scrolling
    for i in range(3):
        page.mouse.wheel(0, 500)
        print(f"Scrolled {i+1} times...")
        page.wait_for_timeout(2000)

    browser.close()