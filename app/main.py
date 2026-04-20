from fastapi import FastAPI
from app.db.database import engine
from app.models import user, task
from app.routes import user_routes, tasks as task_routes
from app.routes import jokes_route as joke_routes
from app.routes import report_routes
from app.core.logger import get_logger

# Create logger
logger = get_logger("main")

# Create tables
user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 ========== SMART TASK API STARTING ========== 🚀")
    logger.info("📦 Database connected")
    logger.info("🔐 Authentication enabled")
    logger.info("📝 Logging system active")
    logger.info("✅ API ready to accept requests")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 ========== SMART TASK API SHUTTING DOWN ========== 👋")

# Include routers
app.include_router(user_routes.router)
app.include_router(task_routes.router)
app.include_router(joke_routes.router)
app.include_router(report_routes.router)

@app.get("/")
def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Welcome to Smart Task API", "endpoints": {...}}