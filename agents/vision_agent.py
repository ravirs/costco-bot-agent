import os
import base64
import requests
from google.genai import Client
from google.genai import types
from models.schemas import ExtractedReceipt
from pydantic import ValidationError

# Initialize the Gemini GenAI client
# It will automatically pick up GEMINI_API_KEY from the environment
try:
    client = Client()
except Exception as e:
    print(f"Failed to initialize Gemini Client: {e}")
    client = None

def download_image_as_base64(url: str) -> str:
    """
    Downloads an image from a URL and converts it to a base64 string.
    """
    try:
                account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        if account_sid and auth_token:
            from requests.auth import HTTPBasicAuth
            response = requests.get(url, auth=HTTPBasicAuth(account_sid, auth_token), timeout=15)
        else:
            response = requests.get(url, timeout=15)
        response.raise_for_status()
        return base64.b64encode(response.content).decode("utf-8")
    except Exception as e:
        print(f"Error downloading image: {e}")
        raise e

def process_receipt_image(image_url: str) -> ExtractedReceipt:
    """
    Uses Gemini Vision 1.5 Pro to extract receipt details.
    """
    if not client:
        raise RuntimeError("Gemini Client is not configured.")

    print(f"Downloading receipt image from {image_url}...")
    base64_image = download_image_as_base64(image_url)
    
    # Construct the image part for the Gemini API
    image_part = types.Part.from_bytes(
        data=base64.b64decode(base64_image),
        mime_type="image/jpeg" # Assuming JPEG, Twilio usually sends standard formats
    )

    prompt = """
    You are an expert receipt extraction AI. Analyze this Costco receipt.
    Extract the following information:
    1. The 'receipt_number' or transaction ID.
    2. The 'date_of_purchase' in YYYY-MM-DD format.
    3. A list of 'items' purchased. For each item, provide:
       - 'item_number': The 6-7 digit Costco item number.
       - 'name': The name of the item.
       - 'purchase_price': The price paid (as a float, no dollar signs). Do not include taxes in the item price.
    
    Ensure the output strictly follows the required JSON schema.
    """

    print("Sending to Gemini for extraction...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[prompt, image_part],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractedReceipt,
                temperature=0.1
            ),
        )
        
        # Parse the JSON response into our Pydantic model
        if response.text:
           # The new gemini sdk handles the schema validation, but we can double check with pydantic
           return ExtractedReceipt.model_validate_json(response.text)
        else:
            raise ValueError("Empty response from Gemini")

    except ValidationError as e:
        print(f"Pydantic Validation Error: {e}")
        raise
    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise
