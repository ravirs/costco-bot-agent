from utils.twilio import send_whatsapp_message
from models.schemas import DBItem

def notify_price_drop(user_whatsapp: str, item: DBItem):
    """
    Generates and sends a price drop alert message to the user.
    """
    savings = item.purchase_price - item.current_price
    
    # Check if we should advise online form or in-store visit
    # For now, generic message
    message = f"🚨 *Costco Price Drop Alert!* 🚨\n\n" \
              f"The item *{item.name}* (Item #{item.item_number}) you bought for ${item.purchase_price:.2f} " \
              f"is now on sale for *${item.current_price:.2f}*!\n\n" \
              f"You could save *${savings:.2f}* if you request a price adjustment within 30 days of purchase.\n\n" \
              f"Reply 'INFO' for details on how to claim this adjustment."
              
    send_whatsapp_message(user_whatsapp, message)
