from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.expense import Expense
from app.core.deps import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ➕ ADD EXPENSE
@router.post("/")
def add_expense(data: dict,
                db: Session = Depends(get_db),
                user_id: int = Depends(get_current_user)):

    new_expense = Expense(
        amount=data["amount"],
        category=data["category"],
        note=data.get("note", ""),
        exp_date=data["exp_date"],
        user_id=user_id
    )

    db.add(new_expense)
    db.commit()

    return {"message": "Expense added successfully"}


# 📜 GET EXPENSES
@router.get("/")
def get_expenses(db: Session = Depends(get_db),
                 user_id: int = Depends(get_current_user)):

    expenses = db.query(Expense).filter(
        Expense.user_id == user_id
    ).all()

    return [
        {
            "id": e.id,
            "amount": float(e.amount),
            "category": e.category,
            "note": e.note,
            "date": str(e.exp_date)
        }
        for e in expenses
    ]