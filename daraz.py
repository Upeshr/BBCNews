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
            title = sb.get_text('xpath=//html/body/section[1]/div/div/div/div/div/div/div[2]/div[2]/div[2]/a[4]/div[2]/p').strip()

            try:
                price = sb.get_text('xpath=//html/body/section[1]/div/div/div/div/div/div/div[2]/div[2]/div[2]/a[4]/div[2]/div[1]/span[2]').strip()
            except Exception:
                price = "N/A"

            print(f"\nPRODUCT: {title}\nPRICE:   {price}")

            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"{title} | {price}\n")

        except Exception as e:
            print(f"Error: {e}")
            sb.save_screenshot("error_screenshot.png")

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://https://www.daraz.com.np"
    scrape_product(target_url)