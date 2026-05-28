from playwright.sync_api import sync_playwright

def catch_package(response):
    # 1. Target the exact API endpoint you discovered
    if "ui/api/page-info" in response.url:
        try:
            # 2. Check if the response contains JSON data
            if "application/json" in response.header_value("content-type"):
                data = response.json()
                
                # 3. Follow the data trail: item -> searchResults -> nodes
                item_box = data.get('item', {})
                search_results = item_box.get('searchResults', {})
                product_nodes = search_results.get('nodes', [])
                
                # 4. Extract data if the list isn't empty
                if product_nodes:
                    print(f"\n[💥 TARGET HIT]: Caught {len(product_nodes)} devices from Smartprix!")
                    print("-" * 50)
                    
                    for product in product_nodes:
                        name = product.get('name')
                        price = product.get('fePrice')  # e.g., ₹23,499
                        rating = product.get('rating')   # Specs score
                        
                        print(f"📱 {name}")
                        print(f"   Price: {price} | Score: {rating}/100")
                        print("-" * 30)
                else:
                    # Debugging: If the API fires but doesn't have 'nodes'
                    print("\n[Notice]: Caught page-info URL, but 'nodes' list was empty.")
                    
        except Exception as e:
            # Safely skip files that aren't valid JSON
            pass

def run_practice():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Connect our updated security guard
        page.on("response", catch_package)

        print("Navigating to Smartprix Mobiles...")
        # Open the mobiles category page
        page.goto("https://www.smartprix.com/mobiles", wait_until="commit")
        page.wait_for_timeout(5000)  # Wait 5 seconds for page load

        print("Scrolling down to trigger the 'page-info' API...")
        # 1. Scroll down to bring the element into view
        print("Scrolling down to locate the Load More area...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight - 1000)")
        page.wait_for_timeout(2000)

        # 2. Target the specific class name: sm-load-more
        try:
            # CSS Selector target for class="sm-load-more"
            load_more_element = page.locator("div.sm-load-more")
            
            if load_more_element.is_visible():
                print("Target acquired! Clicking the 'sm-load-more' div...")
                
                # Force click in case the website tries to protect the div layout
                load_more_element.click(force=True)
                
                # Wait for the page-info API package to clear the network network
                page.wait_for_timeout(5000)
            else:
                print("The 'sm-load-more' div exists but isn't visible on screen yet.")
                
        except Exception as e:
            print(f"Could not click the element. Error: {e}")

        print("\nTesting complete. Closing browser in 10 seconds...")
        page.wait_for_timeout(5000)
        browser.close()

# Run the practice script
run_practice()