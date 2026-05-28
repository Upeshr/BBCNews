from playwright.sync_api import sync_playwright
import json

def lesson_two():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36")
        page = context.new_page()

        def catch_package(response):
            if "page-info" in response.url:
                print(f"Successfully Found data in {response.url[:50]} ")
                
                try:
                    data = response.json()
                    print(f"Data type: {type(data)}")
                    print(f"main keys available: {data.keys()}")

                    # Dig down safely. If any folder is missing, it returns an empty list [] instead of crashing.
                    product_list = data.get("item", {}).get("searchResults", {}).get("nodes", [])

                    # Now you can safely get the length
                    print(len(product_list))
                    if product_list:
                        print(f"\n[Success] intercept {len(product_list)} products")
    # Grab the very first product (Index 0)
                        first_product = product_list[0]
                    
                    # 4. Pull the specific data fields you want
                        name = first_product.get('name')   # Result: "Samsung Galaxy M56 5G"
                        price = first_product.get('price') # Result: "₹23,499"
                    
                        print(f"Product: {name} | Price: {price}")

                        # for product in product_list:
                        #     Name = product.get("name")
                        #     Price = product.get("price")
                        #     Rating = product.get("rating")

                        #     print(f"\n Name: {Name} \n Price: {Price} \n Rating: {Rating}/100")

                    else:
                        print("No products found in nodes!")

# Assuming your data is stored in a variable named 'data'
                    # # This will show you the actual product details
                except Exception as e:
                    print({e})
                    pass

        page.on("response", catch_package)
        print("Navigate to smartprix")
        page.goto("https://www.smartprix.com/mobiles", wait_until="commit")
        page.wait_for_load_state()

        for i in range(10):
            page.evaluate("window.scrollBy(0' 500)")
            print("scroll {i+1}/10 completed")
            page.wait_for_timeout(5000)
        print("practice complete")
        page.wait_for_timeout(5000)
        browser.close()
lesson_two()