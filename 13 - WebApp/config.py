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
    #
    # Required by Flask for sessions, login
    # cookies and flash messages. Set a real
    # value in your .env file for production:
    #
    #   SECRET_KEY=some-long-random-string
    # ==========================================

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this")

    # ==========================================
    # DATABASE (PostgreSQL / MySQL)
    #
    # Set DATABASE_URL in your .env file, e.g.:
    #
    #   DATABASE_URL=postgresql://user:pass@host/db
    # ==========================================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://heartdb_user:jzkYvEIPc79fsNdblaKwxLXl0w5xmxgb@dpg-d9iudo7aqgkc73amkbmg-a/heartdb"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
    ) == "True"

    # ==========================================
    # SESSION / LOGIN BEHAVIOR
    #
    # SESSION_TIMEOUT: how long a normal login
    # session lasts (seconds) before Flask
    # expires it.
    #
    # REMEMBER_COOKIE_DURATION: how long the
    # "Remember me" cookie keeps a user logged
    # in (days), used by Flask-Login.
    # ==========================================

    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv("SESSION_TIMEOUT", 1800))
    )

    REMEMBER_COOKIE_DURATION = timedelta(
        days=int(os.getenv("REMEMBER_COOKIE_DURATION", 30))
    )

    # ==========================================
    # EMAIL & FLASK-MAIL SETTINGS (FORGOT PASSWORD)
    #
    # Used for password reset and verification emails.
    # ==========================================

    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    # Flask-Mail standard configuration required for sending reset links
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL_ADDRESS")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL_ADDRESS", "noreply@cardiopredict.ai")

    # ==========================================
    # SECURITY TOKEN LIFETIMES
    #
    # Defines expiration times for reset tokens.
    # ==========================================

    PASSWORD_RESET_EXPIRE = int(os.getenv("PASSWORD_RESET_EXPIRE", 1800))

    EMAIL_VERIFY_EXPIRE = int(os.getenv("EMAIL_VERIFY_EXPIRE", 3600))

    # ==========================================
    # FILE UPLOADS
    #
    # Reserved for a future profile-picture /
    # report-upload feature. Not yet used by
    # any route.
    # ==========================================

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads")

    PROFILE_FOLDER = os.getenv("PROFILE_FOLDER", "static/uploads/profile")

    REPORT_FOLDER = os.getenv("REPORT_FOLDER", "static/reports")

    # ==========================================
    # APPLICATION METADATA
    # ==========================================

    APP_NAME = os.getenv("APP_NAME", "CardioPredict AI")

    APP_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")