from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine, Base
from app.routes import user_routes, tasks as task_routes
from app.routes import jokes_route, report_routes, health  # ✅ ADDED health import
from app.core.logger import get_logger

# NEW: Import global error handler
from app.middleware.error_handler import GlobalErrorHandler

# Import models so they register with Base
from app.models import user, task

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("🎉 ========== SMART TASK API STARTING ========== 🎉")
    logger.info("✅ Database connected")
    logger.info("✅ All routers registered")
    yield

app = FastAPI(
    title="Smart Task API",
    description="A task management system with authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# 🔥 NEW: Add global error handler (catches ALL errors across ALL routes)
app.add_middleware(GlobalErrorHandler)

# Include routers
app.include_router(user_routes.router)
app.include_router(task_routes.router)
app.include_router(jokes_route.router)
app.include_router(report_routes.router)
app.include_router(health.router)  # ✅ ADDED health router

@app.get("/")
def root():
    return {
        "message": "Welcome to Smart Task API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/signup, /auth/login",
            "tasks": "/tasks",
            "jokes": "/jokes",
            "reports": "/reports",
            "health": "/health"  # ✅ ADDED health to endpoints list
        }
    }