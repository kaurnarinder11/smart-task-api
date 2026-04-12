from fastapi import FastAPI
from app.db.database import engine
from app.models import user, task  # ← ADD user model
from app.routes import user_routes, tasks as task_routes  # ← ADD user_routes

# Create tables
user.Base.metadata.create_all(bind=engine)  # ← ADD THIS
task.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user_routes.router)  # ← ADD THIS
app.include_router(task_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Smart Task API", "endpoints": {...}}