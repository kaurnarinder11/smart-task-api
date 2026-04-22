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
    
    # Validation
    @classmethod
    def validate(cls):
        if not cls.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required!")

# Create single instance to import everywhere
settings = Settings()

# Run validation on import
settings.validate()