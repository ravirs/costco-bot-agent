from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def daily_price_check_job():
    """
    Job that runs daily to check prices of all tracking items.
    """
    logger.info("Starting daily price check job...")
    
    from utils.db import supabase
    from agents.scraper_agent import check_item_price
    from agents.notification_agent import notify_price_drop
    from models.schemas import DBItem
    from datetime import datetime
    
    if not supabase:
        logger.error("Supabase not configured. Cannot run scheduled checks.")
        return

    try:
        # Fetch all items that are currently being tracked
        response = supabase.table("items").select("*, receipts(user_id)").eq("status", "tracking").execute()
        items = response.data
        
        logger.info(f"Found {len(items)} items to check.")
        
        for item_data in items:
            item_number = item_data['item_number']
            purchase_price = item_data['purchase_price']
            user_id = item_data['receipts']['user_id']
            
            # Use scraper to get current price
            current_price = check_item_price(item_number)
            
            if current_price is not None:
                logger.info(f"Item #{item_number} - Purchase: ${purchase_price}, Current: ${current_price}")
                
                # Check for price drop
                if current_price < purchase_price:
                    # Send WhatsApp notification
                    db_item = DBItem(**item_data)
                    db_item.current_price = current_price
                    notify_price_drop(user_id, db_item)
                    
                    # Update status to notified so we don't spam them
                    supabase.table("items").update({
                        "current_price": current_price,
                        "status": "notified",
                        "last_checked": datetime.now().isoformat()
                    }).eq("item_number", item_number).eq("receipt_id", item_data['receipt_id']).execute()
                else:
                    # Update latest price without changing status
                    supabase.table("items").update({
                        "current_price": current_price,
                        "last_checked": datetime.now().isoformat()
                    }).eq("item_number", item_number).eq("receipt_id", item_data['receipt_id']).execute()
                    
    except Exception as e:
        logger.error(f"Error during daily price check: {e}")
        
    logger.info("Finished daily price check job.")

def start_scheduler():
    """
    Initializes and starts the background scheduler.
    """
    scheduler = BackgroundScheduler()
    
    # Run the daily price check every day at 10:00 AM PST (adjust as needed)
    scheduler.add_job(
        daily_price_check_job,
        trigger=CronTrigger(hour=10, minute=0),
        id='daily_price_check',
        name='Check Costco prices for all tracked items',
        replace_existing=True
    )
    
    # For testing purposes, uncomment the following line to run every 5 minutes
    # scheduler.add_job(daily_price_check_job, 'interval', minutes=5, id='test_price_check')
    
    scheduler.start()
    logger.info("Scheduler started successfully.")
    return scheduler
