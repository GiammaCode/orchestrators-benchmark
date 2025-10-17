import os
from pathlib import Path

class Config:
    """
    Configuration class for the Flask application.

    """
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:2727/")
    DB_NAME = "assignment_service"

    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/data/submissions"))

    PROCESSING_DELAY = float(os.getenv("PROCESSING_DELAY", "0.5"))

    FLASK_ENV = os.getenv("FLASK_ENV", "development")