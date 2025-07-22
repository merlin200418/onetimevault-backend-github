
from fastapi import FastAPI
from auth import auth_router
from crud import message_router
from database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(auth_router, prefix="/auth")
app.include_router(message_router, prefix="/message")
