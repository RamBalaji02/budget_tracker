from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import SessionLocal
from app.models.expense import Expense

router = APIRouter(prefix="/expenses")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_expense(data: dict, db: Session = Depends(get_db)):

    expense = Expense(
        amount=data["amount"],
        category=data["category"],
        note=data["note"],
        exp_date=datetime.strptime(data["exp_date"], "%Y-%m-%d").date(),
        user_id=1
    )

    db.add(expense)
    db.commit()

    return {"message": "expense added"}


@router.get("/")
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()