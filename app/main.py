# app/main.py
from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import task  
from app.core.config import settings
from app.routes import tasks



Base.metadata.create_all(bind=engine)

settings.validate()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(tasks.router)

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