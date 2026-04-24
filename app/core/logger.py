import logging
import sys
from datetime import datetime

# Why this file?
# 1. Single source of truth for logging configuration
# 2. Easy to change log levels globally
# 3. Easy to add file logging later

# Configure logging with both console and file output
def setup_logger():
    """Setup application logging configuration"""
    
    # Create logger
    logger = logging.getLogger("smart_task_api")
    logger.setLevel(logging.DEBUG)  # Capture all levels
    
    # Format for logs (why this format?)
    # %(asctime)s - When it happened
    # %(name)s - Which logger (file/module)
    # %(levelname)s - INFO/WARNING/ERROR
    # %(message)s - The actual log message
    # %(lineno)d - Line number where log was called (debugging!)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | Line %(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler (see logs in terminal while running)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Console shows INFO and above
    console_handler.setFormatter(formatter)
    
    # File handler (save logs for later debugging)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # File captures everything
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Create a global logger instance
# Why global? So we can import it anywhere in the app
logger = setup_logger()

# Why create a get_logger function?
# This allows each module to have its own named logger
def get_logger(name: str):
    """Get a logger instance for a specific module"""
    return logger.getChild(name)