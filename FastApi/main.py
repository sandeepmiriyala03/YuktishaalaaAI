import time
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# 1. FastAPI App Initialization
yukaiApp = FastAPI(
    title="Yukai FastAPI",
    version="1.0.0",
    description="Product Management API",
    docs_url="/yukai",
    redoc_url="/redoc",
)

# డేటాబేస్ కాన్ఫిగరేషన్
DB_HOST = "localhost"
DB_NAME = "FASTAPI"
DB_USER = "postgres"
DB_PASS = "1234"


# 2. Helper Function for Database Connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as error:
        print(f"Error connecting to database: {error}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# 3. Startup Database Connection Check Loop
print("Checking database connection...")
while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("Database connected successfully!")
        conn.close()
        break
    except Exception as error:
        print(f"Error connecting to database: {error}. Retrying in 2 seconds...")
        time.sleep(2)


# 4. Pydantic Request Models (అన్ని కాలమ్స్ తో)
class ProductSchema(BaseModel):
    Name: str
    Price: int
    Is_Sale: Optional[bool] = False
    Inventory: Optional[int] = 0


# 5. API Routes

@yukaiApp.get("/")
def read_root():
    return {"message": "Welcome to Yukai FastAPI"}


# FETCH ALL PRODUCTS (READ)
@yukaiApp.get("/products")
def get_products():
    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute('SELECT "Id", "Name", "Price", "Is_Sale", "Inventory", "Created_at" FROM public."Products" ORDER BY "Id" ASC')
        records = cur.fetchall()
        return {"status": "success", "data": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        db.close()


# CREATE A NEW PRODUCT (INSERT)
@yukaiApp.post("/products")
def create_product(product: ProductSchema):
    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO public."Products" ("Name", "Price", "Is_Sale", "Inventory") 
            VALUES (%s, %s, %s, %s) 
            RETURNING *
            ''',
            (product.Name, product.Price, product.Is_Sale, product.Inventory)
        )
        new_product = cur.fetchone()
        db.commit()
        return {"status": "success", "message": "Product created successfully", "data": new_product}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        db.close()


# UPDATE A PRODUCT (UPDATE)
@yukaiApp.put("/products/{product_id}")
def update_product(product_id: int, product: ProductSchema):
    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute(
            '''
            UPDATE public."Products" 
            SET "Name" = %s, "Price" = %s, "Is_Sale" = %s, "Inventory" = %s 
            WHERE "Id" = %s 
            RETURNING *
            ''',
            (product.Name, product.Price, product.Is_Sale, product.Inventory, product_id)
        )
        updated_product = cur.fetchone()
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        db.commit()
        return {"status": "success", "message": "Product updated successfully", "data": updated_product}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        db.close()


# DELETE A PRODUCT (DELETE)
@yukaiApp.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute(
            'DELETE FROM public."Products" WHERE "Id" = %s RETURNING *',
            (product_id,)
        )
        deleted_product = cur.fetchone()
        
        if not deleted_product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        db.commit()
        return {"status": "success", "message": "Product deleted successfully", "data": deleted_product}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        db.close()