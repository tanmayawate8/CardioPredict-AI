# ==========================================================
# HEART DISEASE RISK PREDICTION
# Configuration File
# ==========================================================

from pathlib import Path

# ==========================================================
# Base Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================================
# Models Directory
# ==========================================================

MODELS_DIR = BASE_DIR / "models"

# ==========================================================
# Model File
# ==========================================================

MODEL_FILE = MODELS_DIR / "heart_disease_model.pkl"

# ==========================================================
# Flask Settings
# ==========================================================

DEBUG = True

HOST = "127.0.0.1"

PORT = 5000

# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "Heart Disease Risk Prediction"

APP_VERSION = "1.0"

# ==========================================================
# Expected Input Features
# ==========================================================

FEATURE_COLUMNS = [

    "Age",

    "Sex",

    "ChestPainType",

    "RestingBP",

    "Cholesterol",

    "FastingBS",

    "RestingECG",

    "MaxHR",

    "ExerciseAngina",

    "Oldpeak",

    "ST_Slope"

]

# ==========================================================
# Number of Features
# ==========================================================

NUMBER_OF_FEATURES = len(FEATURE_COLUMNS)