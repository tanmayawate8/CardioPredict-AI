# ==========================================
# SHARED FLASK EXTENSIONS
#
# Kept in their own module (instead of inside
# app.py) so that models.py and app.py can both
# import them without causing circular imports.
# ==========================================

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

# Where Flask-Login redirects a user who tries to
# access a @login_required page while logged out.
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "error"