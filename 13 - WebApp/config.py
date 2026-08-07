# ==========================================
# APPLICATION CONFIGURATION (config.py)
# ==========================================

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load variables from .env file
load_dotenv(BASE_DIR / ".env")


class Config:

    # ==========================================
    # SECRET KEY & SESSION SECURITY
    # ==========================================
    SECRET_KEY = os.getenv("SECRET_KEY", "CardioPredict_Secure_Static_Key_2026_LIVE")

    # ==========================================
    # DATABASE (PostgreSQL / MySQL)
    # ==========================================
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://heartdb_user:jzkYvEIPc79fsNdblaKwxLXl0w5xmxgb@dpg-d9iudo7aqgkc73amkbmg-a/heartdb"
    )

    # Fix legacy postgres:// URL scheme for SQLAlchemy 2.0+
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
    ) == "True"

    # ==========================================
    # DATABASE POOLING & SSL FIX FOR RENDER
    # ==========================================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,       # Verifies connection health before running queries
        "pool_recycle": 300,         # Recycles active connections every 5 minutes
        "pool_timeout": 30,          # Timeout limit for acquiring connections
        "pool_size": 10,             # Base connection pool size
        "max_overflow": 5,           # Additional temporary overflow connections
    }

    # ==========================================
    # SENDGRID API CONFIGURATION
    # ==========================================
    SENDGRID_API_KEY = os.getenv(
        "SENDGRID_API_KEY",
        "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"
    )
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "cardiopredictai@gmail.com")

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