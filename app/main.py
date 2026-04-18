# app/main.py (UPDATED)

from fastapi import FastAPI
from app.db.database import engine
from app.models import user, task
from app.routes import user_routes, tasks as task_routes
from app.routes import jokes_route as joke_routes
from app.routes import report_routes  # ← ADD THIS

# Create tables
user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user_routes.router)
app.include_router(task_routes.router)
app.include_router(joke_routes.router)
app.include_router(report_routes.router)  # ← ADD THIS

@app.get("/")
def root():
    return {"message": "Welcome to Smart Task API", "endpoints": {...}}