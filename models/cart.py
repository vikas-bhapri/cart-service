from sqlalchemy import Column, String, Integer
from database import Base

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    product_name = Column(String)
    product_price = Column(Integer)
    product_quantity = Column(Integer)
    user_id = Column(Integer)
