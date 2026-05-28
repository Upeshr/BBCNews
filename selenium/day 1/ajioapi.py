from playwright.sync_api import sync_playwright
import json

def run_scraper():
    with sync_playwright() as p:
        # headless=False lets you see if a popup or bot-check is blocking the page
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context()
        page = context.new_page()

        print("Visiting AJIO... Please wait for the page to fully load.")

        # This will hold the data if we find it
        product_data = None

        # Enhanced Interceptor
        def handle_response(response):
            nonlocal product_data
            # Look for any response that contains the word 'products' in the JSON
            if "format=json" in response.url or "/api/category" in response.url:
                try:
                    # Check if it's a valid JSON response
                    data = response.json()
                    if "products" in data:
                        print(f"✅ FOUND IT! Captured data from: {response.url[:60]}...")
                        product_data = data
                except:
                    pass

        page.on("response", handle_response)

        # Go to the category page
        try:
            page.goto("https://www.ajio.com/api/category/83?currentPage=1&pageSize=45&format=json&query=%3Arelevance%3Arelevance%3Aundefined&curated=true&curatedid=cookwareandcutlery-212259&facets=relevance%3Aundefined&gridColumns=3&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true&store=ajio&segmentIds=&enableRushDelivery=true&vertexEnabled=false&visitorId=772664056.1778344492&userEncryptedId=6c90986838f071e20c8e6e049a129d5644e70c75af78c71a9cecc5f89dd0cca9&previousSource=Saas&plaAdsProvider=OSMOS&plaAdsEliminationDisabled=false&plpBannerAdsEnabled=false&state=&city=&zone=&userRestriction=&userState=NON_LOGGED_IN", wait_until="domcontentloaded", timeout=60000)
            
            # Human-like behavior: Scroll down to trigger data loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
            page.wait_for_timeout(5000) # Wait 5 seconds for the API to finish
            
            if product_data:
                # Save the found data
                with open('ajio_products.json', 'w', encoding='utf-8') as f:
                    json.dump(product_data, f, indent=4)
                print(f"Successfully saved {len(product_data['products'])} products to ajio_products.json")
            else:
                print("❌ Still couldn't find the API call. Try scrolling manually in the window that opened.")
                # Give you 30 seconds to manually browse/scroll if it failed
                page.wait_for_timeout(30000)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_scraper()