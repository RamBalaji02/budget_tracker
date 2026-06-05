from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.income import router as income_router
from app.api.summary import router as summary_router
from app.api.category import router as category_router

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(income_router)
app.include_router(summary_router)
app.include_router(category_router)


@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}