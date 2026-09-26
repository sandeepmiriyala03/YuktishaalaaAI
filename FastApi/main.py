import time
from fastapi import FastAPI

import models
from database import engine, get_raw_db_connection
from routes.products import router as products_router
from routes.test import router as test_router
from routes.user import router as user_router

# 1. FastAPI App Initialization
yukaiApp = FastAPI(
    title="Yukai FastAPI",
    version="1.0.0",
    description="Product & Test Management API",
    docs_url="/docs",
    redoc_url="/redoc",
)

# SQLAlchemy ద్వారా 'Test' టేబుల్ లేకపోతే ఆటోమేటిక్‌గా క్రియేట్ చేస్తుంది
models.Base.metadata.create_all(bind=engine)
yukaiApp.include_router(user_router)
yukaiApp.include_router(test_router)
yukaiApp.include_router(products_router)


# 3. Startup Database Connection Check Loop
print("Checking database connection...")
while True:
    try:
        conn = get_raw_db_connection()
        print("Database connected successfully!")
        conn.close()
        break
    except Exception as error:
        print(f"Error connecting to database: {error}. Retrying in 2 seconds...")
        time.sleep(2)


# API Routes

@yukaiApp.get("/")
def read_root():
    return {"message": "Welcome to Yukai FastAPI"}



