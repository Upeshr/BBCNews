"""
Smartprix Scraper — Final Version
==================================
- Intercepts /ui/api/page-info endpoint
- Parses exact response shape: item.searchResults.nodes[]
- Extracts features list into readable columns
- Human-like scrolling
- Clicks div.sm-load-more (max 5 times by default)
- Saves all products to CSV using pandas

Requirements:
    pip install playwright pandas
    playwright install chromium
"""

import asyncio
import random
import time

import pandas as pd
from playwright.async_api import async_playwright


# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
TARGET_URL      = "https://www.smartprix.com/mobiles"
OUTPUT_CSV      = "smartprix_products.csv"
HEADLESS        = False     # True = no browser window
SLOW_MO         = 40        # ms between browser actions
API_PATTERN     = "/ui/api/page-info"
MAX_LOAD_MORE   = 5         # maximum "Load More" clicks


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

async def human_scroll(page, steps: int = 6):
    """Scroll in random increments to mimic a real user."""
    for _ in range(steps):
        delta = random.randint(250, 650)
        await page.mouse.wheel(0, delta)
        await asyncio.sleep(random.uniform(0.3, 0.9))


async def pause(min_s=0.8, max_s=2.0):
    await asyncio.sleep(random.uniform(min_s, max_s))


def parse_nodes(nodes: list) -> list[dict]:
    """
    Convert raw nodes from item.searchResults.nodes into flat dicts.

    Raw node shape:
    {
        "type": "Product",
        "id": "pd1fqb2pvjf",
        "name": "Samsung Galaxy M56 5G",
        "priceDrop": -3.26,
        "rating": 90,
        "stock": "UNKNOWN",
        "category": { "id": 13, "canCompare": true },
        "brandId": 2,
        "price": 23499,
        "fePrice": "₹23,499",
        "imageId": "QuP9QFc8",
        "url": "/mobiles/samsung-galaxy-m56-ppd1fqb2pvjf",
        "specsScore": 58,
        "features": [
            { "text": "Dual Sim, 5G, VoLTE, Wi-Fi" },
            { "text": "Exynos 1480, Octa Core, 2.7 GHz Processor" },
            { "text": "8 GB RAM, 128 GB inbuilt" },
            { "text": "5000 mAh Battery with 45W Fast Charging" },
            { "text": "6.74 inches, 1080 x 2340 px, 120 Hz Display" },
            { "text": "50 MP + 8 MP + 2 MP Triple Rear & 12 MP Front" },
            { "text": "Android v15" },
            { "text": "No FM Radio", "style": "no" }
        ]
    }
    """
    rows = []

    # Feature index → human-readable column name
    FEATURE_LABELS = {
        0: "connectivity",
        1: "processor",
        2: "ram_storage",
        3: "battery",
        4: "display",
        5: "camera",
        6: "os",
        7: "extra_note",
    }

    for node in nodes:
        if not isinstance(node, dict):
            continue
        if node.get("type") != "Product":
            continue

        row = {
            "id"          : node.get("id", ""),
            "name"        : node.get("name", ""),
            "price"       : node.get("price", ""),
            "fePrice"     : node.get("fePrice", ""),
            "priceDrop"   : node.get("priceDrop", ""),
            "rating"      : node.get("rating", ""),
            "specsScore"  : node.get("specsScore", ""),
            "stock"       : node.get("stock", ""),
            "brandId"     : node.get("brandId", ""),
            "categoryId"  : node.get("category", {}).get("id", ""),
            "imageId"     : node.get("imageId", ""),
            "url"         : "https://www.smartprix.com" + node.get("url", ""),
        }

        # Flatten features list into named columns
        features = node.get("features") or []
        for i, feat in enumerate(features):
            if not isinstance(feat, dict):
                continue
            col   = FEATURE_LABELS.get(i, f"feature_{i}")
            text  = feat.get("text", "")
            style = feat.get("style", "")          # "no" means a negative feature
            row[col] = f"[NO] {text}" if style == "no" else text

        rows.append(row)

    return rows


# ──────────────────────────────────────────────
# MAIN SCRAPER
# ──────────────────────────────────────────────

async def scrape():
    all_products: list[dict] = []
    seen_ids: set             = set()
    api_call_count            = 0
    load_more_clicks          = 0
    has_next_page             = True     # tracks API's hasNextPage flag

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
            locale="en-IN",
        )
        page = await context.new_page()

        # ── Intercept /ui/api/page-info ───────────────────────────────────────
        async def on_response(response):
            nonlocal api_call_count, has_next_page

            if API_PATTERN not in response.url:
                return

            try:
                body = await response.json()
            except Exception:
                return

            api_call_count += 1

            # Navigate the exact path: item → searchResults
            search_results = (
                body
                .get("item", {})
                .get("searchResults", {})
            )
            has_next_page = search_results.get("pageInfo", {}).get("hasNextPage", False)
            nodes         = search_results.get("nodes", [])
            parsed        = parse_nodes(nodes)

            new_count = 0
            for p in parsed:
                uid = p.get("id", "")
                if uid and uid not in seen_ids:
                    seen_ids.add(uid)
                    all_products.append(p)
                    new_count += 1

            print(
                f"  📡 API #{api_call_count}  →  "
                f"+{new_count} new  |  total={len(all_products)}  |  "
                f"hasNextPage={has_next_page}"
            )

        page.on("response", on_response)

        # ── Navigate ──────────────────────────────────────────────────────────
        print(f"\n🌐 Opening {TARGET_URL} …")
        await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60_000)
        await pause(2.5, 4.0)

        # ── Scroll + Load More loop ───────────────────────────────────────────
        print(f"\n🔄 Starting scroll loop (max {MAX_LOAD_MORE} load-more clicks) …\n")
        round_num        = 0
        no_change_streak = 0
        MAX_NO_CHANGE    = 4

        while no_change_streak < MAX_NO_CHANGE:
            round_num += 1
            before = len(all_products)

            # 1. Human-like scroll
            await human_scroll(page, steps=random.randint(5, 9))
            await pause(0.8, 1.8)

            # 2. Check page bottom
            at_bottom = await page.evaluate(
                "(window.innerHeight + window.scrollY) >= document.body.scrollHeight - 300"
            )

            # 3. Click div.sm-load-more (if limit not reached and more pages exist)
            clicked = False
            if load_more_clicks < MAX_LOAD_MORE and has_next_page:
                load_more = page.locator("div.sm-load-more")
                try:
                    if await load_more.is_visible(timeout=2_000):
                        await load_more.scroll_into_view_if_needed()
                        await pause(0.5, 1.0)
                        await load_more.click()
                        load_more_clicks += 1
                        clicked = True
                        print(
                            f"  🖱️  Round {round_num}: Clicked 'Load More' "
                            f"({load_more_clicks}/{MAX_LOAD_MORE}) — waiting …"
                        )
                        await pause(2.0, 3.5)
                except Exception:
                    pass
            elif load_more_clicks >= MAX_LOAD_MORE:
                print(f"\n🛑 Reached max load-more limit ({MAX_LOAD_MORE} clicks) — stopping.")
                break
            elif not has_next_page:
                print(f"\n✅ API says hasNextPage=false — no more data.")
                break

            # 4. Tally
            after  = len(all_products)
            gained = after - before
            no_change_streak = 0 if gained > 0 else no_change_streak + 1

            print(
                f"  Round {round_num}: +{gained} products  |  "
                f"total={after}  |  bottom={at_bottom}  |  "
                f"clicks={load_more_clicks}/{MAX_LOAD_MORE}  |  "
                f"no_change={no_change_streak}/{MAX_NO_CHANGE}"
            )

            if at_bottom and not clicked and gained == 0:
                print("\n✅ Page bottom with no new products — done.")
                break

        # Final flush
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await pause(1.5, 2.5)
        await browser.close()

    # ── Save CSV ──────────────────────────────────────────────────────────────
    if not all_products:
        print("\n⚠️  No products captured. Check the API response in DevTools.")
        return

    df = pd.DataFrame(all_products)

    # Ordered columns
    priority = [
        "id", "name", "price", "fePrice", "priceDrop", "rating", "specsScore",
        "stock", "brandId", "categoryId",
        "connectivity", "processor", "ram_storage", "battery",
        "display", "camera", "os", "extra_note",
        "imageId", "url",
    ]
    front = [c for c in priority if c in df.columns]
    rest  = [c for c in df.columns if c not in front]
    df    = df[front + rest]

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"\n✅ Saved {len(df)} products  →  '{OUTPUT_CSV}'")
    print(f"   Columns: {list(df.columns)}\n")
    print(df[["name", "price", "rating", "ram_storage", "battery"]].head(10).to_string(index=False))


# ──────────────────────────────────────────────
if __name__ == "__main__":
    t0 = time.time()
    asyncio.run(scrape())
    print(f"\n⏱  Finished in {time.time() - t0:.1f}s")