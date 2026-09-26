import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(item: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(
        item.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    db_item = models.User(email=item.email, password=hashed_password)
    db.add(db_item)

    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered") from error

    db.refresh(db_item)
    return db_item