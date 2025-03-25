from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import cart as cart_schema
from models import cart as cart_model


def add_to_cart(cart: cart_schema.InsertCart, db: Session):
    # check if the user already added the product to the cart
    product = db.query(cart_model.Cart).filter(cart_model.Cart.product_id == cart.product_id, cart_model.Cart.user_id == cart.user_id).first()
    if product:
        product.product_quantity += cart.product_quantity
        db.commit()
        db.refresh(product)
        return product
    
    new_cart = cart_model.Cart(
        product_id=cart.product_id,
        product_name=cart.product_name,
        product_price=cart.product_price,
        product_quantity=cart.product_quantity,
        user_id=cart.user_id
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

def get_cart(user_id: str, db: Session):
    result = db.query(cart_model.Cart).filter(cart_model.Cart.user_id == user_id).all()
    cart_items = [
        {
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_price": item.product_price,
            "product_quantity": item.product_quantity,
            "total_price": item.product_price * item.product_quantity
        }
        for item in result
    ]
    return {
        "user_id": user_id,
        "cart_items": cart_items
    }

def remove_from_cart(cart: cart_schema.RemoveCart, db: Session):
    product = db.query(cart_model.Cart).filter(cart_model.Cart.product_id == cart.product_id, cart_model.Cart.user_id == cart.user_id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found in the cart")
    
    if product.product_quantity > 1:
        product.product_quantity -= 1
        db.commit()
        db.refresh(product)
    else:
        db.delete(product)
        db.commit()
    
    # Fetch the updated cart
    result = db.query(cart_model.Cart).filter(cart_model.Cart.user_id == cart.user_id).all()
    cart_items = [
        {
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_price": item.product_price,
            "product_quantity": item.product_quantity,
            "total_price": item.product_price * item.product_quantity
        }
        for item in result
    ]
    
    return {
        "user_id": cart.user_id,
        "cart_items": cart_items
    }