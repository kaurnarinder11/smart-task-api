# app/main.py
from fastapi import FastAPI
from app.core.config import settings

# Validate config on startup
settings.validate()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

@app.get("/")
def home():
    return {
        "app_name": settings.APP_NAME,
        "debug_mode": settings.DEBUG,
        "secret_loaded": settings.SECRET_KEY is not None
    }

@app.get("/health")
def health():
    return {"status": "ok", "port": settings.PORT}