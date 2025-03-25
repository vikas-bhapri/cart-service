from sqlalchemy import Column, String, Integer, JSON, Boolean, Float
from database import Base

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id= Column(String)
    order_details = Column(String)
    total_price = Column(Float)
    status = Column(String)
    is_success = Column(Boolean)
    reason = Column(String)