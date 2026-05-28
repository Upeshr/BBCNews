from playwright.sync_api import sync_playwright

def lesson_two_engagement():
    with sync_playwright() as p:
        # 1. Launch & setup headers to look real
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()

        # 2. Updated Listener for the 'gateway' URL
        def catch_package(response):
            if "gateway/v4/search" in response.url:
                try:
                    data = response.json()
                    products = data.get('products', [])
                    if products:
                        print(f"\n[TARGET HIT]: Found {len(products)} products on Page {data.get('pageNumber')}")
                except:
                    pass

        page.on("response", catch_package)

        # 3. Navigate and WAIT
        print("Navigating to Myntra...")
        page.goto("https://www.myntra.com/ethnic-tops", wait_until="load")
        page.wait_for_timeout(3000)

        # 4. SCROLL TO FIND THE 'NEXT' BUTTON
        print("Searching for the Next button...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        # 5. CLICK NEXT (Using a flexible selector for the pagination)
        # Myntra usually uses a 'pagination-next' class or a link containing '?p=2'
        try:
            next_button = page.locator('li.pagination-next > a')
            if next_button.is_visible():
                print("Clicking Next Page...")
                next_button.click()
                page.wait_for_timeout(3000)
            else:
                print("Next button not visible, trying direct navigation to P2...")
                page.goto("https://www.myntra.com/ethnic-tops?p=2")
        except:
            print("Could not find Next button, check the selector.")

        # 6. FINAL SCROLL (The trigger you found)
        print("Performing the final scroll to trigger the API...")
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 1000)")
            page.wait_for_timeout(2000)

        print("Done. Keeping browser open to check terminal...")
        page.wait_for_timeout(15000)
        browser.close()

lesson_two_engagement()