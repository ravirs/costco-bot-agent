import sys
from agents.scraper_agent import check_item_price

def test_scraper():
    # Test with a known Costco item number (e.g., KS Paper Towels or Water)
    # Using 1756241 - AirPods Pro (usually available online)
    # Using 1150000 - KS Paper Towels
    test_items = ["1756241", "1150000"]
    
    for item in test_items:
        price = check_item_price(item)
        if price:
            print(f"✅ Success! Price for {item} is ${price}")
        else:
            print(f"❌ Failed to find price for {item}")
            
if __name__ == "__main__":
    test_scraper()
