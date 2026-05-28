from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 1. Use a completely custom folder name that doesn't say "playwright"
    # This will be created in the same folder as your script.
    user_data_dir = "./my_normal_browser_profile"
    
    # 2. Launch your computer's actual, official Google Chrome application
    context = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        # Point directly to your local Windows Google Chrome execution path
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", 
        args=[
            "--disable-blink-features=AutomationControlled", # Hides automation flags
            "--start-maximized"
        ]
    )

    page = context.pages[0]

    # 3. Go to Google Login
    page.goto("https://https://2.rome.api.flipkart.com/api/4/product/swatch")
    
    # STEP FOR YOU: 
    # Log in manually ONE LAST TIME here. Handle the PIN/Password.
    # Because this uses the real Chrome binary and a clean folder path,
    # Google will permanently trust this device session.
    
    input("Log in completely, then press Enter here to save and exit...")
    context.close()