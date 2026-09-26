from fastapi import APIRouter, HTTPException

import schemas
from postgres_database import get_raw_db_connection

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def get_products():
    db = get_raw_db_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT "Id", "Name", "Price", "Is_Sale", "Inventory", "Created_at" '
                'FROM public."Products" ORDER BY "Id" ASC'
            )
            records = cursor.fetchall()
        return {"status": "success", "data": records}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        db.close()


@router.post("")
def create_product(product: schemas.ProductSchema):
    db = get_raw_db_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                'INSERT INTO public."Products" '
                '("Name", "Price", "Is_Sale", "Inventory") '
                'VALUES (%s, %s, %s, %s) RETURNING *',
                (product.Name, product.Price, product.Is_Sale, product.Inventory),
            )
            new_product = cursor.fetchone()
        db.commit()
        return {"status": "success", "message": "Product created successfully", "data": new_product}
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        db.close()


@router.put("/{product_id}")
def update_product(product_id: int, product: schemas.ProductSchema):
    db = get_raw_db_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                'UPDATE public."Products" '
                'SET "Name" = %s, "Price" = %s, "Is_Sale" = %s, "Inventory" = %s '
                'WHERE "Id" = %s RETURNING *',
                (product.Name, product.Price, product.Is_Sale, product.Inventory, product_id),
            )
            updated_product = cursor.fetchone()
        if updated_product is None:
            db.rollback()
            raise HTTPException(status_code=404, detail="Product not found")
        db.commit()
        return {"status": "success", "message": "Product updated successfully", "data": updated_product}
    except HTTPException:
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        db.close()


@router.delete("/{product_id}")
def delete_product(product_id: int):
    db = get_raw_db_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                'DELETE FROM public."Products" WHERE "Id" = %s RETURNING *',
                (product_id,),
            )
            deleted_product = cursor.fetchone()
        if deleted_product is None:
            db.rollback()
            raise HTTPException(status_code=404, detail="Product not found")
        db.commit()
        return {"status": "success", "message": "Product deleted successfully", "data": deleted_product}
    except HTTPException:
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        db.close()