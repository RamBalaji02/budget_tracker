from app.db.database import Base, engine
from app.models.user import User
from app.models.expense import Expense

Base.metadata.create_all(bind=engine)

print("DB CREATED SUCCESSFULLY")