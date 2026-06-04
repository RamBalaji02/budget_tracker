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


def update_expense(db: Session, expense_id: int, data, user_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    if not expense:
        return None
    expense.amount = data.amount
    expense.category = data.category
    expense.note = data.note
    expense.exp_date = data.exp_date
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: int, user_id: int) -> bool:
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    if not expense:
        return False
    db.delete(expense)
    db.commit()
    return True