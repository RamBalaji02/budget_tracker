from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.expense import Expense
from app.models.income import Income
from app.core.deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def summary(db: Session = Depends(get_db),
            user_id: int = Depends(get_current_user)):

    try:
        expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
        income = db.query(Income).filter(Income.user_id == user_id).all()

        total_expense = sum(float(e.amount or 0) for e in expenses)
        total_income = sum(float(i.amount or 0) for i in income)

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense
        }

    except Exception as e:
        # 🔥 IMPORTANT: show real error instead of 500 crash
        return {"error": str(e)}