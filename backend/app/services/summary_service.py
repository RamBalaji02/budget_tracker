from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.models.income import Income

def get_summary(db: Session, user_id: int):

    total_income = sum(i.amount for i in db.query(Income).filter(Income.user_id == user_id).all())

    total_expense = sum(e.amount for e in db.query(Expense).filter(Expense.user_id == user_id).all())

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }