from seleniumbase import SB
import random
import sys

def scrape_product(url: str) -> None:
    with SB(uc=True, test=True) as sb:
        try:
            print(f"Opening: {url}")
            sb.open(url)
            sb.sleep(random.uniform(3, 5))

            # Handle CAPTCHA manually if appears
            print("Waiting 20 seconds — solve CAPTCHA if needed...")
            sb.sleep(20)

            # Wait for title using XPath
            sb.wait_for_element_visible('xpath=//h1[@class="x-item-title__mainTitle"]', timeout=30)

            # Scrape with XPath selectors
            title = sb.get_text('xpath=/html/body/div[2]/div[3]/section[3]/section[3]/ul/li[1]/div/div/div[2]/div[1]/div[1]/span/a/h3').strip()

            try:
                price = sb.get_text('xpath=/html/body/div[2]/div[3]/section[3]/section[3]/ul/li[1]/div/div/div[2]/div[2]/div[1]/span').strip()
            except Exception:
                price = "N/A"

            print(f"\nPRODUCT: {title}\nPRICE:   {price}")

            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"{title} | {price}\n")

        except Exception as e:
            print(f"Error: {e}")
            sb.save_screenshot("error_screenshot.png")

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276"
    scrape_product(target_url)