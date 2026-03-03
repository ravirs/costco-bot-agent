from playwright.sync_api import sync_playwright

def run():
    print("Scraping price for Costco Item #1849333")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-http2"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        
        context.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1"
        })
        
        page = context.new_page()
        search_url = f"https://www.costco.com/CatalogSearch?dept=All&keyword=1849333"
        page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(3000)
        
        html = page.content()
        with open("costco_debug.html", "w") as f:
            f.write(html)
        print("Saved HTML to costco_debug.html")
        browser.close()

if __name__ == "__main__":
    run()
