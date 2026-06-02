from sqlalchemy.orm import Session
from app.models.expense import Expense

def create_expense(db: Session, data, user_id: int):

    expense = Expense(
        amount=data.amount,
        category=data.category,
        note=data.note,
        exp_date=data.exp_date,
        user_id=user_id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()