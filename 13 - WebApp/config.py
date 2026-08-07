# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load variables from your existing .env file
load_dotenv(BASE_DIR / ".env")


class Config:

    # ==========================================
    # SECRET KEY
    # ==========================================

    SECRET_KEY = os.getenv("SECRET_KEY", "CardioPredict_Secure_Static_Key_2026_LIVE")

    # ==========================================
    # DATABASE (PostgreSQL / MySQL)
    # ==========================================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://heartdb_user:jzkYvEIPc79fsNdblaKwxLXl0w5xmxgb@dpg-d9iudo7aqgkc73amkbmg-a/heartdb"
    )

    # Fix postgres:// URL prefix if provided by legacy hosting services
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
    ) == "True"

    # ==========================================
    # CRITICAL SSL & POOL FIX FOR RENDER & CLOUD POSTGRESQL
    # ==========================================

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,       # Verifies connection health before running queries
        "pool_recycle": 300,         # Recycles active connections every 5 minutes
        "pool_timeout": 30,          # Timeout limit for acquiring connections
        "pool_size": 10,             # Base connection pool size
        "max_overflow": 5,           # Additional temporary overflow connections
    }

    # ==========================================
    # SESSION / LOGIN BEHAVIOR
    # ==========================================

    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv("SESSION_TIMEOUT", 1800))
    )

    REMEMBER_COOKIE_DURATION = timedelta(
        days=int(os.getenv("REMEMBER_COOKIE_DURATION", 30))
    )

    # ==========================================
    # EMAIL & FLASK-MAIL SETTINGS (FORGOT PASSWORD)
    # ==========================================

    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    # Flask-Mail standard configuration required for sending reset links
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", os.getenv("EMAIL_ADDRESS", "cardiopredictai@gmail.com"))
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", os.getenv("EMAIL_PASSWORD", ""))
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("EMAIL_ADDRESS", "cardiopredictai@gmail.com"))

    # ==========================================
    # SECURITY TOKEN LIFETIMES
    # ==========================================

    PASSWORD_RESET_EXPIRE = int(os.getenv("PASSWORD_RESET_EXPIRE", 1800))

    EMAIL_VERIFY_EXPIRE = int(os.getenv("EMAIL_VERIFY_EXPIRE", 3600))

    # ==========================================
    # FILE UPLOADS
    # ==========================================

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads")

    PROFILE_FOLDER = os.getenv("PROFILE_FOLDER", "static/uploads/profile")

    REPORT_FOLDER = os.getenv("REPORT_FOLDER", "static/reports")

    # ==========================================
    # APPLICATION METADATA
    # ==========================================

    APP_NAME = os.getenv("APP_NAME", "CardioPredict AI")

    APP_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")