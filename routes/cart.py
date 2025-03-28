from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from controllers import cart as cart_controller
from schemas import cart as cart_schema

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.post("/", response_model=cart_schema.InsertCart, status_code=status.HTTP_201_CREATED)
async def add_to_cart(cart: cart_schema.InsertCart, db: Session = Depends(get_db)):
    return cart_controller.add_to_cart(cart, db)

@router.get("/", response_model=cart_schema.DisplayCart, status_code=status.HTTP_200_OK)
async def get_cart(user_id: str, db: Session = Depends(get_db)):
    return cart_controller.get_cart(user_id, db)

@router.delete("/", response_model=cart_schema.DisplayCart, status_code=status.HTTP_200_OK)
async def delete_from_cart(cart: cart_schema.RemoveCart, db: Session = Depends(get_db)):
    return cart_controller.remove_from_cart(cart, db)

@router.post("/checkout", response_model=cart_schema.Checkout, status_code=status.HTTP_200_OK)
async def checkout(user_id: str, request: cart_schema.UserAddress, db: Session = Depends(get_db)):
    return cart_controller.checkout(user_id, request, db)

@router.put("/order_status", status_code=status.HTTP_200_OK)
def order_status(order_id: int, request: cart_schema.OrderStatus, db: Session = Depends(get_db)):
    return cart_controller.update_order_status(order_id, request, db)