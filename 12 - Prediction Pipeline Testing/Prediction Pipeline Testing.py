# ==========================================
# PHASE 12 : PREDICTION PIPELINE TESTING
# Heart Disease Prediction Project
# ==========================================

# ------------------------------------------
# Step 1 : Import Required Libraries
# ------------------------------------------

from pathlib import Path
import pandas as pd
import pickle

# ------------------------------------------
# Step 2 : Project Folder Paths
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "Phase 11 - Model Serialization"

PREPROCESSING_PATH = BASE_DIR / "Phase 6 - Data Preprocessing"

# ------------------------------------------
# Step 3 : Load Saved Model and Scaler
# ------------------------------------------

with open(MODEL_PATH / "heart_disease_model.pkl", "rb") as file:
    model = pickle.load(file)

with open(PREPROCESSING_PATH / "scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

print("Model Loaded Successfully")
print("Scaler Loaded Successfully")

# ------------------------------------------
# Step 4 : Enter New Patient Data
# ------------------------------------------

patient = {
    "Age": [45],
    "Sex": [1],
    "ChestPainType": [2],
    "RestingBP": [130],
    "Cholesterol": [240],
    "FastingBS": [0],
    "RestingECG": [1],
    "MaxHR": [150],
    "ExerciseAngina": [0],
    "Oldpeak": [1.2],
    "ST_Slope": [2]
}

# ------------------------------------------
# Step 5 : Convert into DataFrame
# ------------------------------------------

patient_df = pd.DataFrame(patient)

# ------------------------------------------
# Step 6 : Scale Numerical Features
# ------------------------------------------

numerical_columns = [
    "Age",
    "RestingBP",
    "Cholesterol",
    "FastingBS",
    "MaxHR",
    "Oldpeak"
]

patient_df[numerical_columns] = scaler.transform(
    patient_df[numerical_columns]
)

# ------------------------------------------
# Step 7 : Predict
# ------------------------------------------

prediction = model.predict(patient_df)

# ------------------------------------------
# Step 8 : Display Result
# ------------------------------------------

print("\nPrediction Result")

if prediction[0] == 1:
    print("Heart Disease Detected")
else:
    print("No Heart Disease Detected")

# ------------------------------------------
# Step 9 : Completion Message
# ------------------------------------------

print("\n===================================")
print("Prediction Pipeline Tested Successfully")
print("===================================")