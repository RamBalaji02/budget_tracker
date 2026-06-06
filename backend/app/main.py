from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.category import router as category_router
from app.api.expense import router as expense_router
from app.api.income import router as income_router
from app.api.summary import router as summary_router

from app.db.database import engine
from app.models.user import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(summary_router)

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}