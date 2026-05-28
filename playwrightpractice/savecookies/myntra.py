from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        "./ultimate_chrome_profile",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--user-agent=Mozilla/5.0 (Window NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        ]
    )

    page = context.new_page()

    # Create stealth object and apply it
    stealth = Stealth()
    stealth.apply_stealth_sync(page)

    page.goto("https://www.google.com/")
    page.wait_for_timeout(10000)
    input("press Enter to exit")

    context.close()