from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models import cart as cart_model
from routes import cart as cart_router

app = FastAPI(
    title="E-Commerce Cart Service API",
    description="This is a simple API for E-Commerce Cart Service",
    version="1.0.0",
    contact={
        "name": "Vikas Bhapri",
        "email": "vikasbhapri@gmail.com"
    }
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cart_router.router)

# Create the database tables
cart_model.Base.metadata.create_all(bind=engine)
