# app/main.py

from fastapi import FastAPI
from app.routers import router
from dotenv import load_dotenv

load_dotenv()  # loads .env

app = FastAPI(title="Production ML API")

app.include_router(router)
