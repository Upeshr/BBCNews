from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Lunch the engine
    browser = p.chromium.launch(headless=False)
    # Create the clean incognito room
    context = browser.new_context() 
    # Open a tab in room
    page = context.new_page()
    page.goto("https://www.google.com")

    browser.close()

