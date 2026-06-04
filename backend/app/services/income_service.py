from sqlalchemy.orm import Session
from app.models.income import Income

def create_income(db: Session, data, user_id: int):

    income = Income(
        amount=data.amount,
        source=data.source,
        date=data.date,
        user_id=user_id
    )

    db.add(income)
    db.commit()
    db.refresh(income)

    return income


def get_income(db: Session, user_id: int):
    return db.query(Income).filter(Income.user_id == user_id).all()


def update_income(db: Session, income_id: int, data, user_id: int):
    income = db.query(Income).filter(Income.id == income_id, Income.user_id == user_id).first()
    if not income:
        return None
    income.amount = data.amount
    income.source = data.source
    income.date = data.date
    db.commit()
    db.refresh(income)
    return income


def delete_income(db: Session, income_id: int, user_id: int) -> bool:
    income = db.query(Income).filter(Income.id == income_id, Income.user_id == user_id).first()
    if not income:
        return False
    db.delete(income)
    db.commit()
    return True