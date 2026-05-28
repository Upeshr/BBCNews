from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    def catch_response(response):
        if "news" in response.url:
            print("\nFound JSON")
            try:
                data = response.json()
                print(data)
            except:
                pass

    page.on("response", catch_response)
    page.goto("http://www.bbc.com/news")
    page.wait_for_timeout(5000)
    browser.close()