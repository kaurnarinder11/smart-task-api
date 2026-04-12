# app/main.py
from fastapi import FastAPI
from app.routes import tasks
from app.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Task API",
    description="A simple task management API with full CRUD",
    version="1.0.0"
)

# Include routers
app.include_router(tasks.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Smart Task API",
        "endpoints": {
            "tasks": "/tasks",
            "create": "POST /tasks/",
            "get_all": "GET /tasks/",
            "get_one": "GET /tasks/{id}",
            "update": "PUT /tasks/{id}",
            "delete": "DELETE /tasks/{id}",
            "complete": "PATCH /tasks/{id}/complete"
        }
    }