from playwright.sync_api import sync_playwright
import time
import re

def check_item_price(item_number: str) -> float:
    """
    Uses Playwright to scrape Costco.com for the current item price.
    """
    print(f"Scraping price for Costco Item #{item_number}")
    
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
        
        # Add headers to look more like a real browser
        context.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1"
        })
        
        page = context.new_page()
        
        try:
            search_url = f"https://www.costco.com/CatalogSearch?dept=All&keyword={item_number}"
            page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
            
            # Wait a moment to ensure client-side rendering finishes
            page.wait_for_timeout(3000)
            
            price_element = page.query_selector(".price, .value, [automation-id='productPrice']")
            
            if price_element:
                price_text = price_element.inner_text()
                match = re.search(r'\$?(\d+\.\d{2})', price_text)
                if match:
                    price = float(match.group(1))
                    print(f"Found price for {item_number}: ${price}")
                    return price
            
            print(f"Could not find price element for {item_number}")
            return None
            
        except Exception as e:
            print(f"Error scraping {item_number}: {e}")
            return None
        finally:
            browser.close()
