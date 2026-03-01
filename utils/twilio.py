import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

# Initialize client if vars are loaded (which might not be the case in early setup without .env)
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    client = None

def send_whatsapp_message(to_number: str, message: str):
    """
    Sends a WhatsApp message via Twilio.
    """
    if not client:
        print(f"Twilio not configured. Would have sent: {message} to {to_number}")
        return None
        
    try:
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=to_number
        )
        return msg.sid
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return None
