import sys
import os
import json
import logging
from dotenv import load_dotenv
load_dotenv()
import base64
from unittest.mock import patch
from agents.vision_agent import process_receipt_image

IMAGE_PATH = "/Users/ravindrasawant/.gemini/antigravity/brain/21dac914-12bc-49e2-b2e7-e0dc04710dc1/media__1772507376938.jpg"

def mock_download_image_as_base64(url):
    with open(IMAGE_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

@patch("agents.vision_agent.download_image_as_base64", mock_download_image_as_base64)
def run():
    receipt_data = process_receipt_image("dummy_url")
    print(receipt_data.model_dump_json(indent=2))

if __name__ == "__main__":
    run()
