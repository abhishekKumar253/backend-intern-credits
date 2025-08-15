from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.connection import SessionLocal 
from ..models.users import User 
from ..models.credits import Credit 
from datetime import datetime 

router = APIRouter(
    prefix="/api/credits",
    tags=["Credits"]
)

# Pydantic models
class CreditAmount(BaseModel):
    amount: int

class ExternalUpdate(BaseModel):
    credits: int

# Dependency to get DB 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET current credit balance
@router.get("/{user_id}")
def get_credit(user_id: int, db: Session = Depends(get_db)): 
    credit = db.query(Credit).filter(Credit.user_id == user_id).first()
    if not credit:
        raise HTTPException(status_code=404, detail="User credits not found")
    return {"user_id": user_id, "credits": credit.credits, "last_updated": credit.last_updated}

# POST add credits
@router.post("/{user_id}/add")
def add_credit(user_id: int, payload: CreditAmount, db: Session = Depends(get_db)): 
    credit = db.query(Credit).filter(Credit.user_id == user_id).first()
    if not credit:
        user_exists = db.query(User).filter(User.user_id == user_id).first()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found for creating credit entry")
        
        credit = Credit(user_id=user_id, credits=payload.amount)
        db.add(credit)
    else:
        credit.credits += payload.amount
    db.commit()
    db.refresh(credit)
    return {"user_id": user_id, "credits": credit.credits}

# POST deduct credits
@router.post("/{user_id}/deduct")
def deduct_credit(user_id: int, payload: CreditAmount, db: Session = Depends(get_db)):
    credit = db.query(Credit).filter(Credit.user_id == user_id).first()
    if not credit:
        raise HTTPException(status_code=404, detail="User credits not found")
    if credit.credits - payload.amount < 0:
        raise HTTPException(status_code=400, detail="Insufficient credits")
    credit.credits -= payload.amount
    db.commit()
    db.refresh(credit)
    return {"user_id": user_id, "credits": credit.credits}

# PATCH reset credits
@router.patch("/{user_id}/reset")
def reset_credit(user_id: int, db: Session = Depends(get_db)):
    credit = db.query(Credit).filter(Credit.user_id == user_id).first()
    if not credit:
        raise HTTPException(status_code=404, detail="User credits not found")
    credit.credits = 0
    db.commit()
    db.refresh(credit)
    return {"user_id": user_id, "credits": credit.credits}

# POST external update
@router.post("/{user_id}/external-update")
def external_update_credit(user_id: int, payload: ExternalUpdate, db: Session = Depends(get_db)): 
    credit = db.query(Credit).filter(Credit.user_id == user_id).first()
    if not credit:
        user_exists = db.query(User).filter(User.user_id == user_id).first()
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found for creating credit entry")

        credit = Credit(user_id=user_id, credits=payload.credits)
        db.add(credit)
    else:
        credit.credits = payload.credits
    db.commit()
    db.refresh(credit)
    return {"user_id": user_id, "credits": credit.credits}