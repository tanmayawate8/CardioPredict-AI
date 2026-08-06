# ==========================================
# DATABASE MODELS
# ==========================================

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

from extensions import db


# ==========================================
# USER MODEL
# ==========================================

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # ==========================================
    # ACCOUNT STATUS FLAG
    # ==========================================
    is_disabled = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ==========================================
    # USER → PREDICTIONS RELATIONSHIP
    # ==========================================
    # One user can save multiple predictions

    predictions = db.relationship(
        "Prediction",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


    # ==========================================
    # PASSWORD HELPERS & TOKENS
    # ==========================================

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )


    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')


    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)['user_id']
        except Exception:
            return None
        return db.session.get(User, user_id)


    # ==========================================
    # REPRESENTATION
    # ==========================================

    def __repr__(self):

        return f"<User {self.username}>"


# ==========================================
# PREDICTION MODEL
# ==========================================

class Prediction(db.Model):

    __tablename__ = "predictions"


    # ==========================================
    # PRIMARY KEY
    # ==========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ==========================================
    # USER RELATIONSHIP
    # ==========================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    # ==========================================
    # PATIENT INPUT DATA
    # ==========================================

    age = db.Column(
        db.Integer,
        nullable=False
    )

    sex = db.Column(
        db.String(20),
        nullable=False
    )

    chest_pain_type = db.Column(
        db.String(100),
        nullable=False
    )

    resting_bp = db.Column(
        db.Integer,
        nullable=False
    )

    cholesterol = db.Column(
        db.Integer,
        nullable=False
    )

    fasting_bs = db.Column(
        db.String(50),
        nullable=False
    )

    resting_ecg = db.Column(
        db.String(50),
        nullable=False
    )

    max_hr = db.Column(
        db.Integer,
        nullable=False
    )

    exercise_angina = db.Column(
        db.String(20),
        nullable=False
    )

    oldpeak = db.Column(
        db.Float,
        nullable=False
    )

    st_slope = db.Column(
        db.String(50),
        nullable=False
    )


    # ==========================================
    # PREDICTION OUTPUT
    # ==========================================

    result = db.Column(
        db.String(50),
        nullable=False
    )

    probability = db.Column(
        db.Float,
        nullable=False
    )


    # ==========================================
    # PREDICTION DATE AND TIME
    # ==========================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ==========================================
    # REPRESENTATION
    # ==========================================

    def __repr__(self):

        return (
            f"<Prediction "
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"result={self.result}>"
        )