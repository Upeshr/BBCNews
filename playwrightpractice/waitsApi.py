from playwright.sync_api import sync_playwright

def lesson_two():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def catch_package(response):
            if "api/category" in response.url:
                print(f"\n[Security Guard]: I caught a package from {response.url[:50]}....")

                try:
                    data = response.json()
                    products = data.get('products', [])
                    print(f"[System]: Successfully extracted {len(products)} products!")
                except Exception as e:
                    print(f"[System]; package was empty or no JSON: {e}")

        page.on("response", catch_package)
        print(f"Navigate to Myntra.....")
        page.goto("https://www.ajio.com/api/category/83?currentPage=1&pageSize=45&format=json&query=%3Arelevance%3Arelevance%3Aundefined&curated=true&curatedid=cookwareandcutlery-212259&facets=relevance%3Aundefined&gridColumns=3&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true&store=ajio&segmentIds=&enableRushDelivery=true&vertexEnabled=false&visitorId=772664056.1778344492&userEncryptedId=6c90986838f071e20c8e6e049a129d5644e70c75af78c71a9cecc5f89dd0cca9&previousSource=Saas&plaAdsProvider=OSMOS&plaAdsEliminationDisabled=false&plpBannerAdsEnabled=false&state=&city=&zone=&userRestriction=&userState=NON_LOGGED_IN")

        page.wait_for_load_state("networkidle")
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(3000)

        browser.close()


lesson_two()