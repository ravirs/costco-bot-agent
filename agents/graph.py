import os
from typing import Dict, List, Any, TypedDict
from langgraph.graph import StateGraph, END
from agents.vision_agent import process_receipt_image
from agents.scraper_agent import check_item_price
from utils.db import supabase
from models.schemas import DBItem, ExtractedReceipt

class AgentState(TypedDict):
    whatsapp_number: str
    media_url: str
    receipt_data: ExtractedReceipt
    items_to_track: List[DBItem]
    messages: List[str]

def extract_receipt(state: AgentState) -> AgentState:
    """Node 1: Extract receipt items from the image URL."""
    print("Extracting receipt...")
    receipt = process_receipt_image(state["media_url"])
    return {"receipt_data": receipt, "messages": [f"Extracted {len(receipt.items)} items."]}

def initial_price_check(state: AgentState) -> AgentState:
    """Node 2: Do an initial price check for the extracted items."""
    print("Performing initial price check...")
    receipt = state["receipt_data"]
    db_items = []
    
    for item in receipt.items:
        current_price = check_item_price(item.item_number)
        
        # Create a DBItem
        db_item = DBItem(
            receipt_id=receipt.receipt_number,
            item_number=item.item_number,
            name=item.name,
            purchase_price=item.purchase_price,
            current_price=current_price
        )
        db_items.append(db_item)
        
    return {"items_to_track": db_items, "messages": ["Completed initial price check."]}

def save_to_database(state: AgentState) -> AgentState:
    """Node 3: Save receipt and items to Supabase."""
    print("Saving to database...")
    if not supabase:
        print("Supabase not configured, skipping DB save.")
        return {"messages": ["Skipping DB save."]}
        
    receipt = state["receipt_data"]
    items = state["items_to_track"]
    
    try:
        # Save Receipt
        supabase.table("receipts").insert({
            "receipt_number": receipt.receipt_number,
            "user_id": state["whatsapp_number"],
            "image_url": state["media_url"],
            "date_of_purchase": receipt.date_of_purchase
        }).execute()
        
        # Save Items
        items_data = [item.model_dump(exclude={'last_checked'}) for item in items]
        if items_data:
             supabase.table("items").insert(items_data).execute()
             
    except Exception as e:
        print(f"Error saving to DB: {e}")
        
    return {"messages": ["Saved to DB."]}

# Define the graph
def build_receipt_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("extract_receipt", extract_receipt)
    workflow.add_node("initial_price_check", initial_price_check)
    workflow.add_node("save_to_database", save_to_database)
    
    workflow.set_entry_point("extract_receipt")
    workflow.add_edge("extract_receipt", "initial_price_check")
    workflow.add_edge("initial_price_check", "save_to_database")
    workflow.add_edge("save_to_database", END)
    
    return workflow.compile()
    
receipt_graph = build_receipt_graph()
