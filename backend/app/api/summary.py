from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.expense import Expense
from app.models.income import Income

router = APIRouter(prefix="/summary")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def summary(db: Session = Depends(get_db)):

    expenses = db.query(Expense).all()
    income = db.query(Income).all()

    total_expense = sum(e.amount or 0 for e in expenses)
    total_income = sum(i.amount or 0 for i in income)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }