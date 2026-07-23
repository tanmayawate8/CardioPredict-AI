# ==========================================
# PHASE 11 : MODEL SERIALIZATION
# XGBoost Model
# Heart Disease Prediction Project
# ==========================================

# ------------------------------------------
# Step 1 : Import Required Libraries
# ------------------------------------------

from pathlib import Path
import pandas as pd
import pickle

from xgboost import XGBClassifier

# ------------------------------------------
# Step 2 : Project Folder Paths
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "Dataset"

CURRENT_FOLDER = Path(__file__).resolve().parent

# ------------------------------------------
# Step 3 : Load Training Dataset
# ------------------------------------------

X_train = pd.read_csv(DATASET_PATH / "X_train.csv")
y_train = pd.read_csv(DATASET_PATH / "y_train.csv")

print("Training Dataset Loaded Successfully")

# ------------------------------------------
# Step 4 : Convert Target into 1-D Array
# ------------------------------------------

y_train = y_train.values.ravel()

# ------------------------------------------
# Step 5 : Create XGBoost Model
# ------------------------------------------

model = XGBClassifier(
    random_state=42,
    eval_metric="logloss"
)

print("Model Created Successfully")

# ------------------------------------------
# Step 6 : Train the Model
# ------------------------------------------

model.fit(X_train, y_train)

print("Model Trained Successfully")

# ------------------------------------------
# Step 7 : Save Model
# ------------------------------------------

with open(CURRENT_FOLDER / "heart_disease_model.pkl", "wb") as file:

    pickle.dump(model, file)

print("Model Saved Successfully")

# ------------------------------------------
# Step 8 : Completion Message
# ------------------------------------------

print("\n===================================")
print("Phase 11 Completed Successfully")
print("Saved File : heart_disease_model.pkl")
print("Location : Phase 11 - Model Serialization")
print("===================================")