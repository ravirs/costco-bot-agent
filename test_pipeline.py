import sys
import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

import base64
from unittest.mock import patch
from agents.vision_agent import process_receipt_image
from agents.scraper_agent import check_item_price

logging.basicConfig(level=logging.INFO)

# The uploaded receipt image from context
IMAGE_PATH = "/Users/ravindrasawant/.gemini/antigravity/brain/21dac914-12bc-49e2-b2e7-e0dc04710dc1/media__1772507376938.jpg"

def mock_download_image_as_base64(url):
    print(f"Mocking the image download by reading {IMAGE_PATH}")
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found at {IMAGE_PATH}")
    with open(IMAGE_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

@patch("agents.vision_agent.download_image_as_base64", mock_download_image_as_base64)
def run_test():
    print("--- Starting Extraction Test ---")
    try:
        receipt_data = process_receipt_image("dummy_url")
        print("Extraction Successful!")
        print(receipt_data.model_dump_json(indent=2))
        
        print("\n--- Starting Scraper Test ---")
        for item in receipt_data.items:
            print(f"\nChecking online price for Item: {item.name} (Code: {item.item_number})")
            if item.item_number and str(item.item_number).strip():
                try:
                    online_price = check_item_price(str(item.item_number))
                    if online_price is not None:
                        print(f"  --> Online Price: ${online_price}")
                        print(f"  --> Receipt Price: ${item.purchase_price}")
                        if float(online_price) < float(item.purchase_price):
                            print("  => 💰 PRICE DROP DETECTED! Eligible for refund.")
                        else:
                            print("  => No price drop.")
                    else:
                        print("  --> Could not retrieve online price.")
                except Exception as ex:
                    print(f"  --> Error during scraping: {ex}")
            else:
                 print("  --> Invalid or missing item number.")

    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    run_test()
