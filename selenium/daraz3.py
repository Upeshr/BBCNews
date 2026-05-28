from seleniumbase import SB
import random
import sys

def scrape_products(url: str) -> None:
    with SB(uc=True, test=True) as sb:
        try:
            print(f"Opening: {url}")
            sb.open(url)

            print("Waiting for page to load...")
            sb.sleep(random.uniform(6, 9))

            # Save screenshot to see what loaded
            sb.save_screenshot("debug.png")

            # Wait using more reliable selector
            sb.wait_for_element_visible('xpath=//a[contains(@href,"/products/")]', timeout=60)

            # Get all product links
            products = sb.find_elements('xpath=//a[contains(@href,"/products/")]')
            prices   = sb.find_elements('xpath=//span[@class="ooOxS"]')

            # Filter only products with title attribute
            products = [p for p in products if p.get_attribute("title")]

            print(f"\nFound {len(products)} products\n" + "="*40)

            with open("results.txt", "a", encoding="utf-8") as f:
                for i, product in enumerate(products):
                    try:
                        title = product.get_attribute("title").strip()
                        link  = "https:" + product.get_attribute("href")
                        price = prices[i].text.strip() if i < len(prices) else "N/A"

                        print(f"PRODUCT: {title}")
                        print(f"PRICE:   {price}")
                        print(f"LINK:    {link}\n")

                        f.write(f"{title} | {price} | {link}\n")
                    except Exception:
                        continue

        except Exception as e:
            print(f"Error: {e}")
            sb.save_screenshot("error_screenshot.png")

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.daraz.com.np/catalog/?q=Water%20Bottles"
    scrape_products(target_url)