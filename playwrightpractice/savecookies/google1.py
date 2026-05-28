from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Open your persistent profile with core anti-bot flags
    context = p.chromium.launch_persistent_context(
    "./ultimate_chrome_profile",
    headless=False,
    # Point directly to your computer's actual Chrome app binary
    executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", 
    args=[
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
        "--lang=en"
    ]
)

    page = context.pages[0]

    # NATIVE UPGRADED STEALTH: Deeply patches prototypes to pass strict scanner tests
    page.add_init_script("""
        // 1. ADVANCED WEBDRIVER BYPASS: Completely purge the webdriver descriptor
        // This ensures both navigator.webdriver and its underlying prototype look exactly like normal Chrome
        const newProto = navigator.__proto__;
        delete newProto.webdriver;
        navigator.__proto__ = newProto;

        // 2. VALID PLUGINARRAY BYPASS: Fake genuine PluginArray types instead of a cheap standard array [1,2,3]
        const mockPlugins = [
            { name: 'PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format' },
            { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: 'Google Chrome PDF' },
            { name: 'Chromium PDF Viewer', filename: 'internal-pdf-viewer', description: 'Chromium Document Viewer' }
        ];

        // Give the array a true PluginArray prototype lookalike structure
        Object.setPrototypeOf(mockPlugins, PluginArray.prototype);
        for (let i = 0; i < mockPlugins.length; i++) {
            Object.setPrototypeOf(mockPlugins[i], Plugin.prototype);
            mockPlugins[mockPlugins[i].name] = mockPlugins[i];
        }

        Object.defineProperty(navigator, 'plugins', {
            get: () => mockPlugins,
            configurable: true
        });

        // 3. Fake chrome runtime properties that headless/automated environments leak
        window.chrome = {
            runtime: {},
            loadTimes: function() {},
            csi: function() {},
            app: {}
        };
        
        // 4. Ensure permissions status matches a genuine desktop environment
        const originalQuery = navigator.permissions.query;
        navigator.permissions.query = (parameters) =>
            parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters);
    """)

    # Run the test again
    page.goto("https://www.google.com/")
    
    input("Holes patched! Press Enter to exit...")
    context.close()