from app.db.database import Base, engine
from app.models.user import User
from app.models.expense import Expense
from app.models.income import Income
from app.models.category import Category

Base.metadata.create_all(bind=engine)

print("DB CREATED SUCCESSFULLY")