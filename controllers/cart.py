import json, requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import cart as cart_schema
from models import cart as cart_model, order as order_model
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
from dotenv import load_dotenv

load_dotenv()

SERVICEBUS_CONNECTION_STRING = os.getenv("SERVICEBUS_CONNECTION_STRING")
TOPIC_NAME = os.getenv("TOPIC_NAME")
PRODUCTS_SVC_URL = os.getenv("PRODUCTS_SVC_URL")

def publish_order_event(order_data, event_type):
    with ServiceBusClient.from_connection_string(SERVICEBUS_CONNECTION_STRING) as client:
        sender = client.get_topic_sender(TOPIC_NAME)
        with sender:
            message = ServiceBusMessage(order_data)
            message.application_properties = {"event_type": event_type}
            sender.send_messages(message)
            print(f"Published order event: {order_data}")

def add_to_cart(cart: cart_schema.InsertCart, db: Session):
    # Fetch the product details from the products service
    product_url = f"{PRODUCTS_SVC_URL}/products/{cart.product_id}"
    response = requests.get(product_url)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product_data = response.json()
    product_stock = product_data.get("stock")
    print(product_stock)
    # check if the user already added the product to the cart
    product = db.query(cart_model.Cart).filter(cart_model.Cart.product_id == cart.product_id, cart_model.Cart.user_id == cart.user_id).first()
    if product:
        product.product_quantity += cart.product_quantity
        if product.product_quantity > product_stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product out of stock")
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


def checkout(user_id: str, db: Session):
    cart_items = db.query(cart_model.Cart).filter(cart_model.Cart.user_id == user_id).all()

    if len(cart_items) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")
    
    total_price = sum([item.product_price * item.product_quantity for item in cart_items])
    
    cart_items_data = [
        {
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_price": item.product_price,
            "product_quantity": item.product_quantity,
            "total_price": item.product_price * item.product_quantity
        }
        for item in cart_items
    ]

    # Create an order
    new_order = order_model.Orders(
        user_id=user_id,
        total_price=total_price,
        order_details=str(cart_items_data),
        status="Processing",
        is_success=None,
        reason=None
    )
    db.add(new_order)
    db.commit()
    
    # Delete the cart items
    db.query(cart_model.Cart).filter(cart_model.Cart.user_id == user_id).delete()
    db.commit()
    db.refresh(new_order)

    try:
        order_event_data = json.dumps({
            "user_id": user_id,
            "order_id": new_order.id,
            "cart_items": cart_items_data
        })
        publish_order_event(order_event_data, "products_check")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": str(e)})

    return {
        "user_id": user_id,
        "cart_items": cart_items_data
    }