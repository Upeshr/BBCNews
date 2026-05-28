from playwright.sync_api import sync_playwright
import time

def lesson_two():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    extra_http_headers={
        "Referer": "https://www.myntra.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }
)
        page = context.new_page()

        def catch_package(response):
    # Use a broader filter to ensure we don't miss the 'v4/search' path
            if "v4/search" in response.url:
                try:
            # Check if the response is actually JSON before trying to parse
                    if "application/json" in response.header_value("content-type"):
                        data = response.json()
                        products = data.get('product', [])
                        if products:
                            print(f"\n[TARGET HIT]: Found Page {data.get('pageNumber', 'Unknown')}")
                            print(f"Items Caught: {len(products)}")
                            print(f"First Item: {products[0].get('productName')}")
                except Exception:
                    pass


                try:
                    data = response.json()
                    products = data.get("plaProduct", [])
                    if products:
                        print(f"[System]: Found {len(products)} products in this batch")
                        print(f"Latest Item {products[0].get('productsName')}")
                    else:
                        print("[System]: produsts was JSON but no 'product' found inside.")
                except Exception as e:
                    pass

        page.on("response", catch_package)
        print("Navigate to Myntra...")
        page.goto("https://www.myntra.com/gateway/v4/search/ethnic-tops?rows=50&o=49&plaEnabled=true&xdEnabled=false&isFacet=true&p=2", wait_until="commit")

        # Wait for the first item to actually appear on the screen
        page.wait_for_selector(".product-base", timeout=10000)
        for i in range(10):  # Scroll 10 times
            page.mouse.wheel(0, 600)  # Move down a bit
            print(f"Scroll {i+1}/10 completed")
            page.wait_for_timeout(1000)
        
        page.wait_for_timeout(5000)

        browser.close()

lesson_two()