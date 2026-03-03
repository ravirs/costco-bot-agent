import os
from fastapi import FastAPI, Request, BackgroundTasks, Form
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

load_dotenv()

from utils.twilio import send_whatsapp_message
from utils.db import supabase
from utils.scheduler import start_scheduler
from agents.vision_agent import process_receipt_image

app = FastAPI(title="Costco Price Check Agent")

@app.on_event("startup")
async def startup_event():
    # Start the background scheduler for daily price checks
    start_scheduler()

@app.get("/")
async def root():
    return {"message": "Costco Price Check Agent is running"}

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Twilio WhatsApp Webhook endpoint.
    """
    form_data = await request.form()
    incoming_msg = form_data.get('Body', '').strip()
    sender = form_data.get('From', '')
    media_url = form_data.get('MediaUrl0', None)
    
    background_tasks.add_task(process_whatsapp_message, sender, incoming_msg, media_url)
    
    # Respond to Twilio immediately with an empty TwiML response
    return PlainTextResponse(content='<Response></Response>', media_type="application/xml")

import traceback

def process_whatsapp_message(sender: str, message: str, media_url: str = None):
    """
    Background task to process the incoming message.
    """
    # 1. Ensure user exists in DB
    user_id = sender.replace("whatsapp:", "")
    if supabase:
        # Simplified user creation check
        try:
            supabase.table("users").upsert({"whatsapp_number": user_id}).execute()
        except Exception as e:
            print(f"Error upserting user: {e}")

    # 2. Handle Media (Receipt Image)
    if media_url:
        send_whatsapp_message(sender, "📸 I received your receipt! Analyzing the image to extract items and prices... This might take a minute.")
        try:
            # Run the LangGraph pipeline
            from agents.graph import receipt_graph
            
            initial_state = {
                "whatsapp_number": user_id,
                "media_url": media_url,
                "receipt_data": None,
                "items_to_track": [],
                "messages": []
            }
            
            # Invoke the graph synchronously (runs in background thread anyway)
            final_state = receipt_graph.invoke(initial_state)
            
            receipt = final_state.get("receipt_data")
            if receipt:
                send_whatsapp_message(sender, f"✅ Analyzed! Found {len(receipt.items)} items on receipt #{receipt.receipt_number}. I will check their prices daily for 30 days and alert you of any drops.")
            else:
                send_whatsapp_message(sender, "❌ Sorry, I had trouble reading that receipt. Please ensure the image is clear and try again.")
                
        except Exception as e:
            print(f"Error processing receipt pipeline: {e}")
            traceback.print_exc()
            send_whatsapp_message(sender, "❌ Sorry, I encountered an internal error processing your receipt.")
        return

    # 3. Handle Text Commands
    message_lower = message.lower()
    
    if message_lower in ["hi", "hello", "start"]:
        welcome_msg = "👋 Welcome to the Costco Price Check Agent!\n\n" \
                      "Simply send a clear photo of your Costco receipt. I will securely extract the items, track their prices daily, and notify you if a price drops within your 30-day window."
        send_whatsapp_message(sender, welcome_msg)
        
    elif message_lower == "status":
        # TODO: Query DB for user's tracked items
        send_whatsapp_message(sender, "📊 You are currently tracking X items from Y receipts. No price drops detected yet.")
        
    elif message_lower == "info":
        info_msg = "ℹ️ *How to request a Price Adjustment:*\n\n" \
                   "1. *Online Purchases*: Go to Costco.com > Customer Service > Request a Price Adjustment and fill out the form.\n" \
                   "2. *In-Store Purchases*: You must visit the Returns desk at a Costco warehouse to receive your refund."
        send_whatsapp_message(sender, info_msg)
        
    else:
        send_whatsapp_message(sender, "🤖 I am a specialized agent. Please send a photo of a Costco receipt to start tracking prices, or type 'status' to see your tracked items.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
