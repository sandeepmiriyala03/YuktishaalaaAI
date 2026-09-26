from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import fastapi_models as models
import schemas
from postgres_database import get_db

router = APIRouter(prefix="/test", tags=["test"])


@router.post("", response_model=schemas.TestResponse, status_code=status.HTTP_201_CREATED)
def create_test_record(item: schemas.TestCreate, db: Session = Depends(get_db)):
    db_item = models.Test(
        name=item.name,
        Fname=item.Fname,
        salary=item.salary,
        createdby=item.createdby,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("", response_model=List[schemas.TestResponse])
def get_all_test_records(db: Session = Depends(get_db)):
    return db.query(models.Test).all()


@router.get("/{test_id}", response_model=schemas.TestResponse)
def get_test_record(test_id: int, db: Session = Depends(get_db)):
    record = db.query(models.Test).filter(models.Test.Id == test_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record