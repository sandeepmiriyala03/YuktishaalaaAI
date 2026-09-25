import time
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

# SQLAlchemy డ్రైవర్లను ఇంపోర్ట్ చేయడం
import models
from database import engine, get_db

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


# డేటాబేస్ కాన్ఫిగరేషన్ (Raw psycopg2 కోసం)
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


# 4. Pydantic Request Models

# Products Schema (Raw SQL కోసం)
class ProductSchema(BaseModel):
    Name: str
    Price: int
    Is_Sale: Optional[bool] = False
    Inventory: Optional[int] = 0

# Test Table Schemas (SQLAlchemy / ORM కోసం)
class TestCreate(BaseModel):
    name: str
    Fname: Optional[str] = None
    salary: Optional[float] = None
    createdby: Optional[str] = "System"

class TestResponse(BaseModel):
    Id: int
    name: str
    Fname: Optional[str] = None
    salary: Optional[float] = None
    createdby: str

    class Config:
        from_attributes = True


# 5. API Routes

@yukaiApp.get("/")
def read_root():
    return {"message": "Welcome to Yukai FastAPI"}


# ==========================================
#  A. PRODUCTS ENDPOINTS (Raw psycopg2 SQL)
# ==========================================

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


# ==========================================
#  B. TEST TABLE ENDPOINTS (SQLAlchemy ORM)
# ==========================================

# 1. CREATE RECORD IN "Test" TABLE
@yukaiApp.post("/test", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
def create_test_record(item: TestCreate, db: Session = Depends(get_db)):
    db_item = models.Test(
        name=item.name,
        Fname=item.Fname,
        salary=item.salary,
        createdby=item.createdby
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# 2. READ ALL RECORDS FROM "Test" TABLE
@yukaiApp.get("/test", response_model=List[TestResponse])
def get_all_test_records(db: Session = Depends(get_db)):
    records = db.query(models.Test).all()
    return records


# 3. READ SINGLE RECORD BY ID
@yukaiApp.get("/test/{test_id}", response_model=TestResponse)
def get_test_record(test_id: int, db: Session = Depends(get_db)):
    record = db.query(models.Test).filter(models.Test.Id == test_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


# CREATE (INSERT) A NEW RECORD IN "Test" TABLE
@yukaiApp.post("/test", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
def create_test_record(item: TestCreate, db: Session = Depends(get_db)):
    # 1. Pydantic schema నుండి SQLAlchemy Model ఆబ్జెక్ట్‌ను క్రియేట్ చేయడం
    db_item = models.Test(
        name=item.name,
        Fname=item.Fname,
        salary=item.salary,
        createdby=item.createdby
    )
    
    # 2. ఆబ్జెక్ట్‌ను DB Session లోకి చేర్చడం (Pending State)
    db.add(db_item)
    
    # 3. డేటాబేస్‌కు INSERT SQL క్వెరీని పంపి సేవ్ చేయడం
    db.commit()
    
    # 4. ఆటో-జెనరేట్ అయిన Id ని DB నుండి ఆబ్జెక్ట్‌లోకి రీఫ్రెష్ చేయడం
    db.refresh(db_item)
    
    # 5. క్రియేట్ అయిన రికార్డును రెస్పాన్స్‌గా పంపడం
    return db_item