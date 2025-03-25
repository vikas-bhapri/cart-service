from pydantic import BaseModel
from typing import List, Optional

class InsertCart(BaseModel):
    user_id: str
    product_id: int
    product_name: Optional[str]
    product_quantity: int
    product_price: float

class RemoveCart(BaseModel):
    user_id: str
    product_id: int

class Product(BaseModel):
    product_id: int
    product_name: str
    product_price: float
    product_quantity: int
    total_price: float

class DisplayCart(BaseModel):
    user_id: str
    cart_items: List[Product]