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
    default_names = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Salary", "Investment", "Other"]
    custom_categories = db.query(Category).filter(Category.user_id == user_id).all()
    
    results = []
    for i, name in enumerate(default_names):
        results.append({
            "id": -(i + 1),
            "name": name,
            "user_id": None
        })
    
    for c in custom_categories:
        if c.name not in default_names:
            results.append({
                "id": c.id,
                "name": c.name,
                "user_id": c.user_id
            })
            
    return results