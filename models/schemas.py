from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ExtractedItem(BaseModel):
    item_number: str = Field(description="The Costco item number, usually a 6-7 digit number.")
    name: str = Field(description="The name of the item on the receipt.")
    purchase_price: float = Field(description="The price paid for the item, as a float.")

class ExtractedReceipt(BaseModel):
    receipt_number: str = Field(description="The unique transaction or receipt number.")
    date_of_purchase: str = Field(description="The date of purchase, in YYYY-MM-DD format if possible.")
    items: List[ExtractedItem] = Field(description="A list of items purchased.")

class DBUser(BaseModel):
    whatsapp_number: str
    created_at: Optional[datetime] = None

class DBReceipt(BaseModel):
    user_id: str
    image_url: Optional[str] = None
    date_of_purchase: str
    receipt_number: str

class DBItem(BaseModel):
    receipt_id: str
    item_number: str
    name: str
    purchase_price: float
    current_price: Optional[float] = None
    last_checked: Optional[datetime] = None
    status: str = "tracking" # tracking, notified, expired
