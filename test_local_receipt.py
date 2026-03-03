import os
import base64
from unittest.mock import patch
import asyncio
import sys

# Change perfectly match path handling since it has spaces
IMAGE_PATH = "/Users/ravindrasawant/Documents/antigravity/costcopricecheck/data/WhatsApp Image 2026-03-02 at 14.50.40.jpeg"

def mock_download_image_as_base64(url):
    print(f"[Mock] Reading local image instead of downloading: {IMAGE_PATH}")
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found at {IMAGE_PATH}")
    with open(IMAGE_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def mock_send_whatsapp_message(to_number: str, message: str):
    print(f"\n[Mock WhatsApp to {to_number}]:\n{message}\n")

@patch("agents.vision_agent.download_image_as_base64", mock_download_image_as_base64)
@patch("main.send_whatsapp_message", mock_send_whatsapp_message)
def run_end_to_end():
    from main import process_whatsapp_message
    
    print("--- Starting End-to-End Test ---")
    try:
        # Simulate Twilio hitting our endpoint with this user and the mock media url
        process_whatsapp_message(
            sender="whatsapp:+15559990000",
            message="",
            media_url="mock_url_does_not_matter"
        )
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    print("--- End of Test ---")

if __name__ == "__main__":
    run_end_to_end()
