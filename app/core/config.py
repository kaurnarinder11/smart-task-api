# app/core/config.py
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    # Required - will crash if missing (add error handling)
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Optional with defaults (FALLBACKS!)
    APP_NAME = os.getenv("APP_NAME", "Smart Task API")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8000))
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # ========== NEW CLOUD SETTINGS ==========
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, staging, production
    
    # S3 Storage (optional - only needed in production)
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", None)
    S3_REGION = os.getenv("S3_REGION", "us-east-1")
    
    # Database (already have DATABASE_URL. Set default if missing)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
    
    # Report storage path (for local development)
    REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")

    # Validation
    @classmethod
    def validate(cls):
        if not cls.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required!")
        
        # Warn if in production without S3 (but don't crash - optional feature)
        if cls.ENVIRONMENT == "production" and not cls.S3_BUCKET_NAME:
            import warnings
            warnings.warn("Running in production without S3_BUCKET_NAME. Files will save locally!")

# Create single instance to import everywhere
settings = Settings()

# Run validation on import
settings.validate()