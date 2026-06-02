from sqlalchemy.orm import Session
from app.models.category import Category

def create_category(db: Session, data, user_id: int):

    category = Category(
        name=data.name,
        user_id=user_id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session, user_id: int):

    return db.query(Category).filter(Category.user_id == user_id).all()